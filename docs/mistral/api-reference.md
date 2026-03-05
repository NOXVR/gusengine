# Source: https://docs.mistral.ai/api
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
- API Specs
- 
- 
- 
- 
- 
Docs & API

Search docs⌘K

Toggle themeReach outTry Studio 

Search docs⌘K

Download OpenAPI SpecGetting Started
- Chat

- postChat Completion
- Fim

- Agents

- Embeddings

- Classifiers

- Files

- Fine Tuning

- Models

- Batch

- Ocr

- Audio Transcriptions
Beta
- Beta Agents

- Beta Conversations

- Beta Libraries

- Beta Libraries Accesses

- Beta Libraries Documents

# Chat Endpoints

Chat Completion API.

Toggle theme
### Examples

Real world code examples

Chat Completion

## POST /v1/chat/completions

### Request Body

application/json
frequency_penaltynumber

Default Value: `0`

The `frequency_penalty` penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.
max_tokensinteger|null

The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.

messages*array<SystemMessage|UserMessage|AssistantMessage|ToolMessage>

The prompt(s) to generate completions for, encoded as a list of dict with role and content.
metadatamap<any>|null

model*string

ID of the model to use. You can use the List Available Models API to see all of your available models, or see our Model overview for model descriptions.
ninteger|null

Number of completions to return for each request, input tokens are only billed once.
parallel_tool_callsboolean

Default Value: `true`

Whether to enable parallel function calling during tool use, when enabled the model can call multiple tools in parallel.

predictionPrediction|null

Enable users to specify an expected completion, optimizing response times by leveraging known or predictable content.
presence_penaltynumber

Default Value: `0`

The `presence_penalty` determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.
prompt_mode"reasoning"

Available options to the prompt_mode argument on the chat completion endpoint.
Values represent high-level intent. Assignment to actual SPs is handled internally.
System prompt may include knowledge cutoff date, model capabilities, tone to use, safety guidelines, etc.
random_seedinteger|null

The seed to use for random sampling. If set, different calls will generate deterministic results.

response_formatResponseFormat|null

Specify the format that the model must output. By default it will use `\{ "type": "text" \}`. Setting to `\{ "type": "json_object" \}` enables JSON mode, which guarantees the message the model generates is in JSON. When using JSON mode you MUST also instruct the model to produce JSON yourself with a system or a user message. Setting to `\{ "type": "json_schema" \}` enables JSON schema mode, which guarantees the message the model generates is in JSON and follows the schema you provide.
safe_promptboolean

Default Value: `false`

Whether to inject a safety prompt before all conversations.
stopstring|array<string>

Stop generation if this token is detected. Or if one of these tokens is detected when providing an array
streamboolean

Default Value: `false`

Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.
temperaturenumber|null

What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.

tool_choiceToolChoice|"auto"|"none"|"any"|"required"

Controls which (if any) tool is called by the model. `none` means the model will not call any tool and instead generates a message. `auto` means the model can pick between generating a message or calling one or more tools. `any` or `required` means the model must call one or more tools. Specifying a particular tool via `\{"type": "function", "function": \{"name": "my_function"\}\}` forces the model to call that tool.

toolsarray<Tool>|null

A list of tools the model may call. Use this to provide a list of functions the model may generate JSON inputs for.
top_pnumber

Default Value: `1`

Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.

200 (application/json)

200 (text/event-stream)

Successful Response

choices*array<ChatCompletionChoice>

created*integer

id*string

model*string

object*string

usage*UsageInfo

Response Typeevent-stream<CompletionEvent>
Successful Response

CompletionEvent {object}Playground
Test the endpoints live

TypeScript

Python

cURL

import { Mistral } from "@mistralai/mistralai";

const mistral = new Mistral({
  apiKey: "MISTRAL_API_KEY",
});

async function run() {
  const result = await mistral.chat.complete({
    model: "mistral-small-latest",
    messages: [
      {
        content: "Who is the best French painter? Answer in one short sentence.",
        role: "user",
      },
    ],
  });

  console.log(result);
}

run();

import { Mistral } from "@mistralai/mistralai";

const mistral = new Mistral({
  apiKey: "MISTRAL_API_KEY",
});

async function run() {
  const result = await mistral.chat.complete({
    model: "mistral-small-latest",
    messages: [
      {
        content: "Who is the best French painter? Answer in one short sentence.",
        role: "user",
      },
    ],
  });

  console.log(result);
}

run();

from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], stream=False)

    # Handle response
    print(res)

from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], stream=False)

    # Handle response
    print(res)

curl https://api.mistral.ai/v1/chat/completions \
 -X POST \
 -H 'Authorization: Bearer YOUR_APIKEY_HERE' \
 -H 'Content-Type: application/json' \
 -d '{
  "messages": [
    {
      "content": "ipsum eiusmod"
    }
  ],
  "model": "mistral-large-latest"
}'

curl https://api.mistral.ai/v1/chat/completions \
 -X POST \
 -H 'Authorization: Bearer YOUR_APIKEY_HERE' \
 -H 'Content-Type: application/json' \
 -d '{
  "messages": [
    {
      "content": "ipsum eiusmod"
    }
  ],
  "model": "mistral-large-latest"
}'
200 (application/json)

200 (text/event-stream)

{
  "choices": [
    {
      "finish_reason": "stop",
      "index": "0",
      "message": {}
    }
  ],
  "created": "1702256327",
  "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",
  "model": "mistral-small-latest",
  "object": "chat.completion",
  "usage": {}
}

{
  "choices": [
    {
      "finish_reason": "stop",
      "index": "0",
      "message": {}
    }
  ],
  "created": "1702256327",
  "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",
  "model": "mistral-small-latest",
  "object": "chat.completion",
  "usage": {}
}

`null`

`null`

### WHY MISTRAL
About usOur customersCareersContact us
### EXPLORE
AI SolutionsPartnersResearch
### DOCUMENTATION
DocumentationContributingCookbooks
### BUILD
AI StudioLe ChatMistral CodeMistral ComputeTry the API
### LEGAL
Terms of servicePrivacy policyLegal noticePrivacy ChoicesBrand
### COMMUNITY
Discord↗X↗Github↗LinkedIn↗Ambassador
Mistral AI © 2026

Toggle theme
