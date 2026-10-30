# PRODUCT_VISION - PandaBear pain research (adapted from Reddit_Scrapper)

## Purpose
Mine investment communities on Reddit for evidence about how self-directed
investors' research process hurts, so PandaBear Investing (PandaInvest,
pandabearinvestments.vercel.app) can pick and serve its target audience from
real community statements instead of guesses.

## What "pain" means here
Problems with the research workflow itself: idea discovery for overlooked
stocks, noise and newsletter overload, screener coverage and data quality
(small-cap, OTC, international), paywall sprawl, source trust and AI
traceability, tool fragmentation, and promotion/shill distrust. NOT stock
picks, price talk, losses, or broker complaints.

## Output
A local SQLite database of scored, quoted pain evidence plus a Streamlit
browser. The questions it answers: who hurts (segment), how often, what they
use now, what they pay, and which PandaInvest surface answers the pain.

## License constraint (load-bearing)
Upstream is Mohamedsaleh14/Reddit_Scrapper under a NON-COMMERCIAL license.
Permitted: educational/research, testing, and personal or INTERNAL use to aid
marketing or product discovery - which covers this audience-research use.
NOT permitted without the author's prior written approval: integrating this
code into a commercial or monetized PandaBear service, or hosting it as a
backend for users. Attribution to "Mohamed-Saleh" and "Cronlytic.com" must be
retained (see README). If PandaInvest ever ships pipeline code derived from
this repo in the paid product, get written approval first or re-implement
from an MIT-licensed base (see the tool scan in the audience research doc).

## Non-goals
- No posting, commenting, or messaging on Reddit (read-only via PRAW).
- No use of logged-in Reddit cookies or personal credentials. PRAW app
  credentials only.
- Not a trading, alerting, or recommendation tool.

## Cost posture
Batch API with a monthly budget cap (default $25). No run without an AI API
budget the owner explicitly approves.

## Next steps
1. Owner creates a Reddit API app (client id/secret) and an AI API key.
2. Run weekly; review top scored pains in the GUI.
3. After 1-2 weeks, revisit the audience call in the research doc.
