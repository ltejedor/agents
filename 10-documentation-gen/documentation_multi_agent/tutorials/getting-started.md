# Getting Started with WhatsApp Business API

This tutorial will guide you through setting up and making your first API call with the WhatsApp Business API. By the end, you'll be able to send a message using the API and understand the next steps for building your WhatsApp integration.

## Prerequisites

Before you begin, make sure you have:
- A Facebook Business Manager account
- A Meta Developer account
- A phone number to use with WhatsApp Business API

## Step 1: Setting Up a WhatsApp Business Account

### 1.1 Create a Business Manager Account

1. Go to [business.facebook.com](https://business.facebook.com) and click "Create Account"
2. Fill in your business details and follow the prompts to complete setup
3. Verify your business through the verification process

### 1.2 Create a WhatsApp Business Account (WABA)

1. In Business Manager, click on "All Tools" and then select "WhatsApp Accounts"
2. Click "Add" and follow the prompts to create a new WhatsApp Business Account
3. Accept the WhatsApp Business Terms of Service

> **Note**: Business verification is required to gain full access to the WhatsApp Business API. This process can take several days, so start early.

## Step 2: Obtaining API Access

### 2.1 Create an App in Meta Developer Portal

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click "My Apps" and then "Create App"
3. Select "Business" as the app type
4. Enter your app name and business details, then click "Create App"

### 2.2 Add WhatsApp to Your App

1. From your app dashboard, click "Add Products"
2. Find and click on "WhatsApp" to add it to your app
3. You'll be taken to the WhatsApp setup page

### 2.3 Connect Your WhatsApp Business Account

1. On the WhatsApp setup page, click "Connect WhatsApp Business Account"
2. Select the WhatsApp Business Account you created earlier
3. Click "Continue" to establish the connection

### 2.4 Set Up a Test Phone Number

1. On the WhatsApp overview page in your app, navigate to "Getting Started"
2. Click "Add phone number" to register a test phone number
3. Enter the phone number and verify it via the one-time password

> **Note**: For initial development, you'll be using a test phone number with limited functionality. For production, you'll need to request access to additional WhatsApp phone numbers.

## Step 3: Making Your First API Call

### 3.1 Generate an Access Token

1. From your app dashboard, go to "Settings" > "Basic"
2. Scroll down to find the "App ID" and "App Secret"
3. Generate a temporary access token for testing:

4. Save the returned access token for your API calls

> **Important**: For production use, you should set up a System User and generate permanent access tokens. Temporary tokens should only be used for testing.

### 3.2 Send Your First Message

Now you're ready to send a message using the API. For this example, we'll send a simple template message:

Replace the following:
- `PHONE_NUMBER_ID`: Your WhatsApp phone number ID (from the API settings page)
- `YOUR_ACCESS_TOKEN`: The access token generated in the previous step
- `RECIPIENT_PHONE_NUMBER`: The phone number you want to send a message to, in international format (e.g., "+1XXXXXXXXXX")

> **Note**: Before sending templates, you need to create and get approval for them. The "hello_world" template is often pre-approved for testing purposes.

## Step 4: Understanding the Response

If your request is successful, you'll receive a response like this:

The important elements of this response are:

- `wa_id`: The WhatsApp ID of the recipient
- `MESSAGE_ID`: A unique identifier for the sent message

You can use the `MESSAGE_ID` to track the status of your message through webhooks.

## Step 5: Setting Up Webhooks for Notifications

To receive notifications about message status and incoming messages, you need to set up webhooks:

1. From your app dashboard, go to "WhatsApp" > "Configuration"
2. Under "Webhooks", click "Edit"
3. Enter your webhook URL and a verification token
4. Select the subscription fields you want to receive:
   - `messages`: To receive incoming messages
   - `message_status`: To receive delivery and read receipts

For webhook verification, your server should respond to a GET request with the `hub.challenge` parameter.

Here's a simple example using Node.js:

## Next Steps

Now that you've set up the WhatsApp Business API and sent your first message, here are some next steps:

1. **Create Message Templates**: Design and submit message templates for approval to enable outbound messaging to users
2. **Implement Conversation Handling**: Set up logic to handle user responses and maintain conversation context
3. **Explore Interactive Messages**: Try using buttons, lists, and other interactive message types
4. **Integrate with Your Systems**: Connect the WhatsApp API to your CRM, support platform, or other business systems
5. **Monitor Performance**: Implement analytics to track message delivery rates, response times, and user engagement

## Additional Resources

- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)
- [Message Templates Guidelines](https://developers.facebook.com/docs/whatsapp/message-templates)
- [Interactive Messages Reference](https://developers.facebook.com/docs/whatsapp/guides/interactive-messages)
- [Webhooks Reference](https://developers.facebook.com/docs/whatsapp/webhooks)
- [Rate Limiting Information](https://developers.facebook.com/docs/whatsapp/api/rate-limits)

