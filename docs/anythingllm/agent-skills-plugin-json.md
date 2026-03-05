# Source: https://docs.anythingllm.com/agent/custom/plugin-json
# Downloaded: 2026-02-16

---

plugin.json reference ~ AnythingLLM
- 
- 
- 
- 
- 🚀 AnythingLLM v1.10.0 is live! Update now →

- ▲ Home
- AnythingLLM Roadmap
- Getting Started
- Introduction
- Feature Overview

- All Features
- AI Agents
- Private Browser Tool
- API Access
- Appearance Customization
- Chat Logs
- Chat Modes
- Embedded Chat Widgets
- Event Logs
- Embedding Models
- Language Models
- Transcription Models
- Vector Database
- Security & Access
- Privacy & Data Handling
- System Prompt Variables
- AnythingLLM Setup

- Embedder Setup

- Overview
- Local

- AnythingLLM Default
- LM Studio
- Local AI
- Ollama
- Cloud

- OpenAI
- Azure OpenAI
- Cohere
- LLM Setup

- Overview
- Local

- AnythingLLM Default
- LM Studio
- Local AI
- Ollama
- KobaldCPP
- Cloud

- Anthropic
- Azure OpenAI
- AWS Bedrock
- Cohere
- Google Gemini
- Groq
- Hugging Face
- Mistral AI
- OpenAI
- OpenAI (generic)
- OpenRouter
- Perplexity AI
- Together AI
- TrueFoundry
- APIpie
- Transcription Setup

- Overview
- Local

- AnythingLLM Default
- Cloud

- OpenAI
- Vector DB Setup

- Overview
- Local

- LanceDB
- Chroma
- Milvus
- Cloud

- AstraDB
- Pinecone
- QDrant
- Weaviate
- Zilliz
- Chat Interface overview
- Other configurations
- AnythingLLM Community Hub
- What is the Community Hub?
- Importing an item
- Uploading an item
- FAQ
- Installation Guides
- AnythingLLM Desktop

- Overview
- System Requirements
- Install for MacOS
- Install for Windows
- Install for Linux
- Desktop FAQ
- Update AnythingLLM
- Where is my data stored?
- Debugging & Logs
- Uninstall AnythingLLM
- Legal & Privacy
- Privacy Policy
- Terms of Use
- AnythingLLM Self-hosted

- Overview
- Docker Images
- System Requirements
- Quickstart
- Local Docker
- Deploy to Cloud VM
- Docker FAQ
- Connecting to localhost
- Debugging & Logs
- AnythingLLM Cloud

- Overview
- Limitations
- 502 Error on AnythingLLM Hosted
- Terms & Conditions
- Terms & Conditions
- Privacy Policy
- AnythingLLM Mobile

- Introduction
- Legal & Privacy
- Terms of Service
- Privacy Policy
- Guides
- MCP Compatibility

- Overview
- MCP on Docker
- MCP on Desktop
- Agent Flows

- What is an Agent Flow?
- Getting Started with Flows
- Tutorial: HackerNews Flow
- All about blocks

- Web Scraper
- API Call
- LLM Instruction
- Read File
- Write File
- Debugging flows
- Using AI Agents

- Overview
- Setup
- Usage
- Custom Skills

- Introduction
- Developer Guide
- plugin.json reference
- handler.js reference
- Importing custom models
- Browser Extension

- Install the AnythingLLM Browser Extension
- Meeting Assistant

- Introduction
- Features
- Frequently Asked Questions
- Using Documents in Chat

- Attaching vs RAG
- RAG in AnythingLLM
- AI Agent not using tools!
- Ollama Connection Debugging
- Fetch failed error on embed
- Manual QNN Model Download
- More
- Beta Previews

- What are beta previews?
- Enable feature previews
- Available previews

- Live document sync
- AI Computer use
- Desktop Changelogs

- Overview
- v1.10.0
- v1.9.1
- v1.9.0
- v1.8.5
- v1.8.4
- v1.8.3
- v1.8.2
- v1.8.1
- v1.8.0
- v1.7.8
- v1.7.7
- v1.7.6
- v1.7.5
- v1.7.4
- v1.7.3
- v1.7.2
- v1.7.1
- v1.7.0
- v1.6.11
- v1.6.10
- v1.6.9
- v1.6.8
- v1.6.7
- v1.6.6
- v1.6.5
- v1.6.4
- v1.6.3
- v1.6.2
- v1.6.1
- v1.6.0
- Contribute
- Community Hub

- FAQ
- Importing from the AnythingLLM Community Hub
- Uploading to the AnythingLLM Community Hub
- What is the Community Hub?
- Support
Light

Using AI Agents
Custom Skills
plugin.json reference
This page is intended for developers who want to create custom agent skills for AnythingLLM.

# `plugin.json` reference

The `plugin.json` file is used to define a custom agent skill for AnythingLLM. It is a JSON file that contains the following properties:

{
  // see #active for more information
  "active": true,
 
  // see #hubId for more information
  "hubId": "open-meteo-weather-api",
 
  // see #name for more information
  "name": "Get Weather",
 
  // see #other_properties for more information
  "schema": "skill-1.0.0",
  "version": "1.0.0",
  "description": "Gets the weather for a given location latitude and longitude using the open-meteo API",
  "author": "@tcarambat",
  "author_url": "https://github.com/tcarambat",
  "license": "MIT",
 
  // see #setup_args for more information
  "setup_args": {
    "OPEN_METEO_API_KEY": {
      "type": "string",
      "required": false,
      "input": {
        "type": "text",
        "default": "YOUR_OPEN_METEO_API_KEY",
        "placeholder": "sk-1234567890",
        "hint": "The API key for the open-meteo API"
      },
    }
  },
 
  // see #examples for more information
  "examples": [
    {
      "prompt": "What is the weather in Tokyo?",
      "call": "{\"latitude\": 35.6895, \"longitude\": 139.6917}"
    },
    {
      "prompt": "What is the weather in San Francisco?",
      "call": "{\"latitude\": 37.7749, \"longitude\": -122.4194}"
    },
    {
      "prompt": "What is the weather in London?",
      "call": "{\"latitude\": 51.5074, \"longitude\": -0.1278}"
    }
  ],
 
  // see #entrypoint for more information
  "entrypoint": {
    "file": "handler.js",
    "params": {
      "latitude": {
        "description": "Latitude of the location",
        "type": "string"
      },
      "longitude": {
        "description": "Longitude of the location",
        "type": "string"
      }
    }
  },
 
  // see #imported for more information
  "imported": true
}

## `active`

The `active` property is a boolean that determines if the custom agent skill is active. If it is set to `false`, the custom agent skill will not be loaded.

## `name`

The `name` property is a string that is used to identify the custom agent skill. This is the human-readable name of the skill that is displayed in the AnythingLLM UI.

## `hubId`

The `hubId` property is a string that is used to identify the custom agent skill. This must be the same as the parent folder name.

## `other_properties`

The `other_properties` property is a list of other properties that are used to define the custom agent skill. These are mostly optional and will not impact performance of the skill directly. See reference below for more information.

{
  "schema": "skill-1.0.0", // REQUIRED - do not change
  "version": "1.0.0", // REQUIRED - can be defined by user
  "description": "short description of the custom agent skill", // REQUIRED
  "author": "@tcarambat", // OPTIONAL - author tag of the custom agent skill
  "author_url": "https://github.com/tcarambat", // OPTIONAL - url of the author of the custom agent skill
  "license": "MIT" // OPTIONAL - license of the custom agent skill
}

## `setup_args`

Setup arguments are used to configure the custom agent skill from the UI and make runtime arguments accessible in the handler.js file when the skill is called.
The key of the setup argument is the name of the argument that is used in the handler.js file, while its properties automatically generate the UI and inputs for the argument in the AnythingLLM UI.

"setup_args": {
    "OPEN_METEO_API_KEY": {
      "type": "string", // What type of value is expected
      "required": false, // Is the argument required
      // Defines the UI of the input to be rendered in the AnythingLLM UI
      "input": {
        "type": "text", // What type of input to be rendered
        "default": "YOUR_OPEN_METEO_API_KEY", // Default value of the input
        "placeholder": "sk-1234567890", // Placeholder text for the input
        "hint": "The API key for the open-meteo API" // Hint text for the input
      },
      "value": "" // (optional) preset value of the argument - will be replaced by the user input in the AnythingLLM UI, but can be hardcoded.
    }
  },

## `examples`

The `examples` property is a array of examples that are used to pre-inject examples into the custom agent skill. These are optional but highly encouraged as providing some expected examples helps LLMs determine the more "use-case" oriented implementation of the skill.
Try to provide anywhere from 1-3 examples that are relevant to the skill as these are injected into the prompt and can help guide the LLM in the correct direction.

The `call` property should match the expected input format of the custom agent skill in the `handler.js` file.

// handler.js
module.exports.runtime = {
  // latitude and longitude are the expected parameters for the custom agent skill
  handler: async function ({ latitude, longitude }) {
    // ... do something with latitude and longitude
  },
};

"examples": [
  // Example prompts and expected invocation format for the custom agent skill
  // these are optional but highly encouraged since they help the LLM understand the expected format of the custom agent skill
  // and when to use the associated skill with respect to the user prompt.
  // This is known as "few-shot prompting" and is a best practice when creating custom agent skills.
  {
    "prompt": "What is the weather in Tokyo?",
    "call": "{\"latitude\": 35.6895, \"longitude\": 139.6917}"
  },
  {
    "prompt": "What is the weather in San Francisco?",
    "call": "{\"latitude\": 37.7749, \"longitude\": -122.4194}"
  },
  {
    "prompt": "What is the weather in London?",
    "call": "{\"latitude\": 51.5074, \"longitude\": -0.1278}"
  }
]

## `entrypoint`

The `entrypoint` property is used to define the entrypoint of the custom agent skill and the expected inputs! This is the file location and invocation parameters that are used to execute the custom agent skill.

"entrypoint": {
  "file": "handler.js", // location of the file to be executed with respect to the plugin.json file
  "params": {
    // all properties require a description and type and should match the expected input format of the custom agent skill in the handler.js file
    "latitude": {
      "description": "Latitude of the location", // Short description of the parameter purpose
      "type": "string" // supported types: string, number, boolean
    },
    "longitude": {
      "description": "Longitude of the location",
      "type": "string"
    }
  }
}

## `imported`

this value must be set to `true`.

Developer Guidehandler.js reference

LightMIT 2026 © Mintplex Labs.
