# What's for Eats: HTML freebie email capture setup

The free-resource flow collects the visitor's email and request details in Google Sheets, then redirects the visitor to the matching styled HTML resource. It does **not** send a PDF attachment. Newsletter permission remains a separate optional checkbox.

## 1. Google Sheet

Use the Google Sheet ID configured in `google-apps-script/FreebieDelivery.gs`. The `Subscribers` tab must use these exact columns, in this order:

`Timestamp | Email | Requested Freebie | Marketing Opt-In | Source URL | Delivery Status`

The script creates the `Subscribers` tab and header row if they do not exist. Keep the optional `Freebie Catalog` tab if you use it for reference. Only send newsletters to people whose `Marketing Opt-In` value is `YES`.

## 2. Update and deploy the Apps Script

1. Open the Google Sheet in a desktop browser and choose **Extensions → Apps Script**. If that menu is missing, open [script.google.com](https://script.google.com) and select the existing project.
2. Replace the Apps Script code with the latest contents of `google-apps-script/FreebieDelivery.gs` from this repository.
3. Confirm `SHEET_ID` matches the Google Sheet ID.
4. Save the project.
5. Choose **Deploy → Manage deployments**, edit the existing Web App deployment, select a new version, and deploy it. Keep the same Web App URL if possible.
6. Confirm the deployment runs as you and accepts public form submissions. Authorize Sheets access if prompted.

**Important:** Updating GitHub does not automatically update code already deployed in Google Apps Script. Redeploy the script for the live endpoint to use this behavior.

## 3. Website configuration

`email-config.js` contains the deployed Apps Script URL and the asset-key-to-HTML-route map. If the Web App URL changes, update `window.FREEBIES_WEB_APP_URL` there and commit the change.

The free resource library and request page use the shared endpoint. Blog pages with free-resource forms submit the same fields. A successful request should create a row with timestamp, email, requested resource, marketing choice, source URL, and status `Recorded — HTML redirect`; then the browser opens the mapped HTML guide.

## 4. Test the full flow

1. Open [the free resource library](https://whatsforeats.online/free-pdfs.html).
2. Choose a guide and submit your own email address with marketing consent unchecked.
3. Confirm a new row appears in `Subscribers`, with `NO` in Marketing Opt-In and the correct source URL.
4. Confirm the browser redirects to the correct styled HTML guide.
5. Repeat with marketing consent checked and confirm that row records `YES`.
6. Test a second resource to ensure each asset key opens the correct page.

## Privacy and behavior

- The email is collected to record the resource request. Newsletter consent is optional and separate.
- This flow does not email PDF attachments. The browser opens the HTML resource after the request is recorded.
- HTML resources are public URLs, so this is a signup flow, not access control or DRM.
- Do not advertise the flow as live until the Apps Script deployment is updated and the full test succeeds.
