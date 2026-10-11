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
