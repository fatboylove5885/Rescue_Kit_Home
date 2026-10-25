# WhatsForEats targeted traffic launch — October 25, 2026

The aim is to attract people who need help deciding and organizing dinner, then lead them from a useful free resource to the 5:47 p.m. Rescue Kit. This launch uses the existing product and article library. Additional subscriptions and advertising spend committed: **$0**. No traffic, ranking, sales, or conversion lift is claimed before measurement.

## Audience and channel choices

| Audience situation | Search/topic hypothesis | Useful destination | Next step |
|---|---|---|---|
| Busy household, tired at dinner time | What should I make for dinner; dinner ideas with no energy | `/what-to-make-for-dinner.html` and `/easy-dinner-ideas-no-energy.html` | Open a recipe; explore the Rescue Kit |
| Short ingredient list needed | 5-ingredient dinners; easy weeknight meals | `/5-ingredient-dinners.html` | Use a recipe; request the matching printable |
| Family with different food preferences | Meal plan for picky families | `/7-night-dinner-plan-for-picky-families.html` | Read the plan; explore the Rescue Kit |
| Dinner budget feels hard to control | Cheap family dinners; cost per serving | `/cheap-family-dinners-cost-per-serving.html` | Use the cost calculator and practical guide |
| Wants to prepare before a busy week | Make-ahead dinners; freezer meals | `/18-make-ahead-dinners.html` and `/freezer-meals-for-busy-weeknights.html` | Choose one prep method; use the printable |

These are audience and intent hypotheses, not paid keyword-volume estimates. Prioritize US English initially because the existing recipes use US measurements. Do not create country-specific duplicate pages just to target keywords. Search Console country data can identify genuine UK, Canadian, Australian, New Zealand and Irish interest later.

Google search and Pinterest are the initial distribution priorities. Google's guidance favors useful original pages, discoverable HTML images and consistent canonical URLs. Pinterest supports linked visual posts and RSS ingestion from a claimed domain. That makes the existing recipe library, printables and new dinner finder a suitable starting point. The dinner finder provides an immediate action without requiring a purchase or email address.

## Implementation

- New crawlable dinner finder: 12 recipe destinations, filters for time, effort and ingredient, random choice, shareable filter URLs, empty states, keyboard operation and a usable no-JavaScript fallback.
- Static images on the homepage and weeknight guide: 28 `<img>` elements replace dependence on JavaScript for initial rendering. Existing JavaScript skips images that already exist.
- A shared discovery block links articles to the tool and free printable library, with native Pinterest Save links. All existing article prose is preserved.
- The product landing page and homepage Rescue Kit CTAs have real hrefs before JavaScript runs. Checkout remains on Whop, via the established landing page.
- Complete missing social metadata and Article URL/image fields. No invented ratings, recipe testing, credentials or nutrition values.
- Sitemap includes the new tool and restored product landing page, and excludes HTML explicitly marked noindex. Email delivery/thank-you resources stay out of the sitemap.
- The same existing GA4 property (`G-QM26ZNDC24`) is loaded consistently only after visitor opt-in. No analytics script loads on a fresh visit before consent. The visitor can decline or withdraw. Campaign fields are limited to simple UTM values; custom events never send email form values.
- Three original 2:3 Pinterest creatives and distinct descriptions are ready in `assets/pins/` and `marketing/pinterest-launch.json`. The images are AI-created illustrations, not photographs proving that recipes were tested.
- RSS 2.0 launch feed: `https://whatsforeats.online/pinterest-feed.xml`. Stable GUIDs prevent the feed generator from presenting unchanged campaign items as new.
- IndexNow ownership file and a manual submission script are included. Run only after the public key file is deployed. Acceptance is a notification receipt, not proof of indexing.

## Campaign publishing

Use **one route** for these three campaign items to avoid duplicate pins:

1. Metricool: connect the correct Pinterest business account, inspect available boards and scheduled posts, then publish/schedule the three distinct items in `pinterest-launch.json`. The recommended launch sequence is dinner finder, five-ingredient guide, family plan, one per day. Pick an account-supported time based on its data; there is no universal best time asserted here.
2. Or native Pinterest RSS: claim `whatsforeats.online`, connect the feed under Import content / Auto-publish, and choose an appropriate board. Pinterest may ingest all three launch items together. Adding the feed to the website alone does not connect it to Pinterest or publish any Pins.

Titles, descriptions, images and tracked destination URLs are fully prepared. Each Pin links to its matching free resource. All product CTAs inside those resources keep using `/5-47-rescue-kit.html`.

At the last account check in this work session, Metricool was connected to ChatGPT but reported no social network attached. Windsor.ai was connected but exposed only an existing TikTok account, with no GA4 or Search Console property. Do not treat app installation as proof that the website or Pinterest account has been authorized. No emails, DMs, community posts, paid ads or social posts have been sent by this launch unless separately recorded in launch results.

## Measurement and next 30 days

First establish a baseline for the last 28 complete days once GA4 and Search Console are connected. Use the actual property/site, filter to `whatsforeats.online`, and exclude the partial current day. Save baseline data privately; do not commit account-level visitor data to this public repository.

| Metric | Source | How to use it |
|---|---|---|
| Search clicks, impressions, CTR, average position by page/query | Search Console | Identify relevant queries already receiving impressions. Compare similar complete periods and watch data latency. |
| Pinterest outbound clicks and saves | Pinterest / Metricool | Prefer clicks to the matching resource over raw impressions. |
| Sessions by source/medium and landing page | GA4 | Compare organic search and `pinterest / organic_social`; consent means this is a partial observed audience. |
| `dinner_finder_filter`, `dinner_finder_pick`, `dinner_recipe_click` | GA4 events | Check whether the tool gets people to recipes. |
| `rescue_kit_view_click`, `checkout_click`, `freebie_click` | GA4 events | Measure movement toward the offer. A checkout click is not a sale and a freebie click is not a confirmed email signup. |
| Completed orders and net revenue | Whop | Confirm real sales. No purchase event or revenue attribution is fabricated on the static site. |

Days 1–3: verify public pages and campaign links, submit the sitemap through the authorized Search Console property, submit IndexNow once, publish the three distinct Pins after Pinterest connection. The scripts do not independently submit to Google or publish social content.

Days 4–10: inspect real query/click data and fix any crawl or broken-link problem. Improve the existing page that matches a relevant query; preserve successful URLs. Do not churn dozens of thin articles.

Days 11–20: create the next distinct Pin set around the best-performing audience problem. Publish helpful resource posts only on the owner's relevant connected accounts. Community answers require a genuinely relevant question and compliance with each community's promotion rules; no repetitive link drops or unsolicited bulk messaging.

Days 21–30: compare complete periods, allowing for search latency. Keep topics producing relevant visits, recipe use or product interest. Adjust weak titles/creative or destination usefulness before considering more volume. Report actual numbers and unknowns. This document is a work plan; it does not activate a recurring agent or schedule.

## Research used

Reviewed October 25, 2026. These are primary sources; the strategy is an inference from their guidance and the observed site, not a traffic forecast.

- Google: people-first content — https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google: image discovery — https://developers.google.com/search/docs/appearance/google-images
- Google: sitemap construction — https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google: canonical consistency — https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google: recipe structured-data requirements — https://developers.google.com/search/docs/appearance/structured-data/recipe
- Pinterest: RSS requirements and claimed-domain setup — https://help.pinterest.com/en/business/article/auto-publish-pins-from-your-rss-feed
- Pinterest: bulk post fields and limits — https://help.pinterest.com/en/business/article/bulk-upload-video-pins
- Pinterest: vertical creative guidance — https://business.pinterest.com/creative-best-practices/
- IndexNow: ownership verification, submission and response semantics — https://www.indexnow.org/documentation

## Maintenance and checks

Run `python scripts/build_dinner_finder.py` when changing the tool's curated data, followed by `python scripts/build_discovery.py` to restore shared metadata and refresh the feed. `build_discovery.py` requires Beautiful Soup 4. Run `python scripts/verify_discovery.py` afterward.

Serve the repository locally on port 8765 and run `node scripts/verify_browser.cjs` with Playwright and its Chromium browser installed. The browser check stubs the analytics script to avoid contaminating real reporting with QA activity.

After deployment, run `python scripts/submit_indexnow.py --submit` once and record the actual response. Do not claim Search Console submission, rich-result validation or account metrics without running those authorized external checks.

The pre-existing privacy page still contains owner-review/contact reminders. The analytics description was updated to match the implemented opt-in; this work does not claim a complete legal review or solve the missing owner contact details.
