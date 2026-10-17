/** What's for Eats printable delivery + subscriber log.
 * Google Sheet compatibility:
 * - Use the updated email-list workbook imported into Google Sheets.
 * - Keep the Subscribers tab and its six columns in this exact order:
 *   Timestamp, Email, Requested Freebie, Marketing Opt-In, Source URL, Delivery Status.
 * - Keep the Freebie Catalog tab as the human-readable catalog/reference list.
 * - The 19 asset keys and HTML guide URLs below must match the Freebie Catalog entries
 *   and the website forms' submitted "asset" values.
 *
 * Setup:
 * 1) Copy the spreadsheet ID from the Google Sheets URL into SHEET_ID below.
 * 2) Extensions > Apps Script; paste/save this file.
 * 3) Deploy as a Web app: Execute as you, access Anyone.
 * 4) Copy the deployed /exec URL into email-config.js.
 * 5) Deploy a new version, then test a signup and confirm a Subscribers row, redirect to the matching HTML guide, and delivery email.
 * Only use Marketing Opt-In = YES when the user explicitly opted in.
 */
const SHEET_ID = '1LMswnT-46ONCQmnVzeCEAgTR41wJufDOg_9iz01lR0Y';
const SITE_NAME = "What's for Eats";
const ASSETS = {
  "20-lazy-dinners-for-when-your-brain-has-left-the-building": {
    "title": "20 Lazy Dinners for When Your Brain Has Left the Building",
    "desc": "A low-effort dinner guide for tired nights.",
    "url": "https://whatsforeats.online/pdfs/dinner-rescue-playbook.html"
  },
  "20-lazy-dinners-sorted-by-how-tired-you-are": {
    "title": "20 Lazy Dinners Sorted by How Tired You Are",
    "desc": "Choose dinner ideas by your energy level.",
    "url": "https://whatsforeats.online/pdfs/energy-level-dinner-selector.html"
  },
  "22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater": {
    "title": "22 Cozy Fall Dinners",
    "desc": "Cozy seasonal dinners and comfort-food inspiration.",
    "url": "https://whatsforeats.online/pdfs/cozy-season-supper-collection.html"
  },
  "5-ingredient-dinners": {
    "title": "5-Ingredient Dinners",
    "desc": "Simplify dinner with a short ingredient list.",
    "url": "https://whatsforeats.online/pdfs/five-ingredient-favorites.html"
  },
  "7-night-dinner-plan-for-picky-families": {
    "title": "7-Night Dinner Plan for Picky Families",
    "desc": "Seven flexible dinners with easy swaps.",
    "url": "https://whatsforeats.online/pdfs/picky-family-weeknight-blueprint.html"
  },
  "cheap-family-dinners-cost-per-serving": {
    "title": "Cheap Family Dinners With Cost Per Serving",
    "desc": "Budget-friendly dinners and cost-per-serving tips.",
    "url": "https://whatsforeats.online/pdfs/budget-bites-cost-guide.html"
  },
  "easy-dinner-ideas-no-energy": {
    "title": "Easy Dinner Ideas for When You Have No Energy",
    "desc": "Fast ideas for low-energy evenings.",
    "url": "https://whatsforeats.online/pdfs/low-energy-meal-survival-guide.html"
  },
  "easy-sheet-pan-dinners": {
    "title": "Easy Sheet-Pan Dinners",
    "desc": "One-pan dinner ideas and cleanup shortcuts.",
    "url": "https://whatsforeats.online/pdfs/sheet-pan-supper-starter.html"
  },
  "easy-weeknight-dinner-recipes": {
    "title": "Easy Weeknight Dinner Recipes",
    "desc": "Weeknight recipes and practical cooking ideas.",
    "url": "https://whatsforeats.online/pdfs/weeknight-dinner-companion.html"
  },
  "freezer-meals-for-busy-weeknights": {
    "title": "Freezer Meals for Busy Weeknights",
    "desc": "Make-ahead meals, freezing, thawing, and reheating.",
    "url": "https://whatsforeats.online/pdfs/freezer-friendly-family-meals.html"
  },
  "leftover-chicken-recipes": {
    "title": "Leftover Chicken Recipes",
    "desc": "Turn cooked chicken into another easy dinner.",
    "url": "https://whatsforeats.online/pdfs/chicken-leftover-reinvention-kit.html"
  },
  "pantry-staples-list-for-budget-cooking": {
    "title": "Pantry Staples List for Budget Cooking",
    "desc": "Build flexible dinners from pantry basics.",
    "url": "https://whatsforeats.online/pdfs/budget-pantry-checklist.html"
  },
  "picky-eater-dinner-ideas": {
    "title": "Picky-Eater Dinner Ideas",
    "desc": "Flexible family meals and low-pressure swaps.",
    "url": "https://whatsforeats.online/pdfs/picky-eater-plate-builder.html"
  },
  "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer": {
    "title": "Sheet Pan vs. Slow Cooker vs. One Pot vs. Air Fryer",
    "desc": "Compare dinner methods, effort, and cleanup.",
    "url": "https://whatsforeats.online/pdfs/cooking-method-cheat-sheet.html"
  },
  "slow-cooker-dinners-for-busy-families": {
    "title": "Slow Cooker Dinners for Busy Families",
    "desc": "Hands-off dinners for busy days.",
    "url": "https://whatsforeats.online/pdfs/slow-cooker-comfort-collection.html"
  },
  "weekly-meal-plan-for-busy-families": {
    "title": "Weekly Meal Plan for Busy Families",
    "desc": "Seven-night planning with a practical shopping list.",
    "url": "https://whatsforeats.online/pdfs/family-meal-planning-map.html"
  },
  "picky-family-7-night-dinner-plan": {
    "title": "7-Night Dinner Plan Printable",
    "desc": "The print-focused weekly meal plan.",
    "url": "https://whatsforeats.online/pdfs/seven-night-picky-eater-menu.html"
  },
  "lazy-dinner-energy-picker": {
    "title": "Energy Level Dinner Picker",
    "desc": "A low-effort guide to match dinner to your energy.",
    "url": "https://whatsforeats.online/pdfs/what-to-cook-tonight-picker.html"
  },
  "cozy-fall-dinner-bingo": {
    "title": "Cozy Fall Dinner Bingo and Dinner Guide",
    "desc": "Seasonal dinner inspiration in printable form.",
    "url": "https://whatsforeats.online/pdfs/cozy-dinner-bingo.html"
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
    if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) return resultPage({ok:false,error:'Enter a valid email address.'});
    if (!asset) return resultPage({ok:false,error:'That printable was not found.'});

    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName('Subscribers');
    if (!sheet) {
      sheet = ss.insertSheet('Subscribers');
      sheet.appendRow(['Timestamp','Email','Requested Freebie','Marketing Opt-In','Source URL','Delivery Status']);
      sheet.setFrozenRows(1);
    }
    const row = sheet.getLastRow() + 1;
    sheet.appendRow([new Date(), email, asset.title, marketing ? 'YES' : 'NO', String(data.source || ''), 'Signup recorded']);

    let status = 'Signup recorded; redirect ready';
    try {
      const subject = 'Your free dinner guide: ' + asset.title;
      const body = 'Thanks for requesting a free resource from ' + SITE_NAME + '.\\n\\nOpen your guide and use its Print button to print or save a PDF: ' + asset.url + '\\n\\nYou requested this delivery email. Marketing emails will only be sent if you separately opted in on the form.\\n\\n— ' + SITE_NAME;
      MailApp.sendEmail({to: email, subject: subject, body: body, name: SITE_NAME});
      status = 'Email sent; redirect ready';
    } catch (mailErr) {
      status = 'Signup recorded; email send failed; redirect ready';
    }
    sheet.getRange(row, 6).setValue(status);
    return resultPage({ok:true,title:asset.title,url:asset.url,marketingOptIn:marketing});
  } catch (err) {
    return resultPage({ok:false,error:'Signup could not be completed. Please try again.'});
  }
}
function resultPage(result) {
  const payload = JSON.stringify(result).replace(/</g, '\\u003c');
  const html = '<!doctype html><html><head><meta charset="utf-8"><title>Free dinner guide</title></head><body><p>' +
    (result.ok ? 'Your guide is ready. Opening it now…' : 'We could not complete your request.') +
    '</p><script>window.parent.postMessage({type:"freebie-signup-result",payload:' + payload + '}, "*");<\/script></body></html>';
  return HtmlService.createHtmlOutput(html).setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
function doGet() {
  return json({ok:true,service:SITE_NAME+' printable delivery',message:'POST email, asset, marketing, and source fields.'});
}
function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
