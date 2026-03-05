# Source: https://docs.lancedb.com/indexing/vector-index
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
- Vector Indexes - LanceDB
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
Indexing
Vector IndexesDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
- Quickstart
- What is LanceDB?

- LanceDB Enterprise

- LanceDB Cloud
User Guide
- Working with tables

- Indexing

- Overview
- Vector Index
- FTS index
- Scalar Index
- GPU indexing
- Quantization
- Reindexing
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
- Option 1: Self-Hosted Indexing
- Option 2: Automated Indexing
- Choose the Right Index
- Indexing Tuning by Index Type
- Example: Construct an IVF Index
- Index Configuration
- 1. Setup
- 2. Construct an IVF Index
- 3. Query the IVF Index
- Search Configuration
- Example: Construct an HNSW Index
- Index Configuration
- 1. Construct an HNSW Index
- 2. Query the HNSW Index
- Example: Construct a Binary Vector Index
- Index Configuration
- 1. Create Table and Schema
- 2. Generate and Add Data
- 3. Construct the Binary Index
- 4. Vector Search
- Check Index Status
- Option 1: Check the UI
- Option 2: Use the APIIndexing
# Vector Indexes

Build and optimize LanceDB vector indexes, including IVF_HNSW_SQ, IVF_RQ, IVF_PQ, and binary indexes.
LanceDB offers two main vector indexing algorithms: Inverted File (IVF) and Hierarchically Navigable Small Worlds (HNSW). You can create multiple vector indexes within a Lance table. This guide walks through common configurations and build patterns.

### ​
Option 1: Self-Hosted Indexing

Manual, Sync or Async: If using LanceDB Open Source, you will have to build indexes manually, as well as reindex and tune indexing parameters. The Python SDK lets you do this synchronously and asynchronously.

### ​
Option 2: Automated Indexing

Automatic and Async: Indexing is automatic in LanceDB Cloud/Enterprise. As soon as data is updated, our system automates index optimization. This is done asynchronously.
Here is what happens in the background - when a table contains a single vector column named `vector`, LanceDB automatically:

- Infers the vector column from the schema

- Creates an optimized `IVF_PQ` index without manual configuration

- The default distance is `l2` or euclidean

Finally, LanceDB Cloud/Enterprise will analyze your data distribution to automatically configure indexing parameters.

You can create a new index with different parameters using `create_index` - this replaces any existing indexAlthough the `create_index` API returns immediately, the building of the vector index is asynchronous. To wait until all data is fully indexed, you can specify the `wait_timeout` parameter.

## ​
Choose the Right Index

Use this table as a quick starting point:
If your top priority is…Use this indexWhyTypical compressed size vs. raw vectorsBest recall/latency trade-off`IVF_HNSW_SQ`Combines IVF partitioning with HNSW graph search for strong quality at low latency.Typically a little larger than `1/4` of raw sizeMaximum compression`IVF_RQ`RaBitQ-style quantization with very strong compression.Around `1/32` of raw sizeHigher accuracy at small dimensions (`dimension <= 256`)`IVF_PQ`On small-dimensional vectors, `IVF_PQ` often provides higher accuracy with similar performance compared to `IVF_RQ`.Usually `1/64` to `1/16` of raw size (depends on `num_sub_vectors`)

If your vector search frequently includes metadata filters (`where(...)`), prefer `IVF_RQ` or `IVF_PQ`. In filtered workloads, `IVF_HNSW_SQ` latency can fluctuate significantly.
Compression ratios are practical rules of thumb and can vary with vector distribution, metric, and configuration.
For small dimensions, choose `IVF_PQ` for accuracy, not for guaranteed higher compression than `IVF_RQ`.

### ​
Indexing Tuning by Index Type

Start with these values, then tune for your workload:

- `IVF_HNSW_SQ`

- `num_partitions`: start at `num_rows // 1,048,576` (rounded to an integer)

- Lower `num_partitions` can reduce search latency, but index build may become slower because partitions are larger.

- `ef_construction`: start at `150`; increase for better recall, decrease for faster indexing.

- `IVF_RQ`

- `num_partitions`: start at `num_rows // 4096` (rounded to an integer). This is a strong default for most datasets.

- `IVF_PQ`

- `num_partitions`: start at `num_rows // 4096` (rounded to an integer).

- `num_sub_vectors`: start at `dimension // 8`. Increase for better recall, decrease for faster search and smaller indexes.

- For small dimensions (`dimension <= 256`), `IVF_PQ` is often preferred over `IVF_RQ` for better accuracy at similar query performance.

## ​
Example: Construct an IVF Index

In this example, we will create an index for a table containing 1536-dimensional vectors. The index will use IVF_PQ with L2 distance, which is well-suited for high-dimensional vector search.
Make sure you have enough data in your table (at least a few thousand rows) for effective index training.

### ​
Index Configuration

Sometimes you need to configure the index beyond default parameters:

- Index Types:

- `IVF_HNSW_SQ`: best recall/latency trade-off

- `IVF_RQ`: best compression for large, high-dimensional datasets

- `IVF_PQ`: often higher accuracy than `IVF_RQ` for small dimensions (`<= 256`) at similar query performance

- `metrics`: default is `l2`, other available are `cosine` or `dot`

- When using `cosine` similarity, distances range from 0 (identical vectors) to 2 (maximally dissimilar)

- `num_partitions`: use index-specific starting points from the section above:

- `IVF_HNSW_SQ`: `num_rows // 1,048,576`

- `IVF_RQ` and `IVF_PQ`: `num_rows // 4096`

- `num_sub_vectors`: applies to `IVF_PQ`; start with `dimension // 8`. Larger values often improve recall but can slow search.

Let’s take a look at a sample request for an IVF index:

### ​
1. Setup

Connect to LanceDB and open the table you want to index.

### ​
2. Construct an IVF Index

Create an `IVF_PQ` index with `cosine` similarity. Specify `vector_column_name` if you use multiple vector columns or non-default names. You can switch `index_type` to `IVF_RQ` or `IVF_HNSW_SQ` depending on your recall/latency/compression target.

### ​
3. Query the IVF Index

Search using a random 1,536-dimensional embedding.
​
Search Configuration
The previous query uses:

- `limit`: number of results to return

- `nprobes`: number of IVF partitions to scan. LanceDB auto-tunes this by default.

- `ef`: primarily relevant for `IVF_HNSW_SQ`; start around `1.5 * k` (where `k=limit`) and increase up to `10 * k` for higher recall.

- `nprobes` by index type:

- `IVF_HNSW_SQ`: usually keep auto-tuned `nprobes`, then tune `ef` first. For filtered search (`where(...)`), expect higher latency variance.

- `IVF_RQ`: keep auto-tuned `nprobes`; increase only when recall is insufficient.

- `IVF_PQ`: keep auto-tuned `nprobes`; increase when recall is insufficient. Often preferred over `IVF_RQ` when `dimension <= 256`.

- `refine_factor`: reads additional candidates and reranks in memory

- `.to_pandas()`: converts the results to a pandas DataFrame

## ​
Example: Construct an HNSW Index

### ​
Index Configuration

There are three key parameters to set when constructing an HNSW index:

- `metric`: The default is `l2` euclidean distance metric. Other available are `dot` and `cosine`.

- `m`: The number of neighbors to select for each vector in the HNSW graph.

- `ef_construction`: The number of candidates to evaluate during the construction of the HNSW graph.

### ​
1. Construct an HNSW Index

### ​
2. Query the HNSW Index

## ​
Example: Construct a Binary Vector Index

Binary vectors are useful for hash-based retrieval, fingerprinting, or any scenario where data can be represented as bits.

### ​
Index Configuration

- Store binary vectors as fixed-size binary data (uint8 arrays, with 8 bits per byte). For storage, pack binary vectors into bytes to save space.

- Index Type: `IVF_FLAT` is used for indexing binary vectors

- `metric`: the `hamming` distance is used for similarity search

- The dimension of binary vectors must be a multiple of 8. For example, a 128-dimensional vector is stored as a uint8 array of size 16.

### ​
1. Create Table and Schema

### ​
2. Generate and Add Data

### ​
3. Construct the Binary Index

### ​
4. Vector Search

## ​
Check Index Status

Vector index creation is fast - typically a few minutes for 1 million vectors with 1536 dimensions. You can check index status in two ways:

### ​
Option 1: Check the UI

Navigate to your table page - the “Index” column shows index status. It remains blank if no index exists or if creation is in progress.

### ​
Option 2: Use the API

Use `list_indices()` and `index_stats()` to check index status. The index name is formed by appending “_idx” to the column name. Note that `list_indices()` only returns information after the index is fully built.
To wait until all data is fully indexed, you can specify the `wait_timeout` parameter on `create_index()` or call `wait_for_index()` on the table.
Was this page helpful?

Yes
No

Suggest edits

Raise issue
OverviewFTS index
⌘I

githublinkedinxdiscordPowered by
