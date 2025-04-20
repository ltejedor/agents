# Troubleshooting Common WhatsApp Business API Issues

This guide covers common issues developers encounter when working with the WhatsApp Business API and their solutions.

## Authentication Issues

### Expired Access Tokens

**Problem**: API calls fail with "Invalid OAuth access token" errors.

**Solution**:
- Temporary access tokens expire after 24 hours
- Generate a new temporary token from the Meta Developer Dashboard
- For production, create a System User in Business Manager and generate a permanent token
- Use token rotation strategies for long-term applications

### Incorrect Permissions

**Problem**: API calls fail with permission-related errors.

**Solution**:
- Ensure your app has the necessary WhatsApp permissions
- Check that your System User has the proper role and permissions
- Review the required permissions for each endpoint in the API reference

## Messaging Issues

### Template Messages Not Delivering

**Problem**: Template messages fail to send or remain in "pending" status.

**Solution**:
- Verify that your template has been approved
- Check that you're using the exact template name, parameters, and language code
- Ensure your template parameters match the expected format
- Verify the recipient's phone number format (include country code, no spaces or special characters)

### Message Rate Limiting

**Problem**: API returns rate limit errors.

**Solution**:
- Implement exponential backoff for retries
- Track your message volume and stay within your tier limits
- Spread out message sending during high-volume campaigns
- Apply for increased limits if needed for your business case

### Media Messages Failing

**Problem**: Media messages (images, documents, etc.) fail to send.

**Solution**:
- Ensure media files meet WhatsApp's requirements (size, format)
- Verify the media URL is publicly accessible
- Check that your media provider allows content-type header requests
- Use WhatsApp's media hosting API for reliable delivery

## Webhook Issues

### Webhook Verification Failing

**Problem**: Cannot set up webhooks due to verification failures.

**Solution**:
- Ensure your server correctly responds to the hub.challenge verification
- Verify your callback URL is publicly accessible (not localhost)
- Check that your server responds within the timeout period
- Implement proper HTTP response codes

### Missing Webhook Events

**Problem**: Not receiving expected webhook events for messages.

**Solution**:
- Verify you've subscribed to the correct webhook fields
- Check your server logs for incoming requests that might be failing
- Ensure your webhook endpoint responds with 200 OK quickly
- Test webhook delivery using the Meta testing tools

### Duplicate Webhook Events

**Problem**: Receiving the same webhook events multiple times.

**Solution**:
- Implement idempotency by tracking message IDs
- Add deduplication logic in your webhook handler
- Respond promptly with 200 OK to all webhook events

## Business Verification Issues

### Business Verification Stuck

**Problem**: Business verification process is taking too long or stuck.

**Solution**:
- Ensure all business details are accurate and match official records
- Provide clear, high-quality documents when requested
- Follow up through Business Manager support channels
- Consider getting a Meta Business Partner to assist

### Display Name Rejection

**Problem**: WhatsApp display name gets rejected.

**Solution**:
- Ensure your display name follows WhatsApp policies
- Avoid generic terms, categories, or location-only names
- Match your display name to your brand or business name
- Resubmit with a more specific, brand-oriented name

## API Response Issues

### Unexpected Error Codes

**Problem**: Receiving unexpected or undocumented error codes.

**Solution**:
- Check the [error codes reference](../reference/error-codes.md) for explanations
- Implement comprehensive error handling for both documented and undocumented errors
- Log full error responses for troubleshooting
- Use status.fb.com to check for WhatsApp platform issues

### Inconsistent API Responses

**Problem**: API behavior seems inconsistent or unpredictable.

**Solution**:
- Verify you're using the correct API version in all requests
- Check for recent API changes in the changelogs
- Ensure consistent headers and authentication across requests
- Test with the Graph API Explorer to isolate issues

## Performance Issues

### Slow API Response Times

**Problem**: API requests take longer than expected.

**Solution**:
- Implement connection pooling for HTTP clients
- Consider geographic proximity to Meta's data centers
- Use asynchronous programming patterns for high-volume applications
- Monitor and optimize your network connectivity

### High Failure Rates

**Problem**: High percentage of API calls are failing.

**Solution**:
- Implement circuit breakers to prevent cascading failures
- Set up comprehensive monitoring and alerting
- Use retry strategies with exponential backoff
- Consider a queue-based architecture for critical messages

## Testing and Development Issues

### Testing Limitations

**Problem**: Limited ability to test all features in development.

**Solution**:
- Use test phone numbers provided in the Developer Console
- Create a separate test app for development
- Implement a mock server to simulate WhatsApp API responses
- Set up staging environments with separate WhatsApp Business Accounts

### Quality Phone Number (QPN) Issues

**Problem**: Issues with the Quality Phone Number (QPN) during testing.

**Solution**:
- Ensure you're using the number correctly for testing
- Be aware of the limitations of test numbers
- Keep track of the 24-hour customer service window limitations
- Use template messages when outside the customer service window

## Recommended Debugging Tools

- **Meta Graph API Explorer**: Test API calls directly
- **Webhook Testing Tools**: Validate webhook functionality
- **Postman Collections**: Use the official WhatsApp Postman collection
- **ngrok**: Create secure tunnels for local webhook testing
- **Log Analysis**: Maintain detailed logs of all API interactions

If you encounter an issue not covered here, check the [official Meta Developer documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/support/) or reach out to support.
