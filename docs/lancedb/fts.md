# Source: https://docs.lancedb.com/search/full-text-search
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
- Full-Text Search (FTS) - LanceDB
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
Full-Text Search (FTS)DocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
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
- Basic Usage
- Table Setup
- Construct FTS Index
- Full-text Search
- Advanced Usage
- Tokenize Table Data
- Filtering Options
- Phrase vs. Terms Queries
- Fuzzy Search
- Search for Substring
- Example: Fuzzy Search
- Generate Data
- Create Table
- Construct FTS Index
- Basic and Fuzzy Search
- Basic Exact Search
- Fuzzy Search with Typos
- Prefix based Match
- Phrase Match
- Flexible Phrase Match
- Search with Boosting
- Boolean Queries
- Combining Two Match Queries
- Example: Substring Search
- Setting Up the Table
- Basic Substring Search
- Handling Short Substrings
- Customizing N-gram Parameters
- Testing Custom N-gram Settings
- Full-Text Search on Array Fields
- Setting Up the Connection
- Defining the Schema
- Creating Sample Data
- Creating the Table and Adding Data
- Building the Full-Text Search Index
- Performing Fuzzy Search
- Performing Phrase SearchSearch
# Full-Text Search (FTS)

Learn how to implement full-text search in LanceDB using BM25 for keyword-based retrieval.
LanceDB provides support for Full-Text Search via Lance, allowing you to incorporate keyword-based search (based on BM25) in your retrieval solutions.

## ​
Basic Usage

Consider that we have a LanceDB table named `my_table`, whose string column `text` we want to index and query via keyword search, the FTS index must be created before you can search via keywords.

### ​
Table Setup

First, open or create the table you want to search:
PythonTypeScriptRust

Copy

Ask AI
import lancedb
from lancedb.index import FTS

uri = "data/sample-lancedb"
db = lancedb.connect(uri)

table = db.create_table(
    "my_table_fts",
    data=[
        {"vector": [3.1, 4.1], "text": "Frodo was a happy puppy"},
        {"vector": [5.9, 26.5], "text": "There are several kittens playing"},
    ],
)

### ​
Construct FTS Index

Create a full-text search index on your text column:
PythonTypeScriptRust

Copy

Ask AI
table.create_fts_index("text")

### ​
Full-text Search

Perform full-text search and retrieve results:
PythonTypeScriptRust

Copy

Ask AI
results = table.search("puppy")
    .limit(10)
    .select(["text"])
    .to_list()
# [{'text': 'Frodo was a happy puppy', '_score': 0.6931471824645996}]

The search is conducted on all indexed columns by default, so it’s useful when there are multiple indexed columns.
If you want to specify which columns to search use `fts_columns="text"`

LanceDB automatically searches on the existing FTS index if the input to the search is of type `str`. If you provide a vector as input, LanceDB will search the ANN index instead.

## ​
Advanced Usage

### ​
Tokenize Table Data

By default, the text is tokenized by splitting on punctuation and whitespaces, and would filter out words that are longer than 40 characters. All words are converted to lowercase.
Stemming is useful for improving search results by reducing words to their root form, e.g. “running” to “run”. LanceDB supports stemming for multiple languages. You should set the `base_tokenizer` parameter rather than `tokenizer_name` because you cannot customize the tokenizer if `tokenizer_name` is specified.
For example, to enable stemming for English:
Python

Copy

Ask AI
table.create_fts_index("text", language="English", replace=True)

The tokenizer is customizable, you can specify how the tokenizer splits the text, and how it filters out words, etc.
Default index parameters:

- `base_tokenizer`: `"simple"`

- `language`: English

- `with_position`: false

- `max_token_length`: 40

- `lower_case`: true

- `stem`: true

- `remove_stop_words`: true

- `ascii_folding`: true

For example, for language with accents, you can specify the tokenizer to use `ascii_folding` to remove accents, e.g. ‘é’ to ‘e’:
Python

Copy

Ask AI
table.create_fts_index(
        "text",
        language="French",
        stem=True,
        ascii_folding=True,
        replace=True,
    )

### ​
Filtering Options

LanceDB full text search supports to filter the search results by a condition, both pre-filtering and post-filtering are supported.
This can be invoked via the familiar `where` syntax.
With pre-filtering:
TypeScriptRust

Copy

Ask AI
await tbl
.search("puppy")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(true)
.toArray();

With post-filtering:
TypeScriptRust

Copy

Ask AI
await tbl
.search("apple")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(false)
.toArray();

### ​
Phrase vs. Terms Queries

Lance-based FTS doesn’t support queries using boolean operators `OR`, `AND` in the search string.
For full-text search you can specify either a phrase query like `"the old man and the sea"`,
or a terms search query like `old man sea`.
To search for a phrase, the index must be created with `with_position=True` and `remove_stop_words=False`:
Python

Copy

Ask AI
table.create_fts_index("text", with_position=True, replace=True)

This will allow you to search for phrases, but it will also significantly increase the index size and indexing time.

### ​
Fuzzy Search

Fuzzy search allows you to find matches even when the search terms contain typos or slight variations.
LanceDB uses the classic Levenshtein distance
to find similar terms within a specified edit distance.
ParameterTypeDefaultDescriptionfuzzinessint0Maximum edit distance allowed for each term. If not specified, automatically set based on term length: 0 for length ≤ 2, 1 for length ≤ 5, 2 for length > 5max_expansionsint50Maximum number of terms to consider for fuzzy matching. Higher values may improve recall but increase search time
Let’s create a sample table and build full-text search indices to demonstrate
fuzzy search capabilities and relevance boosting features.

### ​
Search for Substring

LanceDB supports searching for substrings in the text column, you can set the `base_tokenizer` parameter to `"ngram"` to enable this feature, and use the parameters `ngram_min_length` and `ngram_max_length` to control the length of the substrings:
ParameterTypeDefaultDescriptionngram_min_lengthint3Minimum length of the n-grams to search forngram_max_lengthint3Maximum length of the n-grams to search forprefix_onlyboolfalseWhether to only search for prefixes of the n-grams

## ​
Example: Fuzzy Search

### ​
Generate Data

First, let’s create a table with sample text data for testing fuzzy search:
PythonTypeScript

Copy

Ask AI
import lancedb
import numpy as np
import pandas as pd
import random

# Connect to LanceDB
db = lancedb.connect(
    uri="db://your-project-slug",
    api_key="your-api-key",
    region="us-east-1"
)

# Generate sample data
table_name = "fts-fuzzy-boosting-test"
vectors = [np.random.randn(128) for _ in range(100)]
text_nouns = ("puppy", "car")
text2_nouns = ("rabbit", "girl", "monkey")
verbs = ("runs", "hits", "jumps", "drives", "barfs")
adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
adj = ("adorable", "clueless", "dirty", "odd", "stupid")

# Generate random text combinations
text = [
    " ".join([
        text_nouns[random.randrange(0, len(text_nouns))],
        verbs[random.randrange(0, 5)],
        adv[random.randrange(0, 5)],
        adj[random.randrange(0, 5)],
    ])
    for _ in range(100)
]
text2 = [
    " ".join([
        text2_nouns[random.randrange(0, len(text2_nouns))],
        verbs[random.randrange(0, 5)],
        adv[random.randrange(0, 5)],
        adj[random.randrange(0, 5)],
    ])
    for _ in range(100)
]
count = [random.randint(1, 10000) for _ in range(100)]

### ​
Create Table

PythonTypeScript

Copy

Ask AI
# Create table with sample data
table = db.create_table(
    table_name,
    data=pd.DataFrame({
        "vector": vectors,
        "id": [i % 2 for i in range(100)],
        "text": text,
        "text2": text2,
        "count": count,
    }),
    mode="overwrite"
)

### ​
Construct FTS Index

Create a full-text search index on the first text column:
PythonTypeScript

Copy

Ask AI
# Create FTS index on first text column
table.create_fts_index("text")
wait_for_index(table, "text_idx")

Then, create an index on the second text column:
PythonTypeScript

Copy

Ask AI
# Create FTS index on second text column
table.create_fts_index("text2")
wait_for_index(table, "text2_idx")

### ​
Basic and Fuzzy Search

Now we can perform basic, fuzzy, and prefix match searches:
​
Basic Exact Search
PythonTypeScript

Copy

Ask AI
from lancedb.query import MatchQuery

# Basic match (exact search)
basic_match_results = (
    table.search(MatchQuery("crazily", "text"))
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)

​
Fuzzy Search with Typos
PythonTypeScript

Copy

Ask AI
# Fuzzy match (allows typos)
fuzzy_results = (
    table.search(MatchQuery("craziou", "text", fuzziness=2))
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)

​
Prefix based Match
Prefix-based match allows you to search for documents containing words that start with a specific prefix.
PythonTypeScript

Copy

Ask AI
# Fuzzy match (allows typos)
fuzzy_results = (
    table.search(MatchQuery("cra", "text", prefix_length=3))
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)

### ​
Phrase Match

Phrase matching enables you to search for exact sequences of words. Unlike regular text search
which matches individual terms independently, phrase matching requires words to appear in the
specified order with no intervening terms.

Phrase queries are supported but only for a single column; providing multiple columns with a quoted phrase raises an error.
Phrase matching is particularly useful for:

- Searching for specific multi-word expressions

- Matching exact titles or quotes

- Finding precise word combinations in a specific order

PythonTypeScript

Copy

Ask AI
# Exact phrase match
from lancedb.query import PhraseQuery

print("\n1. Exact phrase match for 'puppy runs':")
phrase_results = (
    table.search(PhraseQuery("puppy runs", "text"))
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)

​
Flexible Phrase Match
To provide more flexible phrase matching, LanceDB supports the `slop` parameter. This allows you to match phrases where the terms appear close to each other, even if they are not directly adjacent or in the exact order, as long as they are within the specified `slop` value.
For example, the phrase query “puppy merrily” would not return any results by default. However, if you set `slop=1`, it will match phrases like “puppy jumps merrily”, “puppy runs merrily”, and similar variations where one word appears between “puppy” and “merrily”.
PythonTypeScript

Copy

Ask AI
# Flexible phrase match with slop=1 for 'puppy merrily'
from lancedb.query import PhraseQuery

print("\n1. Flexible phrase match for 'puppy merrily' with slop=1:")
phrase_results = (
    table.search(PhraseQuery("puppy merrily", "text", slop=1))
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)

### ​
Search with Boosting

Boosting allows you to control the relative importance of different search terms or fields
in your queries. This feature is particularly useful when you need to:

- Prioritize matches in certain columns

- Promote specific terms while demoting others

- Fine-tune relevance scoring for better search results

ParameterTypeDefaultDescriptionpositiveQueryrequiredThe primary query terms to match and promote in resultsnegativeQueryrequiredTerms to demote in the search resultsnegative_boostfloat0.5Multiplier for negative matches (lower values = stronger demotion)
PythonTypeScript

Copy

Ask AI
from lancedb.query import MatchQuery, BoostQuery, MultiMatchQuery

# Boost data with 'runs' in text more than 'puppy' in text
print("\n2. Boosting data with 'runs' in text:")
boosting_results = (
  table.search(
      BoostQuery(
          MatchQuery("runs", "text"),
          MatchQuery("puppy", "text"),
          negative_boost=0.2,
      ),
  )
  .select(["id", "text"])
  .limit(100)
  .to_pandas()
)

"""Test searching across multiple fields."""
print("\n=== Multi Match Query Examples ===")
# Search across both text and text2
print("\n1. Searching 'crazily' in both text and text2:")
multi_match_results = (
    table.search(MultiMatchQuery("crazily", ["text", "text2"]))
    .select(["id", "text", "text2"])
    .limit(100)
    .to_pandas()
)

# Search with field boosting
print("\n2. Searching with boosted text2 field:")
multi_match_boosting_results = (
    table.search(
        MultiMatchQuery("crazily", ["text", "text2"], boosts=[1.0, 2.0]),
    )
    .select(["id", "text", "text2"])
    .limit(100)
    .to_pandas()
)

## Best practices

- Use fuzzy search when handling user input that may contain typos or variations

- Apply field boosting to prioritize matches in more important columns

- Combine fuzzy search with boosting for robust and precise search results
Recommendations for optimal FTS performance:

- Create full-text search indices on text columns that will be frequently searched

- For hybrid search combining text and vectors, see our hybrid search guide

- For performance benchmarks, check our benchmark results

- For complex queries, use SQL to combine FTS with other filter conditions

### ​
Boolean Queries

LanceDB supports boolean logic in full-text search, allowing you to combine multiple queries using `and` and `or` operators. This is useful when you want to match documents that satisfy multiple conditions (intersection) or at least one of several conditions (union).
​
Combining Two Match Queries
In Python, you can combine two MatchQuery objects using either the `and` function or the `&` operator (e.g., `MatchQuery("puppy", "text") and MatchQuery("merrily", "text")`); both methods are supported and yield the same result. Similarly, you can use either the `or` function or the `|` operator to perform an or query.
In TypeScript, boolean queries are constructed using the `BooleanQuery` class with a list of [Occur, subquery] pairs. For example, to perform an AND query:
SQL

Copy

Ask AI
BooleanQuery([
[Occur.Must, new MatchQuery("puppy", "text")],
[Occur.Must, new MatchQuery("merrily", "text")],
])

This approach allows you to specify complex boolean logic by combining multiple subqueries with different Occur values (such as `Must`, `Should`, or `MustNot`).

Which queries are allowed?A boolean query must include at least one `SHOULD` or `MUST` clause. Queries that contain only a `MUST_NOT` clause are not allowed.
PythonTypeScript

Copy

Ask AI
from lancedb.query import MatchQuery

# Example: Find documents containing both "puppy" and "merrily"
and_query = MatchQuery("puppy", "text") & MatchQuery("merrily", "text")
and_results = (
    table.search(and_query)
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)
print("\nDocuments containing both 'puppy' and 'merrily':")
print(and_results)

# Example: Find documents containing either "puppy" or "merrily"
or_query = MatchQuery("puppy", "text") | MatchQuery("merrily", "text")
or_results = (
    table.search(or_query)
    .select(["id", "text"])
    .limit(100)
    .to_pandas()
)
print("\nDocuments containing either 'puppy' OR 'merrily':")
print(or_results)

How to use booleans?

- Use `and`/`&`(Python), `Occur.Must`(Typescript) for intersection (documents must match all queries).

- Use `or`/`|`(Python), `Occur.Should`(Typescript) for union (documents must match at least one query).

## ​
Example: Substring Search

LanceDB supports searching for substrings in text columns using n-gram tokenization. This is useful for finding partial matches within text content.

### ​
Setting Up the Table

First, create a table with sample text data and configure n-gram tokenization:
Python

Copy

Ask AI
import pyarrow as pa
import lancedb

db = lancedb.connect(":memory:")

data = pa.table({"text": ["hello world", "lance database", "lance is cool"]})
table = db.create_table("test", data=data)
table.create_fts_index("text", base_tokenizer="ngram")

### ​
Basic Substring Search

With the default n-gram settings (minimum length of 3), you can search for substrings of length 3 or more:
Python

Copy

Ask AI
results = table.search("lan", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

results = (
    table.search("nce", query_type="fts").limit(10).to_list()
)  # spellchecker:disable-line
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

### ​
Handling Short Substrings

By default, the minimum n-gram length is 3, so shorter substrings like “la” won’t match:
Python

Copy

Ask AI
results = table.search("la", query_type="fts").limit(10).to_list()
assert len(results) == 0

### ​
Customizing N-gram Parameters

You can customize the n-gram behavior by adjusting the minimum length and using prefix-only matching:
Python

Copy

Ask AI
table.create_fts_index(
    "text",
    base_tokenizer="ngram",
    replace=True,
    ngram_min_length=2,
    prefix_only=True,
)

### ​
Testing Custom N-gram Settings

With the new settings, you can now search for shorter substrings and use prefix-only matching:
Python

Copy

Ask AI
results = table.search("lan", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

results = (
    table.search("nce", query_type="fts").limit(10).to_list()
)  # spellchecker:disable-line
assert len(results) == 0

results = table.search("la", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

## ​
Full-Text Search on Array Fields

LanceDB supports full-text search on string array columns, enabling efficient keyword-based search across multiple values within a single field (e.g., tags, keywords).

### ​
Setting Up the Connection

Connect to your LanceDB instance:
PythonTypeScript

Copy

Ask AI
import lancedb

# Connect to LanceDB
db = lancedb.connect(
  uri="db://your-project-slug",
  api_key="your-api-key",
  region="us-east-1"
)

### ​
Defining the Schema

Create a schema that includes an array field for tags:
PythonTypeScript

Copy

Ask AI
table_name = "fts-array-field-test"
schema = pa.schema([
    pa.field("id", pa.string()),
    pa.field("tags", pa.list_(pa.string())),
    pa.field("description", pa.string())
])

### ​
Creating Sample Data

Generate sample data with array fields containing tags:
PythonTypeScript

Copy

Ask AI
# Generate sample data
data = {
    "id": [f"doc_{i}" for i in range(10)],
    "tags": [
        ["python", "machine learning", "data science"],
        ["deep learning", "neural networks", "AI"],
        ["database", "indexing", "search"],
        ["vector search", "embeddings", "AI"],
        ["full text search", "indexing", "database"],
        ["python", "web development", "flask"],
        ["machine learning", "deep learning", "pytorch"],
        ["database", "SQL", "postgresql"],
        ["search engine", "elasticsearch", "indexing"],
        ["AI", "transformers", "NLP"]
    ],
    "description": [
        "Python for data science projects",
        "Deep learning fundamentals",
        "Database indexing techniques",
        "Vector search implementations",
        "Full-text search guide",
        "Web development with Python",
        "Machine learning with PyTorch",
        "Database management systems",
        "Search engine optimization",
        "AI and NLP applications"
    ]
}
See all 28 lines

### ​
Creating the Table and Adding Data

Create the table and populate it with the sample data:
PythonTypeScript

Copy

Ask AI
# Create table and add data
table = db.create_table(table_name, schema=schema, mode="overwrite")
table_data = pa.Table.from_pydict(data, schema=schema)
table.add(table_data)

### ​
Building the Full-Text Search Index

Create an FTS index on the tags column to enable efficient text search:
PythonTypeScript

Copy

Ask AI
# Create FTS index
table.create_fts_index("tags")
wait_for_index(table, "tags_idx")

### ​
Performing Fuzzy Search

Search for terms with typos using fuzzy matching:
PythonTypeScript

Copy

Ask AI
# Search examples
print("\nSearching for 'learning' in tags with a typo:")
result = (
    table.search(MatchQuery("learnin", column="tags", fuzziness=1))
    .select(['id', 'tags', 'description'])
    .to_arrow()
)

### ​
Performing Phrase Search

Search for exact phrases within the array fields:
PythonTypeScript

Copy

Ask AI
print("\nSearching for 'machine learning' in tags:")
result = (
    table.search(PhraseQuery("machine learning", column="tags"))
    .select(['id', 'tags', 'description'])
    .to_arrow()
)

Was this page helpful?

Yes
No

Suggest edits

Raise issue
Multivector searchHybrid search
⌘I

githublinkedinxdiscordPowered by
