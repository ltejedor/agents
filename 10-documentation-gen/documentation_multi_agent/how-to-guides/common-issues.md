# Common Issues with WhatsApp Business API

This guide addresses common issues that developers encounter when working with the WhatsApp Business API and provides solutions to help you troubleshoot and resolve them efficiently.

## Business Verification Problems

### Issue: Business Verification Rejected

**Symptoms:**
- Your business verification request is rejected in Meta Business Manager
- You receive an email stating that your business couldn't be verified
- Limited functionality in your WhatsApp Business Account

**Solutions:**

1. **Check Documentation Accuracy**
   - Ensure all submitted business information matches your official documents exactly
   - Verify that images of documents are clear, complete, and not expired
   - Double-check that your business name on documents matches your business profile

2. **Business Category Issues**
   - Some business categories have additional verification requirements
   - If you selected the wrong category, update it to match your actual business type
   - Consider if your business type requires special approval (e.g., financial services, healthcare)

3. **Appeal the Rejection**
   - In Meta Business Manager, navigate to Security Center > Verification
   - Click "Appeal" next to your rejected verification request
   - Provide additional documentation or clarification as requested
   - Be specific about your intended use of the WhatsApp API

4. **Consider Using a BSP**
   - Business Solution Providers (BSPs) can help navigate the verification process
   - BSPs often have existing relationships with Meta and experience with verification requirements
   - A BSP can advise on required documentation for your specific business type

### Issue: Verification Taking Too Long

**Symptoms:**
- Your verification status has been "In Review" for more than 5 business days
- Development is blocked waiting for verification approval

**Solutions:**

1. **Check Status in Business Manager**
   - Regularly check the verification status in Meta Business Manager
   - Look for any requests for additional information

2. **Prepare for Production While Waiting**
   - Continue development using the test phone number
   - Create and submit message templates for approval
   - Build your webhook infrastructure

3. **Escalate Through Support Channels**
   - If verification exceeds 10 business days, contact Meta Business Support
   - Provide your Business ID and verification submission date

## Message Template Rejections

### Issue: Template Rejected for Policy Violation

**Symptoms:**
- Template submission returns a rejection notice
- Error stating the template violates WhatsApp's Business Policy
- Unclear reason for rejection in the notification

**Solutions:**

1. **Common Rejection Reasons and Fixes:**

   | Rejection Reason | How to Fix |
   |------------------|------------|
   | Prohibited content | Remove references to alcohol, gambling, adult content, weapons, etc. |
   | Personal information requests | Remove requests for sensitive data like account numbers or passwords |
   | Low-quality content | Make templates clear, specific, and professional |
   | Illegal goods/services | Ensure your business and offerings comply with local laws |
   | Missing variables | If using variable content, ensure variables exist and are used correctly |

2. **Template Best Practices:**
   - Keep templates clear, concise, and specific
   - Avoid generic marketing language or sales pitches
   - Match template language to your target audience's location
   - Include a clear business purpose for the message
   - Properly format variables with correct syntax

3. **Testing and Resubmission:**
   - Review your template against WhatsApp's Business Policy
   - Make suggested changes based on the rejection reason
   - Test revised templates with colleagues for clarity
   - Resubmit with a slightly different name (e.g., add a version number)

### Issue: Template Works in Testing but Not in Production

**Symptoms:**
- Template messages work with test phone numbers
- The same templates fail when used with production phone numbers
- Messages show as "sent" but never deliver

**Solutions:**

1. **Check Template Status:**
   - Verify the template is approved for the specific phone number you're using
   - Template approvals are per-number, not account-wide

2. **Parameter Validation:**
   - Ensure all required parameters are provided
   - Check that parameter values match the expected format (e.g., date formats)
   - Verify that text parameters don't exceed length limits

3. **Test with Multiple Recipients:**
   - Try sending to different test numbers
   - Check if issues are specific to certain recipients

## Webhook Configuration Issues

### Issue: Webhook Verification Fails

**Symptoms:**
- Webhook registration fails in the Meta Developer Portal
- "Verification failed" error when setting up webhooks
- Challenge response errors in logs

**Solutions:**

1. **Verify Server Accessibility:**
   - Ensure your webhook endpoint is publicly accessible
   - Confirm your server responds to HTTP requests
   - Test with a tool like Postman or cURL to verify the endpoint works

2. **Check Challenge Response:**
   - Your server must return the `hub.challenge` value exactly as received
   - No additional characters or formatting should be added
   - Verify the response content type is text/plain

3. **Example Node.js Fix:**

### Issue: Not Receiving Webhook Events

**Symptoms:**
- Webhook verification succeeded but no events are received
- Missing message statuses or incoming messages
- One-way communication with WhatsApp API

**Solutions:**

1. **Check Subscription Fields:**
   - Verify you've subscribed to the correct fields in the Developer Portal
   - Common fields: `messages`, `message_status`
   - If using a test number, ensure test webhooks are enabled

2. **Inspect Server Logs:**
   - Check for incoming requests that might be failing
   - Look for HTTP errors in your webhook handling code
   - Verify your server responds with 200 OK to all webhook POSTs

3. **Implement Webhook Logging:**

## Rate Limiting Concerns

### Issue: Hitting Rate Limits

**Symptoms:**
- API responses with HTTP 429 "Too Many Requests"
- Error messages mentioning rate limits
- Messages failing to send during high-volume periods

**Solutions:**

1. **Understand Rate Limit Types:**
   - **User Rate Limits**: Messages per user
   - **Phone Number Rate Limits**: Messages per phone number
   - **App Rate Limits**: Overall app requests
   - **Template Rate Limits**: Messages per template

2. **Implement Rate Limiting Strategies:**
   - Add exponential backoff for retries
   - Queue messages to control send rate
   - Implement a token bucket algorithm on your side

3. **Example Backoff Implementation (Node.js):**

### Issue: Production Scaling Concerns

**Symptoms:**
- As message volume increases, delivery reliability decreases
- Intermittent rate limit errors with high message volumes
- Delays in message delivery during peak times

**Solutions:**

1. **Request Higher Rate Limits:**
   - Business-verified accounts can request higher limits
   - Document your use case and expected volume
   - Request through Meta Business Help Center

2. **Optimize Message Batching:**
   - Space out non-urgent messages
   - Group recipients by priority tiers
   - Implement "quiet hours" for non-critical messages

3. **Monitor and Adjust:**
   - Track rate limit errors as a key metric
   - Set up alerts for rate limit thresholds
   - Adjust send rates based on time of day patterns

## Authentication Problems

### Issue: Invalid or Expired Access Tokens

**Symptoms:**
- API calls return 401 Unauthorized errors
- Error messages mention invalid or expired tokens
- Previously working integrations suddenly stop working

**Solutions:**

1. **Check Token Validity:**
   - Test your token using the Graph API Explorer
   - Verify the token hasn't expired
   - Confirm the token has the correct permissions

2. **System User Setup (Recommended for Production):**
   - Create a System User in Business Manager
   - Assign it to your WhatsApp Business Account
   - Generate a long-lived access token

3. **Set Up System User (Step-by-Step):**
   
   a. In Business Manager, go to "Business Settings" > "Users" > "System Users"
   
   b. Click "Add" and create a new System User with the appropriate role
   
   c. Navigate to "Add Assets" to assign WhatsApp Business Account access
   
   d. Generate a token with the following permissions:
      - `whatsapp_business_management`
      - `whatsapp_business_messaging`
   
   e. Set the token to never expire for production use
   
   f. Securely store the token in your environment variables or secrets manager

### Issue: Permission Problems

**Symptoms:**
- API calls return 403 Forbidden errors
- Error messages mention missing permissions
- Certain API endpoints work while others fail

**Solutions:**

1. **Verify App Permissions:**
   - Check the permissions assigned to your app
   - Ensure WhatsApp permissions are enabled
   - Add missing permissions in App Dashboard

2. **Check Business Manager Roles:**
   - System Users need specific roles to access WhatsApp
   - Admin or Developer roles are typically required
   - Verify asset assignment in Business Manager

3. **Permission Debugging:**
   - Use the Graph API Explorer to test different permission combinations
   - Check error messages for specific missing permissions
   - Try a token with elevated permissions to isolate the issue

## Monitoring and Logging

Regardless of the specific issues you're facing, implementing proper monitoring and logging is crucial for troubleshooting WhatsApp API integrations:

1. **Log All API Interactions:**
   - Log request and response pairs (excluding sensitive data)
   - Include timestamps for rate limit analysis
   - Track message status updates through webhooks

2. **Set Up Alerting:**
   - Alert on high error rates
   - Monitor rate limit proximity
   - Track delivery success rates

3. **Implement Health Checks:**
   - Regularly test your webhook endpoint
   - Verify token validity before it expires
   - Monitor queue depths if using message queuing

## Getting Support

If you're still encountering issues after trying the solutions above:

1. **Meta Developer Support:**
   - Use the Meta for Developers Support page
   - Open support tickets through Business Manager
   - Provide detailed information including your App ID and error logs

2. **Community Resources:**
   - Check the Meta for Developers Forum
   - Search StackOverflow for similar issues
   - Join WhatsApp API community groups

3. **Business Solution Provider Support:**
   - If using a BSP, leverage their technical support
   - BSPs often have direct support channels with Meta
   - BSPs can help with business verification and template approvals
