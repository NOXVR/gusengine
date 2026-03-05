# Source: https://docs.anthropic.com/en/api/messages
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
- Messages - Claude API Reference
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
API Reference
Messages

Copy page

# Messages
Create a Message

POST/v1/messagesCount tokens in a Message

POST/v1/messages/count_tokensModelsExpand 

Collapse 

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

CacheControlEphemeral = object { type, ttl } 
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

CacheCreation = object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsConfigParam = object { enabled } 
enabled: optional boolean

CitationsDelta = object { citation, type } 

citation: CitationCharLocation { cited_text, document_index, document_title, 4 more }  or CitationPageLocation { cited_text, document_index, document_title, 4 more }  or CitationContentBlockLocation { cited_text, document_index, document_title, 4 more }  or 2 more
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
type: "citations_delta"

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

ContentBlock = TextBlock { citations, text, type }  or ThinkingBlock { signature, thinking, type }  or RedactedThinkingBlock { data, type }  or 3 more
Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

ContentBlockParam = TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or DocumentBlockParam { source, type, cache_control, 3 more }  or 7 more

Regular text content.
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

ThinkingBlockParam = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlockParam = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: string
type: "tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more } 
tool_use_id: string
type: "tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

content: optional string or array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:UnionMember0 = string

UnionMember1 = array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string
is_error: optional boolean

ServerToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control } 

content: WebSearchToolResultBlockParamContent
Accepts one of the following:

WebSearchToolResultBlockItem = array of WebSearchResultBlockParam { encrypted_content, title, type, 2 more } 
encrypted_content: string
title: string
type: "web_search_result"
url: string
page_age: optional string

WebSearchToolRequestError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"
tool_use_id: string
type: "web_search_tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

ContentBlockSourceContent = TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control } 
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

InputJSONDelta = object { partial_json, type } 
partial_json: string
type: "input_json_delta"

JSONOutputFormat = object { schema, type } 
schema: map[unknown]

The JSON schema of the format
type: "json_schema"

Message = object { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"

MessageCountTokensTool = Tool { input_schema, name, cache_control, 4 more }  or ToolBash20250124 { name, type, cache_control, strict }  or ToolTextEditor20250124 { name, type, cache_control, strict }  or 3 more
Accepts one of the following:

Tool = object { input_schema, name, cache_control, 4 more } 

input_schema: object { type, properties, required } 

JSON schema for this tool's input.

This defines the shape of the `input` that your tool accepts and that the model will produce.
type: "object"
properties: optional map[unknown]
required: optional array of string

name: string

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
maxLength128minLength1

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

description: optional string

Description of what this tool does.

Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.
eager_input_streaming: optional boolean

Enable eager input streaming for this tool. When true, tool input parameters will be streamed incrementally as they are generated, and types will be inferred on-the-fly rather than buffering the full JSON output. When false, streaming is disabled for this tool even if the fine-grained-tool-streaming beta is active. When null (default), uses the default behavior based on beta headers.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs
type: optional "custom"

ToolBash20250124 = object { name, type, cache_control, strict } 

name: "bash"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "bash_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250124 = object { name, type, cache_control, strict } 

name: "str_replace_editor"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250429 = object { name, type, cache_control, strict } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250429"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250728 = object { name, type, cache_control, 2 more } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250728"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_characters: optional number

Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

WebSearchTool20250305 = object { name, type, allowed_domains, 5 more } 

name: "web_search"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "web_search_20250305"
allowed_domains: optional array of string

If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.
blocked_domains: optional array of string

If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_uses: optional number

Maximum number of times the tool can be used in the API request.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

user_location: optional object { type, city, country, 2 more } 

Parameters for the user's location. Used to provide more relevant search results.
type: "approximate"
city: optional string

The city of the user.
country: optional string

The two letter ISO country code of the user.
region: optional string

The region of the user.
timezone: optional string

The IANA timezone of the user.

MessageDeltaUsage = object { cache_creation_input_tokens, cache_read_input_tokens, input_tokens, 2 more } 
cache_creation_input_tokens: number

The cumulative number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The cumulative number of input tokens read from the cache.
input_tokens: number

The cumulative number of input tokens which were used.
output_tokens: number

The cumulative number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

MessageParam = object { content, role } 

content: string or array of ContentBlockParam
Accepts one of the following:UnionMember0 = string

UnionMember1 = array of ContentBlockParam
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

ThinkingBlockParam = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlockParam = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: string
type: "tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more } 
tool_use_id: string
type: "tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

content: optional string or array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:UnionMember0 = string

UnionMember1 = array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string
is_error: optional boolean

ServerToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control } 

content: WebSearchToolResultBlockParamContent
Accepts one of the following:

WebSearchToolResultBlockItem = array of WebSearchResultBlockParam { encrypted_content, title, type, 2 more } 
encrypted_content: string
title: string
type: "web_search_result"
url: string
page_age: optional string

WebSearchToolRequestError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"
tool_use_id: string
type: "web_search_tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

role: "user" or "assistant"
Accepts one of the following:"user"
"assistant"

MessageTokensCount = object { input_tokens } 
input_tokens: number

The total number of tokens across the provided list of messages, system prompt, and tools.

Metadata = object { user_id } 

user_id: optional string

An external identifier for the user who is associated with the request.

This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.
maxLength256

Model = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more or string

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

OutputConfig = object { effort, format } 

effort: optional "low" or "medium" or "high" or "max"

All possible effort levels.
Accepts one of the following:"low"
"medium"
"high"
"max"

format: optional JSONOutputFormat { schema, type } 

A schema to specify Claude's output format in responses. See structured outputs
schema: map[unknown]

The JSON schema of the format
type: "json_schema"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

RawContentBlockDelta = TextDelta { text, type }  or InputJSONDelta { partial_json, type }  or CitationsDelta { citation, type }  or 2 more
Accepts one of the following:

TextDelta = object { text, type } 
text: string
type: "text_delta"

InputJSONDelta = object { partial_json, type } 
partial_json: string
type: "input_json_delta"

CitationsDelta = object { citation, type } 

citation: CitationCharLocation { cited_text, document_index, document_title, 4 more }  or CitationPageLocation { cited_text, document_index, document_title, 4 more }  or CitationContentBlockLocation { cited_text, document_index, document_title, 4 more }  or 2 more
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
type: "citations_delta"

ThinkingDelta = object { thinking, type } 
thinking: string
type: "thinking_delta"

SignatureDelta = object { signature, type } 
signature: string
type: "signature_delta"

RawContentBlockDeltaEvent = object { delta, index, type } 

delta: RawContentBlockDelta
Accepts one of the following:

TextDelta = object { text, type } 
text: string
type: "text_delta"

InputJSONDelta = object { partial_json, type } 
partial_json: string
type: "input_json_delta"

CitationsDelta = object { citation, type } 

citation: CitationCharLocation { cited_text, document_index, document_title, 4 more }  or CitationPageLocation { cited_text, document_index, document_title, 4 more }  or CitationContentBlockLocation { cited_text, document_index, document_title, 4 more }  or 2 more
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
type: "citations_delta"

ThinkingDelta = object { thinking, type } 
thinking: string
type: "thinking_delta"

SignatureDelta = object { signature, type } 
signature: string
type: "signature_delta"
index: number
type: "content_block_delta"

RawContentBlockStartEvent = object { content_block, index, type } 

content_block: TextBlock { citations, text, type }  or ThinkingBlock { signature, thinking, type }  or RedactedThinkingBlock { data, type }  or 3 more
Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"
index: number
type: "content_block_start"

RawContentBlockStopEvent = object { index, type } 
index: number
type: "content_block_stop"

RawMessageDeltaEvent = object { delta, type, usage } 

delta: object { stop_reason, stop_sequence } 

stop_reason: StopReason
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"
stop_sequence: string
type: "message_delta"

usage: MessageDeltaUsage { cache_creation_input_tokens, cache_read_input_tokens, input_tokens, 2 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.
cache_creation_input_tokens: number

The cumulative number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The cumulative number of input tokens read from the cache.
input_tokens: number

The cumulative number of input tokens which were used.
output_tokens: number

The cumulative number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

RawMessageStartEvent = object { message, type } 

message: Message { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"
type: "message_start"

RawMessageStopEvent = object { type } 
type: "message_stop"

RawMessageStreamEvent = RawMessageStartEvent { message, type }  or RawMessageDeltaEvent { delta, type, usage }  or RawMessageStopEvent { type }  or 3 more
Accepts one of the following:

RawMessageStartEvent = object { message, type } 

message: Message { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"
type: "message_start"

RawMessageDeltaEvent = object { delta, type, usage } 

delta: object { stop_reason, stop_sequence } 

stop_reason: StopReason
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"
stop_sequence: string
type: "message_delta"

usage: MessageDeltaUsage { cache_creation_input_tokens, cache_read_input_tokens, input_tokens, 2 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.
cache_creation_input_tokens: number

The cumulative number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The cumulative number of input tokens read from the cache.
input_tokens: number

The cumulative number of input tokens which were used.
output_tokens: number

The cumulative number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

RawMessageStopEvent = object { type } 
type: "message_stop"

RawContentBlockStartEvent = object { content_block, index, type } 

content_block: TextBlock { citations, text, type }  or ThinkingBlock { signature, thinking, type }  or RedactedThinkingBlock { data, type }  or 3 more
Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"
index: number
type: "content_block_start"

RawContentBlockDeltaEvent = object { delta, index, type } 

delta: RawContentBlockDelta
Accepts one of the following:

TextDelta = object { text, type } 
text: string
type: "text_delta"

InputJSONDelta = object { partial_json, type } 
partial_json: string
type: "input_json_delta"

CitationsDelta = object { citation, type } 

citation: CitationCharLocation { cited_text, document_index, document_title, 4 more }  or CitationPageLocation { cited_text, document_index, document_title, 4 more }  or CitationContentBlockLocation { cited_text, document_index, document_title, 4 more }  or 2 more
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
type: "citations_delta"

ThinkingDelta = object { thinking, type } 
thinking: string
type: "thinking_delta"

SignatureDelta = object { signature, type } 
signature: string
type: "signature_delta"
index: number
type: "content_block_delta"

RawContentBlockStopEvent = object { index, type } 
index: number
type: "content_block_stop"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

RedactedThinkingBlockParam = object { data, type } 
data: string
type: "redacted_thinking"

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

ServerToolUsage = object { web_search_requests } 
web_search_requests: number

The number of web search tool requests.

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

ServerToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

SignatureDelta = object { signature, type } 
signature: string
type: "signature_delta"

StopReason = "end_turn" or "max_tokens" or "stop_sequence" or 3 more
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

TextCitation = CitationCharLocation { cited_text, document_index, document_title, 4 more }  or CitationPageLocation { cited_text, document_index, document_title, 4 more }  or CitationContentBlockLocation { cited_text, document_index, document_title, 4 more }  or 2 more
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

TextCitationParam = CitationCharLocationParam { cited_text, document_index, document_title, 3 more }  or CitationPageLocationParam { cited_text, document_index, document_title, 3 more }  or CitationContentBlockLocationParam { cited_text, document_index, document_title, 3 more }  or 2 more
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

TextDelta = object { text, type } 
text: string
type: "text_delta"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

ThinkingBlockParam = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

ThinkingConfigAdaptive = object { type } 
type: "adaptive"

ThinkingConfigDisabled = object { type } 
type: "disabled"

ThinkingConfigEnabled = object { budget_tokens, type } 

budget_tokens: number

Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

Must be ≥1024 and less than `max_tokens`.

See extended thinking for details.
minimum1024type: "enabled"

ThinkingConfigParam = ThinkingConfigEnabled { budget_tokens, type }  or ThinkingConfigDisabled { type }  or ThinkingConfigAdaptive { type } 

Configuration for enabling Claude's extended thinking.

When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

See extended thinking for details.
Accepts one of the following:

ThinkingConfigEnabled = object { budget_tokens, type } 

budget_tokens: number

Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

Must be ≥1024 and less than `max_tokens`.

See extended thinking for details.
minimum1024type: "enabled"

ThinkingConfigDisabled = object { type } 
type: "disabled"

ThinkingConfigAdaptive = object { type } 
type: "adaptive"

ThinkingDelta = object { thinking, type } 
thinking: string
type: "thinking_delta"

Tool = object { input_schema, name, cache_control, 4 more } 

input_schema: object { type, properties, required } 

JSON schema for this tool's input.

This defines the shape of the `input` that your tool accepts and that the model will produce.
type: "object"
properties: optional map[unknown]
required: optional array of string

name: string

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
maxLength128minLength1

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

description: optional string

Description of what this tool does.

Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.
eager_input_streaming: optional boolean

Enable eager input streaming for this tool. When true, tool input parameters will be streamed incrementally as they are generated, and types will be inferred on-the-fly rather than buffering the full JSON output. When false, streaming is disabled for this tool even if the fine-grained-tool-streaming beta is active. When null (default), uses the default behavior based on beta headers.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs
type: optional "custom"

ToolBash20250124 = object { name, type, cache_control, strict } 

name: "bash"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "bash_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolChoice = ToolChoiceAuto { type, disable_parallel_tool_use }  or ToolChoiceAny { type, disable_parallel_tool_use }  or ToolChoiceTool { name, type, disable_parallel_tool_use }  or ToolChoiceNone { type } 

How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.
Accepts one of the following:

ToolChoiceAuto = object { type, disable_parallel_tool_use } 

The model will automatically decide whether to use tools.
type: "auto"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output at most one tool use.

ToolChoiceAny = object { type, disable_parallel_tool_use } 

The model will use any available tools.
type: "any"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output exactly one tool use.

ToolChoiceTool = object { name, type, disable_parallel_tool_use } 

The model will use the specified tool with `tool_choice.name`.
name: string

The name of the tool to use.
type: "tool"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output exactly one tool use.

ToolChoiceNone = object { type } 

The model will not be allowed to use tools.
type: "none"

ToolChoiceAny = object { type, disable_parallel_tool_use } 

The model will use any available tools.
type: "any"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output exactly one tool use.

ToolChoiceAuto = object { type, disable_parallel_tool_use } 

The model will automatically decide whether to use tools.
type: "auto"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output at most one tool use.

ToolChoiceNone = object { type } 

The model will not be allowed to use tools.
type: "none"

ToolChoiceTool = object { name, type, disable_parallel_tool_use } 

The model will use the specified tool with `tool_choice.name`.
name: string

The name of the tool to use.
type: "tool"

disable_parallel_tool_use: optional boolean

Whether to disable parallel tool use.

Defaults to `false`. If set to `true`, the model will output exactly one tool use.

ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more } 
tool_use_id: string
type: "tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

content: optional string or array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:UnionMember0 = string

UnionMember1 = array of TextBlockParam { text, type, cache_control, citations }  or ImageBlockParam { source, type, cache_control }  or SearchResultBlockParam { content, source, title, 3 more }  or DocumentBlockParam { source, type, cache_control, 3 more } 
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

SearchResultBlockParam = object { content, source, title, 3 more } 

content: array of TextBlockParam { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
source: string
title: string
type: "search_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean

DocumentBlockParam = object { source, type, cache_control, 3 more } 

source: Base64PDFSource { data, media_type, type }  or PlainTextSource { data, media_type, type }  or ContentBlockSource { content, type }  or URLPDFSource { type, url } 
Accepts one of the following:

Base64PDFSource = object { data, media_type, type } 
data: string
media_type: "application/pdf"
type: "base64"

PlainTextSource = object { data, media_type, type } 
data: string
media_type: "text/plain"
type: "text"

ContentBlockSource = object { content, type } 

content: string or array of ContentBlockSourceContent
Accepts one of the following:UnionMember0 = string

ContentBlockSourceContent = array of ContentBlockSourceContent
Accepts one of the following:

TextBlockParam = object { text, type, cache_control, citations } 
text: string
type: "text"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional array of TextCitationParam
Accepts one of the following:

CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
start_char_index: number
type: "char_location"

CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
start_page_number: number
type: "page_location"

CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
start_block_index: number
type: "content_block_location"

CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"

ImageBlockParam = object { source, type, cache_control } 

source: Base64ImageSource { data, media_type, type }  or URLImageSource { type, url } 
Accepts one of the following:

Base64ImageSource = object { data, media_type, type } 
data: string

media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"
Accepts one of the following:"image/jpeg"
"image/png"
"image/gif"
"image/webp"
type: "base64"

URLImageSource = object { type, url } 
type: "url"
url: string
type: "image"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
type: "content"

URLPDFSource = object { type, url } 
type: "url"
url: string
type: "document"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

citations: optional CitationsConfigParam { enabled } 
enabled: optional boolean
context: optional string
title: optional string
is_error: optional boolean

ToolTextEditor20250124 = object { name, type, cache_control, strict } 

name: "str_replace_editor"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250429 = object { name, type, cache_control, strict } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250429"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250728 = object { name, type, cache_control, 2 more } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250728"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_characters: optional number

Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolUnion = Tool { input_schema, name, cache_control, 4 more }  or ToolBash20250124 { name, type, cache_control, strict }  or ToolTextEditor20250124 { name, type, cache_control, strict }  or 3 more
Accepts one of the following:

Tool = object { input_schema, name, cache_control, 4 more } 

input_schema: object { type, properties, required } 

JSON schema for this tool's input.

This defines the shape of the `input` that your tool accepts and that the model will produce.
type: "object"
properties: optional map[unknown]
required: optional array of string

name: string

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
maxLength128minLength1

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

description: optional string

Description of what this tool does.

Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.
eager_input_streaming: optional boolean

Enable eager input streaming for this tool. When true, tool input parameters will be streamed incrementally as they are generated, and types will be inferred on-the-fly rather than buffering the full JSON output. When false, streaming is disabled for this tool even if the fine-grained-tool-streaming beta is active. When null (default), uses the default behavior based on beta headers.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs
type: optional "custom"

ToolBash20250124 = object { name, type, cache_control, strict } 

name: "bash"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "bash_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250124 = object { name, type, cache_control, strict } 

name: "str_replace_editor"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250124"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250429 = object { name, type, cache_control, strict } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250429"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

ToolTextEditor20250728 = object { name, type, cache_control, 2 more } 

name: "str_replace_based_edit_tool"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "text_editor_20250728"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_characters: optional number

Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

WebSearchTool20250305 = object { name, type, allowed_domains, 5 more } 

name: "web_search"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "web_search_20250305"
allowed_domains: optional array of string

If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.
blocked_domains: optional array of string

If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_uses: optional number

Maximum number of times the tool can be used in the API request.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

user_location: optional object { type, city, country, 2 more } 

Parameters for the user's location. Used to provide more relevant search results.
type: "approximate"
city: optional string

The city of the user.
country: optional string

The two letter ISO country code of the user.
region: optional string

The region of the user.
timezone: optional string

The IANA timezone of the user.

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ToolUseBlockParam = object { id, input, name, 2 more } 
id: string
input: map[unknown]
name: string
type: "tool_use"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

URLImageSource = object { type, url } 
type: "url"
url: string

URLPDFSource = object { type, url } 
type: "url"
url: string

Usage = object { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"

WebSearchResultBlock = object { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string

WebSearchResultBlockParam = object { encrypted_content, title, type, 2 more } 
encrypted_content: string
title: string
type: "web_search_result"
url: string
page_age: optional string

WebSearchTool20250305 = object { name, type, allowed_domains, 5 more } 

name: "web_search"

Name of the tool.

This is how the tool will be called by the model and in `tool_use` blocks.
type: "web_search_20250305"
allowed_domains: optional array of string

If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.
blocked_domains: optional array of string

If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"
max_uses: optional number

Maximum number of times the tool can be used in the API request.
strict: optional boolean

When true, guarantees schema validation on tool names and inputs

user_location: optional object { type, city, country, 2 more } 

Parameters for the user's location. Used to provide more relevant search results.
type: "approximate"
city: optional string

The city of the user.
country: optional string

The two letter ISO country code of the user.
region: optional string

The region of the user.
timezone: optional string

The IANA timezone of the user.

WebSearchToolRequestError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

WebSearchToolResultBlockContent = WebSearchToolResultError { error_code, type }  or array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string

WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control } 

content: WebSearchToolResultBlockParamContent
Accepts one of the following:

WebSearchToolResultBlockItem = array of WebSearchResultBlockParam { encrypted_content, title, type, 2 more } 
encrypted_content: string
title: string
type: "web_search_result"
url: string
page_age: optional string

WebSearchToolRequestError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"
tool_use_id: string
type: "web_search_tool_result"

cache_control: optional CacheControlEphemeral { type, ttl } 

Create a cache control breakpoint at this content block.
type: "ephemeral"

ttl: optional "5m" or "1h"

The time-to-live for the cache control breakpoint.

This may be one the following values:

- `5m`: 5 minutes

- `1h`: 1 hour

Defaults to `5m`.
Accepts one of the following:"5m"
"1h"

WebSearchToolResultBlockParamContent = array of WebSearchResultBlockParam { encrypted_content, title, type, 2 more }  or WebSearchToolRequestError { error_code, type } 
Accepts one of the following:

WebSearchToolResultBlockItem = array of WebSearchResultBlockParam { encrypted_content, title, type, 2 more } 
encrypted_content: string
title: string
type: "web_search_result"
url: string
page_age: optional string

WebSearchToolRequestError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"
Messages
BatchesCreate a Message Batch

POST/v1/messages/batchesRetrieve a Message Batch

GET/v1/messages/batches/{message_batch_id}List Message Batches

GET/v1/messages/batchesCancel a Message Batch

POST/v1/messages/batches/{message_batch_id}/cancelDelete a Message Batch

DELETE/v1/messages/batches/{message_batch_id}Retrieve Message Batch results

GET/v1/messages/batches/{message_batch_id}/resultsModelsExpand 

Collapse 

DeletedMessageBatch = object { id, type } 
id: string

ID of the Message Batch.

type: "message_batch_deleted"

Deleted object type.

For Message Batches, this is always `"message_batch_deleted"`.

MessageBatch = object { id, archived_at, cancel_initiated_at, 7 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.
archived_at: string

RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.
cancel_initiated_at: string

RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.
created_at: string

RFC 3339 datetime string representing the time at which the Message Batch was created.

ended_at: string

RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.
formatdate-timeexpires_at: string

RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

processing_status: "in_progress" or "canceling" or "ended"

Processing status of the Message Batch.
Accepts one of the following:"in_progress"
"canceling"
"ended"

request_counts: MessageBatchRequestCounts { canceled, errored, expired, 2 more } 

Tallies requests within the Message Batch, categorized by their status.

Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

canceled: number

Number of requests in the Message Batch that have been canceled.

This is zero until processing of the entire Message Batch has ended.

errored: number

Number of requests in the Message Batch that encountered an error.

This is zero until processing of the entire Message Batch has ended.

expired: number

Number of requests in the Message Batch that have expired.

This is zero until processing of the entire Message Batch has ended.
processing: number

Number of requests in the Message Batch that are processing.

succeeded: number

Number of requests in the Message Batch that have completed successfully.

This is zero until processing of the entire Message Batch has ended.

results_url: string

URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

type: "message_batch"

Object type.

For Message Batches, this is always `"message_batch"`.

MessageBatchCanceledResult = object { type } 
type: "canceled"

MessageBatchErroredResult = object { error, type } 

error: ErrorResponse { error, request_id, type } 

error: ErrorObject
Accepts one of the following:

InvalidRequestError = object { message, type } 
message: string
type: "invalid_request_error"

AuthenticationError = object { message, type } 
message: string
type: "authentication_error"

BillingError = object { message, type } 
message: string
type: "billing_error"

PermissionError = object { message, type } 
message: string
type: "permission_error"

NotFoundError = object { message, type } 
message: string
type: "not_found_error"

RateLimitError = object { message, type } 
message: string
type: "rate_limit_error"

GatewayTimeoutError = object { message, type } 
message: string
type: "timeout_error"

APIErrorObject = object { message, type } 
message: string
type: "api_error"

OverloadedError = object { message, type } 
message: string
type: "overloaded_error"
request_id: string
type: "error"
type: "errored"

MessageBatchExpiredResult = object { type } 
type: "expired"

MessageBatchIndividualResponse = object { custom_id, result } 

This is a single line in the response `.jsonl` file and does not represent the response as a whole.

custom_id: string

Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

Must be unique for each request within the Message Batch.

result: MessageBatchResult

Processing result for this request.

Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.
Accepts one of the following:

MessageBatchSucceededResult = object { message, type } 

message: Message { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"
type: "succeeded"

MessageBatchErroredResult = object { error, type } 

error: ErrorResponse { error, request_id, type } 

error: ErrorObject
Accepts one of the following:

InvalidRequestError = object { message, type } 
message: string
type: "invalid_request_error"

AuthenticationError = object { message, type } 
message: string
type: "authentication_error"

BillingError = object { message, type } 
message: string
type: "billing_error"

PermissionError = object { message, type } 
message: string
type: "permission_error"

NotFoundError = object { message, type } 
message: string
type: "not_found_error"

RateLimitError = object { message, type } 
message: string
type: "rate_limit_error"

GatewayTimeoutError = object { message, type } 
message: string
type: "timeout_error"

APIErrorObject = object { message, type } 
message: string
type: "api_error"

OverloadedError = object { message, type } 
message: string
type: "overloaded_error"
request_id: string
type: "error"
type: "errored"

MessageBatchCanceledResult = object { type } 
type: "canceled"

MessageBatchExpiredResult = object { type } 
type: "expired"

MessageBatchRequestCounts = object { canceled, errored, expired, 2 more } 

canceled: number

Number of requests in the Message Batch that have been canceled.

This is zero until processing of the entire Message Batch has ended.

errored: number

Number of requests in the Message Batch that encountered an error.

This is zero until processing of the entire Message Batch has ended.

expired: number

Number of requests in the Message Batch that have expired.

This is zero until processing of the entire Message Batch has ended.
processing: number

Number of requests in the Message Batch that are processing.

succeeded: number

Number of requests in the Message Batch that have completed successfully.

This is zero until processing of the entire Message Batch has ended.

MessageBatchResult = MessageBatchSucceededResult { message, type }  or MessageBatchErroredResult { error, type }  or MessageBatchCanceledResult { type }  or MessageBatchExpiredResult { type } 

Processing result for this request.

Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.
Accepts one of the following:

MessageBatchSucceededResult = object { message, type } 

message: Message { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"
type: "succeeded"

MessageBatchErroredResult = object { error, type } 

error: ErrorResponse { error, request_id, type } 

error: ErrorObject
Accepts one of the following:

InvalidRequestError = object { message, type } 
message: string
type: "invalid_request_error"

AuthenticationError = object { message, type } 
message: string
type: "authentication_error"

BillingError = object { message, type } 
message: string
type: "billing_error"

PermissionError = object { message, type } 
message: string
type: "permission_error"

NotFoundError = object { message, type } 
message: string
type: "not_found_error"

RateLimitError = object { message, type } 
message: string
type: "rate_limit_error"

GatewayTimeoutError = object { message, type } 
message: string
type: "timeout_error"

APIErrorObject = object { message, type } 
message: string
type: "api_error"

OverloadedError = object { message, type } 
message: string
type: "overloaded_error"
request_id: string
type: "error"
type: "errored"

MessageBatchCanceledResult = object { type } 
type: "canceled"

MessageBatchExpiredResult = object { type } 
type: "expired"

MessageBatchSucceededResult = object { message, type } 

message: Message { id, content, model, 5 more } 

id: string

Unique object identifier.

The format and length of IDs may change over time.

content: array of ContentBlock

Content generated by the model.

This is an array of content blocks, each of which has a `type` that determines its shape.

Example:

[{"type": "text", "text": "Hi, I'm Claude."}]

If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

For example, if the input `messages` were:

[
  {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
  {"role": "assistant", "content": "The best answer is ("}
]

Then the response `content` might be:

[{"type": "text", "text": "B)"}]

Accepts one of the following:

TextBlock = object { citations, text, type } 

citations: array of TextCitation

Citations supporting the text block.

The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.
Accepts one of the following:

CitationCharLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_char_index: number
file_id: string
start_char_index: number
type: "char_location"

CitationPageLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_page_number: number
file_id: string
start_page_number: number
type: "page_location"

CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more } 
cited_text: string
document_index: number
document_title: string
end_block_index: number
file_id: string
start_block_index: number
type: "content_block_location"

CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more } 
cited_text: string
encrypted_index: string
title: string
type: "web_search_result_location"
url: string

CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more } 
cited_text: string
end_block_index: number
search_result_index: number
source: string
start_block_index: number
title: string
type: "search_result_location"
text: string
type: "text"

ThinkingBlock = object { signature, thinking, type } 
signature: string
thinking: string
type: "thinking"

RedactedThinkingBlock = object { data, type } 
data: string
type: "redacted_thinking"

ToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: string
type: "tool_use"

ServerToolUseBlock = object { id, input, name, type } 
id: string
input: map[unknown]
name: "web_search"
type: "server_tool_use"

WebSearchToolResultBlock = object { content, tool_use_id, type } 

content: WebSearchToolResultBlockContent
Accepts one of the following:

WebSearchToolResultError = object { error_code, type } 

error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 3 more
Accepts one of the following:"invalid_tool_input"
"unavailable"
"max_uses_exceeded"
"too_many_requests"
"query_too_long"
"request_too_large"
type: "web_search_tool_result_error"

UnionMember1 = array of WebSearchResultBlock { encrypted_content, page_age, title, 2 more } 
encrypted_content: string
page_age: string
title: string
type: "web_search_result"
url: string
tool_use_id: string
type: "web_search_tool_result"

model: Model

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:

UnionMember0 = "claude-opus-4-6" or "claude-opus-4-5-20251101" or "claude-opus-4-5" or 18 more

The model that will complete your prompt.

See models for additional details and options.
Accepts one of the following:"claude-opus-4-6"

Most intelligent model for building agents and coding
"claude-opus-4-5-20251101"

Premium model combining maximum intelligence with practical performance
"claude-opus-4-5"

Premium model combining maximum intelligence with practical performance
"claude-3-7-sonnet-latest"

High-performance model with early extended thinking
"claude-3-7-sonnet-20250219"

High-performance model with early extended thinking
"claude-3-5-haiku-latest"

Fastest and most compact model for near-instant responsiveness
"claude-3-5-haiku-20241022"

Our fastest model
"claude-haiku-4-5"

Hybrid model, capable of near-instant responses and extended thinking
"claude-haiku-4-5-20251001"

Hybrid model, capable of near-instant responses and extended thinking
"claude-sonnet-4-20250514"

High-performance model with extended thinking
"claude-sonnet-4-0"

High-performance model with extended thinking
"claude-4-sonnet-20250514"

High-performance model with extended thinking
"claude-sonnet-4-5"

Our best model for real-world agents and coding
"claude-sonnet-4-5-20250929"

Our best model for real-world agents and coding
"claude-opus-4-0"

Our most capable model
"claude-opus-4-20250514"

Our most capable model
"claude-4-opus-20250514"

Our most capable model
"claude-opus-4-1-20250805"

Our most capable model
"claude-3-opus-latest"

Excels at writing and complex tasks
"claude-3-opus-20240229"

Excels at writing and complex tasks
"claude-3-haiku-20240307"

Our previous most fast and cost-effective
UnionMember1 = string

role: "assistant"

Conversational role of the generated message.

This will always be `"assistant"`.

stop_reason: StopReason

The reason that we stopped.

This may be one the following values:

- `"end_turn"`: the model reached a natural stopping point

- `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum

- `"stop_sequence"`: one of your provided custom `stop_sequences` was generated

- `"tool_use"`: the model invoked one or more tools

- `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.

- `"refusal"`: when streaming classifiers intervene to handle potential policy violations

In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.
Accepts one of the following:"end_turn"
"max_tokens"
"stop_sequence"
"tool_use"
"pause_turn"
"refusal"

stop_sequence: string

Which custom stop sequence was generated, if any.

This value will be a non-null string if one of your custom stop sequences was generated.

type: "message"

Object type.

For Messages, this is always `"message"`.

usage: Usage { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 5 more } 

Billing and rate-limit usage.

Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

cache_creation: CacheCreation { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } 

Breakdown of cached tokens by TTL
ephemeral_1h_input_tokens: number

The number of input tokens used to create the 1 hour cache entry.
ephemeral_5m_input_tokens: number

The number of input tokens used to create the 5 minute cache entry.
cache_creation_input_tokens: number

The number of input tokens used to create the cache entry.
cache_read_input_tokens: number

The number of input tokens read from the cache.
inference_geo: string

The geographic region where inference was performed for this request.
input_tokens: number

The number of input tokens which were used.
output_tokens: number

The number of output tokens which were used.

server_tool_use: ServerToolUsage { web_search_requests } 

The number of server tool requests.
web_search_requests: number

The number of web search tool requests.

service_tier: "standard" or "priority" or "batch"

If the request used the priority, standard, or batch tier.
Accepts one of the following:"standard"
"priority"
"batch"
type: "succeeded"

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
- Usage policy
