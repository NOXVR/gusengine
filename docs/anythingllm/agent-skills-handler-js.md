# Source: https://docs.anythingllm.com/agent/custom/handler-js
# Downloaded: 2026-02-16

---

handler.js reference ~ AnythingLLM
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
handler.js reference
This page is intended for developers who want to create custom agent skills for AnythingLLM.

## Rules & Guidelines

- 
The `handler.js` file must export a `runtime` object with a `handler`
function.

- 
The `handler` function must accept a single argument which is an object
containing the parameters defined in the `plugin.json` `entrypoint`
property, if any.

- 
The `handler` function must return a string value, anything else may break
the agent invocation or loop indefinitely.

- 
You must use `require` to import any modules you need from the NodeJS
standard library or any modules you have bundled with your custom agent
skill.

- 
You must use `await` when making any calls to external APIs or services.

- 
You must wrap your entire custom agent skill in a `try`/`catch` block and
return any error messages to the agent at invocation time.

## Available runtime properties and methods

### `this.runtimeArgs`

The `this.runtimeArgs` object contains the arguments that were passed to the `setup_args` from the `plugin.json` file.

You can access the value of a specific argument by using the `propertyName` as the key.

// plugin.json excerpt
// "setup_args": {
//     "OPEN_METEO_API_KEY": {
//       "type": "string",
//       "required": false,
//       "input": {
//         "type": "text",
//         "default": "YOUR_OPEN_METEO_API_KEY",
//         "placeholder": "sk-1234567890",
//         "hint": "The API key for the open-meteo API"
//       },
//       "value": "sk-key-for-service",
//     }
//   },
 
this.runtimeArgs["OPEN_METEO_API_KEY"]; // 'sk-key-for-service'

### `this.introspect`

The `this.introspect` function is used to log "thoughts" or "observations" to the user interface while the agent is running.

`this.introspect("Hello, world!"); // must be a string - will be shown to user`

### `this.logger`

The `this.logger` function is used to log messages to the console. This is useful for debugging your custom agent skill via logs.

`this.logger("Hello, world!"); // must be a string - will be printed to console while the agent is running`

### `this.config`

The `this.config` object contains the configuration for your custom agent skill. Useful for when you need to know the name of your custom agent skill or the version or for logs.

this.config.name; // 'Get Weather'
this.config.hubId; // 'open-meteo-weather-api'
this.config.version; // '1.0.0'

# Example `handler.js`

Objective: Get the weather for a given location latitude and longitude using the open-meteo API.

// handler.js
// NOT RECOMMENDED: We're using an external module here for demonstration purposes
// this would be a module we bundled with our custom agent skill and would be located in the same folder as our handler.js file
// Do not require modules outside of the plugin folder. It is recommended to use require within a function scope instead of the global scope.
// const _ExternalApiCaller = require('./external-api-caller.js');
 
module.exports.runtime = {
  handler: async function ({ latitude, longitude }) {
    const callerId = `${this.config.name}-v${this.config.version}`;
    try {
      this.introspect(
        `${callerId} called with lat:${latitude} long:${longitude}...`
      );
      const response = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m`
      );
      const data = await response.json();
      const averageTemperature = this._getAverage(data, "temperature_2m");
      const averageHumidity = this._getAverage(data, "relativehumidity_2m");
      const averageWindSpeed = this._getAverage(data, "windspeed_10m");
      return JSON.stringify({
        averageTemperature,
        averageHumidity,
        averageWindSpeed,
      });
    } catch (e) {
      this.introspect(
        `${callerId} failed to invoke with lat:${latitude} long:${longitude}. Reason: ${e.message}`
      );
      this.logger(
        `${callerId} failed to invoke with lat:${latitude} long:${longitude}`,
        e.message
      );
      return `The tool failed to run for some reason. Here is all we know ${e.message}`;
    }
  },
  // Helper function to get the average of an array of numbers!
  _getAverage(data, property) {
    return (
      data.hourly[property].reduce((a, b) => a + b, 0) /
      data.hourly[property].length
    );
  },
 
  // Recommended: Use this method to call external APIs or services
  // by requiring the module in the function scope and only if the code execution reaches that line
  // this is to prevent any unforseen issues with the global scope and module loading/unloading.
  // This file should be placed in the same folder as your handler.js file.
  _doExternalApiCall(myProp) {
    const _ScopedExternalCaller = require("./external-api-caller.js");
    return _ScopedExternalCaller.doSomething(myProp);
  },
};

plugin.json referenceImporting custom models

LightMIT 2026 © Mintplex Labs.
