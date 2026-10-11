# What's for Eats: printable email capture setup

The site files and subscriber-tracker template are in this repository. The email form is intentionally not live until the site owner authorizes Google Apps Script and supplies the Web App URL and Google Sheet ID.

## 1. Create the Google Sheet

1. Download `freebie-subscriber-tracker-template.csv` from this repository.
2. In Google Drive, create a Google Sheet and use **File → Import → Upload** to import the CSV.
3. Name the first tab `Subscribers`.
4. Copy the Sheet ID from the URL (the part between `/d/` and `/edit`).

The columns are: Timestamp, Email, Requested Freebie, Marketing Opt-In, Source URL, Delivery Status.

## 2. Authorize the email delivery script

1. Open the Sheet and choose **Extensions → Apps Script**.
2. Replace the starter code with `google-apps-script/FreebieDelivery.gs`.
3. Replace `PASTE_GOOGLE_SHEET_ID_HERE` with your Sheet ID.
4. Save, choose **Deploy → New deployment → Web app**.
5. Set **Execute as: Me** and choose an access setting that allows public form submissions (usually **Anyone**). Review Google's warning and approve the permissions for Sheets and sending email.
6. Copy the deployed Web app URL ending in `/exec`.

## 3. Connect the site form

In `freebies.html`, replace `PASTE_YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE` with the deployed URL. Commit the change and wait for the site host to deploy.

## 4. Test before promoting

- Request the new 7-night printable using your own email.
- Confirm the row appears in the `Subscribers` tab.
- Confirm the delivery email arrives and its link opens the print-ready page.
- Try a second test with the newsletter box unchecked; the row should show `NO`.
- Only send future newsletter campaigns to people whose `Marketing Opt-In` value is `YES`.

## Important notes

- The freebie delivery email is transactional: it sends the resource requested by the visitor. Marketing permission is a separate, optional checkbox.
- This static-site version delivers a link to a print-ready page with a **Print / Save as PDF** button. The standalone PDF generated for the current plan is also attached in the working ChatGPT conversation.
- The form is not active until steps 1–3 are completed. Do not advertise the email gate as working before you test it.
- This is a simple soft gate: the print-ready page itself is a public URL. It is designed to encourage signups, not provide DRM or prevent a visitor from sharing the link.
