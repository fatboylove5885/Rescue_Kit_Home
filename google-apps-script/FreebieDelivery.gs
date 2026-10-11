/** What's for Eats printable delivery + subscriber log.
 * 1) Create a Google Sheet from the supplied lead-tracker CSV or a blank sheet.
 * 2) Extensions > Apps Script; paste this file.
 * 3) Set SHEET_ID and deploy as a Web app: Execute as you, access Anyone.
 * 4) Copy the /exec URL into freebies.html as window.FREEBIES_WEB_APP_URL.
 * 5) Test with your own email before promoting. Do not send newsletter messages unless marketingOptIn is true.
 */
const SHEET_ID = 'PASTE_GOOGLE_SHEET_ID_HERE';
const SITE_NAME = "What's for Eats";
const ASSETS = {
  'picky-family-7-night-dinner-plan': {
    title: 'A 7-Night Dinner Plan for Picky Families',
    url: 'https://whatsforeats.online/picky-family-7-night-dinner-plan-printable.html'
  },
  'lazy-dinner-energy-picker': {
    title: 'Energy Level Dinner Picker',
    url: 'https://whatsforeats.online/20-lazy-dinners-for-when-your-brain-has-left-the-building.html#picker'
  },
  'cozy-fall-dinner-bingo': {
    title: 'Cozy Fall Dinner Bingo',
    url: 'https://whatsforeats.online/22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html'
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
    const subject = 'Your free printable: ' + asset.title;
    const body = 'Thanks for requesting a free printable from ' + SITE_NAME + '.\n\nHere is your requested resource: ' + asset.url + '\n\nYou requested this delivery email. You will only receive occasional marketing emails if you separately opted in on the form.\n\n— ' + SITE_NAME;
    MailApp.sendEmail({to: email, subject: subject, body: body, name: SITE_NAME});
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