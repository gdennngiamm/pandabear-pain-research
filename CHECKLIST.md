# CHECKLIST - PandaBear adaptation of Reddit_Scrapper (Oct 30, 2026)

QA legend: PASS (evidence cited), FAIL, BLOCKED (what is missing).
"Done" means verified, not partial.

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Upstream repo inspected for suitability | PASS | Tree, README, prompts and code read via GitHub (Oct 30): PRAW scraper + GPT batch filter/insight + SQLite + Streamlit; architecture fits pain mining. Pipeline keys (relevance_score, emotional_intensity, pain_point_clarity, implementability_score, technical_depth_score, roi_weight, tags) consumed in db/writer.py and scheduler/runner.py - prompt rewrites keep identical keys so no code changes are required. |
| 2 | License inspected before adaptation | PASS | LICENSE is custom NON-COMMERCIAL (not MIT): internal marketing/product-discovery use allowed, commercial hosting/integration needs author approval, attribution required. Constraint recorded in PRODUCT_VISION.md and README. |
| 3 | Retarget to investment communities | PASS | config/config.yaml primary list now ValueInvesting, SecurityAnalysis, investing, stocks, StockMarket, smallcaps, microcaps, undervalued, DeepValue, dividends; exploratory 40/60; age window 5-14 days. |
| 4 | Pain definition rewritten for research workflow | PASS | gpt/prompts/filter.txt rewritten: research-workflow pains only; excludes picks, price talk, brokers, promoters; same JSON keys kept. |
| 5 | Insight extraction rewritten for audience evidence | PASS | gpt/prompts/insight.txt rewritten: segment, tools-in-use, PandaInvest surface mapping, WTP evidence, verbatim quote; same JSON keys kept. |
| 6 | Community discovery retargeted | PASS | gpt/prompts/community_discovery.txt rewritten for investing-adjacent communities; excludes meme/options/crypto. |
| 7 | System prompts in code aligned | PASS | gpt/filters.py and gpt/insights.py system lines retargeted to investment-research analysis. |
| 8 | Scoring re-weighted for audience research | PASS | config.yaml: pain_point 0.35, relevance 0.30, recency 0.20; technical_depth weight 0.0 and min_technical_depth 0 (hard filter off); monthly budget cap lowered to $25. |
| 9 | Attribution retained | PASS | LICENSE file untouched; README adaptation section credits Mohamed-Saleh and Cronlytic.com. |
| 10 | No credentials or cookies committed | PASS | .env.template unchanged (placeholders only); no Reddit cookies, session data, or API keys added anywhere. |
| 11 | PRODUCT_VISION.md present | PASS | This repo root. |
| 12 | CHECKLIST.md present | PASS | This file. |
| 13 | g-denn has push access | BLOCKED | Collaboration invite sent to g-denn from owner account gdennngiamm; access is active once g-denn accepts GitHub's invite. |
| 14 | Pipeline runs end-to-end | BLOCKED | Needs Reddit API app credentials (owner creates at reddit.com/prefs/apps) and an AI API key + budget approval (payment not authorized). Code review only; no execution attempted. |
| 15 | GUI reviewed | BLOCKED | Same as #14 - requires a run first. Code inspection of gui/gui.py shows standard Streamlit filters over the same DB fields, consistent with kept keys. |
