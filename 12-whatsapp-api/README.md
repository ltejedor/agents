# WhatsApp Cloud API Webhook Server (Echo Bot)

This example demonstrates how to set up a webhook server using the WhatsApp Cloud API that echoes back any incoming text messages.

## Prerequisites

- Node.js >= 16
- A Meta Business Account (Business Manager)
- A Developer account on Facebook for Developers
- A WhatsApp Business App with the WhatsApp product added
- A WhatsApp Business phone number (for production) or use one of the 5 test numbers provided by Meta in the sandbox

## Signing Up for WhatsApp Cloud API

1. Create a Meta Business Account at https://business.facebook.com/.
2. Sign up as a developer at https://developers.facebook.com/.
3. Create a new App in Facebook Developers: https://developers.facebook.com/apps.
4. In your App dashboard, select **Add Product** and choose **WhatsApp**.
5. Under **Business Assets > Business Manager**, assign your App to the Business Manager account you created earlier.
6. Follow the official WhatsApp Cloud API Get Started guide to set up your phone number, generate credentials, and configure webhooks:  
   https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/

## Obtaining Credentials

After completing the steps above, you will need the following:

- **GRAPH_API_TOKEN**: A permanent access token generated for your App (via a System User or Facebook Login)  
  Reference: https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login  
- **WEBHOOK_VERIFY_TOKEN**: An arbitrary string you choose to verify webhook setup  
- **PHONE_NUMBER_ID**: The ID of the phone number you are using (shown in the Cloud API dashboard)  

## Environment Variables

Create a `.env` file in the `server` directory or set these variables in your environment:

```
GRAPH_API_TOKEN=<your_graph_api_token>
WEBHOOK_VERIFY_TOKEN=<your_verify_token>
PORT=3000
```

## Running the Server

```bash
cd server
npm install
npm start
```

If you are developing locally, use a tunneling service (e.g., ngrok) to expose your webhook endpoint to the internet:

```bash
npx ngrok http 3000
```

Use the forwarded URL from ngrok (e.g., `https://abcd1234.ngrok.io/webhook`) when configuring the webhook in the Facebook Developers console.

## Testing the Echo Bot

1. Send a WhatsApp message to your Business phone number or test number.  
2. The server will receive the webhook event and echo back your message prefixed with `Echo:`.  

## Notes

- This App is currently in **Testing** mode. In testing, you can only send messages to up to 5 phone numbers registered as test recipients.  
- To move to production, submit your App for App Review in the Facebook Developers dashboard.  


