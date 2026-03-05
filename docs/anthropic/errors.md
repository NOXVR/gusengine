# Source: https://docs.anthropic.com/en/api/errors
# Downloaded: 2026-02-16

---

- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- Errors - Claude API Docs
- 
- 
- 
- 
- 
- Loading...

English
Log in

Search...⌘KUsing the APIAPI overviewBeta headersErrorsClient SDKs
Messages

Create a Message

Count tokens in a MessageBatches
Models

List Models

Get a ModelBeta
Models
Messages
Files
Skills
AdminOrganizations
Invites
Users
Workspaces
API Keys
Usage Report
Cost Report
Completions

Create a Text CompletionSupport & configurationRate limitsService tiersVersionsIP addressesSupported regionsOpenAI SDK compatibility

Console
Log in
Using the API
ErrorsLoading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...

### Solutions

- AI agents
- Code modernization
- Coding
- Customer support
- Education
- Financial services
- Government
- Life sciences
### Partners

- Amazon Bedrock
- Google Cloud's Vertex AI
### Learn

- Blog
- Catalog
- Courses
- Use cases
- Connectors
- Customer stories
- Engineering at Anthropic
- Events
- Powered by Claude
- Service partners
- Startups program
### Company

- Anthropic
- Careers
- Economic Futures
- Research
- News
- Responsible Scaling Policy
- Security and compliance
- Transparency
### Learn

- Blog
- Catalog
- Courses
- Use cases
- Connectors
- Customer stories
- Engineering at Anthropic
- Events
- Powered by Claude
- Service partners
- Startups program
### Help and security

- Availability
- Status
- Support
- Discord
### Terms and policies

- Privacy policy
- Responsible disclosure policy
- Terms of service: Commercial
- Terms of service: Consumer
- Usage policyUsing the API
# Errors

Copy page

Copy page

HTTP errors

Our API follows a predictable HTTP error code format:

- 

400 - `invalid_request_error`: There was an issue with the format or content of your request. We may also use this error type for other 4XX status codes not listed below.

- 

401 - `authentication_error`: There's an issue with your API key.

- 

403 - `permission_error`: Your API key does not have permission to use the specified resource.

- 

404 - `not_found_error`: The requested resource was not found.

- 

413 - `request_too_large`: Request exceeds the maximum allowed number of bytes. The maximum request size is 32 MB for standard API endpoints.

- 

429 - `rate_limit_error`: Your account has hit a rate limit.

- 

500 - `api_error`: An unexpected error has occurred internal to Anthropic's systems.

- 

529 - `overloaded_error`: The API is temporarily overloaded.

529 errors can occur when APIs experience high traffic across all users.

In rare cases, if your organization has a sharp increase in usage, you might see 429 errors due to acceleration limits on the API. To avoid hitting acceleration limits, ramp up your traffic gradually and maintain consistent usage patterns.

When receiving a streaming response via SSE, it's possible that an error can occur after returning a 200 response, in which case error handling wouldn't follow these standard mechanisms.

Request size limits

The API enforces request size limits to ensure optimal performance:

Endpoint TypeMaximum Request SizeMessages API32 MBToken Counting API32 MBBatch API256 MBFiles API500 MB

If you exceed these limits, you'll receive a 413 `request_too_large` error. The error is returned from Cloudflare before the request reaches our API servers.

Error shapes

Errors are always returned as JSON, with a top-level `error` object that always includes a `type` and `message` value. The response also includes a `request_id` field for easier tracking and debugging. For example:

JSON

{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "The requested resource could not be found."
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}

In accordance with our versioning policy, we may expand the values within these objects, and it is possible that the `type` values will grow over time.

Request id

Every API response includes a unique `request-id` header. This header contains a value such as `req_018EeWyXxfu5pfWkrYcMdjWG`. When contacting support about a specific request, please include this ID to help us quickly resolve your issue.

Our official SDKs provide this value as a property on top-level response objects, containing the value of the `request-id` header:

Python

import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(f"Request ID: {message._request_id}")

Long requests

We highly encourage using the streaming Messages API or Message Batches API for long running requests, especially those over 10 minutes.

We do not recommend setting a large `max_tokens` values without using our streaming Messages API
or Message Batches API:

- Some networks may drop idle connections after a variable period of time, which
can cause the request to fail or timeout without receiving a response from Anthropic.

- Networks differ in reliability; our Message Batches API can help you
manage the risk of network issues by allowing you to poll for results rather than requiring an uninterrupted network connection.

If you are building a direct API integration, you should be aware that setting a TCP socket keep-alive can reduce the impact of idle connection timeouts on some networks.

Our SDKs will validate that your non-streaming Messages API requests are not expected to exceed a 10 minute timeout and
also will set a socket option for TCP keep-alive.

If you don't need to process events incrementally, use `.stream()` with `.get_final_message()` (Python) or `.finalMessage()` (TypeScript) to get the complete `Message` object without writing event-handling code:

Python

with client.messages.stream(
    max_tokens=128000,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
    model="claude-opus-4-6",
) as stream:
    message = stream.get_final_message()

See Streaming Messages for more details.

Common validation errors

Prefill not supported

Claude Opus 4.6 does not support prefilling assistant messages. Sending a request with a prefilled last assistant message to this model returns a 400 `invalid_request_error`:

{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "Prefilling assistant messages is not supported for this model."
  }
}

Use structured outputs, system prompt instructions, or `output_config.format` instead.

Was this page helpful?
