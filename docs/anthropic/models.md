# Source: https://docs.anthropic.com/en/docs/about-claude/models
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
- Models overview - Claude API Docs
- 
- 
- 
- 
- 
- Loading...

English
Log in

Search...⌘KFirst stepsIntro to ClaudeQuickstartModels & pricingModels overviewChoosing a modelWhat's new in Claude 4.6Migration guideModel deprecationsPricingBuild with ClaudeFeatures overviewUsing the Messages APIHandling stop reasonsPrompting best practicesModel capabilitiesExtended thinkingAdaptive thinkingEffortFast mode (research preview)Structured outputsCitationsStreaming MessagesBatch processingPDF supportSearch resultsMultilingual supportEmbeddingsVisionToolsOverviewHow to implement tool useWeb search toolWeb fetch toolCode execution toolMemory toolBash toolComputer use toolText editor toolTool infrastructureTool searchProgrammatic tool callingFine-grained tool streamingContext managementContext windowsCompactionContext editingPrompt cachingToken countingFiles & assetsFiles APIAgent SkillsOverviewQuickstartBest practicesSkills for enterpriseUsing Skills with the APIAgent SDKOverviewQuickstartTypeScript SDKTypeScript V2 (preview)Python SDKMigration GuideGuides
MCP in the APIMCP connectorRemote MCP serversClaude on 3rd-party platformsAmazon BedrockMicrosoft FoundryVertex AIPrompt engineeringOverviewPrompt generatorUse prompt templatesPrompt improverBe clear and directUse examples (multishot prompting)Let Claude think (CoT)Use XML tagsGive Claude a role (system prompts)Chain complex promptsLong context tipsExtended thinking tipsTest & evaluateDefine success criteriaDevelop test casesUsing the Evaluation ToolReducing latencyStrengthen guardrailsReduce hallucinationsIncrease output consistencyMitigate jailbreaksStreaming refusalsReduce prompt leakKeep Claude in characterAdministration and monitoringAdmin API overviewData residencyWorkspacesUsage and Cost APIClaude Code Analytics APIZero Data Retention

Console
Log in
Models & pricing
Models overviewLoading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...Loading...

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
- Usage policyModels & pricing
# Models overview

Copy page
Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces our models and compares their performance.

Copy page

Choosing a model

If you're unsure which model to use, we recommend starting with Claude Opus 4.6 for the most complex tasks. It is our latest generation model with exceptional performance in coding and reasoning.

All current Claude models support text and image input, text output, multilingual capabilities, and vision. Models are available via the Anthropic API, AWS Bedrock, and Google Vertex AI.

Once you've picked a model, learn how to make your first API call.

Latest models comparison
FeatureClaude Opus 4.6Claude Sonnet 4.5Claude Haiku 4.5DescriptionOur most intelligent model for building agents and codingOur best combination of speed and intelligenceOur fastest model with near-frontier intelligenceClaude API IDclaude-opus-4-6claude-sonnet-4-5-20250929claude-haiku-4-5-20251001Claude API aliasclaude-opus-4-6claude-sonnet-4-5claude-haiku-4-5AWS Bedrock IDanthropic.claude-opus-4-6-v1anthropic.claude-sonnet-4-5-20250929-v1:0anthropic.claude-haiku-4-5-20251001-v1:0GCP Vertex AI IDclaude-opus-4-6claude-sonnet-4-5@20250929claude-haiku-4-5@20251001Pricing1$5 / input MTok
$25 / output MTok$3 / input MTok
$15 / output MTok$1 / input MTok
$5 / output MTokExtended thinkingYesYesYesAdaptive thinkingYesNoNoPriority TierYesYesYesComparative latencyModerateFastFastestContext window200K tokens / 
 1M tokens (beta)3200K tokens / 
 1M tokens (beta)3200K tokensMax output128K tokens64K tokens64K tokensReliable knowledge cutoffMay 20252Jan 20252Feb 2025Training data cutoffAug 2025Jul 2025Jul 2025

1 - See our pricing page for complete pricing information including batch API discounts, prompt caching rates, extended thinking costs, and vision processing fees.

2 - Reliable knowledge cutoff indicates the date through which a model's knowledge is most extensive and reliable. Training data cutoff is the broader date range of training data used. For more information, see Anthropic's Transparency Hub.

3 - Claude Opus 4.6 and Sonnet 4.5 support a 1M token context window when using the `context-1m-2025-08-07` beta header. Long context pricing applies to requests exceeding 200K tokens.

Models with the same snapshot date (e.g., 20240620) are identical across all platforms and do not change. The snapshot date in the model name ensures consistency and allows developers to rely on stable performance across different environments.

Starting with Claude Sonnet 4.5 and all subsequent models, AWS Bedrock and Google Vertex AI offer two endpoint types: global endpoints (dynamic routing for maximum availability) and regional endpoints (guaranteed data routing through specific geographic regions). For more information, see the third-party platform pricing section.

### 
Legacy models

Prompt and output performance

Claude 4 models excel in:

- 

Performance: Top-tier results in reasoning, coding, multilingual tasks, long-context handling, honesty, and image processing. See the Claude 4 blog post for more information.

- 

Engaging responses: Claude models are ideal for applications that require rich, human-like interactions.

- If you prefer more concise responses, you can adjust your prompts to guide the model toward the desired output length. Refer to our prompt engineering guides for details.

- For prompting best practices, see our prompting best practices guide.

- 

Output quality: When migrating from previous model generations to Claude 4, you may notice larger improvements in overall performance.

Migrating to Claude 4.6

If you're currently using older Claude models, we recommend migrating to Claude Opus 4.6 to take advantage of improved intelligence and enhanced capabilities. For detailed migration instructions, see Migrating to Claude 4.6.

Get started with Claude

If you're ready to start exploring what Claude can do for you, let's dive in! Whether you're a developer looking to integrate Claude into your applications or a user wanting to experience the power of AI firsthand, we've got you covered.

Looking to chat with Claude? Visit claude.ai!

Intro to Claude
Explore Claude's capabilities and development flow.

Quickstart
Learn how to make your first API call in minutes.

Claude Console
Craft and test powerful prompts directly in your browser.

If you have any questions or need assistance, don't hesitate to reach out to our support team or consult the Discord community.

Was this page helpful?
