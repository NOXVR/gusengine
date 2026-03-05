# Source: https://docs.lancedb.com/embedding/quickstart
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
- 
- 
- Embeddings: Quickstart - LanceDB
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
Embeddings
Embeddings: QuickstartDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
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

- Overview
- Quickstart
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
- Step 1: Import Required Libraries
- Step 2: Connect to LanceDB Cloud
- Step 3: Initialize the Embedding Function
- Step 4: Define Your Schema
- Step 5: Create Table and Ingest Data
- Step 6: Query with Automatic Embedding
- ExamplesEmbeddings
# Embeddings: Quickstart

Quickstart guide for generating and working with embeddings.
LanceDB will automatically vectorize the data both at ingestion and query time. All you need to do is specify which model to use.
We support popular embedding models like OpenAI, Hugging Face, Sentence Transformers, CLIP, and more.

## ​
Step 1: Import Required Libraries

First, import the necessary LanceDB components:
Python

Copy

Ask AI
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

- `lancedb`: The main database connection and operations

- `LanceModel`: Pydantic model for defining table schemas

- `Vector`: Field type for storing vector embeddings

- `get_registry()`: Access to the embedding function registry. It has all the supported as well custom embedding functions registered by the user

## ​
Step 2: Connect to LanceDB Cloud

Establish a connection to your LanceDB instance:
Python

Copy

Ask AI
# Enter your LanceDB connection URI for OSS, Cloud or Enterprise here
db = lancedb.connect(...)

## ​
Step 3: Initialize the Embedding Function

Choose and configure your embedding model:
Python

Copy

Ask AI
model = get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5", )

This creates a Sentence Transformers embedding function using the BGE model. You can:

- Change `"sentence-transformers"` to other providers like `"openai"`, `"cohere"`, etc.

- Modify the model name for different embedding models

- Set `device="cuda"` for GPU acceleration if available

## ​
Step 4: Define Your Schema

Create a Pydantic model that defines your table structure:
Python

Copy

Ask AI
class Words(LanceModel):
    text: str = model.SourceField()  
    vector: Vector(model.ndims()) = model.VectorField()

- `SourceField()`: This field will be embedded

- `VectorField()`: This stores the embeddings

- `model.ndims()`: Sets vector dimensions for your model

## ​
Step 5: Create Table and Ingest Data

Create a table with your schema and add data:
Python

Copy

Ask AI
table = db.create_table("words", schema=Words)
table.add([
    {"text": "hello world"},
    {"text": "goodbye world"}
])

The `table.add()` call automatically:

- Takes the text from each document

- Generates embeddings using your chosen model

- Stores both the original text and the vector embeddings

## ​
Step 6: Query with Automatic Embedding

Note: On LanceDB cloud, automatic query embedding is not supported. You need to pass the embedding vector directly.
Search your data using natural language queries:
Python

Copy

Ask AI
query = "greetings"
actual = table.search(query).limit(1).to_pydantic(Words)[0]
print(actual.text)

The search process:

- Automatically converts your query text to embeddings

- Finds the most similar vectors in your table

- Returns the matching documents

## ​
Examples

LanceDB currently supports the via SDKs in Python, Typescript and Rust.
Below are some examples of generating and querying embeddings when using the embedding registry.
Was this page helpful?

Yes
No

Suggest edits

Raise issue
OverviewStorage options
⌘I

githublinkedinxdiscordPowered by
