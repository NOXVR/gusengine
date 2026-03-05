# Source: https://docs.cohere.com/reference/rerank
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

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
- Rerank API (v2) | Cohere
- 
- 
- 
Search/Ask AI

- 
- 
- [Guides and concepts](/docs/the-cohere-platform)[API Reference](/reference/about)[Release Notes](/changelog)[LLMU](https://cohere.com/llmu)[Cookbooks](/page/cookbooks)
Search/Ask AI

Guides and concepts
API Reference
Release Notes
LLMU
Cookbooks
- Cohere API
- [About](/reference/about)
- [Teams and Roles](/reference/teams-and-roles)
- [Errors](/reference/errors)
- [Migrating From API v1 to API v2](/docs/migrating-v1-to-v2)
- [Using the OpenAI SDK](/docs/compatibility-api)
- Endpoints
- v2/chat

- v2/rerank

- v2/embed

- v1/embed-jobs

- v1/datasets

- v1/tokenize

- v1/detokenize

- v1/models

- Deprecated
- v1/classify

- v1/connectors

- v1/finetuning

Light[Endpoints](/reference/chat)
[v2/rerank](/reference/rerank)
# 
Rerank API (v2)

Copy page
POSThttps://api.cohere.com/v2/rerank
POST/v2/rerankPython

```
1import cohere23co = cohere.ClientV2()45docs = [6    "Carson City is the capital city of the American state of Nevada.",7    "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",8    "Capitalization or capitalisation in English grammar is the use of a capital letter at the start of a word. English usage varies from capitalization in other languages.",9    "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",10    "Capital punishment has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",11]1213response = co.rerank(14    model="rerank-v4.0-pro",15    query="What is the capital of the United States?",16    documents=docs,17    top_n=3,18)19print(response)
```

Try it200Successful

```
1{2  "results": [3    {4      "index": 3,5      "relevance_score": 0.9990716    },7    {8      "index": 4,9      "relevance_score": 0.786786710    },11    {12      "index": 0,13      "relevance_score": 0.3271306814    }15  ],16  "id": "07734bd2-2473-4f07-94e1-0d9f0e6843cf",17  "meta": {18    "api_version": {19      "version": "2",20      "is_experimental": false21    },22    "billed_units": {23      "search_units": 124    }25  }26}
```
This endpoint takes in a query and a list of texts and produces an ordered array with each text assigned a relevance score.
### Authentication
AuthorizationBearer
Bearer authentication of the form `Bearer <token>`, where token is your auth token.

### Headers
X-Client-NamestringOptionalThe name of the project that is making the request.

### Request
modelstringRequired
The identifier of the model to use, eg `rerank-v3.5`.
querystringRequiredThe search querydocumentslist of stringsRequiredA list of texts that will be compared to the `query`.
For optimal performance we recommend against sending more than 1,000 documents in a single request.

**Note**: long documents will automatically be truncated to the value of `max_tokens_per_doc`.

**Note**: structured data should be formatted as YAML strings for best performance.top_nintegerOptional`>=1`Limits the number of returned rerank results to the specified value. If not passed, all the rerank results will be returned.max_tokens_per_docintegerOptional
Defaults to `4096`. Long documents will be automatically truncated to the specified number of tokens.
priorityintegerOptional`0-999`Defaults to `0`
Controls how early the request is handled. Lower numbers indicate higher priority (default: 0, the highest). When the system is under load, higher-priority requests are processed first and are the least likely to be dropped.

### Response
OKresultslist of objectsAn ordered list of ranked documents

Show 2 propertiesidstring or nullmetaobject or null

Show 5 properties
### Errors
400Bad Request Error401Unauthorized Error403Forbidden Error404Not Found Error422Unprocessable Entity Error429Too Many Requests Error498Invalid Token Error499Client Closed Request Error500Internal Server Error501Not Implemented Error503Service Unavailable Error504Gateway Timeout ErrorWas this page helpful?

Yes

NoBuilt with

[docs](/)v2 API

v2 API

[DASHBOARD](https://dashboard.cohere.com/)[PLAYGROUND](https://dashboard.cohere.com/playground/generate)[DOCS](/)[COMMUNITY](https://discord.com/invite/co-mmunity)LOG IN

A list of texts that will be compared to the `query`.
For optimal performance we recommend against sending more than 1,000 documents in a single request.

Note: long documents will automatically be truncated to the value of `max_tokens_per_doc`.

Note: structured data should be formatted as YAML strings for best performance.
