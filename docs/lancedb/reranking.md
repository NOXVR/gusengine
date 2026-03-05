# Source: https://docs.lancedb.com/reranking/index
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
- Reranking Search Results - LanceDB
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
Reranking
Reranking Search ResultsDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
- Quickstart
- What is LanceDB?

- LanceDB Enterprise

- LanceDB Cloud
User Guide
- Working with tables

- Indexing

- Search

- Reranking

- Overview
- Custom rerankers
- Evaluation
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
- Quickstart
- Supported Rerankers
- Multi-vector reranking
- Creating Custom RerankersReranking
# Reranking Search Results

Use a reranker to improve search relevance.
Reranking is the process of re-ordering search results to improve relevance, often using a
different model than the one used for the initial search. LanceDB has built-in support for reranking
with models from Cohere, Sentence-Transformers, and more.

### ​
Quickstart

To use a reranker, you perform a search and then pass the results to the `rerank()` method.
Python

Copy

Ask AI
import lancedb
from lancedb.rerank import CohereReranker

db = lancedb.connect("/tmp/lancedb")
table = db.open_table("my_table")

query = "what is the capital of france"

# Search with reranking
reranker = CohereReranker()
reranked_results = table.search(query).limit(10).rerank(reranker=reranker).to_df()

### ​
Supported Rerankers

LanceDB supports several rerankers out of the box. Here are a few examples:
RerankerDefault Model`CohereReranker``rerank-english-v2.0``CrossEncoderReranker``cross-encoder/ms-marco-MiniLM-L-6-v2``ColbertReranker``colbert-ir/colbertv2.0`
You can find more details about these and other rerankers in the integrations section.

### ​
Multi-vector reranking

Most rerankers support reranking based on multiple vectors. To rerank based on multiple vectors, you can pass a list of vectors to the `rerank` method. Here’s an example of how to rerank based on multiple vector columns using the `CrossEncoderReranker`:
Python

Copy

Ask AI
from lancedb.rerankers import CrossEncoderReranker

reranker = CrossEncoderReranker()

query = "hello"

res1 = table.search(query, vector_column_name="vector").limit(3)
res2 = table.search(query, vector_column_name="text_vector").limit(3)
res3 = table.search(query, vector_column_name="meta_vector").limit(3)

reranked = reranker.rerank_multivector([res1, res2, res3],  deduplicate=True)

## ​
Creating Custom Rerankers

LanceDB also you to create custom rerankers by extending the base `Reranker` class. The custom reranker
should implement the `rerank` method that takes a list of search results and returns a reranked list of
search results. This is covered in more detail in the creating custom rerankers section.
Was this page helpful?

Yes
No

Suggest edits

Raise issue
FTS with SQLCustom rerankers
⌘I

githublinkedinxdiscordPowered by
