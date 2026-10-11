/** What's for Eats HTML free-resource capture + subscriber log.
 * Google Sheet compatibility:
 * - Use the updated email-list workbook imported into Google Sheets.
 * - Keep the Subscribers tab and its six columns in this exact order:
 *   Timestamp, Email, Requested Freebie, Marketing Opt-In, Source URL, Delivery Status.
 * - Keep the Freebie Catalog tab as the human-readable catalog/reference list.
 * - The 19 asset keys and HTML resource URLs below must match the Freebie Catalog entries
 *   and the website forms' submitted "asset" values.
 *
 * Setup:
 * 1) Copy the spreadsheet ID from the Google Sheets URL into SHEET_ID below.
 * 2) Extensions > Apps Script; paste/save this file.
 * 3) Deploy as a Web app: Execute as you, access Anyone.
 * 4) Copy the deployed /exec URL into email-config.js.
 * 5) Test a signup with your own email and confirm a Subscribers row and the correct HTML redirect.
 * Only use Marketing Opt-In = YES when the user explicitly opted in.
 */
const SHEET_ID = '1LMswnT-46ONCQmnVzeCEAgTR41wJufDOg_9iz01lR0Y';
const SITE_NAME = "What's for Eats";
const ASSETS = {
  "20-lazy-dinners-for-when-your-brain-has-left-the-building": {
    "title": "20 Lazy Dinners for When Your Brain Has Left the Building",
    "desc": "A low-effort dinner guide for tired nights.",
    "url": "https://whatsforeats.online/20-lazy-dinners-for-when-your-brain-has-left-the-building.html"
  },
  "20-lazy-dinners-sorted-by-how-tired-you-are": {
    "title": "20 Lazy Dinners Sorted by How Tired You Are",
    "desc": "Choose dinner ideas by your energy level.",
    "url": "https://whatsforeats.online/20-lazy-dinners-sorted-by-how-tired-you-are.html"
  },
  "22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater": {
    "title": "22 Cozy Fall Dinners",
    "desc": "Cozy seasonal dinners and comfort-food inspiration.",
    "url": "https://whatsforeats.online/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html"
  },
  "5-ingredient-dinners": {
    "title": "5-Ingredient Dinners",
    "desc": "Simplify dinner with a short ingredient list.",
    "url": "https://whatsforeats.online/5-ingredient-dinners.html"
  },
  "7-night-dinner-plan-for-picky-families": {
    "title": "7-Night Dinner Plan for Picky Families",
    "desc": "Seven flexible dinners with easy swaps.",
    "url": "https://whatsforeats.online/7-night-dinner-plan-for-picky-families.html"
  },
  "cheap-family-dinners-cost-per-serving": {
    "title": "Cheap Family Dinners With Cost Per Serving",
    "desc": "Budget-friendly dinners and cost-per-serving tips.",
    "url": "https://whatsforeats.online/cheap-family-dinners-cost-per-serving.html"
  },
  "easy-dinner-ideas-no-energy": {
    "title": "Easy Dinner Ideas for When You Have No Energy",
    "desc": "Fast ideas for low-energy evenings.",
    "url": "https://whatsforeats.online/easy-dinner-ideas-no-energy.html"
  },
  "easy-sheet-pan-dinners": {
    "title": "Easy Sheet-Pan Dinners",
    "desc": "One-pan dinner ideas and cleanup shortcuts.",
    "url": "https://whatsforeats.online/easy-sheet-pan-dinners.html"
  },
  "easy-weeknight-dinner-recipes": {
    "title": "Easy Weeknight Dinner Recipes",
    "desc": "Weeknight recipes and practical cooking ideas.",
    "url": "https://whatsforeats.online/easy-weeknight-dinner-recipes.html"
  },
  "freezer-meals-for-busy-weeknights": {
    "title": "Freezer Meals for Busy Weeknights",
    "desc": "Make-ahead meals, freezing, thawing, and reheating.",
    "url": "https://whatsforeats.online/freezer-meals-for-busy-weeknights.html"
  },
  "leftover-chicken-recipes": {
    "title": "Leftover Chicken Recipes",
    "desc": "Turn cooked chicken into another easy dinner.",
    "url": "https://whatsforeats.online/leftover-chicken-recipes.html"
  },
  "pantry-staples-list-for-budget-cooking": {
    "title": "Pantry Staples List for Budget Cooking",
    "desc": "Build flexible dinners from pantry basics.",
    "url": "https://whatsforeats.online/pantry-staples-list-for-budget-cooking.html"
  },
  "picky-eater-dinner-ideas": {
    "title": "Picky-Eater Dinner Ideas",
    "desc": "Flexible family meals and low-pressure swaps.",
    "url": "https://whatsforeats.online/picky-eater-dinner-ideas.html"
  },
  "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer": {
    "title": "Sheet Pan vs. Slow Cooker vs. One Pot vs. Air Fryer",
    "desc": "Compare dinner methods, effort, and cleanup.",
    "url": "https://whatsforeats.online/sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer.html"
  },
  "slow-cooker-dinners-for-busy-families": {
    "title": "Slow Cooker Dinners for Busy Families",
    "desc": "Hands-off dinners for busy days.",
    "url": "https://whatsforeats.online/slow-cooker-dinners-for-busy-families.html"
  },
  "weekly-meal-plan-for-busy-families": {
    "title": "Weekly Meal Plan for Busy Families",
    "desc": "Seven-night planning with a practical shopping list.",
    "url": "https://whatsforeats.online/weekly-meal-plan-for-busy-families.html"
  },
  "picky-family-7-night-dinner-plan": {
    "title": "7-Night Dinner Plan Printable",
    "desc": "The print-focused weekly meal plan.",
    "url": "https://whatsforeats.online/picky-family-7-night-dinner-plan-printable.html"
  },
  "lazy-dinner-energy-picker": {
    "title": "Energy Level Dinner Picker",
    "desc": "A low-effort guide to match dinner to your energy.",
    "url": "https://whatsforeats.online/20-lazy-dinners-sorted-by-how-tired-you-are.html"
  },
  "cozy-fall-dinner-bingo": {
    "title": "Cozy Fall Dinner Bingo and Dinner Guide",
    "desc": "Seasonal dinner inspiration in printable form.",
    "url": "https://whatsforeats.online/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html"
  }
};
function doPost(e) {
  try {
    let data = (e && e.parameter) ? e.parameter : {};
    if (e && e.postData && e.postData.contents && String(e.postData.type || '').indexOf('application/json') !== -1) data = JSON.parse(e.postData.contents);
    const email = String(data.email || '').trim().toLowerCase();
    const assetKey = String(data.asset || 'picky-family-7-night-dinner-plan');
    const asset = ASSETS[assetKey];
    const marketing = data.marketing === true || String(data.marketing || '').toLowerCase() === 'true';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return resultPage({ok:false,message:'Enter a valid email address.'});
    if (!asset) return resultPage({ok:false,message:'That free resource was not found. Please choose it again from the library.'});
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName('Subscribers');
    if (!sheet) {
      sheet = ss.insertSheet('Subscribers');
      sheet.appendRow(['Timestamp','Email','Requested Freebie','Marketing Opt-In','Source URL','Delivery Status']);
      sheet.setFrozenRows(1);
    }
    const row = sheet.getLastRow() + 1;
    sheet.appendRow([new Date(), email, asset.title, marketing ? 'YES' : 'NO', String(data.source || ''), 'Recorded — HTML redirect']);
    sheet.getRange(row, 6).setValue('Recorded — HTML redirect');
    return resultPage({ok:true, redirect:asset.url, message:'Request saved. Opening your resource.'});

  } catch (err) {
    return resultPage({ok:false,message:'Signup could not be saved. Please try again.'});
  }
}
function doGet() {
  return json({ok:true,service:SITE_NAME+' HTML free-resource capture',message:'POST email, asset, marketing, and source fields.'});
}
function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function resultPage(result) {
  const payload = JSON.stringify(result).replace(/</g, '\\u003c');
  const status = result.ok ? 'Opening your resource…' : 'Your request could not be saved.';
  const html = '<!doctype html><html><head><meta charset="utf-8"><title>Free resource</title></head><body><p>' + status + '</p><script>window.parent.postMessage({type:"freebie-signup-result",payload:1,...' + payload + '}, "*");</script></body></html>';
  return HtmlService.createHtmlOutput(html).setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
