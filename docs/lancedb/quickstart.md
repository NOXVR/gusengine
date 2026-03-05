# Source: https://docs.lancedb.com/quickstart
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
- Quickstart - LanceDB
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
Get started
QuickstartDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
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
- 1. Install LanceDB
- 2. Connect to a LanceDB database
- Optional: LanceDB Cloud or Enterprise versions
- 3. Obtain data and ingest into LanceDB
- 4. Run a vector similarity search
- What’s next?Get started
# Quickstart

Get started with LanceDB in minutes.
The easiest way to get started with LanceDB is the open source version, which is an embedded database that
runs in-process (like SQLite). Let’s get started in just a few steps!

## ​
1. Install LanceDB

Install LanceDB in your client SDK.
PythonTypeScriptRust

Copy

Ask AI
pip install lancedb  # or uv add lancedb

## ​
2. Connect to a LanceDB database

Using LanceDB’s open source version is as simple as importing LanceDB as a library
and pointing to a local path — no servers needed!

### ​
Optional: LanceDB Cloud or Enterprise versions

If you’re looking for a fully-managed solution,
you can use LanceDB Cloud, which provides managed infrastructure,
security, and automatic backups. Simply replace the local path with a remote `uri`
that points to where your data is stored, and you’re ready to go.
For enormous scale and more advanced use cases beyond just search — like
feature engineering, model training and more, check out LanceDB Enterprise.

## ​
3. Obtain data and ingest into LanceDB

Let’s look at an example. We have the following records of characters in an adventure board game.
The vector column holds 3-dimensional embeddings representing each character.
To ingest the data into LanceDB, obtain data of the required shape
and pass in the data object to the `create_table` method as shown below.
Note that LanceDB tables require a schema. If you don’t provide one, LanceDB
will infer it from the data.

The `vector` arrays here are synthetic and for demonstration purposes only. In your real-world
applications, you’d generate these vectors from the raw text fields using a suitable embedding model.

## ​
4. Run a vector similarity search

Now, let’s perform a vector similarity search. The query vector should have the same
dimensionality as your data vectors and be generated using the same embedding model.
The search returns the most similar vectors based on a chosen distance metric (default is L2,
or Euclidean distance).
Our query is a vector that represents a “warrior”. Let’s find the result that’s most similar
to it!
The example for Python above shows how to convert results to a Polars DataFrame.
Depending on your language, you can collect query results as a list/array of objects or DataFrames
to be used downstream in your application.

Pandas users in Python can get results as a Pandas DataFrame
Use the `to_pandas()` method to convert query results into a Pandas DataFrame.

See the full code for these examples (including helper functions) in the
`quickstart` file for the appropriate client language in the
docs repo.

## ​
What’s next?

You’ve learned how to install LanceDB, connect, create a table, and run a first
vector search. In the real world, embeddings capture meaning and vector search
allows you to find the most relevant data based on semantic similarity.
Note that LanceDB is much more than “just a vector database” — it’s
a multimodal lakehouse.
There’s a lot more you can do with it! Continue
to the Table management guide to build on
this example with schema options, appending data, updates, and versioning.
As you explore LanceDB further, you can combine vector search with other techniques like filtering based
on metadata fields, full-text search, hybrid search, and more. Check out the tutorials
and guides below to continue learning.

## Basic table operations
Build on this quickstart with table creation, updates, and schema tips.

## LanceDB Cloud Quickstart
Get started with LanceDB Cloud in minutes.

## Build a RAG App
Learn how to build Retrieval-Augmented Generation (RAG) applications using LanceDB.
Was this page helpful?

Yes
No

Suggest edits

Raise issueLanceDB
⌘I

githublinkedinxdiscordPowered by
