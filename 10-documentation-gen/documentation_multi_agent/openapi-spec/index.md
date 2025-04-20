# Meta Cloud API for WhatsApp

Welcome to the interactive documentation for the Meta Cloud API for WhatsApp. This documentation is designed to help you understand and integrate with the WhatsApp Business API using Meta's Cloud-hosted solution.

## Overview

The Meta Cloud API for WhatsApp allows businesses to interact with their customers through WhatsApp messaging. With this API, you can:

- Send text, media, and interactive messages
- Receive and process incoming messages
- Track message delivery status
- Manage templates and business profile information
- Handle customer interactions at scale

## How to Use This Documentation

This interactive documentation is built using the OpenAPI specification and follows the Diataxis documentation model. Here's how to make the most of it:

### Navigation

The documentation is organized into logical categories:

- **Messages**: Endpoints for sending various types of messages
- **Media**: Endpoints for uploading and managing media files
- **Templates**: Endpoints for creating and managing message templates 
- **Business Profile**: Endpoints for managing your business profile
- **Webhooks**: Information about webhook events and management

Use the sidebar navigation to browse between different endpoint categories.

### Interactive Features

Each endpoint documentation includes:

1. **Try It Out**: Test API calls directly from the browser
2. **Code Samples**: Ready-to-use code snippets in multiple languages
3. **Request Builder**: Interactive forms to build valid API requests
4. **Response Examples**: Sample responses for successful calls and errors

To use the "Try It Out" feature:

1. Click the "Try It Out" button on any endpoint
2. Fill in the required parameters
3. Enter your access token in the authorization field
4. Click "Execute" to make a live API call
5. View the response directly in the documentation

### Code Generation

You can generate client code for any endpoint:

1. Configure an endpoint with your parameters
2. Click the "Code Generation" button
3. Select your preferred programming language
4. Copy the generated code to use in your application

## Authentication

All WhatsApp Cloud API requests require authentication using an access token:

### Access Token Types

1. **Temporary Access Token**: Short-lived token for testing
2. **System User Access Token**: Long-lived token for production use (recommended)

### Obtaining Access Tokens

To obtain a temporary access token:

1. Go to your Meta App Dashboard
2. Navigate to your app
3. Go to "Settings" > "Basic"
4. Use the App ID and App Secret to generate a token

For production, set up a System User:

1. In Business Manager, go to "Business Settings" > "Users" > "System Users"
2. Create a new System User with the appropriate role
3. Assign WhatsApp Business access to the System User
4. Generate a token with `whatsapp_business_messaging` permission
5. Set the token to never expire

### Using Access Tokens

Include your access token in the Authorization header of all requests:

## Rate Limits

The WhatsApp Cloud API has rate limits to ensure fair usage:

- Default: 200 calls per hour, per app, per WhatsApp Business Account
- Business-verified accounts can apply for higher limits
- Different endpoints may have specific limits
- Error code 429 indicates you've hit a rate limit

Implement exponential backoff and queuing strategies to handle rate limits effectively.

## Error Handling

The API uses standard HTTP status codes and returns JSON error objects:

Common error codes:

| HTTP Status | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid token |
| 403 | Forbidden - Insufficient permissions |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## API Versioning

This documentation covers Meta Graph API v17.0. Meta regularly updates their API, so check the [Meta Developers Changelog](https://developers.facebook.com/docs/graph-api/changelog/) for updates.

## Main Endpoint Categories

### [Messages](/openapi-spec/messages.html)
Send text, template, media, and interactive messages to WhatsApp users.

### [Media](/openapi-spec/media.html)
Upload, download, and manage media files for WhatsApp messages.

### [Templates](/openapi-spec/templates.html)
Create, update, and manage message templates for outbound conversations.

### [Business Profile](/openapi-spec/business-profile.html)
Manage your WhatsApp Business Profile information.

### [Phone Numbers](/openapi-spec/phone-numbers.html)
Manage WhatsApp Business API phone numbers and retrieve information.

## Common Workflows

We've documented common workflow patterns to help you implement common use cases:

- [Customer Onboarding](/openapi-spec/workflows/customer-onboarding.html)
- [Customer Support](/openapi-spec/workflows/customer-support.html)
- [Order Updates](/openapi-spec/workflows/order-updates.html)
- [Two-Factor Authentication](/openapi-spec/workflows/two-factor-authentication.html)

Each workflow includes a sequence diagram, sample API calls, and best practices.

## Additional Resources

- [WhatsApp Business Platform Documentation](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers Forum](https://developers.facebook.com/community/)
- [Meta Business Help Center](https://www.facebook.com/business/help)

## Getting Support

If you encounter issues or have questions:

1. Check our [Common Issues Guide](/how-to-guides/common-issues.html)
2. Visit the [Meta for Developers Forum](https://developers.facebook.com/community/)
3. Contact [Meta Business Support](https://www.facebook.com/business/help)
