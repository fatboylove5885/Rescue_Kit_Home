# Content overhaul review notes — October 2026

This work is a **review branch**, not a live deployment.

## Publishing checks
- Review the new dinner instructions, quantities and recipe safety notes with a knowledgeable human editor before merging.
- Confirm your identity and contact details. The existing privacy page currently contains a reminder to add the site's actual contact information.
- The site should not claim tested recipes or professional nutrition credentials unless independently documented. Our new About page avoids those claims.
- Confirm all free download forms really deliver as promised and the links to paid products work.
- Review all internal SVG visuals in real desktop and mobile browsers; SVGs are diagrams, not food photography.
- Validate the site using Google Search Console, Rich Results Test, PageSpeed Insights and accessibility checks.
- Monitor organic impressions, search queries, click-through rate, scroll engagement, outbound clicks and revenue per page after publication.

## Important limitations
- More copy and original diagrams alone do not guarantee higher ranking, longer session time, search traffic or AdSense acceptance.
- Existing published URLs remain unchanged to protect inbound links. The former “20 Lazy Dinners Sorted...” article contained 22 cozy fall recipes; title and introductory navigation were adjusted to match the real recipe list.
- Newly added FAQ-like prose is not marked up with fake ratings or nonexistent user reviews.
- Prices are illustrative only; the site cannot claim actual testing, ratings or nutrition calculations that were not performed.
- Do not deploy AdSense tags until the privacy policy, cookie disclosures, legal consent management and contact details match the live setup.
- This review does not replace a live browser check of GitHub Pages or a professional food-safety review.

## Supporting sources
- Google Search Central people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central SEO starter guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search Central image SEO: https://developers.google.com/search/docs/appearance/google-images
- Google Search Central structured recipe guidance: https://developers.google.com/search/docs/appearance/structured-data/recipe
- Google AdSense required privacy statements: https://support.google.com/adsense/answer/1348695
- USDA leftovers: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety
- USDA food safety: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/steps-keep-food-safe
- Academy of Nutrition and Dietetics: https://www.eatright.org/food/planning/meals-and-snacks/end-mealtime-battles

## Verified scope and per-article growth (October 18, 2026)
All 17 article HTML files gained visible words relative to original commit `36b8881960b8b9e63d64bfa7a516287c4a49be3b`. Counts exclude script and style content; minor differences may result from treating punctuation as whitespace. No article is shorter.

| Article | Original words | Review-branch words | Gain |
|---|---:|---:|---:|
| 18 Make-Ahead Dinners | 7075 | 7464 | +389 |
| 20 Lazy Dinners (Brain Left the Building) | 6063 | 6402 | +339 |
| 22 Low-Effort Fall Dinners (legacy lazy URL) | 7746 | 8078 | +332 |
| 22 Cozy Fall Dinners | 1265 | 2487 | +1222 |
| 5-Ingredient Dinners | 819 | 2154 | +1335 |
| 7-Night Plan for Picky Families | 2890 | 3291 | +401 |
| Cheap Family Dinners / Cost per Serving | 852 | 1633 | +781 |
| Easy Dinners When You Have No Energy | 992 | 1712 | +720 |
| Easy Sheet-Pan Dinners | 842 | 1885 | +1043 |
| Easy Weeknight Dinner Recipes | 4029 | 4346 | +317 |
| Freezer Meals | 805 | 1650 | +845 |
| Leftover Chicken Recipes | 742 | 1510 | +768 |
| Pantry Staples for Budget Cooking | 782 | 1479 | +697 |
| Picky-Eater Dinner Ideas | 846 | 1580 | +734 |
| Sheet Pan vs Slow Cooker vs One Pot vs Air Fryer | 2061 | 2427 | +366 |
| Slow Cooker Dinners | 896 | 1932 | +1036 |
| Weekly Meal Plan | 851 | 1537 | +686 |
| **Total** | **39556** | **51567** | **+12011** |

## Detailed changes in this review branch
- Original explanatory SVG visuals: six topic diagrams and seven separate family-dinner serving guides. The seven visible image placeholders in the picky-family article were replaced with actual `<img>` references and descriptive text. These SVGs are original diagrams, **not** photographic evidence of prepared dishes.
- Added accessible, collapsible full cooking instructions for seven five-ingredient meals, five sheet-pan dinners and five slow-cooker meals, including starter quantities, sequence, substitutions and temperature checks.
- Expanded freezer, chicken leftovers, pantry, picky-eater, low-energy dinner and weekly-planning articles with multi-night examples, real use cases, shopping guidance and troubleshooting.
- Added a client-side cost-per-serving calculator to the budget article. Values remain in the visitor's browser; no data is transmitted by the calculator itself.
- Preserved article URLs, existing content sections, recipes, navigation and the site's overall look. Added internal cross-links and supporting links to authoritative food-safety and feeding guidance.
- Updated seasonal article titles and blog-index labels to reflect actual contents when the file's historical slug did not match its recipes. Preserved URLs to avoid breaking existing incoming links.
- Added relevant Open Graph / Twitter preview images to articles that lacked them, pointing to existing local photographs.
- Added an editorial About page and expanded the privacy-policy **draft** to describe observed analytics / email services and future advertising disclosure needs. A real operator contact address and confirmation of cookie settings remain required before publication.
- Cleaned the blog index, updated the sitemap and created these review notes.

## Competition and editorial research boundaries
Compared content conventions against live public examples including [Budget Bytes recipes under $5](https://www.budgetbytes.com/category/recipes/cost-per-recipe/recipes-under-5/) and [Allrecipes](https://www.allrecipes.com/), focusing on usable methods, cost context and practical cooking advice. Originality and honest cooking instructions were prioritized over keyword repetition or simply meeting a target length. This work is **not** a claim that every recipe was independently test-cooked or that the site outranks those publishers. Better ranking, retention and ad acceptance require observation after deployment.

## Before production deployment
1. Add verified site-owner contact information and approve privacy/cookie disclosures. Configure any legally necessary consent solution, especially if future AdSense serves EEA/UK/Swiss visitors.
2. Verify actual freebie delivery, paid-product links, mobile navigation, footer links, calculator interactions, embedded illustrations and responsive rendering.
3. Review recipe times, quantities and safety instructions with a knowledgeable human editor. Never imply test-cooked recipes or certified nutritional estimates if they were not independently verified.
4. Confirm external images are appropriately licensed or replace them with owned, purpose-made food photography. The 13 SVG diagrams are illustrative, not substitutes for original tested-recipe photographs.
5. Run Google Search Console, Rich Results Test, PageSpeed Insights and accessibility testing on a live/staging URL. Obtain performance baselines and monitor post-publication data.
6. Resolve the divergence from `main` before merging: an initial overhaul commit already exists on `main` (commit `e8614bf55c94b73afddd9e1d32a3de28854e066c`), while later refinements are on this review branch. Confirm merge strategy and avoid overwriting other changes.
