# Freebie HTML guide delivery

The free-resource library uses the designed, interactive HTML guides in `/pdfs/*.html`. Each guide includes checkboxes and a **Print or save as PDF** control.

## Signup flow

1. A visitor chooses a guide from `free-pdfs.html` or submits the email gate on a blog page.
2. The form posts the email, resource key, optional marketing consent, and source URL to the Apps Script web app configured in `email-config.js`.
3. `google-apps-script/FreebieDelivery.gs` validates the request and writes it to the `Subscribers` sheet.
4. Apps Script emails the guide link, then returns a small HTML response that posts a result message to the parent page.
5. The form page redirects to the matching `/pdfs/<guide>.html` route. The guide's Print button can create a printable/PDF copy.

## Required Apps Script deployment step

Updating this repository does **not** automatically update an already-deployed Google Apps Script web app.

1. Open the Google Apps Script project attached to the existing web-app URL configured in `email-config.js`.
2. Replace the script with the current contents of `google-apps-script/FreebieDelivery.gs`.
3. Save the project.
4. Choose **Deploy → Manage deployments**, edit the existing web-app deployment, select **New version**, and deploy. Keep the same deployment URL if editing the existing deployment.
5. Confirm the deployment executes as the owner and is accessible to anyone.
6. Test a signup using your own email. Confirm a new row appears in `Subscribers`, the browser opens the correct HTML guide, and the email contains the matching guide link.

Do not mark the delivery system as fully live until that end-to-end test passes.
