# Getting Started with WhatsApp Business API

This tutorial will guide you through the process of setting up and using the WhatsApp Business API through Meta's Cloud API.

## Prerequisites

Before you begin, ensure you have:

- A Meta developer account
- A business that complies with WhatsApp's Commerce Policy and Business Policy
- A smartphone with an active phone number for testing
- Basic understanding of API concepts

## Step 1: Create a Meta Developer Account

1. Visit the [Meta for Developers](https://developers.facebook.com/) website
2. Click on **Get Started** or **Log In** (if you already have a Facebook account)
3. Complete the registration process or log in with your existing credentials

## Step 2: Create a Meta App

1. Log in to your Meta Developer account
2. Navigate to **My Apps** in the top navigation
3. Click on **Create App**
4. Select **Business** as the app type
5. Fill in the app details (name, contact email)
6. Click **Create App**

## Step 3: Add WhatsApp to Your App

1. In your app dashboard, scroll down to find the product list
2. Find **WhatsApp** and click **Set up**
3. You'll be prompted to select an existing Business Manager or create a new one
4. Select or create a business account as needed

## Step 4: Access Your WhatsApp API Credentials

1. Navigate to the **WhatsApp** > **API Setup** section
2. Here you'll find your:
   - Phone Number ID
   - WhatsApp Business Account ID
   - Temporary access token

> **Note:** The temporary access token expires in 24 hours. For production, you'll need to generate a permanent access token.

## Step 5: Set Up a Test Phone Number

1. In the **API Setup** panel, you'll see your test phone number
2. This number is provided by Meta for development purposes
3. You can add up to 5 recipient phone numbers for testing
4. Add your own number to the test number list by clicking **Add Phone Number**

## Step 6: Send Your First Test Message

1. In the **API Setup** panel, ensure your test phone number is selected
2. Select a recipient phone number from your test list
3. Click **Send Message**
4. Select the pre-approved `hello_world` template
5. Send the test message

## Step 7: Test the API Using cURL

Use the following cURL command to send a test message via API:

Replace:
- `PHONE_NUMBER_ID` with your phone number ID
- `ACCESS_TOKEN` with your temporary access token
- `RECIPIENT_PHONE_NUMBER` with the recipient's phone number (including country code)

## Step 8: Set Up Webhooks for Receiving Messages

1. Go to **WhatsApp** > **Configuration** > **Webhooks**
2. Click **Edit**
3. Enter your webhook URL (where you'll receive incoming messages)
4. Set a verify token (a string you create to verify webhook requests)
5. Select the webhook fields you want to subscribe to
6. Click **Verify and Save**

## Moving to Production

Once you've successfully tested the API, you'll need to:

1. Verify your business with Meta
2. Request approval for your WhatsApp display name
3. Create and get approval for message templates
4. Generate a permanent access token
5. Complete any other requirements specified by Meta

## Next Steps

Now that you've set up your WhatsApp Business API, you can:

- [Learn about message templates](../how-to-guides/create-templates.md)
- [Implement webhooks for receiving messages](../how-to-guides/implement-webhooks.md)
- [Explore the API endpoints reference](../reference/api-endpoints.md)
- [Understand conversation-based pricing](../explanation/pricing-model.md)

## Common Setup Issues

- **Access Token Expired**: The temporary access token lasts only 24 hours. Generate a new one or create a permanent token.
- **Webhook Verification Fails**: Ensure your server is correctly responding to the verification challenge.
- **Message Sending Fails**: Verify that your recipient number is in the correct format including country code.
- **Rate Limit Exceeded**: Be aware of WhatsApp's rate limits during testing.
- **Template Message Rejected**: Templates must comply with WhatsApp's policy guidelines.
