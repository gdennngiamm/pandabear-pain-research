# gpt/openrouter_sync.py
# Zero-spend AI route: OpenRouter free models via synchronous chat/completions.
# Official basis (verified Oct 30, 2026):
#   - Free variant:  https://openrouter.ai/docs/guides/routing/model-variants/free
#   - Free router:   https://openrouter.ai/docs/guides/routing/routers/free-router
#   - Limits/FAQ:    https://openrouter.ai/docs/api_reference/limits , /docs/faq
#     free models: 50 requests/day (<10 credits purchased), 1000/day (>=10 credits).
# Consumes the repo's existing prepared items ({"id","messages"} from
# gpt.filters.prepare_batch_payload / gpt.insights.prepare_insight_batch) and
# writes result JSONL in the OpenAI line format that
# gpt.batch_provider.extract_content_from_result already parses, so downstream
# runner code is unchanged.
# Fail-closed rules: only free models allowed; no key -> refuse; daily cap
# reached -> refuse (no request sent).

import glob
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from config.config_loader import get_config

UTC = timezone.utc  # py3.10 compat

API_URL = "https://openrouter.ai/api/v1/chat/completions"
FREE_ROUTER = "openrouter/free"
USAGE_FILE = Path("data/openrouter_usage.json")
RESULT_DIR = Path("data/batch_responses")


def _cfg():
    return get_config().get("ai", {}).get("openrouter", {})


def _daily_cap() -> int:
    return int(_cfg().get("daily_request_cap", 50))


def configured_model(kind: str = "model_filter") -> str:
    return _cfg().get(kind, FREE_ROUTER)


def is_free_model(model: str) -> bool:
    """Only zero-cost models are allowed: the free router or a :free variant."""
    return model == FREE_ROUTER or model.endswith(":free")


def require_free_model(model: str) -> str:
    if not is_free_model(model):
        raise RuntimeError(
            f"Refusing non-free model '{model}'. Only '{FREE_ROUTER}' or "
            "models ending in ':free' are permitted on the zero-spend route."
        )
    return model


def _load_usage() -> dict:
    if USAGE_FILE.exists():
        return json.loads(USAGE_FILE.read_text())
    return {"day": "", "count": 0}


def _record_usage(n: int = 1) -> None:
    u = _load_usage()
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    if u.get("day") != today:
        u = {"day": today, "count": 0}
    u["count"] += n
    USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    USAGE_FILE.write_text(json.dumps(u))


def remaining_requests_today() -> int:
    u = _load_usage()
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    used = u["count"] if u.get("day") == today else 0
    return max(0, _daily_cap() - used)


def can_send(n: int = 1) -> bool:
    return remaining_requests_today() >= n


def build_payload(model: str, messages, max_tokens: int = 1000) -> dict:
    """Single-model payload only. Never includes a fallback 'models' array,
    so a free request can never silently route to a billed model."""
    require_free_model(model)
    return {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        # Route only to providers that do not collect/train on prompts.
        # https://openrouter.ai/docs/guides/routing/provider-selection
        "provider": {"data_collection": "deny"},
    }


def _post(url, body, headers):
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def send_item(item: dict, model: str, api_key=None, http_post=None) -> dict:
    """Send one prepared item; return an OpenAI-format result line."""
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set; refusing to send (fail closed).")
    if not can_send(1):
        raise RuntimeError("OpenRouter daily free cap reached; refusing to send (fail closed).")
    payload = build_payload(model, item["messages"])
    resp = (http_post or _post)(
        API_URL, json.dumps(payload).encode(),
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    _record_usage(1)
    return {"custom_id": item["id"], "response": {"body": resp}}


def run_stage(items, model_kind: str, label: str, api_key=None, http_post=None, sleep_s: float = 1.0):
    """Process prepared items up to the daily free cap; write one result JSONL.
    Returns list of written file paths (runner-compatible)."""
    model = require_free_model(configured_model(model_kind))
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    path = RESULT_DIR / f"{label}_result_{ts}.jsonl"
    sent = 0
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            if not can_send(1):
                break  # fail closed: stop quietly at the free cap
            line = send_item(item, model, api_key=api_key, http_post=http_post)
            f.write(json.dumps(line) + "\n")
            sent += 1
            time.sleep(sleep_s)
    return [str(path)] if sent else []


def run_filter_stage(filter_batch, **kw):
    return run_stage(filter_batch, "model_filter", "filter", **kw)


def run_insight_stage(insight_batch, **kw):
    return run_stage(insight_batch, "model_deep", "insight", **kw)
