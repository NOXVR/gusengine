# Source: https://docs.lancedb.com/troubleshooting
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
- Troubleshooting - LanceDB
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
- Skip to main content
Why Multimodal Data Needs a Better Lakehouse? — Download the Research Study

LanceDB home page
Search...⌘K

Ask AI

Search...

Navigation
Support
TroubleshootingDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
- Quickstart
- What is LanceDB?

- LanceDB Enterprise

- LanceDB Cloud
User Guide
- Working with tables

- Indexing

- Search

- Reranking

- Embeddings

- Storage

- Training
Feature Engineering (Geneva)
- Overview
- What is feature engineering?
- User Defined Functions (UDFs)

- Jobs

- Operations

- Deployment

- Geneva Python SDKSupport
- Troubleshooting
- FAQ

On this page
- Frequently-asked questions
- Getting technical support
- General issues
- Slow or unexpected query results
- Python’s multiprocessing module
- Logging: LanceDB CloudSupport
# Troubleshooting

Tips for troubleshooting basic LanceDB issues.

## ​
Frequently-asked questions

For commonly asked questions about LanceDB, please refer to our FAQ section.

## ​
Getting technical support

If you’re using LanceDB OSS or LanceDB Cloud, the best place to get help is in our
Discord community,
under the relevant language channel for Python, TypeScript, or Rust.
By asking in the language-specific channel, you can get help from the community
and our engineering team.
If you are a LanceDB Enterprise user, please contact our support team at support@lancedb.com for dedicated assistance.

## ​
General issues

### ​
Slow or unexpected query results

If you have slow queries or unexpected query results, it can be helpful to
print the resolved query plan.
LanceDB provides two powerful tools for query analysis and optimization: `explain_plan` and `analyze_plan`.
Read the full guide on Query Optimization.

### ​
Python’s multiprocessing module

Multiprocessing with `fork` is not supported. You should use `spawn` instead.

### ​
Logging: LanceDB Cloud

To provide more information, especially for LanceDB Cloud related issues, enable
debug logging. You can set the `LANCEDB_LOG` environment variable:

Copy

Ask AI
export LANCEDB_LOG=debug

You can turn off colors and formatting in the logs by setting

Copy

Ask AI
export LANCEDB_LOG_STYLE=never

Was this page helpful?

Yes
No

Suggest edits

Raise issue
Geneva Python SDKFAQ
⌘I

githublinkedinxdiscordPowered by
