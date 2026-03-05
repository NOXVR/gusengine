# Source: https://docs.lancedb.com/search/multivector-search
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
- Multivector Search - LanceDB
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
Search
Multivector SearchDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
- Quickstart
- What is LanceDB?

- LanceDB Enterprise

- LanceDB Cloud
User Guide
- Working with tables

- Indexing

- Search

- Overview
- Vector search
- Multivector search
- Full-Text Search (FTS)
- Hybrid search
- Filtering
- Query optimization
- Enterprise SQL

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
- Multivector Support
- Computing Similarity
- Example: Multivector Search
- 1. Setup
- 2. Define Schema
- 3. Generate Multivectors
- 4. Create a Table
- 5. Build an Index
- 6. Query a Single Vector
- 7. Query Multiple Vectors
- What’s Next?Search
# Multivector Search

Learn how to perform multivector search in LanceDB to handle multiple vector embeddings per document, ideal for late interaction models like ColBERT and ColPaLi.
LanceDB’s multivector support enables you to store and search multiple vector embeddings for a single item.
This capability is particularly valuable when working with late interaction models like ColBERT and ColPaLi that generate multiple embeddings per document.
In this tutorial, you’ll create a table with multiple vector embeddings per document and learn how to perform multivector search. For all the code - open in Colab

## ​
Multivector Support

Each item in your dataset can have a column containing multiple vectors, which LanceDB can efficiently index and search. When performing a search, you can query using either a single vector embedding or multiple vector embeddings.
LanceDB also integrates with ConteXtualized Token Retriever (XTR), an advanced retrieval model that prioritizes the most semantically important document tokens during search. This integration enhances the quality of search results by focusing on the most relevant token matches.

- Currently, only the `cosine` metric is supported for multivector search.

- The vector value type can be `float16`, `float32`, or `float64`.

### ​
Computing Similarity

MaxSim (Maximum Similarity) is a key concept in late interaction models that:

- Computes the maximum similarity between each query embedding and all document embeddings

- Sums these maximum similarities to get the final relevance score

- Effectively captures fine-grained semantic matches between query and document tokens

The MaxSim calculation can be expressed as:
MaxSim(Q,D)=∑i=1∣Q∣max⁡j=1∣D∣sim(qi,dj)\text{MaxSim}(Q, D) = \sum_{i=1}^{|Q|} \max_{j=1}^{|D|} \text{sim}(q_i, d_j)MaxSim(Q,D)=i=1∑∣Q∣​j=1max∣D∣​sim(qi​,dj​)
Where simsimsim is the similarity function (e.g. cosine similarity).
Q={q1,q2,...,q∣Q∣}Q = \{q_1, q_2, ..., q_{|Q|}\}Q={q1​,q2​,...,q∣Q∣​}
QQQ represents the query vector, and D={d1,d2,...,d∣D∣}D = \{d_1, d_2, ..., d_{|D|}\}D={d1​,d2​,...,d∣D∣​} represents the document vectors.

For now, you should use only the `cosine` metric for multivector search.
The vector value type can be `float16`, `float32` or `float64`.

## ​
Example: Multivector Search

### ​
1. Setup

Connect to LanceDB and import required libraries for data management.
Python

Copy

Ask AI
import lancedb
import numpy as np
import pyarrow as pa

db = lancedb.connect(
    uri="db://your-project-slug",
    api_key="your-api-key",
    region="your-cloud-region"
)

### ​
2. Define Schema

Define a schema that specifies a multivector field. A multivector field is a nested list structure where each document contains multiple vectors. In this case, we’ll create a schema with:

- An ID field as an integer (int64)

- A vector field that is a list of lists of float32 values

- The outer list represents multiple vectors per document

- Each inner list is a 256-dimensional vector

- Using float32 for memory efficiency while maintaining precision

Python

Copy

Ask AI
db = lancedb.connect("data/multivector_demo")
schema = pa.schema(
    [
        pa.field("id", pa.int64()),
        # float16, float32, and float64 are supported
        pa.field("vector", pa.list_(pa.list_(pa.float32(), 256))),
    ]
)

### ​
3. Generate Multivectors

Generate sample data where each document contains multiple vector embeddings, which could represent different aspects or views of the same document.
In this example, we create 1024 documents where each document has 2 random vectors of dimension 256, simulating a real-world scenario where you might have multiple embeddings per item.
Python

Copy

Ask AI
data = [
    {
        "id": i,
        "vector": np.random.random(size=(2, 256)).tolist(),  # Each document has 2 vectors
    }
    for i in range(1024)
]

### ​
4. Create a Table

Create a table with the defined schema and sample data, which will store multiple vectors per document for similarity search.
Python

Copy

Ask AI
tbl = db.create_table("multivector_example", data=data, schema=schema)

### ​
5. Build an Index

Only cosine similarity is supported as the distance metric for multivector search operations.
For faster search, build the standard `IVF_PQ` index over your vectors:
Python

Copy

Ask AI
tbl.create_index(metric="cosine", vector_column_name="vector")

### ​
6. Query a Single Vector

When searching with a single query vector, it will be compared against all vectors in each document, and the similarity scores will be aggregated to find the most relevant documents.
Python

Copy

Ask AI
query = np.random.random(256)
results_single = tbl.search(query).limit(5).to_pandas()

### ​
7. Query Multiple Vectors

With multiple vector queries, LanceDB calculates similarity using late interaction - a technique that computes relevance by finding the best matching pairs between query and document vectors. This approach provides more nuanced matching while maintaining fast retrieval speeds.
Python

Copy

Ask AI
query_multi = np.random.random(size=(2, 256))
results_multi = tbl.search(query_multi).limit(5).to_pandas()

## ​
What’s Next?

If you still need more guidance, you can try the complete Multivector Search Notebook.
Was this page helpful?

Yes
No

Suggest edits

Raise issue
Vector searchFull-Text Search (FTS)
⌘I

githublinkedinxdiscordPowered by
