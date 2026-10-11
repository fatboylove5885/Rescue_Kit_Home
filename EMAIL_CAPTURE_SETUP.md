# What's for Eats: printable email capture setup

The site files and subscriber-tracker template are in this repository. The email form is intentionally not live until the site owner authorizes Google Apps Script and supplies the Web App URL and Google Sheet ID.

## 1. Create the Google Sheet

1. Download `freebie-subscriber-tracker-template.csv` from this repository.
2. In Google Drive, create a Google Sheet and use **File → Import → Upload** to import the CSV.
3. Name the first tab `Subscribers`.
4. Copy the Sheet ID from the URL (the part between `/d/` and `/edit`).

The columns are: Timestamp, Email, Requested Freebie, Marketing Opt-In, Source URL, Delivery Status.

## If “Extensions → Apps Script” is missing

- Open the spreadsheet in a **desktop browser** at `https://sheets.google.com` or `https://docs.google.com/spreadsheets/`. The Google Sheets iPhone/iPad app does not expose the full Apps Script editor menu.
- Make sure you are in the actual spreadsheet editor (URL normally contains `/spreadsheets/d/...`), not Drive's preview, a CSV preview, or an Excel file opened in compatibility mode.
- If you imported the CSV, save it as a native Google Sheets spreadsheet: open a new Google Sheet, use **File → Import → Upload**, select the CSV, and choose **Insert new sheet(s)** or import into the spreadsheet. Confirm the tab is named `Subscribers`.
- Confirm you have edit access. A view-only file or managed work/school account with Apps Script disabled may hide or block the menu.
- Then use **Extensions → Apps Script** from the desktop editor. You can also open Apps Script from `https://script.google.com`, create a project, paste the supplied script, and set the Sheet ID in the code.

## 2. Authorize the email delivery script

1. Open the Sheet and choose **Extensions → Apps Script**.
2. Replace the starter code with `google-apps-script/FreebieDelivery.gs`.
3. Replace `PASTE_GOOGLE_SHEET_ID_HERE` with your Sheet ID.
4. Save, choose **Deploy → New deployment → Web app**.
5. Set **Execute as: Me** and choose an access setting that allows public form submissions (usually **Anyone**). Review Google's warning and approve the permissions for Sheets and sending email.
6. Copy the deployed Web app URL ending in `/exec`.

## 3. Connect the site form

In `email-config.js`, replace `PASTE_YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE` with the deployed `/exec` URL. This single shared config connects the inline email gates on every blog and the Free PDFs library. Commit the change and wait for the site host to deploy.

## 4. Test before promoting

- Request the new 7-night printable using your own email.
- Confirm the row appears in the `Subscribers` tab.
- Confirm the delivery email arrives and its link opens the print-ready page.
- Try a second test with the newsletter box unchecked; the row should show `NO`.
- Only send future newsletter campaigns to people whose `Marketing Opt-In` value is `YES`.

## Important notes

- The freebie delivery email is transactional: it sends the resource requested by the visitor. Marketing permission is a separate, optional checkbox.
- This site emails the requested standalone PDF as an attachment and includes a direct PDF link. The static PDFs are publicly hosted, so this is a soft email gate rather than access control; anyone who already has a PDF URL can open it directly.
- The form is not active until steps 1–3 are completed. Do not advertise the email gate as working before you test it.
- This is a simple soft gate: the print-ready page itself is a public URL. It is designed to encourage signups, not provide DRM or prevent a visitor from sharing the link.

## If the Extensions menu is missing

The Apps Script editor is available only from a native Google Sheets spreadsheet that you can edit. If you opened the CSV file itself, an Excel preview, or a view-only file, **Extensions** may not appear. Open the actual spreadsheet from [Google Sheets](https://sheets.google.com), confirm you have Editor access, and if needed choose **File → Save as Google Sheets** to convert an Excel file. Then open **Extensions → Apps Script** from that converted, editable spreadsheet.
