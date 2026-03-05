# Source: https://docs.lancedb.com/storage/configuration
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
- Configuring Cloud Storage in LanceDB - LanceDB
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
Storage
Configuring Cloud Storage in LanceDBDocumentationIntegrationsTutorialsDemosAPI ReferenceGet started
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

- Storage options
- Configuring storage
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
- Object stores
- Configuration options
- General object store options
- AWS S3
- S3-compatible stores
- S3 Express
- DynamoDB commit store for concurrent writes
- Google Cloud Storage
- Azure Blob Storage
- Tigris Object StorageStorage
# Configuring Cloud Storage in LanceDB

Configure LanceDB to use S3, GCS, Azure Blob, and S3-compatible object stores with environment variables or storage options.
When using LanceDB OSS, you can choose where to store your data. The tradeoffs between storage options are covered in the storage architecture guide. This page shows how to configure each backend.

## ​
Object stores

LanceDB supports AWS S3 (and compatible stores), Azure Blob Storage, and Google Cloud Storage. The URI scheme in your `connect` call selects the backend.

### ​
Configuration options

When running inside the target cloud with correct IAM bindings, LanceDB often needs no extra configuration. When running elsewhere, provide credentials via environment variables or `storage_options`.

Keys are case-insensitive. Use lowercase in `storage_options` and uppercase in environment variables.
If you need the option to apply only to a specific table:
​
General object store options
KeyDescription`allow_http`Allow non-TLS connections. Default: `false`.`allow_invalid_certificates`Skip certificate validation. Default: `false`.`connect_timeout`Timeout for the connect phase. Default: `5s`.`timeout`Timeout for the full request. Default: `30s`.`user_agent`User agent string to send with requests.`proxy_url`Proxy URL to route requests through.`proxy_ca_certificate`PEM-formatted CA certificate for proxy connections.`proxy_excludes`Comma-separated hosts that bypass the proxy (domains or CIDR).

## ​
AWS S3

Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN` as environment variables or pass them in `storage_options`. Region is optional for AWS but required for most S3-compatible stores.
Minimum permissions usually include `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, `s3:ListBucket`, and `s3:GetBucketLocation` scoped to the relevant bucket/prefix.

### ​
S3-compatible stores

If the endpoint is `http://` (common in local development), also set `ALLOW_HTTP=true` or pass `allow_http=True` in `storage_options`.

### ​
S3 Express

Consult AWS networking requirements for S3 Express before enabling.

### ​
DynamoDB commit store for concurrent writes

S3 lacks atomic writes. To enable safe concurrent writers, use DynamoDB as a commit store by switching to the `s3+ddb` scheme and specifying the table name.
Create the DynamoDB table with hash key `base_uri` (string) and range key `version` (number). Small provisioned throughput (for example `ReadCapacityUnits=1`, `WriteCapacityUnits=1`) is sufficient for coordination.

LanceDB aborts multipart uploads on graceful shutdown, but crashes can leave incomplete uploads. Add an S3 lifecycle rule to delete in-progress uploads after a few days.

## ​
Google Cloud Storage

Provide credentials via `GOOGLE_SERVICE_ACCOUNT` (path to JSON) or include the path in `storage_options`. GCS defaults to HTTP/1; set `HTTP1_ONLY=false` if you need HTTP/2.

## ​
Azure Blob Storage

Set `AZURE_STORAGE_ACCOUNT_NAME` and `AZURE_STORAGE_ACCOUNT_KEY` as environment variables, or pass them via `storage_options`.
Other supported keys include service principal credentials (`azure_client_id`, `azure_client_secret`, `azure_tenant_id`), SAS tokens, managed identities, and custom endpoints.

## ​
Tigris Object Storage

Tigris exposes an S3-compatible API. Configure the endpoint and region:
Environment variables `AWS_ENDPOINT=https://t3.storage.dev` and `AWS_DEFAULT_REGION=auto` achieve the same configuration.
Was this page helpful?

Yes
No

Suggest edits

Raise issue
Storage optionsData loading and shuffles
⌘I

githublinkedinxdiscordPowered by
