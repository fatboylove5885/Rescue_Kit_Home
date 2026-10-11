/* What's for Eats — shared freebie capture configuration.
   Each request is logged, then redirected to the matching styled HTML resource.
   Newsletter consent remains optional. Keep the endpoint synced with the deployed Apps Script.
*/
window.FREEBIES_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzqWjkThQ0gjfqTMzwp4ovuVfjNFXgK6Q79ZXRUHWIB92gjjdTAR2NwyYrPjoeFUVY7/exec";
window.FREEBIE_HTML_ROUTES = {
  "20-lazy-dinners-for-when-your-brain-has-left-the-building": "/20-lazy-dinners-for-when-your-brain-has-left-the-building.html",
  "20-lazy-dinners-sorted-by-how-tired-you-are": "/20-lazy-dinners-sorted-by-how-tired-you-are.html",
  "22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater": "/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html",
  "5-ingredient-dinners": "/5-ingredient-dinners.html",
  "7-night-dinner-plan-for-picky-families": "/7-night-dinner-plan-for-picky-families.html",
  "cheap-family-dinners-cost-per-serving": "/cheap-family-dinners-cost-per-serving.html",
  "easy-dinner-ideas-no-energy": "/easy-dinner-ideas-no-energy.html",
  "easy-sheet-pan-dinners": "/easy-sheet-pan-dinners.html",
  "easy-weeknight-dinner-recipes": "/easy-weeknight-dinner-recipes.html",
  "freezer-meals-for-busy-weeknights": "/freezer-meals-for-busy-weeknights.html",
  "leftover-chicken-recipes": "/leftover-chicken-recipes.html",
  "pantry-staples-list-for-budget-cooking": "/pantry-staples-list-for-budget-cooking.html",
  "picky-eater-dinner-ideas": "/picky-eater-dinner-ideas.html",
  "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer": "/sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer.html",
  "slow-cooker-dinners-for-busy-families": "/slow-cooker-dinners-for-busy-families.html",
  "weekly-meal-plan-for-busy-families": "/weekly-meal-plan-for-busy-families.html",
  "picky-family-7-night-dinner-plan": "/picky-family-7-night-dinner-plan-printable.html",
  "lazy-dinner-energy-picker": "/20-lazy-dinners-sorted-by-how-tired-you-are.html",
  "cozy-fall-dinner-bingo": "/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html"
};
(function () {
  window.addEventListener("message", function (event) {
    var data = event && event.data;
    if (!data || data.type !== "freebie-signup-result") return;
    if (data.ok && data.redirect) {
      try {
        var destination = new URL(data.redirect, window.location.origin);
        if (destination.origin === window.location.origin) window.location.assign(destination.href);
      } catch (_) {}
      return;
    }
    var message = (data && data.message) || "We couldn't save your request. Please try again.";
    var alertBox = document.querySelector("#error, #pdf-gate-error, [role='alert'], .error");
    if (alertBox) { alertBox.textContent = message; alertBox.style.display = "block"; }
    var submitButton = document.querySelector("#submit, #pdf-gate-submit, button[type='submit']");
    if (submitButton) { submitButton.disabled = false; submitButton.textContent = "Try again"; }
  });
})();
