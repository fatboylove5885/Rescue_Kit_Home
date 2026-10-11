/** What's for Eats printable delivery + subscriber log.
 * 1) Create a Google Sheet from the supplied lead-tracker CSV or a blank sheet.
 * 2) Extensions > Apps Script; paste this file.
 * 3) Set SHEET_ID and deploy as a Web app: Execute as you, access Anyone.
 * 4) Copy the /exec URL into email-config.js as window.FREEBIES_WEB_APP_URL.
 * 5) Test with your own email before promoting. Do not send newsletter messages unless marketingOptIn is true.
 */
const SHEET_ID = 'PASTE_GOOGLE_SHEET_ID_HERE';
const SITE_NAME = "What's for Eats";
const ASSETS = {
  "20-lazy-dinners-for-when-your-brain-has-left-the-building": {
    "title": "20 Lazy Dinners for When Your Brain Has Left the Building",
    "desc": "A low-effort dinner guide for tired nights.",
    "url": "https://whatsforeats.online/pdfs/20-lazy-dinners-for-when-your-brain-has-left-the-building.pdf"
  },
  "20-lazy-dinners-sorted-by-how-tired-you-are": {
    "title": "20 Lazy Dinners Sorted by How Tired You Are",
    "desc": "Choose dinner ideas by your energy level.",
    "url": "https://whatsforeats.online/pdfs/20-lazy-dinners-sorted-by-how-tired-you-are.pdf"
  },
  "22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater": {
    "title": "22 Cozy Fall Dinners",
    "desc": "Cozy seasonal dinners and comfort-food inspiration.",
    "url": "https://whatsforeats.online/pdfs/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.pdf"
  },
  "5-ingredient-dinners": {
    "title": "5-Ingredient Dinners",
    "desc": "Simplify dinner with a short ingredient list.",
    "url": "https://whatsforeats.online/pdfs/5-ingredient-dinners.pdf"
  },
  "7-night-dinner-plan-for-picky-families": {
    "title": "7-Night Dinner Plan for Picky Families",
    "desc": "Seven flexible dinners with easy swaps.",
    "url": "https://whatsforeats.online/pdfs/7-night-dinner-plan-for-picky-families.pdf"
  },
  "cheap-family-dinners-cost-per-serving": {
    "title": "Cheap Family Dinners With Cost Per Serving",
    "desc": "Budget-friendly dinners and cost-per-serving tips.",
    "url": "https://whatsforeats.online/pdfs/cheap-family-dinners-cost-per-serving.pdf"
  },
  "easy-dinner-ideas-no-energy": {
    "title": "Easy Dinner Ideas for When You Have No Energy",
    "desc": "Fast ideas for low-energy evenings.",
    "url": "https://whatsforeats.online/pdfs/easy-dinner-ideas-no-energy.pdf"
  },
  "easy-sheet-pan-dinners": {
    "title": "Easy Sheet-Pan Dinners",
    "desc": "One-pan dinner ideas and cleanup shortcuts.",
    "url": "https://whatsforeats.online/pdfs/easy-sheet-pan-dinners.pdf"
  },
  "easy-weeknight-dinner-recipes": {
    "title": "Easy Weeknight Dinner Recipes",
    "desc": "Weeknight recipes and practical cooking ideas.",
    "url": "https://whatsforeats.online/pdfs/easy-weeknight-dinner-recipes.pdf"
  },
  "freezer-meals-for-busy-weeknights": {
    "title": "Freezer Meals for Busy Weeknights",
    "desc": "Make-ahead meals, freezing, thawing, and reheating.",
    "url": "https://whatsforeats.online/pdfs/freezer-meals-for-busy-weeknights.pdf"
  },
  "leftover-chicken-recipes": {
    "title": "Leftover Chicken Recipes",
    "desc": "Turn cooked chicken into another easy dinner.",
    "url": "https://whatsforeats.online/pdfs/leftover-chicken-recipes.pdf"
  },
  "pantry-staples-list-for-budget-cooking": {
    "title": "Pantry Staples List for Budget Cooking",
    "desc": "Build flexible dinners from pantry basics.",
    "url": "https://whatsforeats.online/pdfs/pantry-staples-list-for-budget-cooking.pdf"
  },
  "picky-eater-dinner-ideas": {
    "title": "Picky-Eater Dinner Ideas",
    "desc": "Flexible family meals and low-pressure swaps.",
    "url": "https://whatsforeats.online/pdfs/picky-eater-dinner-ideas.pdf"
  },
  "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer": {
    "title": "Sheet Pan vs. Slow Cooker vs. One Pot vs. Air Fryer",
    "desc": "Compare dinner methods, effort, and cleanup.",
    "url": "https://whatsforeats.online/pdfs/sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer.pdf"
  },
  "slow-cooker-dinners-for-busy-families": {
    "title": "Slow Cooker Dinners for Busy Families",
    "desc": "Hands-off dinners for busy days.",
    "url": "https://whatsforeats.online/pdfs/slow-cooker-dinners-for-busy-families.pdf"
  },
  "weekly-meal-plan-for-busy-families": {
    "title": "Weekly Meal Plan for Busy Families",
    "desc": "Seven-night planning with a practical shopping list.",
    "url": "https://whatsforeats.online/pdfs/weekly-meal-plan-for-busy-families.pdf"
  },
  "picky-family-7-night-dinner-plan": {
    "title": "7-Night Dinner Plan Printable",
    "desc": "The print-focused weekly meal plan.",
    "url": "https://whatsforeats.online/pdfs/picky-family-7-night-dinner-plan-printable.pdf"
  },
  "lazy-dinner-energy-picker": {
    "title": "Energy Level Dinner Picker",
    "desc": "A low-effort guide to match dinner to your energy.",
    "url": "https://whatsforeats.online/pdfs/lazy-dinner-energy-picker.pdf"
  },
  "cozy-fall-dinner-bingo": {
    "title": "Cozy Fall Dinner Bingo and Dinner Guide",
    "desc": "Seasonal dinner inspiration in printable form.",
    "url": "https://whatsforeats.online/pdfs/cozy-fall-dinner-bingo.pdf"
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
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ok:false,error:'Enter a valid email address.'});
    if (!asset) return json({ok:false,error:'That printable was not found.'});
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName('Subscribers');
    if (!sheet) {
      sheet = ss.insertSheet('Subscribers');
      sheet.appendRow(['Timestamp','Email','Requested Freebie','Marketing Opt-In','Source URL','Delivery Status']);
      sheet.setFrozenRows(1);
    }
    const row = sheet.getLastRow() + 1;
    sheet.appendRow([new Date(), email, asset.title, marketing ? 'YES' : 'NO', String(data.source || ''), 'Pending']);
    const subject = 'Your free PDF: ' + asset.title;
    const body = 'Thanks for requesting a free PDF from ' + SITE_NAME + '.\n\nYour PDF is attached, and you can also open it here: ' + asset.url + '\n\nYou requested this delivery email. You will only receive occasional marketing emails if you separately opted in on the form.\n\n— ' + SITE_NAME;
    const response = UrlFetchApp.fetch(asset.url, {muteHttpExceptions:true, followRedirects:true});
    if (response.getResponseCode() < 200 || response.getResponseCode() >= 300) throw new Error('PDF could not be retrieved for attachment: ' + asset.url);
    const pdfBlob = response.getBlob().setName(asset.title.replace(/[^a-z0-9 -]/gi, '').replace(/\\s+/g, '-') + '.pdf');
    MailApp.sendEmail({to: email, subject: subject, body: body, name: SITE_NAME, attachments:[pdfBlob]});
    sheet.getRange(row, 6).setValue('Email sent');
    return json({ok:true,marketingOptIn:marketing});
  } catch (err) {
    return json({ok:false,error:'Signup could not be completed.'});
  }
}
function doGet() {
  return json({ok:true,service:SITE_NAME+' printable delivery',message:'POST email, asset, marketing, and source fields.'});
}
function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}