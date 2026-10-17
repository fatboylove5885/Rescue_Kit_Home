/* What's for Eats — shared freebie email-delivery endpoint.
   Connect this file to the Google Apps Script deployment:
   1) Open google-apps-script/FreebieDelivery.gs and set SHEET_ID to the ID
      of the Google Sheet that contains the Subscribers and Freebie Catalog tabs.
   2) Deploy that script as a Web app (execute as you; access: anyone).
   3) Paste the deployed Web app URL ending in /exec below.
   The Subscribers tab must use these exact columns, in this order:
   Timestamp | Email | Requested Freebie | Marketing Opt-In | Source URL | Delivery Status
   Do not put the Google Sheet ID or Apps Script URL in public-facing HTML.
*/
window.FREEBIES_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzqWjkThQ0gjfqTMzwp4ovuVfjNFXgK6Q79ZXRUHWIB92gjjdTAR2NwyYrPjoeFUVY7/exec";

// Routes used after a successful email capture. Each guide has a Print / Save as PDF control.
window.FREEBIE_HTML_ROUTES = {
  "20-lazy-dinners-for-when-your-brain-has-left-the-building": "/pdfs/dinner-rescue-playbook.html",
  "20-lazy-dinners-sorted-by-how-tired-you-are": "/pdfs/energy-level-dinner-selector.html",
  "22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater": "/pdfs/cozy-season-supper-collection.html",
  "5-ingredient-dinners": "/pdfs/five-ingredient-favorites.html",
  "7-night-dinner-plan-for-picky-families": "/pdfs/picky-family-weeknight-blueprint.html",
  "cheap-family-dinners-cost-per-serving": "/pdfs/budget-bites-cost-guide.html",
  "easy-dinner-ideas-no-energy": "/pdfs/low-energy-meal-survival-guide.html",
  "easy-sheet-pan-dinners": "/pdfs/sheet-pan-supper-starter.html",
  "easy-weeknight-dinner-recipes": "/pdfs/weeknight-dinner-companion.html",
  "freezer-meals-for-busy-weeknights": "/pdfs/freezer-friendly-family-meals.html",
  "leftover-chicken-recipes": "/pdfs/chicken-leftover-reinvention-kit.html",
  "pantry-staples-list-for-budget-cooking": "/pdfs/budget-pantry-checklist.html",
  "picky-eater-dinner-ideas": "/pdfs/picky-eater-plate-builder.html",
  "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer": "/pdfs/cooking-method-cheat-sheet.html",
  "slow-cooker-dinners-for-busy-families": "/pdfs/slow-cooker-comfort-collection.html",
  "weekly-meal-plan-for-busy-families": "/pdfs/family-meal-planning-map.html",
  "picky-family-7-night-dinner-plan": "/pdfs/seven-night-picky-eater-menu.html",
  "lazy-dinner-energy-picker": "/pdfs/what-to-cook-tonight-picker.html",
  "cozy-fall-dinner-bingo": "/pdfs/cozy-dinner-bingo.html"
};
