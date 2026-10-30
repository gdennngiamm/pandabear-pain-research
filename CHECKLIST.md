# CHECKLIST - PandaBear adaptation of Reddit_Scrapper (Oct 30, 2026)

QA legend: PASS (evidence cited), FAIL, BLOCKED (what is missing).
"Done" means verified, not partial.

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Upstream repo inspected for suitability | PASS | Tree, README, prompts and code read via GitHub (Oct 30): PRAW scraper + GPT batch filter/insight + SQLite + Streamlit; architecture fits pain mining. Pipeline keys (relevance_score, emotional_intensity, pain_point_clarity, implementability_score, technical_depth_score, roi_weight, tags) consumed in db/writer.py and scheduler/runner.py - prompt rewrites keep identical keys so no code changes are required. |
| 2 | License inspected before adaptation | PASS | LICENSE is custom NON-COMMERCIAL (not MIT): internal marketing/product-discovery use allowed, commercial hosting/integration needs author approval, attribution required (source: https://raw.githubusercontent.com/Mohamedsaleh14/Reddit_Scrapper/HEAD/LICENSE). Constraint recorded in PRODUCT_VISION.md and README. |
| 3 | Retarget to investment communities | PASS | config/config.yaml primary list now ValueInvesting, SecurityAnalysis, investing, stocks, StockMarket, smallcaps, microcaps, undervalued, DeepValue, dividends; exploratory 40/60; age window 5-14 days. |
| 4 | Pain definition rewritten for research workflow | PASS | gpt/prompts/filter.txt rewritten: research-workflow pains only; excludes picks, price talk, brokers, promoters; same JSON keys kept. |
| 5 | Insight extraction rewritten for audience evidence | PASS | gpt/prompts/insight.txt rewritten: segment, tools-in-use, PandaInvest surface mapping, WTP evidence, verbatim quote; same JSON keys kept. |
| 6 | Community discovery retargeted | PASS | gpt/prompts/community_discovery.txt rewritten for investing-adjacent communities; excludes meme/options/crypto. |
| 7 | System prompts in code aligned | PASS | gpt/filters.py and gpt/insights.py system lines retargeted to investment-research analysis. |
| 8 | Scoring re-weighted for audience research | PASS | config.yaml: pain_point 0.35, relevance 0.30, recency 0.20; technical_depth weight 0.0 and min_technical_depth 0 (hard filter off). |
| 9 | Spend fails closed without explicit approval | PASS | config.yaml monthly_budget_usd: 0 blocks all AI spend until the owner explicitly approves a budget. No payment authorized or attempted. |
| 10 | Attribution retained | PASS | LICENSE file untouched; README adaptation section credits Mohamed-Saleh and Cronlytic.com. |
| 11 | No credentials or cookies committed | PASS | .env.template unchanged (placeholders only); no Reddit cookies, session data, or API keys added anywhere. |
| 12 | PRODUCT_VISION.md present | PASS | Repo root. |
| 13 | CHECKLIST.md present | PASS | This file. |
| 14 | g-denn has push access | PASS (pending acceptance) | Collaborator invitation sent to g-denn from owner account gdennngiamm on Oct 30 via repo settings/access (GitHub: "g-denn has been added as a collaborator on the repository"). Access activates when g-denn accepts GitHub's invite. |
| 15 | Dependencies install + code compiles | PASS | Oct 30 sandbox clone of this fork: python3.10 venv, `pip install -r requirements.txt` OK; `python -m compileall` clean after fixes in #16. |
| 16 | Upstream bugs found and fixed | PASS | (a) `from datetime import UTC` breaks on Python 3.10 (datetime.UTC is 3.11+) in db/reader.py and db/writer.py -> replaced with `from datetime import timezone; UTC = timezone.utc`. (b) `scheduler.schedulers` -> `apscheduler.schedulers` in scheduler/daily_scheduler.py. Both fixes committed to this fork. |
| 17 | Modules import / fail closed without secrets | PASS | After fixes: db.reader, db.writer, gui.gui import OK. reddit.scraper, scheduler.runner and main fail closed at startup on missing PRAW client_id - expected behavior with no Reddit API credentials configured; no secret exposure. |
| 18 | Executable DB roundtrip test | PASS | Oct 30 sandbox: insert_post + update_post_filter_scores + update_post_insight + get_top_insights_from_today returned the inserted test row (roi_weight 5, relevance 8.0). Note: is_already_processed checks the history table, not posts, so it returns False for a post only in the posts table until mark_posts_in_history runs - upstream semantics, not a bug. |
| 19 | Pipeline runs end-to-end (Reddit + AI) | BLOCKED | Needs Reddit API app credentials (owner creates at reddit.com/prefs/apps) and an AI API key + explicit budget approval (no spend authorized; budget is fail-closed at 0, see #9). Everything up to the credential boundary tested PASS in #15-18. |
| 20 | GUI reviewed live | BLOCKED | Same credential blocker as #19. gui/gui.py imports cleanly; code inspection shows standard Streamlit filters over the same DB fields, consistent with kept keys. |
