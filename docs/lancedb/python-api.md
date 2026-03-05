# Source: https://lancedb.github.io/lancedb/python/python/
# Downloaded: 2026-02-16

---

- 
      
      
        
- 
      
      
        
- 
      
      
      
- 
      
    
    
      
        Python - LanceDB
      
    
    
      
- 
      
        
        
- 
      
      

  
  
  
  
  

    
    
      
    
    
      
        
        
        
- 
        
- 
        
      
    
    
      
- 
    
      
- 
    
      
- 
    
    
    
      
  

  
  

  
    
  

    
    
    
  
  
  
    
    
      
    
    
    
    
    
  
    
    
    
    
    
      
        
        
          Skip to content
        
      
    
    
      
    
    
    
      

  

  
      
    
    
      
        
          
            Initializing search
          
          
        
      
    
  

    
    
      
        
  
    
    

  
  
    lancedb/lancedb
  

      
    
  
  

    
    
      
      
        
          
        
      
      
        
          
            
              
              
                
                  
                    

  

      
        
- 
  
    
      Tables (Synchronous)
    
  
  
    
  

      
        
- 
  
    
      Querying (Synchronous)
    
  
  
    
  

      
        
- 
  
    
      Embeddings
    
  
  
    
  

      
        
- 
  
    
      Remote configuration
    
  
  
    
  

      
        
- 
  
    
      Context
    
  
  
    
  

      
        
- 
  
    
      Full text search
    
  
  
    
  

      
        
- 
  
    
      Utilities
    
  
  
    
  

      
        
- 
  
    
      Integrations
    
  
  

      
        
- 
  
    
      Pydantic
    
  
  
    
  

      
        
- 
  
    
      Reranking
    
  
  
    
  

      
        
- 
  
    
      Connections (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Tables (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Indices (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Querying (Asynchronous)
    
  
  
    
  

      
    
  

      
    
  

              
            
              
                
  
  
  
  
    
- 
      
        
  
  
    Javascript/TypeScript
  
  

      
    
  

              
            
              
                
  
  
  
  
    
- 
      
        
  
  
    Java
  
  

      
    
  

              
            
              
                
  
  
  
  
    
- 
      
        
  
  
    Rust
  
  

      
    
  

              
            
          
        
      
    
  

    
  

                  
                
              
            
            
              
              
                
                  
                    

  

      
        
- 
  
    
      Tables (Synchronous)
    
  
  
    
  

      
        
- 
  
    
      Querying (Synchronous)
    
  
  
    
  

      
        
- 
  
    
      Embeddings
    
  
  
    
  

      
        
- 
  
    
      Remote configuration
    
  
  
    
  

      
        
- 
  
    
      Context
    
  
  
    
  

      
        
- 
  
    
      Full text search
    
  
  
    
  

      
        
- 
  
    
      Utilities
    
  
  
    
  

      
        
- 
  
    
      Integrations
    
  
  

      
        
- 
  
    
      Pydantic
    
  
  
    
  

      
        
- 
  
    
      Reranking
    
  
  
    
  

      
        
- 
  
    
      Connections (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Tables (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Indices (Asynchronous)
    
  
  
    
  

      
        
- 
  
    
      Querying (Asynchronous)
    
  
  
    
  

      
    
  

                  
                
              
            
          
          
            
              
                
                  

  
    
      
      

    
  
  

# Python API Reference¶

This section contains the API reference for the Python API of LanceDB. Both synchronous and asynchronous APIs are available.

The general flow of using the API is:

- Use lancedb.connect or lancedb.connect_async to connect to a database.

- Use the returned lancedb.DBConnection or lancedb.AsyncConnection to
   create or open tables.

- Use the returned lancedb.table.Table or lancedb.AsyncTable to query
   or modify tables.

## Installation¶

pip install lancedb

The following methods describe the synchronous API client. There
is also an asynchronous API client.

## Connections (Synchronous)¶

            lancedb.connect

¶

connect(uri: URI, *, api_key: Optional[str] = None, region: str = 'us-east-1', host_override: Optional[str] = None, read_consistency_interval: Optional[timedelta] = None, request_thread_pool: Optional[Union[int, ThreadPoolExecutor]] = None, client_config: Union[ClientConfig, Dict[str, Any], None] = None, storage_options: Optional[Dict[str, str]] = None, session: Optional[Session] = None, **kwargs: Any) -> DBConnection

    

      
Connect to a LanceDB database.

Parameters:

    
        
- 
          `uri`
              (`URI`)
          –
          
            
The uri of the database.

          
        
        
- 
          `api_key`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
If presented, connect to LanceDB cloud.
Otherwise, connect to a database on file system or cloud storage.
Can be set via environment variable `LANCEDB_API_KEY`.

          
        
        
- 
          `region`
              (`str`, default:
                  `'us-east-1'`
)
          –
          
            
The region to use for LanceDB Cloud.

          
        
        
- 
          `host_override`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The override url for LanceDB Cloud.

          
        
        
- 
          `read_consistency_interval`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
(For LanceDB OSS only)
The interval at which to check for updates to the table from other
processes. If None, then consistency is not checked. For performance
reasons, this is the default. For strong consistency, set this to
zero seconds. Then every read will check for updates from other
processes. As a compromise, you can set this to a non-zero timedelta
for eventual consistency. If more than that interval has passed since
the last check, then the table will be checked for updates. Note: this
consistency only applies to read operations. Write operations are
always consistent.

          
        
        
- 
          `client_config`
              (`Union[ClientConfig, Dict[str, Any], None]`, default:
                  `None`
)
          –
          
            
Configuration options for the LanceDB Cloud HTTP client. If a dict, then
the keys are the attributes of the ClientConfig class. If None, then the
default configuration is used.

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. See available options at
https://lancedb.com/docs/storage/

          
        
        
- 
          `session`
              (`Optional[Session]`, default:
                  `None`
)
          –
          
            
(For LanceDB OSS only)
A session to use for this connection. Sessions allow you to configure
cache sizes for index and metadata caches, which can significantly
impact memory use and performance. They can also be re-used across
multiple connections to share the same cache state.

          
        
    

Examples:

    
For a local directory, provide a path for the database:

    
>>> import lancedb
>>> db = lancedb.connect("~/.lancedb")

    
For object storage, use a URI prefix:

    
>>> db = lancedb.connect("s3://my-bucket/lancedb",
...                      storage_options={"aws_access_key_id": "***"})

    
Connect to LanceDB cloud:

    
>>> db = lancedb.connect("db://my_database", api_key="ldb_...",
...                      client_config={"retry_config": {"retries": 5}})

Returns:

    
        
- 
`conn` (              `DBConnection`
)          –
          
            
A connection to a LanceDB database.

          
        
    

            
              Source code in `lancedb/__init__.py`
              
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
def connect(
    uri: URI,
    *,
    api_key: Optional[str] = None,
    region: str = "us-east-1",
    host_override: Optional[str] = None,
    read_consistency_interval: Optional[timedelta] = None,
    request_thread_pool: Optional[Union[int, ThreadPoolExecutor]] = None,
    client_config: Union[ClientConfig, Dict[str, Any], None] = None,
    storage_options: Optional[Dict[str, str]] = None,
    session: Optional[Session] = None,
    **kwargs: Any,
) -> DBConnection:
    """Connect to a LanceDB database.

    Parameters
    ----------
    uri: str or Path
        The uri of the database.
    api_key: str, optional
        If presented, connect to LanceDB cloud.
        Otherwise, connect to a database on file system or cloud storage.
        Can be set via environment variable `LANCEDB_API_KEY`.
    region: str, default "us-east-1"
        The region to use for LanceDB Cloud.
    host_override: str, optional
        The override url for LanceDB Cloud.
    read_consistency_interval: timedelta, default None
        (For LanceDB OSS only)
        The interval at which to check for updates to the table from other
        processes. If None, then consistency is not checked. For performance
        reasons, this is the default. For strong consistency, set this to
        zero seconds. Then every read will check for updates from other
        processes. As a compromise, you can set this to a non-zero timedelta
        for eventual consistency. If more than that interval has passed since
        the last check, then the table will be checked for updates. Note: this
        consistency only applies to read operations. Write operations are
        always consistent.
    client_config: ClientConfig or dict, optional
        Configuration options for the LanceDB Cloud HTTP client. If a dict, then
        the keys are the attributes of the ClientConfig class. If None, then the
        default configuration is used.
    storage_options: dict, optional
        Additional options for the storage backend. See available options at
        <https://lancedb.com/docs/storage/>
    session: Session, optional
        (For LanceDB OSS only)
        A session to use for this connection. Sessions allow you to configure
        cache sizes for index and metadata caches, which can significantly
        impact memory use and performance. They can also be re-used across
        multiple connections to share the same cache state.

    Examples
    --------

    For a local directory, provide a path for the database:

    >>> import lancedb
    >>> db = lancedb.connect("~/.lancedb")

    For object storage, use a URI prefix:

    >>> db = lancedb.connect("s3://my-bucket/lancedb",
    ...                      storage_options={"aws_access_key_id": "***"})

    Connect to LanceDB cloud:

    >>> db = lancedb.connect("db://my_database", api_key="ldb_...",
    ...                      client_config={"retry_config": {"retries": 5}})

    Returns
    -------
    conn : DBConnection
        A connection to a LanceDB database.
    """
    if isinstance(uri, str) and uri.startswith("db://"):
        if api_key is None:
            api_key = os.environ.get("LANCEDB_API_KEY")
        if api_key is None:
            raise ValueError(f"api_key is required to connect to LanceDB cloud: {uri}")
        if isinstance(request_thread_pool, int):
            request_thread_pool = ThreadPoolExecutor(request_thread_pool)
        return RemoteDBConnection(
            uri,
            api_key,
            region,
            host_override,
            # TODO: remove this (deprecation warning downstream)
            request_thread_pool=request_thread_pool,
            client_config=client_config,
            storage_options=storage_options,
            **kwargs,
        )
    _check_s3_bucket_with_dots(str(uri), storage_options)

    if kwargs:
        raise ValueError(f"Unknown keyword arguments: {kwargs}")

    return LanceDBConnection(
        uri,
        read_consistency_interval=read_consistency_interval,
        storage_options=storage_options,
        session=session,
    )

            
    

            lancedb.db.DBConnection

¶

    
            

              Bases: `EnforceOverrides`

      
An active LanceDB connection interface.

              
                Source code in `lancedb/db.py`
                
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
class DBConnection(EnforceOverrides):
    """An active LanceDB connection interface."""

    def list_namespaces(
        self,
        namespace: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ListNamespacesResponse:
        """List immediate child namespace names in the given namespace.

        Parameters
        ----------
        namespace: List[str], default []
            The parent namespace to list namespaces in.
            Empty list represents root namespace.
        page_token: str, optional
            Token for pagination. Use the token from a previous response
            to get the next page of results.
        limit: int, optional
            The maximum number of results to return.

        Returns
        -------
        ListNamespacesResponse
            Response containing namespace names and optional page_token for pagination.
        """
        if namespace is None:
            namespace = []
        return ListNamespacesResponse(namespaces=[], page_token=None)

    def create_namespace(
        self,
        namespace: List[str],
        mode: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> CreateNamespaceResponse:
        """Create a new namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to create.
        mode: str, optional
            Creation mode - "create" (fail if exists), "exist_ok" (skip if exists),
            or "overwrite" (replace if exists). Case insensitive.
        properties: Dict[str, str], optional
            Properties to set on the namespace.

        Returns
        -------
        CreateNamespaceResponse
            Response containing the properties of the created namespace.
        """
        raise NotImplementedError(
            "Namespace operations are not supported for this connection type"
        )

    def drop_namespace(
        self,
        namespace: List[str],
        mode: Optional[str] = None,
        behavior: Optional[str] = None,
    ) -> DropNamespaceResponse:
        """Drop a namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to drop.
        mode: str, optional
            Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
        behavior: str, optional
            Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
            Case insensitive.

        Returns
        -------
        DropNamespaceResponse
            Response containing properties and transaction_id if applicable.
        """
        raise NotImplementedError(
            "Namespace operations are not supported for this connection type"
        )

    def describe_namespace(self, namespace: List[str]) -> DescribeNamespaceResponse:
        """Describe a namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to describe.

        Returns
        -------
        DescribeNamespaceResponse
            Response containing the namespace properties.
        """
        raise NotImplementedError(
            "Namespace operations are not supported for this connection type"
        )

    def list_tables(
        self,
        namespace: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ListTablesResponse:
        """List all tables in this database with pagination support.

        Parameters
        ----------
        namespace: List[str], optional
            The namespace to list tables in.
            None or empty list represents root namespace.
        page_token: str, optional
            Token for pagination. Use the token from a previous response
            to get the next page of results.
        limit: int, optional
            The maximum number of results to return.

        Returns
        -------
        ListTablesResponse
            Response containing table names and optional page_token for pagination.
        """
        raise NotImplementedError(
            "list_tables is not supported for this connection type"
        )

    @abstractmethod
    def table_names(
        self,
        page_token: Optional[str] = None,
        limit: int = 10,
        *,
        namespace: Optional[List[str]] = None,
    ) -> Iterable[str]:
        """List all tables in this database, in sorted order

        Parameters
        ----------
        namespace: List[str], default []
            The namespace to list tables in.
            Empty list represents root namespace.
        page_token: str, optional
            The token to use for pagination. If not present, start from the beginning.
            Typically, this token is last table name from the previous page.
        limit: int, default 10
            The size of the page to return.

        Returns
        -------
        Iterable of str
        """
        pass

    @abstractmethod
    def create_table(
        self,
        name: str,
        data: Optional[DATA] = None,
        schema: Optional[Union[pa.Schema, LanceModel]] = None,
        mode: str = "create",
        exist_ok: bool = False,
        on_bad_vectors: str = "error",
        fill_value: float = 0.0,
        embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None,
        *,
        namespace: Optional[List[str]] = None,
        storage_options: Optional[Dict[str, str]] = None,
        storage_options_provider: Optional["StorageOptionsProvider"] = None,
        data_storage_version: Optional[str] = None,
        enable_v2_manifest_paths: Optional[bool] = None,
    ) -> Table:
        """Create a [Table][lancedb.table.Table] in the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], default []
            The namespace to create the table in.
            Empty list represents root namespace.
        data: The data to initialize the table, *optional*
            User must provide at least one of `data` or `schema`.
            Acceptable types are:

            - list-of-dict

            - pandas.DataFrame

            - pyarrow.Table or pyarrow.RecordBatch
        schema: The schema of the table, *optional*
            Acceptable types are:

            - pyarrow.Schema

            - [LanceModel][lancedb.pydantic.LanceModel]
        mode: str; default "create"
            The mode to use when creating the table.
            Can be either "create" or "overwrite".
            By default, if the table already exists, an exception is raised.
            If you want to overwrite the table, use mode="overwrite".
        exist_ok: bool, default False
            If a table by the same name already exists, then raise an exception
            if exist_ok=False. If exist_ok=True, then open the existing table;
            it will not add the provided data but will validate against any
            schema that's specified.
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contains NaNs.
            One of "error", "drop", "fill".
        fill_value: float
            The value to use when filling vectors. Only used if on_bad_vectors="fill".
        storage_options: dict, optional
            Additional options for the storage backend. Options already set on the
            connection will be inherited by the table, but can be overridden here.
            See available options at
            <https://lancedb.com/docs/storage/>

            To enable stable row IDs (row IDs remain stable after compaction,
            update, delete, and merges), set `new_table_enable_stable_row_ids`
            to `"true"` in storage_options when connecting to the database.
        data_storage_version: optional, str, default "stable"
            Deprecated.  Set `storage_options` when connecting to the database and set
            `new_table_data_storage_version` in the options.
        enable_v2_manifest_paths: optional, bool, default False
            Deprecated.  Set `storage_options` when connecting to the database and set
            `new_table_enable_v2_manifest_paths` in the options.
        Returns
        -------
        LanceTable
            A reference to the newly created table.

        !!! note

            The vector index won't be created by default.
            To create the index, call the `create_index` method on the table.

        Examples
        --------

        Can create with list of tuples or dictionaries:

        >>> import lancedb
        >>> db = lancedb.connect("./.lancedb")
        >>> data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
        ...         {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
        >>> db.create_table("my_table", data)
        LanceTable(name='my_table', version=1, ...)
        >>> db["my_table"].head()
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: double
        long: double
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        You can also pass a pandas DataFrame:

        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...    "vector": [[1.1, 1.2], [0.2, 1.8]],
        ...    "lat": [45.5, 40.1],
        ...    "long": [-122.7, -74.1]
        ... })
        >>> db.create_table("table2", data)
        LanceTable(name='table2', version=1, ...)
        >>> db["table2"].head()
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: double
        long: double
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        Data is converted to Arrow before being written to disk. For maximum
        control over how data is saved, either provide the PyArrow schema to
        convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

        >>> import pyarrow as pa
        >>> custom_schema = pa.schema([
        ...   pa.field("vector", pa.list_(pa.float32(), 2)),
        ...   pa.field("lat", pa.float32()),
        ...   pa.field("long", pa.float32())
        ... ])
        >>> db.create_table("table3", data, schema = custom_schema)
        LanceTable(name='table3', version=1, ...)
        >>> db["table3"].head()
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: float
        long: float
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

        >>> import pyarrow as pa
        >>> def make_batches():
        ...     for i in range(5):
        ...         yield pa.RecordBatch.from_arrays(
        ...             [
        ...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
        ...                     pa.list_(pa.float32(), 2)),
        ...                 pa.array(["foo", "bar"]),
        ...                 pa.array([10.0, 20.0]),
        ...             ],
        ...             ["vector", "item", "price"],
        ...         )
        >>> schema=pa.schema([
        ...     pa.field("vector", pa.list_(pa.float32(), 2)),
        ...     pa.field("item", pa.utf8()),
        ...     pa.field("price", pa.float32()),
        ... ])
        >>> db.create_table("table4", make_batches(), schema=schema)
        LanceTable(name='table4', version=1, ...)

        """
        raise NotImplementedError

    def __getitem__(self, name: str) -> LanceTable:
        return self.open_table(name)

    def open_table(
        self,
        name: str,
        *,
        namespace: Optional[List[str]] = None,
        storage_options: Optional[Dict[str, str]] = None,
        storage_options_provider: Optional["StorageOptionsProvider"] = None,
        index_cache_size: Optional[int] = None,
    ) -> Table:
        """Open a Lance Table in the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], optional
            The namespace to open the table from.
            None or empty list represents root namespace.
        index_cache_size: int, default 256
            **Deprecated**: Use session-level cache configuration instead.
            Create a Session with custom cache sizes and pass it to lancedb.connect().

            Set the size of the index cache, specified as a number of entries

            The exact meaning of an "entry" will depend on the type of index:
            * IVF - there is one entry for each IVF partition
            * BTREE - there is one entry for the entire index

            This cache applies to the entire opened table, across all indices.
            Setting this value higher will increase performance on larger datasets
            at the expense of more RAM
        storage_options: dict, optional
            Additional options for the storage backend. Options already set on the
            connection will be inherited by the table, but can be overridden here.
            See available options at
            <https://lancedb.com/docs/storage/>

        Returns
        -------
        A LanceTable object representing the table.
        """
        raise NotImplementedError

    def drop_table(self, name: str, namespace: Optional[List[str]] = None):
        """Drop a table from the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], default []
            The namespace to drop the table from.
            Empty list represents root namespace.
        """
        if namespace is None:
            namespace = []
        raise NotImplementedError

    def rename_table(
        self,
        cur_name: str,
        new_name: str,
        cur_namespace: Optional[List[str]] = None,
        new_namespace: Optional[List[str]] = None,
    ):
        """Rename a table in the database.

        Parameters
        ----------
        cur_name: str
            The current name of the table.
        new_name: str
            The new name of the table.
        cur_namespace: List[str], optional
            The namespace of the current table.
            None or empty list represents root namespace.
        new_namespace: List[str], optional
            The namespace to move the table to.
            If not specified, defaults to the same as cur_namespace.
        """
        if cur_namespace is None:
            cur_namespace = []
        if new_namespace is None:
            new_namespace = []
        raise NotImplementedError

    def drop_database(self):
        """
        Drop database
        This is the same thing as dropping all the tables
        """
        raise NotImplementedError

    def drop_all_tables(self, namespace: Optional[List[str]] = None):
        """
        Drop all tables from the database

        Parameters
        ----------
        namespace: List[str], optional
            The namespace to drop all tables from.
            None or empty list represents root namespace.
        """
        if namespace is None:
            namespace = []
        raise NotImplementedError

    @property
    def uri(self) -> str:
        return self._uri

              

  

            list_namespaces

¶

list_namespaces(namespace: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListNamespacesResponse

    

      
List immediate child namespace names in the given namespace.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The parent namespace to list namespaces in.
Empty list represents root namespace.

          
        
        
- 
          `page_token`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Token for pagination. Use the token from a previous response
to get the next page of results.

          
        
        
- 
          `limit`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of results to return.

          
        
    

Returns:

    
        
- 
              `ListNamespacesResponse`
          –
          
            
Response containing namespace names and optional page_token for pagination.

          
        
    

            
              Source code in `lancedb/db.py`
              
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
def list_namespaces(
    self,
    namespace: Optional[List[str]] = None,
    page_token: Optional[str] = None,
    limit: Optional[int] = None,
) -> ListNamespacesResponse:
    """List immediate child namespace names in the given namespace.

    Parameters
    ----------
    namespace: List[str], default []
        The parent namespace to list namespaces in.
        Empty list represents root namespace.
    page_token: str, optional
        Token for pagination. Use the token from a previous response
        to get the next page of results.
    limit: int, optional
        The maximum number of results to return.

    Returns
    -------
    ListNamespacesResponse
        Response containing namespace names and optional page_token for pagination.
    """
    if namespace is None:
        namespace = []
    return ListNamespacesResponse(namespaces=[], page_token=None)

            
    

            create_namespace

¶

create_namespace(namespace: List[str], mode: Optional[str] = None, properties: Optional[Dict[str, str]] = None) -> CreateNamespaceResponse

    

      
Create a new namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to create.

          
        
        
- 
          `mode`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Creation mode - "create" (fail if exists), "exist_ok" (skip if exists),
or "overwrite" (replace if exists). Case insensitive.

          
        
        
- 
          `properties`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Properties to set on the namespace.

          
        
    

Returns:

    
        
- 
              `CreateNamespaceResponse`
          –
          
            
Response containing the properties of the created namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
def create_namespace(
    self,
    namespace: List[str],
    mode: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
) -> CreateNamespaceResponse:
    """Create a new namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to create.
    mode: str, optional
        Creation mode - "create" (fail if exists), "exist_ok" (skip if exists),
        or "overwrite" (replace if exists). Case insensitive.
    properties: Dict[str, str], optional
        Properties to set on the namespace.

    Returns
    -------
    CreateNamespaceResponse
        Response containing the properties of the created namespace.
    """
    raise NotImplementedError(
        "Namespace operations are not supported for this connection type"
    )

            
    

            drop_namespace

¶

drop_namespace(namespace: List[str], mode: Optional[str] = None, behavior: Optional[str] = None) -> DropNamespaceResponse

    

      
Drop a namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to drop.

          
        
        
- 
          `mode`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.

          
        
        
- 
          `behavior`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
Case insensitive.

          
        
    

Returns:

    
        
- 
              `DropNamespaceResponse`
          –
          
            
Response containing properties and transaction_id if applicable.

          
        
    

            
              Source code in `lancedb/db.py`
              
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
def drop_namespace(
    self,
    namespace: List[str],
    mode: Optional[str] = None,
    behavior: Optional[str] = None,
) -> DropNamespaceResponse:
    """Drop a namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to drop.
    mode: str, optional
        Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
    behavior: str, optional
        Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
        Case insensitive.

    Returns
    -------
    DropNamespaceResponse
        Response containing properties and transaction_id if applicable.
    """
    raise NotImplementedError(
        "Namespace operations are not supported for this connection type"
    )

            
    

            describe_namespace

¶

describe_namespace(namespace: List[str]) -> DescribeNamespaceResponse

    

      
Describe a namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to describe.

          
        
    

Returns:

    
        
- 
              `DescribeNamespaceResponse`
          –
          
            
Response containing the namespace properties.

          
        
    

            
              Source code in `lancedb/db.py`
              
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
def describe_namespace(self, namespace: List[str]) -> DescribeNamespaceResponse:
    """Describe a namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to describe.

    Returns
    -------
    DescribeNamespaceResponse
        Response containing the namespace properties.
    """
    raise NotImplementedError(
        "Namespace operations are not supported for this connection type"
    )

            
    

            list_tables

¶

list_tables(namespace: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListTablesResponse

    

      
List all tables in this database with pagination support.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to list tables in.
None or empty list represents root namespace.

          
        
        
- 
          `page_token`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Token for pagination. Use the token from a previous response
to get the next page of results.

          
        
        
- 
          `limit`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of results to return.

          
        
    

Returns:

    
        
- 
              `ListTablesResponse`
          –
          
            
Response containing table names and optional page_token for pagination.

          
        
    

            
              Source code in `lancedb/db.py`
              
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
def list_tables(
    self,
    namespace: Optional[List[str]] = None,
    page_token: Optional[str] = None,
    limit: Optional[int] = None,
) -> ListTablesResponse:
    """List all tables in this database with pagination support.

    Parameters
    ----------
    namespace: List[str], optional
        The namespace to list tables in.
        None or empty list represents root namespace.
    page_token: str, optional
        Token for pagination. Use the token from a previous response
        to get the next page of results.
    limit: int, optional
        The maximum number of results to return.

    Returns
    -------
    ListTablesResponse
        Response containing table names and optional page_token for pagination.
    """
    raise NotImplementedError(
        "list_tables is not supported for this connection type"
    )

            
    

            table_names

  
      `abstractmethod`
  

¶

table_names(page_token: Optional[str] = None, limit: int = 10, *, namespace: Optional[List[str]] = None) -> Iterable[str]

    

      
List all tables in this database, in sorted order

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to list tables in.
Empty list represents root namespace.

          
        
        
- 
          `page_token`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The token to use for pagination. If not present, start from the beginning.
Typically, this token is last table name from the previous page.

          
        
        
- 
          `limit`
              (`int`, default:
                  `10`
)
          –
          
            
The size of the page to return.

          
        
    

Returns:

    
        
- 
              `Iterable of str`
          –
          
            
          
        
    

            
              Source code in `lancedb/db.py`
              
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
@abstractmethod
def table_names(
    self,
    page_token: Optional[str] = None,
    limit: int = 10,
    *,
    namespace: Optional[List[str]] = None,
) -> Iterable[str]:
    """List all tables in this database, in sorted order

    Parameters
    ----------
    namespace: List[str], default []
        The namespace to list tables in.
        Empty list represents root namespace.
    page_token: str, optional
        The token to use for pagination. If not present, start from the beginning.
        Typically, this token is last table name from the previous page.
    limit: int, default 10
        The size of the page to return.

    Returns
    -------
    Iterable of str
    """
    pass

            
    

            create_table

  
      `abstractmethod`
  

¶

create_table(name: str, data: Optional[DATA] = None, schema: Optional[Union[Schema, LanceModel]] = None, mode: str = 'create', exist_ok: bool = False, on_bad_vectors: str = 'error', fill_value: float = 0.0, embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None, *, namespace: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, storage_options_provider: Optional['StorageOptionsProvider'] = None, data_storage_version: Optional[str] = None, enable_v2_manifest_paths: Optional[bool] = None) -> Table

    

      
Create a Table in the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to create the table in.
Empty list represents root namespace.

          
        
        
- 
          `data`
              (`Optional[DATA]`, default:
                  `None`
)
          –
          
            
User must provide at least one of `data` or `schema`.
Acceptable types are:

- 

list-of-dict

- 

pandas.DataFrame

- 

pyarrow.Table or pyarrow.RecordBatch

          
        
        
- 
          `schema`
              (`Optional[Union[Schema, LanceModel]]`, default:
                  `None`
)
          –
          
            
Acceptable types are:

- 

pyarrow.Schema

- 

LanceModel

          
        
        
- 
          `mode`
              (`str`, default:
                  `'create'`
)
          –
          
            
The mode to use when creating the table.
Can be either "create" or "overwrite".
By default, if the table already exists, an exception is raised.
If you want to overwrite the table, use mode="overwrite".

          
        
        
- 
          `exist_ok`
              (`bool`, default:
                  `False`
)
          –
          
            
If a table by the same name already exists, then raise an exception
if exist_ok=False. If exist_ok=True, then open the existing table;
it will not add the provided data but will validate against any
schema that's specified.

          
        
        
- 
          `on_bad_vectors`
              (`str`, default:
                  `'error'`
)
          –
          
            
What to do if any of the vectors are not the same size or contains NaNs.
One of "error", "drop", "fill".

          
        
        
- 
          `fill_value`
              (`float`, default:
                  `0.0`
)
          –
          
            
The value to use when filling vectors. Only used if on_bad_vectors="fill".

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. Options already set on the
connection will be inherited by the table, but can be overridden here.
See available options at
https://lancedb.com/docs/storage/

To enable stable row IDs (row IDs remain stable after compaction,
update, delete, and merges), set `new_table_enable_stable_row_ids`
to `"true"` in storage_options when connecting to the database.

          
        
        
- 
          `data_storage_version`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Deprecated.  Set `storage_options` when connecting to the database and set
`new_table_data_storage_version` in the options.

          
        
        
- 
          `enable_v2_manifest_paths`
              (`Optional[bool]`, default:
                  `None`
)
          –
          
            
Deprecated.  Set `storage_options` when connecting to the database and set
`new_table_enable_v2_manifest_paths` in the options.

          
        
    

Returns:

    
        
- 
              `LanceTable`
          –
          
            
A reference to the newly created table.

          
        
        
- 
              `!!! note`
          –
          
            
The vector index won't be created by default.
To create the index, call the `create_index` method on the table.

          
        
    

Examples:

    
Can create with list of tuples or dictionaries:

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
...         {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
>>> db.create_table("my_table", data)
LanceTable(name='my_table', version=1, ...)
>>> db["my_table"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
You can also pass a pandas DataFrame:

    
>>> import pandas as pd
>>> data = pd.DataFrame({
...    "vector": [[1.1, 1.2], [0.2, 1.8]],
...    "lat": [45.5, 40.1],
...    "long": [-122.7, -74.1]
... })
>>> db.create_table("table2", data)
LanceTable(name='table2', version=1, ...)
>>> db["table2"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
Data is converted to Arrow before being written to disk. For maximum
control over how data is saved, either provide the PyArrow schema to
convert to or else provide a PyArrow Table directly.

    
>>> import pyarrow as pa
>>> custom_schema = pa.schema([
...   pa.field("vector", pa.list_(pa.float32(), 2)),
...   pa.field("lat", pa.float32()),
...   pa.field("long", pa.float32())
... ])
>>> db.create_table("table3", data, schema = custom_schema)
LanceTable(name='table3', version=1, ...)
>>> db["table3"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: float
long: float
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

    
>>> import pyarrow as pa
>>> def make_batches():
...     for i in range(5):
...         yield pa.RecordBatch.from_arrays(
...             [
...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
...                     pa.list_(pa.float32(), 2)),
...                 pa.array(["foo", "bar"]),
...                 pa.array([10.0, 20.0]),
...             ],
...             ["vector", "item", "price"],
...         )
>>> schema=pa.schema([
...     pa.field("vector", pa.list_(pa.float32(), 2)),
...     pa.field("item", pa.utf8()),
...     pa.field("price", pa.float32()),
... ])
>>> db.create_table("table4", make_batches(), schema=schema)
LanceTable(name='table4', version=1, ...)

            
              Source code in `lancedb/db.py`
              
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
@abstractmethod
def create_table(
    self,
    name: str,
    data: Optional[DATA] = None,
    schema: Optional[Union[pa.Schema, LanceModel]] = None,
    mode: str = "create",
    exist_ok: bool = False,
    on_bad_vectors: str = "error",
    fill_value: float = 0.0,
    embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None,
    *,
    namespace: Optional[List[str]] = None,
    storage_options: Optional[Dict[str, str]] = None,
    storage_options_provider: Optional["StorageOptionsProvider"] = None,
    data_storage_version: Optional[str] = None,
    enable_v2_manifest_paths: Optional[bool] = None,
) -> Table:
    """Create a [Table][lancedb.table.Table] in the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], default []
        The namespace to create the table in.
        Empty list represents root namespace.
    data: The data to initialize the table, *optional*
        User must provide at least one of `data` or `schema`.
        Acceptable types are:

        - list-of-dict

        - pandas.DataFrame

        - pyarrow.Table or pyarrow.RecordBatch
    schema: The schema of the table, *optional*
        Acceptable types are:

        - pyarrow.Schema

        - [LanceModel][lancedb.pydantic.LanceModel]
    mode: str; default "create"
        The mode to use when creating the table.
        Can be either "create" or "overwrite".
        By default, if the table already exists, an exception is raised.
        If you want to overwrite the table, use mode="overwrite".
    exist_ok: bool, default False
        If a table by the same name already exists, then raise an exception
        if exist_ok=False. If exist_ok=True, then open the existing table;
        it will not add the provided data but will validate against any
        schema that's specified.
    on_bad_vectors: str, default "error"
        What to do if any of the vectors are not the same size or contains NaNs.
        One of "error", "drop", "fill".
    fill_value: float
        The value to use when filling vectors. Only used if on_bad_vectors="fill".
    storage_options: dict, optional
        Additional options for the storage backend. Options already set on the
        connection will be inherited by the table, but can be overridden here.
        See available options at
        <https://lancedb.com/docs/storage/>

        To enable stable row IDs (row IDs remain stable after compaction,
        update, delete, and merges), set `new_table_enable_stable_row_ids`
        to `"true"` in storage_options when connecting to the database.
    data_storage_version: optional, str, default "stable"
        Deprecated.  Set `storage_options` when connecting to the database and set
        `new_table_data_storage_version` in the options.
    enable_v2_manifest_paths: optional, bool, default False
        Deprecated.  Set `storage_options` when connecting to the database and set
        `new_table_enable_v2_manifest_paths` in the options.
    Returns
    -------
    LanceTable
        A reference to the newly created table.

    !!! note

        The vector index won't be created by default.
        To create the index, call the `create_index` method on the table.

    Examples
    --------

    Can create with list of tuples or dictionaries:

    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
    ...         {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
    >>> db.create_table("my_table", data)
    LanceTable(name='my_table', version=1, ...)
    >>> db["my_table"].head()
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: double
    long: double
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    You can also pass a pandas DataFrame:

    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...    "vector": [[1.1, 1.2], [0.2, 1.8]],
    ...    "lat": [45.5, 40.1],
    ...    "long": [-122.7, -74.1]
    ... })
    >>> db.create_table("table2", data)
    LanceTable(name='table2', version=1, ...)
    >>> db["table2"].head()
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: double
    long: double
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    Data is converted to Arrow before being written to disk. For maximum
    control over how data is saved, either provide the PyArrow schema to
    convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

    >>> import pyarrow as pa
    >>> custom_schema = pa.schema([
    ...   pa.field("vector", pa.list_(pa.float32(), 2)),
    ...   pa.field("lat", pa.float32()),
    ...   pa.field("long", pa.float32())
    ... ])
    >>> db.create_table("table3", data, schema = custom_schema)
    LanceTable(name='table3', version=1, ...)
    >>> db["table3"].head()
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: float
    long: float
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

    >>> import pyarrow as pa
    >>> def make_batches():
    ...     for i in range(5):
    ...         yield pa.RecordBatch.from_arrays(
    ...             [
    ...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
    ...                     pa.list_(pa.float32(), 2)),
    ...                 pa.array(["foo", "bar"]),
    ...                 pa.array([10.0, 20.0]),
    ...             ],
    ...             ["vector", "item", "price"],
    ...         )
    >>> schema=pa.schema([
    ...     pa.field("vector", pa.list_(pa.float32(), 2)),
    ...     pa.field("item", pa.utf8()),
    ...     pa.field("price", pa.float32()),
    ... ])
    >>> db.create_table("table4", make_batches(), schema=schema)
    LanceTable(name='table4', version=1, ...)

    """
    raise NotImplementedError

            
    

            open_table

¶

open_table(name: str, *, namespace: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, storage_options_provider: Optional['StorageOptionsProvider'] = None, index_cache_size: Optional[int] = None) -> Table

    

      
Open a Lance Table in the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to open the table from.
None or empty list represents root namespace.

          
        
        
- 
          `index_cache_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
Deprecated: Use session-level cache configuration instead.
Create a Session with custom cache sizes and pass it to lancedb.connect().

Set the size of the index cache, specified as a number of entries

The exact meaning of an "entry" will depend on the type of index:
* IVF - there is one entry for each IVF partition
* BTREE - there is one entry for the entire index

This cache applies to the entire opened table, across all indices.
Setting this value higher will increase performance on larger datasets
at the expense of more RAM

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. Options already set on the
connection will be inherited by the table, but can be overridden here.
See available options at
https://lancedb.com/docs/storage/

          
        
    

Returns:

    
        
- 
              `A LanceTable object representing the table.`
          –
          
            
          
        
    

            
              Source code in `lancedb/db.py`
              
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
def open_table(
    self,
    name: str,
    *,
    namespace: Optional[List[str]] = None,
    storage_options: Optional[Dict[str, str]] = None,
    storage_options_provider: Optional["StorageOptionsProvider"] = None,
    index_cache_size: Optional[int] = None,
) -> Table:
    """Open a Lance Table in the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], optional
        The namespace to open the table from.
        None or empty list represents root namespace.
    index_cache_size: int, default 256
        **Deprecated**: Use session-level cache configuration instead.
        Create a Session with custom cache sizes and pass it to lancedb.connect().

        Set the size of the index cache, specified as a number of entries

        The exact meaning of an "entry" will depend on the type of index:
        * IVF - there is one entry for each IVF partition
        * BTREE - there is one entry for the entire index

        This cache applies to the entire opened table, across all indices.
        Setting this value higher will increase performance on larger datasets
        at the expense of more RAM
    storage_options: dict, optional
        Additional options for the storage backend. Options already set on the
        connection will be inherited by the table, but can be overridden here.
        See available options at
        <https://lancedb.com/docs/storage/>

    Returns
    -------
    A LanceTable object representing the table.
    """
    raise NotImplementedError

            
    

            drop_table

¶

drop_table(name: str, namespace: Optional[List[str]] = None)

    

      
Drop a table from the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to drop the table from.
Empty list represents root namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
443
444
445
446
447
448
449
450
451
452
453
454
455
456
def drop_table(self, name: str, namespace: Optional[List[str]] = None):
    """Drop a table from the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], default []
        The namespace to drop the table from.
        Empty list represents root namespace.
    """
    if namespace is None:
        namespace = []
    raise NotImplementedError

            
    

            rename_table

¶

rename_table(cur_name: str, new_name: str, cur_namespace: Optional[List[str]] = None, new_namespace: Optional[List[str]] = None)

    

      
Rename a table in the database.

Parameters:

    
        
- 
          `cur_name`
              (`str`)
          –
          
            
The current name of the table.

          
        
        
- 
          `new_name`
              (`str`)
          –
          
            
The new name of the table.

          
        
        
- 
          `cur_namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace of the current table.
None or empty list represents root namespace.

          
        
        
- 
          `new_namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to move the table to.
If not specified, defaults to the same as cur_namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
def rename_table(
    self,
    cur_name: str,
    new_name: str,
    cur_namespace: Optional[List[str]] = None,
    new_namespace: Optional[List[str]] = None,
):
    """Rename a table in the database.

    Parameters
    ----------
    cur_name: str
        The current name of the table.
    new_name: str
        The new name of the table.
    cur_namespace: List[str], optional
        The namespace of the current table.
        None or empty list represents root namespace.
    new_namespace: List[str], optional
        The namespace to move the table to.
        If not specified, defaults to the same as cur_namespace.
    """
    if cur_namespace is None:
        cur_namespace = []
    if new_namespace is None:
        new_namespace = []
    raise NotImplementedError

            
    

            drop_database

¶

drop_database()

    

      
Drop database
This is the same thing as dropping all the tables

            
              Source code in `lancedb/db.py`
              
486
487
488
489
490
491
def drop_database(self):
    """
    Drop database
    This is the same thing as dropping all the tables
    """
    raise NotImplementedError

            
    

            drop_all_tables

¶

drop_all_tables(namespace: Optional[List[str]] = None)

    

      
Drop all tables from the database

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to drop all tables from.
None or empty list represents root namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
493
494
495
496
497
498
499
500
501
502
503
504
505
def drop_all_tables(self, namespace: Optional[List[str]] = None):
    """
    Drop all tables from the database

    Parameters
    ----------
    namespace: List[str], optional
        The namespace to drop all tables from.
        None or empty list represents root namespace.
    """
    if namespace is None:
        namespace = []
    raise NotImplementedError

            
    

  

    

## Tables (Synchronous)¶

            lancedb.table.Table

¶

    
            

              Bases: `ABC`

      
A Table is a collection of Records in a LanceDB Database.

Examples:

    
Create using DBConnection.create_table
(more examples in that method's documentation).

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data=[{"vector": [1.1, 1.2], "b": 2}])
>>> table.head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
b: int64
----
vector: [[[1.1,1.2]]]
b: [[2]]

    
Can append new data with Table.add().

    
>>> table.add([{"vector": [0.5, 1.3], "b": 4}])
AddResult(version=2)

    
Can query the table with Table.search.

    
>>> table.search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
   b      vector  _distance
0  4  [0.5, 1.3]       0.82
1  2  [1.1, 1.2]       1.13

    
Search queries are much faster when an index is created. See
Table.create_index.

              
                Source code in `lancedb/table.py`
                
 557
 558
 559
 560
 561
 562
 563
 564
 565
 566
 567
 568
 569
 570
 571
 572
 573
 574
 575
 576
 577
 578
 579
 580
 581
 582
 583
 584
 585
 586
 587
 588
 589
 590
 591
 592
 593
 594
 595
 596
 597
 598
 599
 600
 601
 602
 603
 604
 605
 606
 607
 608
 609
 610
 611
 612
 613
 614
 615
 616
 617
 618
 619
 620
 621
 622
 623
 624
 625
 626
 627
 628
 629
 630
 631
 632
 633
 634
 635
 636
 637
 638
 639
 640
 641
 642
 643
 644
 645
 646
 647
 648
 649
 650
 651
 652
 653
 654
 655
 656
 657
 658
 659
 660
 661
 662
 663
 664
 665
 666
 667
 668
 669
 670
 671
 672
 673
 674
 675
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
1672
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
class Table(ABC):
    """
    A Table is a collection of Records in a LanceDB Database.

    Examples
    --------

    Create using [DBConnection.create_table][lancedb.DBConnection.create_table]
    (more examples in that method's documentation).

    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data=[{"vector": [1.1, 1.2], "b": 2}])
    >>> table.head()
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    b: int64
    ----
    vector: [[[1.1,1.2]]]
    b: [[2]]

    Can append new data with [Table.add()][lancedb.table.Table.add].

    >>> table.add([{"vector": [0.5, 1.3], "b": 4}])
    AddResult(version=2)

    Can query the table with [Table.search][lancedb.table.Table.search].

    >>> table.search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
       b      vector  _distance
    0  4  [0.5, 1.3]       0.82
    1  2  [1.1, 1.2]       1.13

    Search queries are much faster when an index is created. See
    [Table.create_index][lancedb.table.Table.create_index].
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of this Table"""
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> int:
        """The version of this Table"""
        raise NotImplementedError

    @property
    @abstractmethod
    def schema(self) -> pa.Schema:
        """The [Arrow Schema](https://arrow.apache.org/docs/python/api/datatypes.html#)
        of this Table

        """
        raise NotImplementedError

    @property
    @abstractmethod
    def tags(self) -> Tags:
        """Tag management for the table.

        Similar to Git, tags are a way to add metadata to a specific version of the
        table.

        .. warning::

            Tagged versions are exempted from the :py:meth:`cleanup_old_versions()`
            process.

            To remove a version that has been tagged, you must first
            :py:meth:`~Tags.delete` the associated tag.

        Examples
        --------

        .. code-block:: python

            table = db.open_table("my_table")
            table.tags.create("v2-prod-20250203", 10)

            tags = table.tags.list()

        """
        raise NotImplementedError

    def __len__(self) -> int:
        """The number of rows in this Table"""
        return self.count_rows(None)

    @property
    @abstractmethod
    def embedding_functions(self) -> Dict[str, EmbeddingFunctionConfig]:
        """
        Get a mapping from vector column name to it's configured embedding function.
        """

    @abstractmethod
    def count_rows(self, filter: Optional[str] = None) -> int:
        """
        Count the number of rows in the table.

        Parameters
        ----------
        filter: str, optional
            A SQL where clause to filter the rows to count.
        """
        raise NotImplementedError

    def to_pandas(self) -> "pandas.DataFrame":
        """Return the table as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
        """
        return self.to_arrow().to_pandas()

    @abstractmethod
    def to_arrow(self) -> pa.Table:
        """Return the table as a pyarrow Table.

        Returns
        -------
        pa.Table
        """
        raise NotImplementedError

    def to_lance(self, **kwargs) -> lance.LanceDataset:
        """Return the table as a lance.LanceDataset.

        Returns
        -------
        lance.LanceDataset
        """
        raise NotImplementedError

    def to_polars(self, **kwargs) -> "pl.DataFrame":
        """Return the table as a polars.DataFrame.

        Returns
        -------
        polars.DataFrame
        """
        raise NotImplementedError

    def create_index(
        self,
        metric="l2",
        num_partitions=256,
        num_sub_vectors=96,
        vector_column_name: str = VECTOR_COLUMN_NAME,
        replace: bool = True,
        accelerator: Optional[str] = None,
        index_cache_size: Optional[int] = None,
        *,
        index_type: VectorIndexType = "IVF_PQ",
        wait_timeout: Optional[timedelta] = None,
        num_bits: int = 8,
        max_iterations: int = 50,
        sample_rate: int = 256,
        m: int = 20,
        ef_construction: int = 300,
        name: Optional[str] = None,
        train: bool = True,
        target_partition_size: Optional[int] = None,
    ):
        """Create an index on the table.

        Parameters
        ----------
        metric: str, default "l2"
            The distance metric to use when creating the index.
            Valid values are "l2", "cosine", "dot", or "hamming".
            l2 is euclidean distance.
            Hamming is available only for binary vectors.
        num_partitions: int, default 256
            The number of IVF partitions to use when creating the index.
            Default is 256.
        num_sub_vectors: int, default 96
            The number of PQ sub-vectors to use when creating the index.
            Default is 96.
        vector_column_name: str, default "vector"
            The vector column name to create the index.
        replace: bool, default True
            - If True, replace the existing index if it exists.

            - If False, raise an error if duplicate index exists.
        accelerator: str, default None
            If set, use the given accelerator to create the index.
            Only support "cuda" for now.
        index_cache_size : int, optional
            The size of the index cache in number of entries. Default value is 256.
        num_bits: int
            The number of bits to encode sub-vectors. Only used with the IVF_PQ index.
            Only 4 and 8 are supported.
        wait_timeout: timedelta, optional
            The timeout to wait if indexing is asynchronous.
        name: str, optional
            The name of the index. If not provided, a default name will be generated.
        train: bool, default True
            Whether to train the index with existing data. Vector indices always train
            with existing data.
        """
        raise NotImplementedError

    def drop_index(self, name: str) -> None:
        """
        Drop an index from the table.

        Parameters
        ----------
        name: str
            The name of the index to drop.

        Notes
        -----
        This does not delete the index from disk, it just removes it from the table.
        To delete the index, run [optimize][lancedb.table.Table.optimize]
        after dropping the index.

        Use [list_indices][lancedb.table.Table.list_indices] to find the names of
        the indices.
        """
        raise NotImplementedError

    def wait_for_index(
        self, index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)
    ) -> None:
        """
        Wait for indexing to complete for the given index names.
        This will poll the table until all the indices are fully indexed,
        or raise a timeout exception if the timeout is reached.

        Parameters
        ----------
        index_names: str
            The name of the indices to poll
        timeout: timedelta
            Timeout to wait for asynchronous indexing. The default is 5 minutes.
        """
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> TableStatistics:
        """
        Retrieve table and fragment statistics.
        """
        raise NotImplementedError

    @abstractmethod
    def create_scalar_index(
        self,
        column: str,
        *,
        replace: bool = True,
        index_type: ScalarIndexType = "BTREE",
        wait_timeout: Optional[timedelta] = None,
        name: Optional[str] = None,
    ):
        """Create a scalar index on a column.

        Parameters
        ----------
        column : str
            The column to be indexed.  Must be a boolean, integer, float,
            or string column.
        replace : bool, default True
            Replace the existing index if it exists.
        index_type: Literal["BTREE", "BITMAP", "LABEL_LIST"], default "BTREE"
            The type of index to create.
        wait_timeout: timedelta, optional
            The timeout to wait if indexing is asynchronous.
        name: str, optional
            The name of the index. If not provided, a default name will be generated.
        Examples
        --------

        Scalar indices, like vector indices, can be used to speed up scans.  A scalar
        index can speed up scans that contain filter expressions on the indexed column.
        For example, the following scan will be faster if the column ``my_col`` has
        a scalar index:

        >>> import lancedb # doctest: +SKIP
        >>> db = lancedb.connect("/data/lance") # doctest: +SKIP
        >>> img_table = db.open_table("images") # doctest: +SKIP
        >>> my_df = img_table.search().where("my_col = 7", # doctest: +SKIP
        ...                                  prefilter=True).to_pandas()

        Scalar indices can also speed up scans containing a vector search and a
        prefilter:

        >>> import lancedb # doctest: +SKIP
        >>> db = lancedb.connect("/data/lance") # doctest: +SKIP
        >>> img_table = db.open_table("images") # doctest: +SKIP
        >>> img_table.search([1, 2, 3, 4], vector_column_name="vector") # doctest: +SKIP
        ...     .where("my_col != 7", prefilter=True)
        ...     .to_pandas()

        Scalar indices can only speed up scans for basic filters using
        equality, comparison, range (e.g. ``my_col BETWEEN 0 AND 100``), and set
        membership (e.g. `my_col IN (0, 1, 2)`)

        Scalar indices can be used if the filter contains multiple indexed columns and
        the filter criteria are AND'd or OR'd together
        (e.g. ``my_col < 0 AND other_col> 100``)

        Scalar indices may be used if the filter contains non-indexed columns but,
        depending on the structure of the filter, they may not be usable.  For example,
        if the column ``not_indexed`` does not have a scalar index then the filter
        ``my_col = 0 OR not_indexed = 1`` will not be able to use any scalar index on
        ``my_col``.
        """
        raise NotImplementedError

    def create_fts_index(
        self,
        field_names: Union[str, List[str]],
        *,
        ordering_field_names: Optional[Union[str, List[str]]] = None,
        replace: bool = False,
        writer_heap_size: Optional[int] = 1024 * 1024 * 1024,
        use_tantivy: bool = False,
        tokenizer_name: Optional[str] = None,
        with_position: bool = False,
        # tokenizer configs:
        base_tokenizer: BaseTokenizerType = "simple",
        language: str = "English",
        max_token_length: Optional[int] = 40,
        lower_case: bool = True,
        stem: bool = True,
        remove_stop_words: bool = True,
        ascii_folding: bool = True,
        ngram_min_length: int = 3,
        ngram_max_length: int = 3,
        prefix_only: bool = False,
        wait_timeout: Optional[timedelta] = None,
        name: Optional[str] = None,
    ):
        """Create a full-text search index on the table.

        Warning - this API is highly experimental and is highly likely to change
        in the future.

        Parameters
        ----------
        field_names: str or list of str
            The name(s) of the field to index.
            If ``use_tantivy`` is False (default), only a single field name
            (str) is supported. To index multiple fields, create a separate
            FTS index for each field.
        replace: bool, default False
            If True, replace the existing index if it exists. Note that this is
            not yet an atomic operation; the index will be temporarily
            unavailable while the new index is being created.
        writer_heap_size: int, default 1GB
            Only available with use_tantivy=True
        ordering_field_names:
            A list of unsigned type fields to index to optionally order
            results on at search time.
            only available with use_tantivy=True
        tokenizer_name: str, default "default"
            The tokenizer to use for the index. Can be "raw", "default" or the 2 letter
            language code followed by "_stem". So for english it would be "en_stem".
            For available languages see: https://docs.rs/tantivy/latest/tantivy/tokenizer/enum.Language.html
        use_tantivy: bool, default False
            If True, use the legacy full-text search implementation based on tantivy.
            If False, use the new full-text search implementation based on lance-index.
        with_position: bool, default False
            Only available with use_tantivy=False
            If False, do not store the positions of the terms in the text.
            This can reduce the size of the index and improve indexing speed.
            But it will raise an exception for phrase queries.
        base_tokenizer : str, default "simple"
            The base tokenizer to use for tokenization. Options are:
            - "simple": Splits text by whitespace and punctuation.
            - "whitespace": Split text by whitespace, but not punctuation.
            - "raw": No tokenization. The entire text is treated as a single token.
            - "ngram": N-Gram tokenizer.
        language : str, default "English"
            The language to use for tokenization.
        max_token_length : int, default 40
            The maximum token length to index. Tokens longer than this length will be
            ignored.
        lower_case : bool, default True
            Whether to convert the token to lower case. This makes queries
            case-insensitive.
        stem : bool, default True
            Whether to stem the token. Stemming reduces words to their root form.
            For example, in English "running" and "runs" would both be reduced to "run".
        remove_stop_words : bool, default True
            Whether to remove stop words. Stop words are common words that are often
            removed from text before indexing. For example, in English "the" and "and".
        ascii_folding : bool, default True
            Whether to fold ASCII characters. This converts accented characters to
            their ASCII equivalent. For example, "café" would be converted to "cafe".
        ngram_min_length: int, default 3
            The minimum length of an n-gram.
        ngram_max_length: int, default 3
            The maximum length of an n-gram.
        prefix_only: bool, default False
            Whether to only index the prefix of the token for ngram tokenizer.
        wait_timeout: timedelta, optional
            The timeout to wait if indexing is asynchronous.
        name: str, optional
            The name of the index. If not provided, a default name will be generated.
        """
        raise NotImplementedError

    @abstractmethod
    def add(
        self,
        data: DATA,
        mode: AddMode = "append",
        on_bad_vectors: OnBadVectorsType = "error",
        fill_value: float = 0.0,
    ) -> AddResult:
        """Add more data to the [Table](Table).

        Parameters
        ----------
        data: DATA
            The data to insert into the table. Acceptable types are:

            - list-of-dict

            - pandas.DataFrame

            - pyarrow.Table or pyarrow.RecordBatch
        mode: str
            The mode to use when writing the data. Valid values are
            "append" and "overwrite".
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contains NaNs.
            One of "error", "drop", "fill".
        fill_value: float, default 0.
            The value to use when filling vectors. Only used if on_bad_vectors="fill".

        Returns
        -------
        AddResult
            An object containing the new version number of the table after adding data.
        """
        raise NotImplementedError

    def merge_insert(self, on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder:
        """
        Returns a [`LanceMergeInsertBuilder`][lancedb.merge.LanceMergeInsertBuilder]
        that can be used to create a "merge insert" operation

        This operation can add rows, update rows, and remove rows all in a single
        transaction. It is a very generic tool that can be used to create
        behaviors like "insert if not exists", "update or insert (i.e. upsert)",
        or even replace a portion of existing data with new data (e.g. replace
        all data where month="january")

        The merge insert operation works by combining new data from a
        **source table** with existing data in a **target table** by using a
        join.  There are three categories of records.

        "Matched" records are records that exist in both the source table and
        the target table. "Not matched" records exist only in the source table
        (e.g. these are new data) "Not matched by source" records exist only
        in the target table (this is old data)

        The builder returned by this method can be used to customize what
        should happen for each category of data.

        Please note that the data may appear to be reordered as part of this
        operation.  This is because updated rows will be deleted from the
        dataset and then reinserted at the end with the new values.

        Parameters
        ----------

        on: Union[str, Iterable[str]]
            A column (or columns) to join on.  This is how records from the
            source table and target table are matched.  Typically this is some
            kind of key or id column.

        Examples
        --------
        >>> import lancedb
        >>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", data)
        >>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
        >>> # Perform a "upsert" operation
        >>> res = table.merge_insert("a")     \\
        ...      .when_matched_update_all()     \\
        ...      .when_not_matched_insert_all() \\
        ...      .execute(new_data)
        >>> res
        MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
        >>> # The order of new rows is non-deterministic since we use
        >>> # a hash-join as part of this operation and so we sort here
        >>> table.to_arrow().sort_by("a").to_pandas()
           a  b
        0  1  b
        1  2  x
        2  3  y
        3  4  z
        """  # noqa: E501
        on = [on] if isinstance(on, str) else list(iter(on))

        return LanceMergeInsertBuilder(self, on)

    @abstractmethod
    def search(
        self,
        query: Optional[
            Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]
        ] = None,
        vector_column_name: Optional[str] = None,
        query_type: QueryType = "auto",
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> LanceQueryBuilder:
        """Create a search query to find the nearest neighbors
        of the given query vector. We currently support [vector search][search]
        and [full-text search][experimental-full-text-search].

        All query options are defined in
        [LanceQueryBuilder][lancedb.query.LanceQueryBuilder].

        Examples
        --------
        >>> import lancedb
        >>> db = lancedb.connect("./.lancedb")
        >>> data = [
        ...    {"original_width": 100, "caption": "bar", "vector": [0.1, 2.3, 4.5]},
        ...    {"original_width": 2000, "caption": "foo",  "vector": [0.5, 3.4, 1.3]},
        ...    {"original_width": 3000, "caption": "test", "vector": [0.3, 6.2, 2.6]}
        ... ]
        >>> table = db.create_table("my_table", data)
        >>> query = [0.4, 1.4, 2.4]
        >>> (table.search(query)
        ...     .where("original_width > 1000", prefilter=True)
        ...     .select(["caption", "original_width", "vector"])
        ...     .limit(2)
        ...     .to_pandas())
          caption  original_width           vector  _distance
        0     foo            2000  [0.5, 3.4, 1.3]   5.220000
        1    test            3000  [0.3, 6.2, 2.6]  23.089996

        Parameters
        ----------
        query: list/np.ndarray/str/PIL.Image.Image, default None
            The targetted vector to search for.

            - *default None*.
            Acceptable types are: list, np.ndarray, PIL.Image.Image

            - If None then the select/where/limit clauses are applied to filter
            the table
        vector_column_name: str, optional
            The name of the vector column to search.

            The vector column needs to be a pyarrow fixed size list type

            - If not specified then the vector column is inferred from
            the table schema

            - If the table has multiple vector columns then the *vector_column_name*
            needs to be specified. Otherwise, an error is raised.
        query_type: str
            *default "auto"*.
            Acceptable types are: "vector", "fts", "hybrid", or "auto"

            - If "auto" then the query type is inferred from the query;

                - If `query` is a list/np.ndarray then the query type is
                "vector";

                - If `query` is a PIL.Image.Image then either do vector search,
                or raise an error if no corresponding embedding function is found.

            - If `query` is a string, then the query type is "vector" if the
            table has embedding functions else the query type is "fts"

        Returns
        -------
        LanceQueryBuilder
            A query builder object representing the query.
            Once executed, the query returns

            - selected columns

            - the vector

            - and also the "_distance" column which is the distance between the query
            vector and the returned vector.
        """
        raise NotImplementedError

    @abstractmethod
    def take_offsets(
        self, offsets: list[int], *, with_row_id: bool = False
    ) -> LanceTakeQueryBuilder:
        """
        Take a list of offsets from the table.

        Offsets are 0-indexed and relative to the current version of the table.  Offsets
        are not stable.  A row with an offset of N may have a different offset in a
        different version of the table (e.g. if an earlier row is deleted).

        Offsets are mostly useful for sampling as the set of all valid offsets is easily
        known in advance to be [0, len(table)).

        No guarantees are made regarding the order in which results are returned.  If
        you desire an output order that matches the order of the given offsets, you will
        need to add the row offset column to the output and align it yourself.

        Parameters
        ----------
        offsets: list[int]
            The offsets to take.

        Returns
        -------
        pa.RecordBatch
            A record batch containing the rows at the given offsets.
        """

    def __getitems__(self, offsets: list[int]) -> pa.RecordBatch:
        """
        Take a list of offsets from the table and return as a record batch.

        This method uses the `take_offsets` method to take the rows.  However, it
        aligns the offsets to the passed in offsets.  This means the return type
        is a record batch (and so users should take care not to pass in too many
        offsets)

        Note: this method is primarily intended to fulfill the Dataset contract
        for pytorch.

        Parameters
        ----------
        offsets: list[int]
            The offsets to take.

        Returns
        -------
        pa.RecordBatch
            A record batch containing the rows at the given offsets.
        """
        # We don't know the order of the results at all.  So we calculate a permutation
        # for ordering the given offsets.  Then we load the data with the _rowoffset
        # column.  Then we sort by _rowoffset and apply the inverse of the permutation
        # that we calculated.
        #
        # Note: this is potentially a lot of memory copy if we're operating on large
        # batches :(
        num_offsets = len(offsets)
        indices = list(range(num_offsets))
        permutation = sorted(indices, key=lambda idx: offsets[idx])
        permutation_inv = [0] * num_offsets
        for i in range(num_offsets):
            permutation_inv[permutation[i]] = i

        columns = self.schema.names
        columns.append("_rowoffset")
        tbl = (
            self.take_offsets(offsets)
            .select(columns)
            .to_arrow()
            .sort_by("_rowoffset")
            .take(permutation_inv)
            .combine_chunks()
            .drop_columns(["_rowoffset"])
        )

        return tbl

    @abstractmethod
    def take_row_ids(
        self, row_ids: list[int], *, with_row_id: bool = False
    ) -> LanceTakeQueryBuilder:
        """
        Take a list of row ids from the table.

        Row ids are not stable and are relative to the current version of the table.
        They can change due to compaction and updates.

        No guarantees are made regarding the order in which results are returned.  If
        you desire an output order that matches the order of the given ids, you will
        need to add the row id column to the output and align it yourself.

        Unlike offsets, row ids are not 0-indexed and no assumptions should be made
        about the possible range of row ids.  In order to use this method you must
        first obtain the row ids by scanning or searching the table.

        Even so, row ids are more stable than offsets and can be useful in some
        situations.

        There is an ongoing effort to make row ids stable which is tracked at
        https://github.com/lancedb/lancedb/issues/1120

        Parameters
        ----------
        row_ids: list[int]
            The row ids to take.

        Returns
        -------
        AsyncTakeQuery
            A query object that can be executed to get the rows.
        """

    @abstractmethod
    def _execute_query(
        self,
        query: Query,
        *,
        batch_size: Optional[int] = None,
        timeout: Optional[timedelta] = None,
    ) -> pa.RecordBatchReader: ...

    @abstractmethod
    def _explain_plan(self, query: Query, verbose: Optional[bool] = False) -> str: ...

    @abstractmethod
    def _analyze_plan(self, query: Query) -> str: ...

    @abstractmethod
    def _output_schema(self, query: Query) -> pa.Schema: ...

    @abstractmethod
    def _do_merge(
        self,
        merge: LanceMergeInsertBuilder,
        new_data: DATA,
        on_bad_vectors: OnBadVectorsType,
        fill_value: float,
    ) -> MergeResult: ...

    @abstractmethod
    def delete(self, where: str) -> DeleteResult:
        """Delete rows from the table.

        This can be used to delete a single row, many rows, all rows, or
        sometimes no rows (if your predicate matches nothing).

        Parameters
        ----------
        where: str
            The SQL where clause to use when deleting rows.

            - For example, 'x = 2' or 'x IN (1, 2, 3)'.

            The filter must not be empty, or it will error.

        Returns
        -------
        DeleteResult
            An object containing the new version number of the table after deletion.

        Examples
        --------
        >>> import lancedb
        >>> data = [
        ...    {"x": 1, "vector": [1.0, 2]},
        ...    {"x": 2, "vector": [3.0, 4]},
        ...    {"x": 3, "vector": [5.0, 6]}
        ... ]
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", data)
        >>> table.to_pandas()
           x      vector
        0  1  [1.0, 2.0]
        1  2  [3.0, 4.0]
        2  3  [5.0, 6.0]
        >>> table.delete("x = 2")
        DeleteResult(version=2)
        >>> table.to_pandas()
           x      vector
        0  1  [1.0, 2.0]
        1  3  [5.0, 6.0]

        If you have a list of values to delete, you can combine them into a
        stringified list and use the `IN` operator:

        >>> to_remove = [1, 5]
        >>> to_remove = ", ".join([str(v) for v in to_remove])
        >>> to_remove
        '1, 5'
        >>> table.delete(f"x IN ({to_remove})")
        DeleteResult(version=3)
        >>> table.to_pandas()
           x      vector
        0  3  [5.0, 6.0]
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        where: Optional[str] = None,
        values: Optional[dict] = None,
        *,
        values_sql: Optional[Dict[str, str]] = None,
    ) -> UpdateResult:
        """
        This can be used to update zero to all rows depending on how many
        rows match the where clause. If no where clause is provided, then
        all rows will be updated.

        Either `values` or `values_sql` must be provided. You cannot provide
        both.

        Parameters
        ----------
        where: str, optional
            The SQL where clause to use when updating rows. For example, 'x = 2'
            or 'x IN (1, 2, 3)'. The filter must not be empty, or it will error.
        values: dict, optional
            The values to update. The keys are the column names and the values
            are the values to set.
        values_sql: dict, optional
            The values to update, expressed as SQL expression strings. These can
            reference existing columns. For example, {"x": "x + 1"} will increment
            the x column by 1.

        Returns
        -------
        UpdateResult
            - rows_updated: The number of rows that were updated
            - version: The new version number of the table after the update

        Examples
        --------
        >>> import lancedb
        >>> import pandas as pd
        >>> data = pd.DataFrame({"x": [1, 2, 3], "vector": [[1.0, 2], [3, 4], [5, 6]]})
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", data)
        >>> table.to_pandas()
           x      vector
        0  1  [1.0, 2.0]
        1  2  [3.0, 4.0]
        2  3  [5.0, 6.0]
        >>> table.update(where="x = 2", values={"vector": [10.0, 10]})
        UpdateResult(rows_updated=1, version=2)
        >>> table.to_pandas()
           x        vector
        0  1    [1.0, 2.0]
        1  3    [5.0, 6.0]
        2  2  [10.0, 10.0]
        >>> table.update(values_sql={"x": "x + 1"})
        UpdateResult(rows_updated=3, version=3)
        >>> table.to_pandas()
           x        vector
        0  2    [1.0, 2.0]
        1  4    [5.0, 6.0]
        2  3  [10.0, 10.0]
        """
        raise NotImplementedError

    @abstractmethod
    def cleanup_old_versions(
        self,
        older_than: Optional[timedelta] = None,
        *,
        delete_unverified: bool = False,
    ) -> "CleanupStats":
        """
        Clean up old versions of the table, freeing disk space.

        Parameters
        ----------
        older_than: timedelta, default None
            The minimum age of the version to delete. If None, then this defaults
            to two weeks.
        delete_unverified: bool, default False
            Because they may be part of an in-progress transaction, files newer
            than 7 days old are not deleted by default. If you are sure that
            there are no in-progress transactions, then you can set this to True
            to delete all files older than `older_than`.

        Returns
        -------
        CleanupStats
            The stats of the cleanup operation, including how many bytes were
            freed.

        See Also
        --------
        [Table.optimize][lancedb.table.Table.optimize]: A more comprehensive
            optimization operation that includes cleanup as well as other operations.

        Notes
        -----
        This function is not available in LanceDb Cloud (since LanceDB
        Cloud manages cleanup for you automatically)
        """

    @abstractmethod
    def compact_files(self, *args, **kwargs):
        """
        Run the compaction process on the table.
        This can be run after making several small appends to optimize the table
        for faster reads.

        Arguments are passed onto Lance's
        [compact_files][lance.dataset.DatasetOptimizer.compact_files].
        For most cases, the default should be fine.

        See Also
        --------
        [Table.optimize][lancedb.table.Table.optimize]: A more comprehensive
            optimization operation that includes cleanup as well as other operations.

        Notes
        -----
        This function is not available in LanceDB Cloud (since LanceDB
        Cloud manages compaction for you automatically)
        """

    @abstractmethod
    def optimize(
        self,
        *,
        cleanup_older_than: Optional[timedelta] = None,
        delete_unverified: bool = False,
        retrain: bool = False,
    ):
        """
        Optimize the on-disk data and indices for better performance.

        Modeled after ``VACUUM`` in PostgreSQL.

        Optimization covers three operations:

         * Compaction: Merges small files into larger ones
         * Prune: Removes old versions of the dataset
         * Index: Optimizes the indices, adding new data to existing indices

        Parameters
        ----------
        cleanup_older_than: timedelta, optional default 7 days
            All files belonging to versions older than this will be removed.  Set
            to 0 days to remove all versions except the latest.  The latest version
            is never removed.
        delete_unverified: bool, default False
            Files leftover from a failed transaction may appear to be part of an
            in-progress operation (e.g. appending new data) and these files will not
            be deleted unless they are at least 7 days old. If delete_unverified is True
            then these files will be deleted regardless of their age.
        retrain: bool, default False
            This parameter is no longer used and is deprecated.

        Experimental API
        ----------------

        The optimization process is undergoing active development and may change.
        Our goal with these changes is to improve the performance of optimization and
        reduce the complexity.

        That being said, it is essential today to run optimize if you want the best
        performance.  It should be stable and safe to use in production, but it our
        hope that the API may be simplified (or not even need to be called) in the
        future.

        The frequency an application shoudl call optimize is based on the frequency of
        data modifications.  If data is frequently added, deleted, or updated then
        optimize should be run frequently.  A good rule of thumb is to run optimize if
        you have added or modified 100,000 or more records or run more than 20 data
        modification operations.
        """

    @abstractmethod
    def list_indices(self) -> Iterable[IndexConfig]:
        """
        List all indices that have been created with
        [Table.create_index][lancedb.table.Table.create_index]
        """

    @abstractmethod
    def index_stats(self, index_name: str) -> Optional[IndexStatistics]:
        """
        Retrieve statistics about an index

        Parameters
        ----------
        index_name: str
            The name of the index to retrieve statistics for

        Returns
        -------
        IndexStatistics or None
            The statistics about the index. Returns None if the index does not exist.
        """

    @abstractmethod
    def add_columns(
        self, transforms: Dict[str, str] | pa.Field | List[pa.Field] | pa.Schema
    ):
        """
        Add new columns with defined values.

        Parameters
        ----------
        transforms: Dict[str, str], pa.Field, List[pa.Field], pa.Schema
            A map of column name to a SQL expression to use to calculate the
            value of the new column. These expressions will be evaluated for
            each row in the table, and can reference existing columns.
            Alternatively, a pyarrow Field or Schema can be provided to add
            new columns with the specified data types. The new columns will
            be initialized with null values.

        Returns
        -------
        AddColumnsResult
            version: the new version number of the table after adding columns.
        """

    @abstractmethod
    def alter_columns(self, *alterations: Iterable[Dict[str, str]]):
        """
        Alter column names and nullability.

        Parameters
        ----------
        alterations : Iterable[Dict[str, Any]]
            A sequence of dictionaries, each with the following keys:
            - "path": str
                The column path to alter. For a top-level column, this is the name.
                For a nested column, this is the dot-separated path, e.g. "a.b.c".
            - "rename": str, optional
                The new name of the column. If not specified, the column name is
                not changed.
            - "data_type": pyarrow.DataType, optional
               The new data type of the column. Existing values will be casted
               to this type. If not specified, the column data type is not changed.
            - "nullable": bool, optional
                Whether the column should be nullable. If not specified, the column
                nullability is not changed. Only non-nullable columns can be changed
                to nullable. Currently, you cannot change a nullable column to
                non-nullable.

        Returns
        -------
        AlterColumnsResult
            version: the new version number of the table after the alteration.
        """

    @abstractmethod
    def drop_columns(self, columns: Iterable[str]) -> DropColumnsResult:
        """
        Drop columns from the table.

        Parameters
        ----------
        columns : Iterable[str]
            The names of the columns to drop.

        Returns
        -------
        DropColumnsResult
            version: the new version number of the table dropping the columns.
        """

    @abstractmethod
    def checkout(self, version: Union[int, str]):
        """
        Checks out a specific version of the Table

        Any read operation on the table will now access the data at the checked out
        version. As a consequence, calling this method will disable any read consistency
        interval that was previously set.

        This is a read-only operation that turns the table into a sort of "view"
        or "detached head".  Other table instances will not be affected.  To make the
        change permanent you can use the `[Self::restore]` method.

        Any operation that modifies the table will fail while the table is in a checked
        out state.

        Parameters
        ----------
        version: int | str,
            The version to check out. A version number (`int`) or a tag
            (`str`) can be provided.

        To return the table to a normal state use `[Self::checkout_latest]`
        """

    @abstractmethod
    def checkout_latest(self):
        """
        Ensures the table is pointing at the latest version

        This can be used to manually update a table when the read_consistency_interval
        is None
        It can also be used to undo a `[Self::checkout]` operation
        """

    @abstractmethod
    def restore(self, version: Optional[Union[int, str]] = None):
        """Restore a version of the table. This is an in-place operation.

        This creates a new version where the data is equivalent to the
        specified previous version. Data is not copied (as of python-v0.2.1).

        Parameters
        ----------
        version : int or str, default None
            The version number or version tag to restore.
            If unspecified then restores the currently checked out version.
            If the currently checked out version is the
            latest version then this is a no-op.
        """

    @abstractmethod
    def list_versions(self) -> List[Dict[str, Any]]:
        """List all versions of the table"""

    @cached_property
    def _dataset_uri(self) -> str:
        return _table_uri(self._conn.uri, self.name)

    def _get_fts_index_path(self) -> Tuple[str, pa_fs.FileSystem, bool]:
        from .remote.table import RemoteTable

        if isinstance(self, RemoteTable) or get_uri_scheme(self._dataset_uri) != "file":
            return ("", None, False)
        path = join_uri(self._dataset_uri, "_indices", "fts")
        fs, path = fs_from_uri(path)
        index_exists = fs.get_file_info(path).type != pa_fs.FileType.NotFound
        return (path, fs, index_exists)

    @abstractmethod
    def uses_v2_manifest_paths(self) -> bool:
        """
        Check if the table is using the new v2 manifest paths.

        Returns
        -------
        bool
            True if the table is using the new v2 manifest paths, False otherwise.
        """

    @abstractmethod
    def migrate_v2_manifest_paths(self):
        """
        Migrate the manifest paths to the new format.

        This will update the manifest to use the new v2 format for paths.

        This function is idempotent, and can be run multiple times without
        changing the state of the object store.

        !!! danger

            This should not be run while other concurrent operations are happening.
            And it should also run until completion before resuming other operations.

        You can use
        [Table.uses_v2_manifest_paths][lancedb.table.Table.uses_v2_manifest_paths]
        to check if the table is already using the new path style.
        """

              

  

            name

  
      `abstractmethod`
      `property`
  

¶

name: str

    

      
The name of this Table

    

            version

  
      `abstractmethod`
      `property`
  

¶

version: int

    

      
The version of this Table

    

            schema

  
      `abstractmethod`
      `property`
  

¶

schema: Schema

    

      
The Arrow Schema
of this Table

    

            tags

  
      `abstractmethod`
      `property`
  

¶

tags: Tags

    

      
Tag management for the table.

Similar to Git, tags are a way to add metadata to a specific version of the
table.

.. warning::

Tagged versions are exempted from the :py:meth:`cleanup_old_versions()`
process.

To remove a version that has been tagged, you must first
:py:meth:`~Tags.delete` the associated tag.

Examples:

    
.. code-block:: python

table = db.open_table("my_table")
table.tags.create("v2-prod-20250203", 10)

tags = table.tags.list()

    

            embedding_functions

  
      `abstractmethod`
      `property`
  

¶

embedding_functions: Dict[str, EmbeddingFunctionConfig]

    

      
Get a mapping from vector column name to it's configured embedding function.

    

            __len__

¶

__len__() -> int

    

      
The number of rows in this Table

            
              Source code in `lancedb/table.py`
              
645
646
647
def __len__(self) -> int:
    """The number of rows in this Table"""
    return self.count_rows(None)

            
    

            count_rows

  
      `abstractmethod`
  

¶

count_rows(filter: Optional[str] = None) -> int

    

      
Count the number of rows in the table.

Parameters:

    
        
- 
          `filter`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
A SQL where clause to filter the rows to count.

          
        
    

            
              Source code in `lancedb/table.py`
              
656
657
658
659
660
661
662
663
664
665
666
@abstractmethod
def count_rows(self, filter: Optional[str] = None) -> int:
    """
    Count the number of rows in the table.

    Parameters
    ----------
    filter: str, optional
        A SQL where clause to filter the rows to count.
    """
    raise NotImplementedError

            
    

            to_pandas

¶

to_pandas() -> 'pandas.DataFrame'

    

      
Return the table as a pandas DataFrame.

Returns:

    
        
- 
              `DataFrame`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
668
669
670
671
672
673
674
675
def to_pandas(self) -> "pandas.DataFrame":
    """Return the table as a pandas DataFrame.

    Returns
    -------
    pd.DataFrame
    """
    return self.to_arrow().to_pandas()

            
    

            to_arrow

  
      `abstractmethod`
  

¶

to_arrow() -> Table

    

      
Return the table as a pyarrow Table.

Returns:

    
        
- 
              `Table`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
677
678
679
680
681
682
683
684
685
@abstractmethod
def to_arrow(self) -> pa.Table:
    """Return the table as a pyarrow Table.

    Returns
    -------
    pa.Table
    """
    raise NotImplementedError

            
    

            to_lance

¶

to_lance(**kwargs) -> LanceDataset

    

      
Return the table as a lance.LanceDataset.

Returns:

    
        
- 
              `LanceDataset`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
687
688
689
690
691
692
693
694
def to_lance(self, **kwargs) -> lance.LanceDataset:
    """Return the table as a lance.LanceDataset.

    Returns
    -------
    lance.LanceDataset
    """
    raise NotImplementedError

            
    

            to_polars

¶

to_polars(**kwargs) -> 'pl.DataFrame'

    

      
Return the table as a polars.DataFrame.

Returns:

    
        
- 
              `DataFrame`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
696
697
698
699
700
701
702
703
def to_polars(self, **kwargs) -> "pl.DataFrame":
    """Return the table as a polars.DataFrame.

    Returns
    -------
    polars.DataFrame
    """
    raise NotImplementedError

            
    

            create_index

¶

create_index(metric='l2', num_partitions=256, num_sub_vectors=96, vector_column_name: str = VECTOR_COLUMN_NAME, replace: bool = True, accelerator: Optional[str] = None, index_cache_size: Optional[int] = None, *, index_type: VectorIndexType = 'IVF_PQ', wait_timeout: Optional[timedelta] = None, num_bits: int = 8, max_iterations: int = 50, sample_rate: int = 256, m: int = 20, ef_construction: int = 300, name: Optional[str] = None, train: bool = True, target_partition_size: Optional[int] = None)

    

      
Create an index on the table.

Parameters:

    
        
- 
          `metric`
          –
          
            
The distance metric to use when creating the index.
Valid values are "l2", "cosine", "dot", or "hamming".
l2 is euclidean distance.
Hamming is available only for binary vectors.

          
        
        
- 
          `num_partitions`
          –
          
            
The number of IVF partitions to use when creating the index.
Default is 256.

          
        
        
- 
          `num_sub_vectors`
          –
          
            
The number of PQ sub-vectors to use when creating the index.
Default is 96.

          
        
        
- 
          `vector_column_name`
              (`str`, default:
                  `VECTOR_COLUMN_NAME`
)
          –
          
            
The vector column name to create the index.

          
        
        
- 
          `replace`
              (`bool`, default:
                  `True`
)
          –
          
            

- 

If True, replace the existing index if it exists.

- 

If False, raise an error if duplicate index exists.

          
        
        
- 
          `accelerator`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
If set, use the given accelerator to create the index.
Only support "cuda" for now.

          
        
        
- 
          `index_cache_size`
              (`int`, default:
                  `None`
)
          –
          
            
The size of the index cache in number of entries. Default value is 256.

          
        
        
- 
          `num_bits`
              (`int`, default:
                  `8`
)
          –
          
            
The number of bits to encode sub-vectors. Only used with the IVF_PQ index.
Only 4 and 8 are supported.

          
        
        
- 
          `wait_timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The timeout to wait if indexing is asynchronous.

          
        
        
- 
          `name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the index. If not provided, a default name will be generated.

          
        
        
- 
          `train`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to train the index with existing data. Vector indices always train
with existing data.

          
        
    

            
              Source code in `lancedb/table.py`
              
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
def create_index(
    self,
    metric="l2",
    num_partitions=256,
    num_sub_vectors=96,
    vector_column_name: str = VECTOR_COLUMN_NAME,
    replace: bool = True,
    accelerator: Optional[str] = None,
    index_cache_size: Optional[int] = None,
    *,
    index_type: VectorIndexType = "IVF_PQ",
    wait_timeout: Optional[timedelta] = None,
    num_bits: int = 8,
    max_iterations: int = 50,
    sample_rate: int = 256,
    m: int = 20,
    ef_construction: int = 300,
    name: Optional[str] = None,
    train: bool = True,
    target_partition_size: Optional[int] = None,
):
    """Create an index on the table.

    Parameters
    ----------
    metric: str, default "l2"
        The distance metric to use when creating the index.
        Valid values are "l2", "cosine", "dot", or "hamming".
        l2 is euclidean distance.
        Hamming is available only for binary vectors.
    num_partitions: int, default 256
        The number of IVF partitions to use when creating the index.
        Default is 256.
    num_sub_vectors: int, default 96
        The number of PQ sub-vectors to use when creating the index.
        Default is 96.
    vector_column_name: str, default "vector"
        The vector column name to create the index.
    replace: bool, default True
        - If True, replace the existing index if it exists.

        - If False, raise an error if duplicate index exists.
    accelerator: str, default None
        If set, use the given accelerator to create the index.
        Only support "cuda" for now.
    index_cache_size : int, optional
        The size of the index cache in number of entries. Default value is 256.
    num_bits: int
        The number of bits to encode sub-vectors. Only used with the IVF_PQ index.
        Only 4 and 8 are supported.
    wait_timeout: timedelta, optional
        The timeout to wait if indexing is asynchronous.
    name: str, optional
        The name of the index. If not provided, a default name will be generated.
    train: bool, default True
        Whether to train the index with existing data. Vector indices always train
        with existing data.
    """
    raise NotImplementedError

            
    

            drop_index

¶

drop_index(name: str) -> None

    

      
Drop an index from the table.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the index to drop.

          
        
    

  Notes
  
This does not delete the index from disk, it just removes it from the table.
To delete the index, run optimize
after dropping the index.

Use list_indices to find the names of
the indices.

            
              Source code in `lancedb/table.py`
              
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
def drop_index(self, name: str) -> None:
    """
    Drop an index from the table.

    Parameters
    ----------
    name: str
        The name of the index to drop.

    Notes
    -----
    This does not delete the index from disk, it just removes it from the table.
    To delete the index, run [optimize][lancedb.table.Table.optimize]
    after dropping the index.

    Use [list_indices][lancedb.table.Table.list_indices] to find the names of
    the indices.
    """
    raise NotImplementedError

            
    

            wait_for_index

¶

wait_for_index(index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)) -> None

    

      
Wait for indexing to complete for the given index names.
This will poll the table until all the indices are fully indexed,
or raise a timeout exception if the timeout is reached.

Parameters:

    
        
- 
          `index_names`
              (`Iterable[str]`)
          –
          
            
The name of the indices to poll

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `timedelta(seconds=300)`
)
          –
          
            
Timeout to wait for asynchronous indexing. The default is 5 minutes.

          
        
    

            
              Source code in `lancedb/table.py`
              
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
def wait_for_index(
    self, index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)
) -> None:
    """
    Wait for indexing to complete for the given index names.
    This will poll the table until all the indices are fully indexed,
    or raise a timeout exception if the timeout is reached.

    Parameters
    ----------
    index_names: str
        The name of the indices to poll
    timeout: timedelta
        Timeout to wait for asynchronous indexing. The default is 5 minutes.
    """
    raise NotImplementedError

            
    

            stats

  
      `abstractmethod`
  

¶

stats() -> TableStatistics

    

      
Retrieve table and fragment statistics.

            
              Source code in `lancedb/table.py`
              
802
803
804
805
806
807
@abstractmethod
def stats(self) -> TableStatistics:
    """
    Retrieve table and fragment statistics.
    """
    raise NotImplementedError

            
    

            create_scalar_index

  
      `abstractmethod`
  

¶

create_scalar_index(column: str, *, replace: bool = True, index_type: ScalarIndexType = 'BTREE', wait_timeout: Optional[timedelta] = None, name: Optional[str] = None)

    

      
Create a scalar index on a column.

Parameters:

    
        
- 
          `column`
              (`str`)
          –
          
            
The column to be indexed.  Must be a boolean, integer, float,
or string column.

          
        
        
- 
          `replace`
              (`bool`, default:
                  `True`
)
          –
          
            
Replace the existing index if it exists.

          
        
        
- 
          `index_type`
              (`ScalarIndexType`, default:
                  `'BTREE'`
)
          –
          
            
The type of index to create.

          
        
        
- 
          `wait_timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The timeout to wait if indexing is asynchronous.

          
        
        
- 
          `name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the index. If not provided, a default name will be generated.

          
        
    

Examples:

    
Scalar indices, like vector indices, can be used to speed up scans.  A scalar
index can speed up scans that contain filter expressions on the indexed column.
For example, the following scan will be faster if the column `my_col` has
a scalar index:

    
>>> import lancedb
>>> db = lancedb.connect("/data/lance")
>>> img_table = db.open_table("images")
>>> my_df = img_table.search().where("my_col = 7",
...                                  prefilter=True).to_pandas()

    
Scalar indices can also speed up scans containing a vector search and a
prefilter:

    
>>> import lancedb
>>> db = lancedb.connect("/data/lance")
>>> img_table = db.open_table("images")
>>> img_table.search([1, 2, 3, 4], vector_column_name="vector")
...     .where("my_col != 7", prefilter=True)
...     .to_pandas()

    
Scalar indices can only speed up scans for basic filters using
equality, comparison, range (e.g. `my_col BETWEEN 0 AND 100`), and set
membership (e.g. `my_col IN (0, 1, 2)`)

Scalar indices can be used if the filter contains multiple indexed columns and
the filter criteria are AND'd or OR'd together
(e.g. `my_col < 0 AND other_col> 100`)

Scalar indices may be used if the filter contains non-indexed columns but,
depending on the structure of the filter, they may not be usable.  For example,
if the column `not_indexed` does not have a scalar index then the filter
`my_col = 0 OR not_indexed = 1` will not be able to use any scalar index on
`my_col`.

            
              Source code in `lancedb/table.py`
              
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
@abstractmethod
def create_scalar_index(
    self,
    column: str,
    *,
    replace: bool = True,
    index_type: ScalarIndexType = "BTREE",
    wait_timeout: Optional[timedelta] = None,
    name: Optional[str] = None,
):
    """Create a scalar index on a column.

    Parameters
    ----------
    column : str
        The column to be indexed.  Must be a boolean, integer, float,
        or string column.
    replace : bool, default True
        Replace the existing index if it exists.
    index_type: Literal["BTREE", "BITMAP", "LABEL_LIST"], default "BTREE"
        The type of index to create.
    wait_timeout: timedelta, optional
        The timeout to wait if indexing is asynchronous.
    name: str, optional
        The name of the index. If not provided, a default name will be generated.
    Examples
    --------

    Scalar indices, like vector indices, can be used to speed up scans.  A scalar
    index can speed up scans that contain filter expressions on the indexed column.
    For example, the following scan will be faster if the column ``my_col`` has
    a scalar index:

    >>> import lancedb # doctest: +SKIP
    >>> db = lancedb.connect("/data/lance") # doctest: +SKIP
    >>> img_table = db.open_table("images") # doctest: +SKIP
    >>> my_df = img_table.search().where("my_col = 7", # doctest: +SKIP
    ...                                  prefilter=True).to_pandas()

    Scalar indices can also speed up scans containing a vector search and a
    prefilter:

    >>> import lancedb # doctest: +SKIP
    >>> db = lancedb.connect("/data/lance") # doctest: +SKIP
    >>> img_table = db.open_table("images") # doctest: +SKIP
    >>> img_table.search([1, 2, 3, 4], vector_column_name="vector") # doctest: +SKIP
    ...     .where("my_col != 7", prefilter=True)
    ...     .to_pandas()

    Scalar indices can only speed up scans for basic filters using
    equality, comparison, range (e.g. ``my_col BETWEEN 0 AND 100``), and set
    membership (e.g. `my_col IN (0, 1, 2)`)

    Scalar indices can be used if the filter contains multiple indexed columns and
    the filter criteria are AND'd or OR'd together
    (e.g. ``my_col < 0 AND other_col> 100``)

    Scalar indices may be used if the filter contains non-indexed columns but,
    depending on the structure of the filter, they may not be usable.  For example,
    if the column ``not_indexed`` does not have a scalar index then the filter
    ``my_col = 0 OR not_indexed = 1`` will not be able to use any scalar index on
    ``my_col``.
    """
    raise NotImplementedError

            
    

            create_fts_index

¶

create_fts_index(field_names: Union[str, List[str]], *, ordering_field_names: Optional[Union[str, List[str]]] = None, replace: bool = False, writer_heap_size: Optional[int] = 1024 * 1024 * 1024, use_tantivy: bool = False, tokenizer_name: Optional[str] = None, with_position: bool = False, base_tokenizer: BaseTokenizerType = 'simple', language: str = 'English', max_token_length: Optional[int] = 40, lower_case: bool = True, stem: bool = True, remove_stop_words: bool = True, ascii_folding: bool = True, ngram_min_length: int = 3, ngram_max_length: int = 3, prefix_only: bool = False, wait_timeout: Optional[timedelta] = None, name: Optional[str] = None)

    

      
Create a full-text search index on the table.

Warning - this API is highly experimental and is highly likely to change
in the future.

Parameters:

    
        
- 
          `field_names`
              (`Union[str, List[str]]`)
          –
          
            
The name(s) of the field to index.
If `use_tantivy` is False (default), only a single field name
(str) is supported. To index multiple fields, create a separate
FTS index for each field.

          
        
        
- 
          `replace`
              (`bool`, default:
                  `False`
)
          –
          
            
If True, replace the existing index if it exists. Note that this is
not yet an atomic operation; the index will be temporarily
unavailable while the new index is being created.

          
        
        
- 
          `writer_heap_size`
              (`Optional[int]`, default:
                  `1024 * 1024 * 1024`
)
          –
          
            
Only available with use_tantivy=True

          
        
        
- 
          `ordering_field_names`
              (`Optional[Union[str, List[str]]]`, default:
                  `None`
)
          –
          
            
A list of unsigned type fields to index to optionally order
results on at search time.
only available with use_tantivy=True

          
        
        
- 
          `tokenizer_name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The tokenizer to use for the index. Can be "raw", "default" or the 2 letter
language code followed by "_stem". So for english it would be "en_stem".
For available languages see: https://docs.rs/tantivy/latest/tantivy/tokenizer/enum.Language.html

          
        
        
- 
          `use_tantivy`
              (`bool`, default:
                  `False`
)
          –
          
            
If True, use the legacy full-text search implementation based on tantivy.
If False, use the new full-text search implementation based on lance-index.

          
        
        
- 
          `with_position`
              (`bool`, default:
                  `False`
)
          –
          
            
Only available with use_tantivy=False
If False, do not store the positions of the terms in the text.
This can reduce the size of the index and improve indexing speed.
But it will raise an exception for phrase queries.

          
        
        
- 
          `base_tokenizer`
              (`str`, default:
                  `"simple"`
)
          –
          
            
The base tokenizer to use for tokenization. Options are:
- "simple": Splits text by whitespace and punctuation.
- "whitespace": Split text by whitespace, but not punctuation.
- "raw": No tokenization. The entire text is treated as a single token.
- "ngram": N-Gram tokenizer.

          
        
        
- 
          `language`
              (`str`, default:
                  `"English"`
)
          –
          
            
The language to use for tokenization.

          
        
        
- 
          `max_token_length`
              (`int`, default:
                  `40`
)
          –
          
            
The maximum token length to index. Tokens longer than this length will be
ignored.

          
        
        
- 
          `lower_case`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to convert the token to lower case. This makes queries
case-insensitive.

          
        
        
- 
          `stem`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to stem the token. Stemming reduces words to their root form.
For example, in English "running" and "runs" would both be reduced to "run".

          
        
        
- 
          `remove_stop_words`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to remove stop words. Stop words are common words that are often
removed from text before indexing. For example, in English "the" and "and".

          
        
        
- 
          `ascii_folding`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to fold ASCII characters. This converts accented characters to
their ASCII equivalent. For example, "café" would be converted to "cafe".

          
        
        
- 
          `ngram_min_length`
              (`int`, default:
                  `3`
)
          –
          
            
The minimum length of an n-gram.

          
        
        
- 
          `ngram_max_length`
              (`int`, default:
                  `3`
)
          –
          
            
The maximum length of an n-gram.

          
        
        
- 
          `prefix_only`
              (`bool`, default:
                  `False`
)
          –
          
            
Whether to only index the prefix of the token for ngram tokenizer.

          
        
        
- 
          `wait_timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The timeout to wait if indexing is asynchronous.

          
        
        
- 
          `name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the index. If not provided, a default name will be generated.

          
        
    

            
              Source code in `lancedb/table.py`
              
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
def create_fts_index(
    self,
    field_names: Union[str, List[str]],
    *,
    ordering_field_names: Optional[Union[str, List[str]]] = None,
    replace: bool = False,
    writer_heap_size: Optional[int] = 1024 * 1024 * 1024,
    use_tantivy: bool = False,
    tokenizer_name: Optional[str] = None,
    with_position: bool = False,
    # tokenizer configs:
    base_tokenizer: BaseTokenizerType = "simple",
    language: str = "English",
    max_token_length: Optional[int] = 40,
    lower_case: bool = True,
    stem: bool = True,
    remove_stop_words: bool = True,
    ascii_folding: bool = True,
    ngram_min_length: int = 3,
    ngram_max_length: int = 3,
    prefix_only: bool = False,
    wait_timeout: Optional[timedelta] = None,
    name: Optional[str] = None,
):
    """Create a full-text search index on the table.

    Warning - this API is highly experimental and is highly likely to change
    in the future.

    Parameters
    ----------
    field_names: str or list of str
        The name(s) of the field to index.
        If ``use_tantivy`` is False (default), only a single field name
        (str) is supported. To index multiple fields, create a separate
        FTS index for each field.
    replace: bool, default False
        If True, replace the existing index if it exists. Note that this is
        not yet an atomic operation; the index will be temporarily
        unavailable while the new index is being created.
    writer_heap_size: int, default 1GB
        Only available with use_tantivy=True
    ordering_field_names:
        A list of unsigned type fields to index to optionally order
        results on at search time.
        only available with use_tantivy=True
    tokenizer_name: str, default "default"
        The tokenizer to use for the index. Can be "raw", "default" or the 2 letter
        language code followed by "_stem". So for english it would be "en_stem".
        For available languages see: https://docs.rs/tantivy/latest/tantivy/tokenizer/enum.Language.html
    use_tantivy: bool, default False
        If True, use the legacy full-text search implementation based on tantivy.
        If False, use the new full-text search implementation based on lance-index.
    with_position: bool, default False
        Only available with use_tantivy=False
        If False, do not store the positions of the terms in the text.
        This can reduce the size of the index and improve indexing speed.
        But it will raise an exception for phrase queries.
    base_tokenizer : str, default "simple"
        The base tokenizer to use for tokenization. Options are:
        - "simple": Splits text by whitespace and punctuation.
        - "whitespace": Split text by whitespace, but not punctuation.
        - "raw": No tokenization. The entire text is treated as a single token.
        - "ngram": N-Gram tokenizer.
    language : str, default "English"
        The language to use for tokenization.
    max_token_length : int, default 40
        The maximum token length to index. Tokens longer than this length will be
        ignored.
    lower_case : bool, default True
        Whether to convert the token to lower case. This makes queries
        case-insensitive.
    stem : bool, default True
        Whether to stem the token. Stemming reduces words to their root form.
        For example, in English "running" and "runs" would both be reduced to "run".
    remove_stop_words : bool, default True
        Whether to remove stop words. Stop words are common words that are often
        removed from text before indexing. For example, in English "the" and "and".
    ascii_folding : bool, default True
        Whether to fold ASCII characters. This converts accented characters to
        their ASCII equivalent. For example, "café" would be converted to "cafe".
    ngram_min_length: int, default 3
        The minimum length of an n-gram.
    ngram_max_length: int, default 3
        The maximum length of an n-gram.
    prefix_only: bool, default False
        Whether to only index the prefix of the token for ngram tokenizer.
    wait_timeout: timedelta, optional
        The timeout to wait if indexing is asynchronous.
    name: str, optional
        The name of the index. If not provided, a default name will be generated.
    """
    raise NotImplementedError

            
    

            add

  
      `abstractmethod`
  

¶

add(data: DATA, mode: AddMode = 'append', on_bad_vectors: OnBadVectorsType = 'error', fill_value: float = 0.0) -> AddResult

    

      
Add more data to the Table.

Parameters:

    
        
- 
          `data`
              (`DATA`)
          –
          
            
The data to insert into the table. Acceptable types are:

- 

list-of-dict

- 

pandas.DataFrame

- 

pyarrow.Table or pyarrow.RecordBatch

          
        
        
- 
          `mode`
              (`AddMode`, default:
                  `'append'`
)
          –
          
            
The mode to use when writing the data. Valid values are
"append" and "overwrite".

          
        
        
- 
          `on_bad_vectors`
              (`OnBadVectorsType`, default:
                  `'error'`
)
          –
          
            
What to do if any of the vectors are not the same size or contains NaNs.
One of "error", "drop", "fill".

          
        
        
- 
          `fill_value`
              (`float`, default:
                  `0.0`
)
          –
          
            
The value to use when filling vectors. Only used if on_bad_vectors="fill".

          
        
    

Returns:

    
        
- 
              `AddResult`
          –
          
            
An object containing the new version number of the table after adding data.

          
        
    

            
              Source code in `lancedb/table.py`
              
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
@abstractmethod
def add(
    self,
    data: DATA,
    mode: AddMode = "append",
    on_bad_vectors: OnBadVectorsType = "error",
    fill_value: float = 0.0,
) -> AddResult:
    """Add more data to the [Table](Table).

    Parameters
    ----------
    data: DATA
        The data to insert into the table. Acceptable types are:

        - list-of-dict

        - pandas.DataFrame

        - pyarrow.Table or pyarrow.RecordBatch
    mode: str
        The mode to use when writing the data. Valid values are
        "append" and "overwrite".
    on_bad_vectors: str, default "error"
        What to do if any of the vectors are not the same size or contains NaNs.
        One of "error", "drop", "fill".
    fill_value: float, default 0.
        The value to use when filling vectors. Only used if on_bad_vectors="fill".

    Returns
    -------
    AddResult
        An object containing the new version number of the table after adding data.
    """
    raise NotImplementedError

            
    

            merge_insert

¶

merge_insert(on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder

    

      
Returns a `LanceMergeInsertBuilder`
that can be used to create a "merge insert" operation

This operation can add rows, update rows, and remove rows all in a single
transaction. It is a very generic tool that can be used to create
behaviors like "insert if not exists", "update or insert (i.e. upsert)",
or even replace a portion of existing data with new data (e.g. replace
all data where month="january")

The merge insert operation works by combining new data from a
source table with existing data in a target table by using a
join.  There are three categories of records.

"Matched" records are records that exist in both the source table and
the target table. "Not matched" records exist only in the source table
(e.g. these are new data) "Not matched by source" records exist only
in the target table (this is old data)

The builder returned by this method can be used to customize what
should happen for each category of data.

Please note that the data may appear to be reordered as part of this
operation.  This is because updated rows will be deleted from the
dataset and then reinserted at the end with the new values.

Parameters:

    
        
- 
          `on`
              (`Union[str, Iterable[str]]`)
          –
          
            
A column (or columns) to join on.  This is how records from the
source table and target table are matched.  Typically this is some
kind of key or id column.

          
        
    

Examples:

    
>>> import lancedb
>>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
>>> # Perform a "upsert" operation
>>> res = table.merge_insert("a")     \
...      .when_matched_update_all()     \
...      .when_not_matched_insert_all() \
...      .execute(new_data)
>>> res
MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
>>> # The order of new rows is non-deterministic since we use
>>> # a hash-join as part of this operation and so we sort here
>>> table.to_arrow().sort_by("a").to_pandas()
   a  b
0  1  b
1  2  x
2  3  y
3  4  z

            
              Source code in `lancedb/table.py`
              
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
def merge_insert(self, on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder:
    """
    Returns a [`LanceMergeInsertBuilder`][lancedb.merge.LanceMergeInsertBuilder]
    that can be used to create a "merge insert" operation

    This operation can add rows, update rows, and remove rows all in a single
    transaction. It is a very generic tool that can be used to create
    behaviors like "insert if not exists", "update or insert (i.e. upsert)",
    or even replace a portion of existing data with new data (e.g. replace
    all data where month="january")

    The merge insert operation works by combining new data from a
    **source table** with existing data in a **target table** by using a
    join.  There are three categories of records.

    "Matched" records are records that exist in both the source table and
    the target table. "Not matched" records exist only in the source table
    (e.g. these are new data) "Not matched by source" records exist only
    in the target table (this is old data)

    The builder returned by this method can be used to customize what
    should happen for each category of data.

    Please note that the data may appear to be reordered as part of this
    operation.  This is because updated rows will be deleted from the
    dataset and then reinserted at the end with the new values.

    Parameters
    ----------

    on: Union[str, Iterable[str]]
        A column (or columns) to join on.  This is how records from the
        source table and target table are matched.  Typically this is some
        kind of key or id column.

    Examples
    --------
    >>> import lancedb
    >>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data)
    >>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
    >>> # Perform a "upsert" operation
    >>> res = table.merge_insert("a")     \\
    ...      .when_matched_update_all()     \\
    ...      .when_not_matched_insert_all() \\
    ...      .execute(new_data)
    >>> res
    MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
    >>> # The order of new rows is non-deterministic since we use
    >>> # a hash-join as part of this operation and so we sort here
    >>> table.to_arrow().sort_by("a").to_pandas()
       a  b
    0  1  b
    1  2  x
    2  3  y
    3  4  z
    """  # noqa: E501
    on = [on] if isinstance(on, str) else list(iter(on))

    return LanceMergeInsertBuilder(self, on)

            
    

            search

  
      `abstractmethod`
  

¶

search(query: Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]] = None, vector_column_name: Optional[str] = None, query_type: QueryType = 'auto', ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None) -> LanceQueryBuilder

    

      
Create a search query to find the nearest neighbors
of the given query vector. We currently support vector search
and [full-text search][experimental-full-text-search].

All query options are defined in
LanceQueryBuilder.

Examples:

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> data = [
...    {"original_width": 100, "caption": "bar", "vector": [0.1, 2.3, 4.5]},
...    {"original_width": 2000, "caption": "foo",  "vector": [0.5, 3.4, 1.3]},
...    {"original_width": 3000, "caption": "test", "vector": [0.3, 6.2, 2.6]}
... ]
>>> table = db.create_table("my_table", data)
>>> query = [0.4, 1.4, 2.4]
>>> (table.search(query)
...     .where("original_width > 1000", prefilter=True)
...     .select(["caption", "original_width", "vector"])
...     .limit(2)
...     .to_pandas())
  caption  original_width           vector  _distance
0     foo            2000  [0.5, 3.4, 1.3]   5.220000
1    test            3000  [0.3, 6.2, 2.6]  23.089996

Parameters:

    
        
- 
          `query`
              (`Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]]`, default:
                  `None`
)
          –
          
            
The targetted vector to search for.

- 

default None.
Acceptable types are: list, np.ndarray, PIL.Image.Image

- 

If None then the select/where/limit clauses are applied to filter
the table

          
        
        
- 
          `vector_column_name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the vector column to search.

The vector column needs to be a pyarrow fixed size list type

- 

If not specified then the vector column is inferred from
the table schema

- 

If the table has multiple vector columns then the vector_column_name
needs to be specified. Otherwise, an error is raised.

          
        
        
- 
          `query_type`
              (`QueryType`, default:
                  `'auto'`
)
          –
          
            
default "auto".
Acceptable types are: "vector", "fts", "hybrid", or "auto"

- 

If "auto" then the query type is inferred from the query;

- 

If `query` is a list/np.ndarray then the query type is
"vector";

- 

If `query` is a PIL.Image.Image then either do vector search,
or raise an error if no corresponding embedding function is found.

- 

If `query` is a string, then the query type is "vector" if the
table has embedding functions else the query type is "fts"

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
A query builder object representing the query.
Once executed, the query returns

- 

selected columns

- 

the vector

- 

and also the "_distance" column which is the distance between the query
vector and the returned vector.

          
        
    

            
              Source code in `lancedb/table.py`
              
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
@abstractmethod
def search(
    self,
    query: Optional[
        Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]
    ] = None,
    vector_column_name: Optional[str] = None,
    query_type: QueryType = "auto",
    ordering_field_name: Optional[str] = None,
    fts_columns: Optional[Union[str, List[str]]] = None,
) -> LanceQueryBuilder:
    """Create a search query to find the nearest neighbors
    of the given query vector. We currently support [vector search][search]
    and [full-text search][experimental-full-text-search].

    All query options are defined in
    [LanceQueryBuilder][lancedb.query.LanceQueryBuilder].

    Examples
    --------
    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> data = [
    ...    {"original_width": 100, "caption": "bar", "vector": [0.1, 2.3, 4.5]},
    ...    {"original_width": 2000, "caption": "foo",  "vector": [0.5, 3.4, 1.3]},
    ...    {"original_width": 3000, "caption": "test", "vector": [0.3, 6.2, 2.6]}
    ... ]
    >>> table = db.create_table("my_table", data)
    >>> query = [0.4, 1.4, 2.4]
    >>> (table.search(query)
    ...     .where("original_width > 1000", prefilter=True)
    ...     .select(["caption", "original_width", "vector"])
    ...     .limit(2)
    ...     .to_pandas())
      caption  original_width           vector  _distance
    0     foo            2000  [0.5, 3.4, 1.3]   5.220000
    1    test            3000  [0.3, 6.2, 2.6]  23.089996

    Parameters
    ----------
    query: list/np.ndarray/str/PIL.Image.Image, default None
        The targetted vector to search for.

        - *default None*.
        Acceptable types are: list, np.ndarray, PIL.Image.Image

        - If None then the select/where/limit clauses are applied to filter
        the table
    vector_column_name: str, optional
        The name of the vector column to search.

        The vector column needs to be a pyarrow fixed size list type

        - If not specified then the vector column is inferred from
        the table schema

        - If the table has multiple vector columns then the *vector_column_name*
        needs to be specified. Otherwise, an error is raised.
    query_type: str
        *default "auto"*.
        Acceptable types are: "vector", "fts", "hybrid", or "auto"

        - If "auto" then the query type is inferred from the query;

            - If `query` is a list/np.ndarray then the query type is
            "vector";

            - If `query` is a PIL.Image.Image then either do vector search,
            or raise an error if no corresponding embedding function is found.

        - If `query` is a string, then the query type is "vector" if the
        table has embedding functions else the query type is "fts"

    Returns
    -------
    LanceQueryBuilder
        A query builder object representing the query.
        Once executed, the query returns

        - selected columns

        - the vector

        - and also the "_distance" column which is the distance between the query
        vector and the returned vector.
    """
    raise NotImplementedError

            
    

            take_offsets

  
      `abstractmethod`
  

¶

take_offsets(offsets: list[int], *, with_row_id: bool = False) -> LanceTakeQueryBuilder

    

      
Take a list of offsets from the table.

Offsets are 0-indexed and relative to the current version of the table.  Offsets
are not stable.  A row with an offset of N may have a different offset in a
different version of the table (e.g. if an earlier row is deleted).

Offsets are mostly useful for sampling as the set of all valid offsets is easily
known in advance to be [0, len(table)).

No guarantees are made regarding the order in which results are returned.  If
you desire an output order that matches the order of the given offsets, you will
need to add the row offset column to the output and align it yourself.

Parameters:

    
        
- 
          `offsets`
              (`list[int]`)
          –
          
            
The offsets to take.

          
        
    

Returns:

    
        
- 
              `RecordBatch`
          –
          
            
A record batch containing the rows at the given offsets.

          
        
    

            
              Source code in `lancedb/table.py`
              
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
@abstractmethod
def take_offsets(
    self, offsets: list[int], *, with_row_id: bool = False
) -> LanceTakeQueryBuilder:
    """
    Take a list of offsets from the table.

    Offsets are 0-indexed and relative to the current version of the table.  Offsets
    are not stable.  A row with an offset of N may have a different offset in a
    different version of the table (e.g. if an earlier row is deleted).

    Offsets are mostly useful for sampling as the set of all valid offsets is easily
    known in advance to be [0, len(table)).

    No guarantees are made regarding the order in which results are returned.  If
    you desire an output order that matches the order of the given offsets, you will
    need to add the row offset column to the output and align it yourself.

    Parameters
    ----------
    offsets: list[int]
        The offsets to take.

    Returns
    -------
    pa.RecordBatch
        A record batch containing the rows at the given offsets.
    """

            
    

            __getitems__

¶

__getitems__(offsets: list[int]) -> RecordBatch

    

      
Take a list of offsets from the table and return as a record batch.

This method uses the `take_offsets` method to take the rows.  However, it
aligns the offsets to the passed in offsets.  This means the return type
is a record batch (and so users should take care not to pass in too many
offsets)

Note: this method is primarily intended to fulfill the Dataset contract
for pytorch.

Parameters:

    
        
- 
          `offsets`
              (`list[int]`)
          –
          
            
The offsets to take.

          
        
    

Returns:

    
        
- 
              `RecordBatch`
          –
          
            
A record batch containing the rows at the given offsets.

          
        
    

            
              Source code in `lancedb/table.py`
              
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
def __getitems__(self, offsets: list[int]) -> pa.RecordBatch:
    """
    Take a list of offsets from the table and return as a record batch.

    This method uses the `take_offsets` method to take the rows.  However, it
    aligns the offsets to the passed in offsets.  This means the return type
    is a record batch (and so users should take care not to pass in too many
    offsets)

    Note: this method is primarily intended to fulfill the Dataset contract
    for pytorch.

    Parameters
    ----------
    offsets: list[int]
        The offsets to take.

    Returns
    -------
    pa.RecordBatch
        A record batch containing the rows at the given offsets.
    """
    # We don't know the order of the results at all.  So we calculate a permutation
    # for ordering the given offsets.  Then we load the data with the _rowoffset
    # column.  Then we sort by _rowoffset and apply the inverse of the permutation
    # that we calculated.
    #
    # Note: this is potentially a lot of memory copy if we're operating on large
    # batches :(
    num_offsets = len(offsets)
    indices = list(range(num_offsets))
    permutation = sorted(indices, key=lambda idx: offsets[idx])
    permutation_inv = [0] * num_offsets
    for i in range(num_offsets):
        permutation_inv[permutation[i]] = i

    columns = self.schema.names
    columns.append("_rowoffset")
    tbl = (
        self.take_offsets(offsets)
        .select(columns)
        .to_arrow()
        .sort_by("_rowoffset")
        .take(permutation_inv)
        .combine_chunks()
        .drop_columns(["_rowoffset"])
    )

    return tbl

            
    

            take_row_ids

  
      `abstractmethod`
  

¶

take_row_ids(row_ids: list[int], *, with_row_id: bool = False) -> LanceTakeQueryBuilder

    

      
Take a list of row ids from the table.

Row ids are not stable and are relative to the current version of the table.
They can change due to compaction and updates.

No guarantees are made regarding the order in which results are returned.  If
you desire an output order that matches the order of the given ids, you will
need to add the row id column to the output and align it yourself.

Unlike offsets, row ids are not 0-indexed and no assumptions should be made
about the possible range of row ids.  In order to use this method you must
first obtain the row ids by scanning or searching the table.

Even so, row ids are more stable than offsets and can be useful in some
situations.

There is an ongoing effort to make row ids stable which is tracked at
https://github.com/lancedb/lancedb/issues/1120

Parameters:

    
        
- 
          `row_ids`
              (`list[int]`)
          –
          
            
The row ids to take.

          
        
    

Returns:

    
        
- 
              `AsyncTakeQuery`
          –
          
            
A query object that can be executed to get the rows.

          
        
    

            
              Source code in `lancedb/table.py`
              
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
@abstractmethod
def take_row_ids(
    self, row_ids: list[int], *, with_row_id: bool = False
) -> LanceTakeQueryBuilder:
    """
    Take a list of row ids from the table.

    Row ids are not stable and are relative to the current version of the table.
    They can change due to compaction and updates.

    No guarantees are made regarding the order in which results are returned.  If
    you desire an output order that matches the order of the given ids, you will
    need to add the row id column to the output and align it yourself.

    Unlike offsets, row ids are not 0-indexed and no assumptions should be made
    about the possible range of row ids.  In order to use this method you must
    first obtain the row ids by scanning or searching the table.

    Even so, row ids are more stable than offsets and can be useful in some
    situations.

    There is an ongoing effort to make row ids stable which is tracked at
    https://github.com/lancedb/lancedb/issues/1120

    Parameters
    ----------
    row_ids: list[int]
        The row ids to take.

    Returns
    -------
    AsyncTakeQuery
        A query object that can be executed to get the rows.
    """

            
    

            delete

  
      `abstractmethod`
  

¶

delete(where: str) -> DeleteResult

    

      
Delete rows from the table.

This can be used to delete a single row, many rows, all rows, or
sometimes no rows (if your predicate matches nothing).

Parameters:

    
        
- 
          `where`
              (`str`)
          –
          
            
The SQL where clause to use when deleting rows.

- For example, 'x = 2' or 'x IN (1, 2, 3)'.

The filter must not be empty, or it will error.

          
        
    

Returns:

    
        
- 
              `DeleteResult`
          –
          
            
An object containing the new version number of the table after deletion.

          
        
    

Examples:

    
>>> import lancedb
>>> data = [
...    {"x": 1, "vector": [1.0, 2]},
...    {"x": 2, "vector": [3.0, 4]},
...    {"x": 3, "vector": [5.0, 6]}
... ]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.delete("x = 2")
DeleteResult(version=2)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  3  [5.0, 6.0]

    
If you have a list of values to delete, you can combine them into a
stringified list and use the `IN` operator:

    
>>> to_remove = [1, 5]
>>> to_remove = ", ".join([str(v) for v in to_remove])
>>> to_remove
'1, 5'
>>> table.delete(f"x IN ({to_remove})")
DeleteResult(version=3)
>>> table.to_pandas()
   x      vector
0  3  [5.0, 6.0]

            
              Source code in `lancedb/table.py`
              
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
@abstractmethod
def delete(self, where: str) -> DeleteResult:
    """Delete rows from the table.

    This can be used to delete a single row, many rows, all rows, or
    sometimes no rows (if your predicate matches nothing).

    Parameters
    ----------
    where: str
        The SQL where clause to use when deleting rows.

        - For example, 'x = 2' or 'x IN (1, 2, 3)'.

        The filter must not be empty, or it will error.

    Returns
    -------
    DeleteResult
        An object containing the new version number of the table after deletion.

    Examples
    --------
    >>> import lancedb
    >>> data = [
    ...    {"x": 1, "vector": [1.0, 2]},
    ...    {"x": 2, "vector": [3.0, 4]},
    ...    {"x": 3, "vector": [5.0, 6]}
    ... ]
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data)
    >>> table.to_pandas()
       x      vector
    0  1  [1.0, 2.0]
    1  2  [3.0, 4.0]
    2  3  [5.0, 6.0]
    >>> table.delete("x = 2")
    DeleteResult(version=2)
    >>> table.to_pandas()
       x      vector
    0  1  [1.0, 2.0]
    1  3  [5.0, 6.0]

    If you have a list of values to delete, you can combine them into a
    stringified list and use the `IN` operator:

    >>> to_remove = [1, 5]
    >>> to_remove = ", ".join([str(v) for v in to_remove])
    >>> to_remove
    '1, 5'
    >>> table.delete(f"x IN ({to_remove})")
    DeleteResult(version=3)
    >>> table.to_pandas()
       x      vector
    0  3  [5.0, 6.0]
    """
    raise NotImplementedError

            
    

            update

  
      `abstractmethod`
  

¶

update(where: Optional[str] = None, values: Optional[dict] = None, *, values_sql: Optional[Dict[str, str]] = None) -> UpdateResult

    

      
This can be used to update zero to all rows depending on how many
rows match the where clause. If no where clause is provided, then
all rows will be updated.

Either `values` or `values_sql` must be provided. You cannot provide
both.

Parameters:

    
        
- 
          `where`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The SQL where clause to use when updating rows. For example, 'x = 2'
or 'x IN (1, 2, 3)'. The filter must not be empty, or it will error.

          
        
        
- 
          `values`
              (`Optional[dict]`, default:
                  `None`
)
          –
          
            
The values to update. The keys are the column names and the values
are the values to set.

          
        
        
- 
          `values_sql`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
The values to update, expressed as SQL expression strings. These can
reference existing columns. For example, {"x": "x + 1"} will increment
the x column by 1.

          
        
    

Returns:

    
        
- 
              `UpdateResult`
          –
          
            

- rows_updated: The number of rows that were updated

- version: The new version number of the table after the update

          
        
    

Examples:

    
>>> import lancedb
>>> import pandas as pd
>>> data = pd.DataFrame({"x": [1, 2, 3], "vector": [[1.0, 2], [3, 4], [5, 6]]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.update(where="x = 2", values={"vector": [10.0, 10]})
UpdateResult(rows_updated=1, version=2)
>>> table.to_pandas()
   x        vector
0  1    [1.0, 2.0]
1  3    [5.0, 6.0]
2  2  [10.0, 10.0]
>>> table.update(values_sql={"x": "x + 1"})
UpdateResult(rows_updated=3, version=3)
>>> table.to_pandas()
   x        vector
0  2    [1.0, 2.0]
1  4    [5.0, 6.0]
2  3  [10.0, 10.0]

            
              Source code in `lancedb/table.py`
              
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
@abstractmethod
def update(
    self,
    where: Optional[str] = None,
    values: Optional[dict] = None,
    *,
    values_sql: Optional[Dict[str, str]] = None,
) -> UpdateResult:
    """
    This can be used to update zero to all rows depending on how many
    rows match the where clause. If no where clause is provided, then
    all rows will be updated.

    Either `values` or `values_sql` must be provided. You cannot provide
    both.

    Parameters
    ----------
    where: str, optional
        The SQL where clause to use when updating rows. For example, 'x = 2'
        or 'x IN (1, 2, 3)'. The filter must not be empty, or it will error.
    values: dict, optional
        The values to update. The keys are the column names and the values
        are the values to set.
    values_sql: dict, optional
        The values to update, expressed as SQL expression strings. These can
        reference existing columns. For example, {"x": "x + 1"} will increment
        the x column by 1.

    Returns
    -------
    UpdateResult
        - rows_updated: The number of rows that were updated
        - version: The new version number of the table after the update

    Examples
    --------
    >>> import lancedb
    >>> import pandas as pd
    >>> data = pd.DataFrame({"x": [1, 2, 3], "vector": [[1.0, 2], [3, 4], [5, 6]]})
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data)
    >>> table.to_pandas()
       x      vector
    0  1  [1.0, 2.0]
    1  2  [3.0, 4.0]
    2  3  [5.0, 6.0]
    >>> table.update(where="x = 2", values={"vector": [10.0, 10]})
    UpdateResult(rows_updated=1, version=2)
    >>> table.to_pandas()
       x        vector
    0  1    [1.0, 2.0]
    1  3    [5.0, 6.0]
    2  2  [10.0, 10.0]
    >>> table.update(values_sql={"x": "x + 1"})
    UpdateResult(rows_updated=3, version=3)
    >>> table.to_pandas()
       x        vector
    0  2    [1.0, 2.0]
    1  4    [5.0, 6.0]
    2  3  [10.0, 10.0]
    """
    raise NotImplementedError

            
    

            cleanup_old_versions

  
      `abstractmethod`
  

¶

cleanup_old_versions(older_than: Optional[timedelta] = None, *, delete_unverified: bool = False) -> 'CleanupStats'

    

      
Clean up old versions of the table, freeing disk space.

Parameters:

    
        
- 
          `older_than`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The minimum age of the version to delete. If None, then this defaults
to two weeks.

          
        
        
- 
          `delete_unverified`
              (`bool`, default:
                  `False`
)
          –
          
            
Because they may be part of an in-progress transaction, files newer
than 7 days old are not deleted by default. If you are sure that
there are no in-progress transactions, then you can set this to True
to delete all files older than `older_than`.

          
        
    

Returns:

    
        
- 
              `CleanupStats`
          –
          
            
The stats of the cleanup operation, including how many bytes were
freed.

          
        
    

  See Also
  
Table.optimize: A more comprehensive
    optimization operation that includes cleanup as well as other operations.

  Notes
  
This function is not available in LanceDb Cloud (since LanceDB
Cloud manages cleanup for you automatically)

            
              Source code in `lancedb/table.py`
              
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
@abstractmethod
def cleanup_old_versions(
    self,
    older_than: Optional[timedelta] = None,
    *,
    delete_unverified: bool = False,
) -> "CleanupStats":
    """
    Clean up old versions of the table, freeing disk space.

    Parameters
    ----------
    older_than: timedelta, default None
        The minimum age of the version to delete. If None, then this defaults
        to two weeks.
    delete_unverified: bool, default False
        Because they may be part of an in-progress transaction, files newer
        than 7 days old are not deleted by default. If you are sure that
        there are no in-progress transactions, then you can set this to True
        to delete all files older than `older_than`.

    Returns
    -------
    CleanupStats
        The stats of the cleanup operation, including how many bytes were
        freed.

    See Also
    --------
    [Table.optimize][lancedb.table.Table.optimize]: A more comprehensive
        optimization operation that includes cleanup as well as other operations.

    Notes
    -----
    This function is not available in LanceDb Cloud (since LanceDB
    Cloud manages cleanup for you automatically)
    """

            
    

            compact_files

  
      `abstractmethod`
  

¶

compact_files(*args, **kwargs)

    

      
Run the compaction process on the table.
This can be run after making several small appends to optimize the table
for faster reads.

Arguments are passed onto Lance's
[compact_files][lance.dataset.DatasetOptimizer.compact_files].
For most cases, the default should be fine.

  See Also
  
Table.optimize: A more comprehensive
    optimization operation that includes cleanup as well as other operations.

  Notes
  
This function is not available in LanceDB Cloud (since LanceDB
Cloud manages compaction for you automatically)

            
              Source code in `lancedb/table.py`
              
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
@abstractmethod
def compact_files(self, *args, **kwargs):
    """
    Run the compaction process on the table.
    This can be run after making several small appends to optimize the table
    for faster reads.

    Arguments are passed onto Lance's
    [compact_files][lance.dataset.DatasetOptimizer.compact_files].
    For most cases, the default should be fine.

    See Also
    --------
    [Table.optimize][lancedb.table.Table.optimize]: A more comprehensive
        optimization operation that includes cleanup as well as other operations.

    Notes
    -----
    This function is not available in LanceDB Cloud (since LanceDB
    Cloud manages compaction for you automatically)
    """

            
    

            optimize

  
      `abstractmethod`
  

¶

optimize(*, cleanup_older_than: Optional[timedelta] = None, delete_unverified: bool = False, retrain: bool = False)

    

      
Optimize the on-disk data and indices for better performance.

Modeled after `VACUUM` in PostgreSQL.

Optimization covers three operations:

- Compaction: Merges small files into larger ones

- Prune: Removes old versions of the dataset

- Index: Optimizes the indices, adding new data to existing indices

Parameters:

    
        
- 
          `cleanup_older_than`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
All files belonging to versions older than this will be removed.  Set
to 0 days to remove all versions except the latest.  The latest version
is never removed.

          
        
        
- 
          `delete_unverified`
              (`bool`, default:
                  `False`
)
          –
          
            
Files leftover from a failed transaction may appear to be part of an
in-progress operation (e.g. appending new data) and these files will not
be deleted unless they are at least 7 days old. If delete_unverified is True
then these files will be deleted regardless of their age.

          
        
        
- 
          `retrain`
              (`bool`, default:
                  `False`
)
          –
          
            
This parameter is no longer used and is deprecated.

          
        
    

  Experimental API
  
The optimization process is undergoing active development and may change.
Our goal with these changes is to improve the performance of optimization and
reduce the complexity.

That being said, it is essential today to run optimize if you want the best
performance.  It should be stable and safe to use in production, but it our
hope that the API may be simplified (or not even need to be called) in the
future.

The frequency an application shoudl call optimize is based on the frequency of
data modifications.  If data is frequently added, deleted, or updated then
optimize should be run frequently.  A good rule of thumb is to run optimize if
you have added or modified 100,000 or more records or run more than 20 data
modification operations.

            
              Source code in `lancedb/table.py`
              
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
@abstractmethod
def optimize(
    self,
    *,
    cleanup_older_than: Optional[timedelta] = None,
    delete_unverified: bool = False,
    retrain: bool = False,
):
    """
    Optimize the on-disk data and indices for better performance.

    Modeled after ``VACUUM`` in PostgreSQL.

    Optimization covers three operations:

     * Compaction: Merges small files into larger ones
     * Prune: Removes old versions of the dataset
     * Index: Optimizes the indices, adding new data to existing indices

    Parameters
    ----------
    cleanup_older_than: timedelta, optional default 7 days
        All files belonging to versions older than this will be removed.  Set
        to 0 days to remove all versions except the latest.  The latest version
        is never removed.
    delete_unverified: bool, default False
        Files leftover from a failed transaction may appear to be part of an
        in-progress operation (e.g. appending new data) and these files will not
        be deleted unless they are at least 7 days old. If delete_unverified is True
        then these files will be deleted regardless of their age.
    retrain: bool, default False
        This parameter is no longer used and is deprecated.

    Experimental API
    ----------------

    The optimization process is undergoing active development and may change.
    Our goal with these changes is to improve the performance of optimization and
    reduce the complexity.

    That being said, it is essential today to run optimize if you want the best
    performance.  It should be stable and safe to use in production, but it our
    hope that the API may be simplified (or not even need to be called) in the
    future.

    The frequency an application shoudl call optimize is based on the frequency of
    data modifications.  If data is frequently added, deleted, or updated then
    optimize should be run frequently.  A good rule of thumb is to run optimize if
    you have added or modified 100,000 or more records or run more than 20 data
    modification operations.
    """

            
    

            list_indices

  
      `abstractmethod`
  

¶

list_indices() -> Iterable[IndexConfig]

    

      
List all indices that have been created with
Table.create_index

            
              Source code in `lancedb/table.py`
              
1529
1530
1531
1532
1533
1534
@abstractmethod
def list_indices(self) -> Iterable[IndexConfig]:
    """
    List all indices that have been created with
    [Table.create_index][lancedb.table.Table.create_index]
    """

            
    

            index_stats

  
      `abstractmethod`
  

¶

index_stats(index_name: str) -> Optional[IndexStatistics]

    

      
Retrieve statistics about an index

Parameters:

    
        
- 
          `index_name`
              (`str`)
          –
          
            
The name of the index to retrieve statistics for

          
        
    

Returns:

    
        
- 
              `IndexStatistics or None`
          –
          
            
The statistics about the index. Returns None if the index does not exist.

          
        
    

            
              Source code in `lancedb/table.py`
              
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
@abstractmethod
def index_stats(self, index_name: str) -> Optional[IndexStatistics]:
    """
    Retrieve statistics about an index

    Parameters
    ----------
    index_name: str
        The name of the index to retrieve statistics for

    Returns
    -------
    IndexStatistics or None
        The statistics about the index. Returns None if the index does not exist.
    """

            
    

            add_columns

  
      `abstractmethod`
  

¶

add_columns(transforms: Dict[str, str] | Field | List[Field] | Schema)

    

      
Add new columns with defined values.

Parameters:

    
        
- 
          `transforms`
              (`Dict[str, str] | Field | List[Field] | Schema`)
          –
          
            
A map of column name to a SQL expression to use to calculate the
value of the new column. These expressions will be evaluated for
each row in the table, and can reference existing columns.
Alternatively, a pyarrow Field or Schema can be provided to add
new columns with the specified data types. The new columns will
be initialized with null values.

          
        
    

Returns:

    
        
- 
              `AddColumnsResult`
          –
          
            
version: the new version number of the table after adding columns.

          
        
    

            
              Source code in `lancedb/table.py`
              
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
@abstractmethod
def add_columns(
    self, transforms: Dict[str, str] | pa.Field | List[pa.Field] | pa.Schema
):
    """
    Add new columns with defined values.

    Parameters
    ----------
    transforms: Dict[str, str], pa.Field, List[pa.Field], pa.Schema
        A map of column name to a SQL expression to use to calculate the
        value of the new column. These expressions will be evaluated for
        each row in the table, and can reference existing columns.
        Alternatively, a pyarrow Field or Schema can be provided to add
        new columns with the specified data types. The new columns will
        be initialized with null values.

    Returns
    -------
    AddColumnsResult
        version: the new version number of the table after adding columns.
    """

            
    

            alter_columns

  
      `abstractmethod`
  

¶

alter_columns(*alterations: Iterable[Dict[str, str]])

    

      
Alter column names and nullability.

Parameters:

    
        
- 
          `alterations`
              (`Iterable[Dict[str, Any]]`, default:
                  `()`
)
          –
          
            
A sequence of dictionaries, each with the following keys:
- "path": str
    The column path to alter. For a top-level column, this is the name.
    For a nested column, this is the dot-separated path, e.g. "a.b.c".
- "rename": str, optional
    The new name of the column. If not specified, the column name is
    not changed.
- "data_type": pyarrow.DataType, optional
   The new data type of the column. Existing values will be casted
   to this type. If not specified, the column data type is not changed.
- "nullable": bool, optional
    Whether the column should be nullable. If not specified, the column
    nullability is not changed. Only non-nullable columns can be changed
    to nullable. Currently, you cannot change a nullable column to
    non-nullable.

          
        
    

Returns:

    
        
- 
              `AlterColumnsResult`
          –
          
            
version: the new version number of the table after the alteration.

          
        
    

            
              Source code in `lancedb/table.py`
              
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
@abstractmethod
def alter_columns(self, *alterations: Iterable[Dict[str, str]]):
    """
    Alter column names and nullability.

    Parameters
    ----------
    alterations : Iterable[Dict[str, Any]]
        A sequence of dictionaries, each with the following keys:
        - "path": str
            The column path to alter. For a top-level column, this is the name.
            For a nested column, this is the dot-separated path, e.g. "a.b.c".
        - "rename": str, optional
            The new name of the column. If not specified, the column name is
            not changed.
        - "data_type": pyarrow.DataType, optional
           The new data type of the column. Existing values will be casted
           to this type. If not specified, the column data type is not changed.
        - "nullable": bool, optional
            Whether the column should be nullable. If not specified, the column
            nullability is not changed. Only non-nullable columns can be changed
            to nullable. Currently, you cannot change a nullable column to
            non-nullable.

    Returns
    -------
    AlterColumnsResult
        version: the new version number of the table after the alteration.
    """

            
    

            drop_columns

  
      `abstractmethod`
  

¶

drop_columns(columns: Iterable[str]) -> DropColumnsResult

    

      
Drop columns from the table.

Parameters:

    
        
- 
          `columns`
              (`Iterable[str]`)
          –
          
            
The names of the columns to drop.

          
        
    

Returns:

    
        
- 
              `DropColumnsResult`
          –
          
            
version: the new version number of the table dropping the columns.

          
        
    

            
              Source code in `lancedb/table.py`
              
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
@abstractmethod
def drop_columns(self, columns: Iterable[str]) -> DropColumnsResult:
    """
    Drop columns from the table.

    Parameters
    ----------
    columns : Iterable[str]
        The names of the columns to drop.

    Returns
    -------
    DropColumnsResult
        version: the new version number of the table dropping the columns.
    """

            
    

            checkout

  
      `abstractmethod`
  

¶

checkout(version: Union[int, str])

    

      
Checks out a specific version of the Table

Any read operation on the table will now access the data at the checked out
version. As a consequence, calling this method will disable any read consistency
interval that was previously set.

This is a read-only operation that turns the table into a sort of "view"
or "detached head".  Other table instances will not be affected.  To make the
change permanent you can use the `[Self::restore]` method.

Any operation that modifies the table will fail while the table is in a checked
out state.

Parameters:

    
        
- 
          `version`
              (`Union[int, str]`)
          –
          
            
The version to check out. A version number (`int`) or a tag
(`str`) can be provided.

          
        
        
- 
          `To`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
@abstractmethod
def checkout(self, version: Union[int, str]):
    """
    Checks out a specific version of the Table

    Any read operation on the table will now access the data at the checked out
    version. As a consequence, calling this method will disable any read consistency
    interval that was previously set.

    This is a read-only operation that turns the table into a sort of "view"
    or "detached head".  Other table instances will not be affected.  To make the
    change permanent you can use the `[Self::restore]` method.

    Any operation that modifies the table will fail while the table is in a checked
    out state.

    Parameters
    ----------
    version: int | str,
        The version to check out. A version number (`int`) or a tag
        (`str`) can be provided.

    To return the table to a normal state use `[Self::checkout_latest]`
    """

            
    

            checkout_latest

  
      `abstractmethod`
  

¶

checkout_latest()

    

      
Ensures the table is pointing at the latest version

This can be used to manually update a table when the read_consistency_interval
is None
It can also be used to undo a `[Self::checkout]` operation

            
              Source code in `lancedb/table.py`
              
1646
1647
1648
1649
1650
1651
1652
1653
1654
@abstractmethod
def checkout_latest(self):
    """
    Ensures the table is pointing at the latest version

    This can be used to manually update a table when the read_consistency_interval
    is None
    It can also be used to undo a `[Self::checkout]` operation
    """

            
    

            restore

  
      `abstractmethod`
  

¶

restore(version: Optional[Union[int, str]] = None)

    

      
Restore a version of the table. This is an in-place operation.

This creates a new version where the data is equivalent to the
specified previous version. Data is not copied (as of python-v0.2.1).

Parameters:

    
        
- 
          `version`
              (`int or str`, default:
                  `None`
)
          –
          
            
The version number or version tag to restore.
If unspecified then restores the currently checked out version.
If the currently checked out version is the
latest version then this is a no-op.

          
        
    

            
              Source code in `lancedb/table.py`
              
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
@abstractmethod
def restore(self, version: Optional[Union[int, str]] = None):
    """Restore a version of the table. This is an in-place operation.

    This creates a new version where the data is equivalent to the
    specified previous version. Data is not copied (as of python-v0.2.1).

    Parameters
    ----------
    version : int or str, default None
        The version number or version tag to restore.
        If unspecified then restores the currently checked out version.
        If the currently checked out version is the
        latest version then this is a no-op.
    """

            
    

            list_versions

  
      `abstractmethod`
  

¶

list_versions() -> List[Dict[str, Any]]

    

      
List all versions of the table

            
              Source code in `lancedb/table.py`
              
1672
1673
1674
@abstractmethod
def list_versions(self) -> List[Dict[str, Any]]:
    """List all versions of the table"""

            
    

            uses_v2_manifest_paths

  
      `abstractmethod`
  

¶

uses_v2_manifest_paths() -> bool

    

      
Check if the table is using the new v2 manifest paths.

Returns:

    
        
- 
              `bool`
          –
          
            
True if the table is using the new v2 manifest paths, False otherwise.

          
        
    

            
              Source code in `lancedb/table.py`
              
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
@abstractmethod
def uses_v2_manifest_paths(self) -> bool:
    """
    Check if the table is using the new v2 manifest paths.

    Returns
    -------
    bool
        True if the table is using the new v2 manifest paths, False otherwise.
    """

            
    

            migrate_v2_manifest_paths

  
      `abstractmethod`
  

¶

migrate_v2_manifest_paths()

    

      
Migrate the manifest paths to the new format.

This will update the manifest to use the new v2 format for paths.

This function is idempotent, and can be run multiple times without
changing the state of the object store.

Danger

This should not be run while other concurrent operations are happening.
And it should also run until completion before resuming other operations.

You can use
Table.uses_v2_manifest_paths
to check if the table is already using the new path style.

            
              Source code in `lancedb/table.py`
              
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
@abstractmethod
def migrate_v2_manifest_paths(self):
    """
    Migrate the manifest paths to the new format.

    This will update the manifest to use the new v2 format for paths.

    This function is idempotent, and can be run multiple times without
    changing the state of the object store.

    !!! danger

        This should not be run while other concurrent operations are happening.
        And it should also run until completion before resuming other operations.

    You can use
    [Table.uses_v2_manifest_paths][lancedb.table.Table.uses_v2_manifest_paths]
    to check if the table is already using the new path style.
    """

            
    

  

    

            lancedb.table.FragmentStatistics

  
      `dataclass`
  

¶

    

      
Statistics about fragments.

Attributes:

    
        
- 
          `num_fragments`
              (`int`)
          –
          
            
The total number of fragments in the table.

          
        
        
- 
          `num_small_fragments`
              (`int`)
          –
          
            
The total number of small fragments in the table.
Small fragments have low row counts and may need to be compacted.

          
        
        
- 
          `lengths`
              (`FragmentSummaryStats`)
          –
          
            
Statistics about the number of rows in the table fragments.

          
        
    

              
                Source code in `lancedb/table.py`
                
4711
4712
4713
4714
4715
4716
4717
4718
4719
4720
4721
4722
4723
4724
4725
4726
4727
4728
4729
@dataclass
class FragmentStatistics:
    """
    Statistics about fragments.

    Attributes
    ----------
    num_fragments: int
        The total number of fragments in the table.
    num_small_fragments: int
        The total number of small fragments in the table.
        Small fragments have low row counts and may need to be compacted.
    lengths: FragmentSummaryStats
        Statistics about the number of rows in the table fragments.
    """

    num_fragments: int
    num_small_fragments: int
    lengths: FragmentSummaryStats

              

  

  

    

            lancedb.table.FragmentSummaryStats

  
      `dataclass`
  

¶

    

      
Statistics about fragments sizes

Attributes:

    
        
- 
          `min`
              (`int`)
          –
          
            
The number of rows in the fragment with the fewest rows.

          
        
        
- 
          `max`
              (`int`)
          –
          
            
The number of rows in the fragment with the most rows.

          
        
        
- 
          `mean`
              (`int`)
          –
          
            
The mean number of rows in the fragments.

          
        
        
- 
          `p25`
              (`int`)
          –
          
            
The 25th percentile of number of rows in the fragments.

          
        
        
- 
          `p50`
              (`int`)
          –
          
            
The 50th percentile of number of rows in the fragments.

          
        
        
- 
          `p75`
              (`int`)
          –
          
            
The 75th percentile of number of rows in the fragments.

          
        
        
- 
          `p99`
              (`int`)
          –
          
            
The 99th percentile of number of rows in the fragments.

          
        
    

              
                Source code in `lancedb/table.py`
                
4732
4733
4734
4735
4736
4737
4738
4739
4740
4741
4742
4743
4744
4745
4746
4747
4748
4749
4750
4751
4752
4753
4754
4755
4756
4757
4758
4759
4760
4761
@dataclass
class FragmentSummaryStats:
    """
    Statistics about fragments sizes

    Attributes
    ----------
    min: int
        The number of rows in the fragment with the fewest rows.
    max: int
        The number of rows in the fragment with the most rows.
    mean: int
        The mean number of rows in the fragments.
    p25: int
        The 25th percentile of number of rows in the fragments.
    p50: int
        The 50th percentile of number of rows in the fragments.
    p75: int
        The 75th percentile of number of rows in the fragments.
    p99: int
        The 99th percentile of number of rows in the fragments.
    """

    min: int
    max: int
    mean: int
    p25: int
    p50: int
    p75: int
    p99: int

              

  

  

    

            lancedb.table.Tags

¶

    

      
Table tag manager.

              
                Source code in `lancedb/table.py`
                
4764
4765
4766
4767
4768
4769
4770
4771
4772
4773
4774
4775
4776
4777
4778
4779
4780
4781
4782
4783
4784
4785
4786
4787
4788
4789
4790
4791
4792
4793
4794
4795
4796
4797
4798
4799
4800
4801
4802
4803
4804
4805
4806
4807
4808
4809
4810
4811
4812
4813
4814
4815
4816
4817
4818
4819
4820
4821
4822
4823
4824
4825
4826
4827
4828
4829
4830
class Tags:
    """
    Table tag manager.
    """

    def __init__(self, table):
        self._table = table

    def list(self) -> Dict[str, Tag]:
        """
        List all table tags.

        Returns
        -------
        dict[str, Tag]
            A dictionary mapping tag names to version numbers.
        """
        return LOOP.run(self._table.tags.list())

    def get_version(self, tag: str) -> int:
        """
        Get the version of a tag.

        Parameters
        ----------
        tag: str,
            The name of the tag to get the version for.
        """
        return LOOP.run(self._table.tags.get_version(tag))

    def create(self, tag: str, version: int) -> None:
        """
        Create a tag for a given table version.

        Parameters
        ----------
        tag: str,
            The name of the tag to create. This name must be unique among all tag
            names for the table.
        version: int,
            The table version to tag.
        """
        LOOP.run(self._table.tags.create(tag, version))

    def delete(self, tag: str) -> None:
        """
        Delete tag from the table.

        Parameters
        ----------
        tag: str,
            The name of the tag to delete.
        """
        LOOP.run(self._table.tags.delete(tag))

    def update(self, tag: str, version: int) -> None:
        """
        Update tag to a new version.

        Parameters
        ----------
        tag: str,
            The name of the tag to update.
        version: int,
            The new table version to tag.
        """
        LOOP.run(self._table.tags.update(tag, version))

              

  

            list

¶

list() -> Dict[str, Tag]

    

      
List all table tags.

Returns:

    
        
- 
              `dict[str, Tag]`
          –
          
            
A dictionary mapping tag names to version numbers.

          
        
    

            
              Source code in `lancedb/table.py`
              
4772
4773
4774
4775
4776
4777
4778
4779
4780
4781
def list(self) -> Dict[str, Tag]:
    """
    List all table tags.

    Returns
    -------
    dict[str, Tag]
        A dictionary mapping tag names to version numbers.
    """
    return LOOP.run(self._table.tags.list())

            
    

            get_version

¶

get_version(tag: str) -> int

    

      
Get the version of a tag.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to get the version for.

          
        
    

            
              Source code in `lancedb/table.py`
              
4783
4784
4785
4786
4787
4788
4789
4790
4791
4792
def get_version(self, tag: str) -> int:
    """
    Get the version of a tag.

    Parameters
    ----------
    tag: str,
        The name of the tag to get the version for.
    """
    return LOOP.run(self._table.tags.get_version(tag))

            
    

            create

¶

create(tag: str, version: int) -> None

    

      
Create a tag for a given table version.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to create. This name must be unique among all tag
names for the table.

          
        
        
- 
          `version`
              (`int`)
          –
          
            
The table version to tag.

          
        
    

            
              Source code in `lancedb/table.py`
              
4794
4795
4796
4797
4798
4799
4800
4801
4802
4803
4804
4805
4806
def create(self, tag: str, version: int) -> None:
    """
    Create a tag for a given table version.

    Parameters
    ----------
    tag: str,
        The name of the tag to create. This name must be unique among all tag
        names for the table.
    version: int,
        The table version to tag.
    """
    LOOP.run(self._table.tags.create(tag, version))

            
    

            delete

¶

delete(tag: str) -> None

    

      
Delete tag from the table.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to delete.

          
        
    

            
              Source code in `lancedb/table.py`
              
4808
4809
4810
4811
4812
4813
4814
4815
4816
4817
def delete(self, tag: str) -> None:
    """
    Delete tag from the table.

    Parameters
    ----------
    tag: str,
        The name of the tag to delete.
    """
    LOOP.run(self._table.tags.delete(tag))

            
    

            update

¶

update(tag: str, version: int) -> None

    

      
Update tag to a new version.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to update.

          
        
        
- 
          `version`
              (`int`)
          –
          
            
The new table version to tag.

          
        
    

            
              Source code in `lancedb/table.py`
              
4819
4820
4821
4822
4823
4824
4825
4826
4827
4828
4829
4830
def update(self, tag: str, version: int) -> None:
    """
    Update tag to a new version.

    Parameters
    ----------
    tag: str,
        The name of the tag to update.
    version: int,
        The new table version to tag.
    """
    LOOP.run(self._table.tags.update(tag, version))

            
    

  

    

## Querying (Synchronous)¶

            lancedb.query.Query

¶

    
            

              Bases: `BaseModel`

      
A LanceDB Query

Queries are constructed by the `Table.search` method.  This class is a
python representation of the query.  Normally you will not need to interact
with this class directly.  You can build up a query and execute it using
collection methods such as `to_batches()`, `to_arrow()`, `to_pandas()`,
etc.

However, you can use the `to_query()` method to get the underlying query object.
This can be useful for serializing a query or using it in a different context.

Attributes:

    
        
- 
          `filter`
              (`Optional[str]`)
          –
          
            
sql filter to refine the query with

          
        
        
- 
          `limit`
              (`Optional[int]`)
          –
          
            
The limit on the number of results to return.  If this is a vector or FTS query,
then this is required.  If this is a plain SQL query, then this is optional.

          
        
        
- 
          `offset`
              (`Optional[int]`)
          –
          
            
The offset to start fetching results from

This is ignored for vector / FTS search (will be None).

          
        
        
- 
          `columns`
              (`Optional[Union[List[str], Dict[str, str]]]`)
          –
          
            
which columns to return in the results

This can be a list of column names or a dictionary.  If it is a dictionary,
then the keys are the column names and the values are sql expressions to
use to calculate the result.

If this is None then all columns are returned.  This can be expensive.

          
        
        
- 
          `with_row_id`
              (`Optional[bool]`)
          –
          
            
if True then include the row id in the results

          
        
        
- 
          `vector`
              (`Optional[Union[List[float], List[List[float]], Array, List[Array]]]`)
          –
          
            
the vector to search for, if this a vector search or hybrid search.  It will
be None for full text search and plain SQL filtering.

          
        
        
- 
          `vector_column`
              (`Optional[str]`)
          –
          
            
the name of the vector column to use for vector search

If this is None then a default vector column will be used.

          
        
        
- 
          `distance_type`
              (`Optional[str]`)
          –
          
            
the distance type to use for vector search

This can be l2 (default), cosine and dot.  See metric definitions for
more details.

If this is not a vector search this will be None.

          
        
        
- 
          `postfilter`
              (`bool`)
          –
          
            
if True then apply the filter after vector / FTS search.  This is ignored for
plain SQL filtering.

          
        
        
- 
          `nprobes`
              (`Optional[int]`)
          –
          
            
The number of IVF partitions to search.  If this is None then a default
number of partitions will be used.

- 

A higher number makes search more accurate but also slower.

- 

See discussion in [Querying an ANN Index][querying-an-ann-index] for
  tuning advice.

Will be None if this is not a vector search.

          
        
        
- 
          `refine_factor`
              (`Optional[int]`)
          –
          
            
Refine the results by reading extra elements and re-ranking them in memory.

- 

A higher number makes search more accurate but also slower.

- 

See discussion in [Querying an ANN Index][querying-an-ann-index] for
  tuning advice.

Will be None if this is not a vector search.

          
        
        
- 
          `lower_bound`
              (`Optional[float]`)
          –
          
            
The lower bound for distance search

Only results with a distance greater than or equal to this value
will be returned.

This will only be set on vector search.

          
        
        
- 
          `upper_bound`
              (`Optional[float]`)
          –
          
            
The upper bound for distance search

Only results with a distance less than or equal to this value
will be returned.

This will only be set on vector search.

          
        
        
- 
          `ef`
              (`Optional[int]`)
          –
          
            
The size of the nearest neighbor list maintained during HNSW search

This will only be set on vector search.

          
        
        
- 
          `full_text_query`
              (`Optional[Union[str, dict]]`)
          –
          
            
The full text search query

This can be a string or a dictionary.  A dictionary will be used to search
multiple columns.  The keys are the column names and the values are the
search queries.

This will only be set on FTS or hybrid queries.

          
        
        
- 
          `fast_search`
              (`Optional[bool]`)
          –
          
            
Skip a flat search of unindexed data. This will improve
search performance but search results will not include unindexed data.

The default is False

          
        
    

              
                Source code in `lancedb/query.py`
                
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
class Query(pydantic.BaseModel):
    """A LanceDB Query

    Queries are constructed by the `Table.search` method.  This class is a
    python representation of the query.  Normally you will not need to interact
    with this class directly.  You can build up a query and execute it using
    collection methods such as `to_batches()`, `to_arrow()`, `to_pandas()`,
    etc.

    However, you can use the `to_query()` method to get the underlying query object.
    This can be useful for serializing a query or using it in a different context.

    Attributes
    ----------
    filter : Optional[str]
        sql filter to refine the query with
    limit : Optional[int]
        The limit on the number of results to return.  If this is a vector or FTS query,
        then this is required.  If this is a plain SQL query, then this is optional.
    offset: Optional[int]
        The offset to start fetching results from

        This is ignored for vector / FTS search (will be None).
    columns : Optional[Union[List[str], Dict[str, str]]]
        which columns to return in the results

        This can be a list of column names or a dictionary.  If it is a dictionary,
        then the keys are the column names and the values are sql expressions to
        use to calculate the result.

        If this is None then all columns are returned.  This can be expensive.
    with_row_id : Optional[bool]
        if True then include the row id in the results
    vector : Optional[Union[List[float], List[List[float]], pa.Array, List[pa.Array]]]
        the vector to search for, if this a vector search or hybrid search.  It will
        be None for full text search and plain SQL filtering.
    vector_column : Optional[str]
        the name of the vector column to use for vector search

        If this is None then a default vector column will be used.
    distance_type : Optional[str]
        the distance type to use for vector search

        This can be l2 (default), cosine and dot.  See [metric definitions][search] for
        more details.

        If this is not a vector search this will be None.
    postfilter : bool
        if True then apply the filter after vector / FTS search.  This is ignored for
        plain SQL filtering.
    nprobes : Optional[int]
        The number of IVF partitions to search.  If this is None then a default
        number of partitions will be used.

        - A higher number makes search more accurate but also slower.

        - See discussion in [Querying an ANN Index][querying-an-ann-index] for
          tuning advice.

        Will be None if this is not a vector search.
    refine_factor : Optional[int]
        Refine the results by reading extra elements and re-ranking them in memory.

        - A higher number makes search more accurate but also slower.

        - See discussion in [Querying an ANN Index][querying-an-ann-index] for
          tuning advice.

        Will be None if this is not a vector search.
    lower_bound : Optional[float]
        The lower bound for distance search

        Only results with a distance greater than or equal to this value
        will be returned.

        This will only be set on vector search.
    upper_bound : Optional[float]
        The upper bound for distance search

        Only results with a distance less than or equal to this value
        will be returned.

        This will only be set on vector search.
    ef : Optional[int]
        The size of the nearest neighbor list maintained during HNSW search

        This will only be set on vector search.
    full_text_query : Optional[Union[str, dict]]
        The full text search query

        This can be a string or a dictionary.  A dictionary will be used to search
        multiple columns.  The keys are the column names and the values are the
        search queries.

        This will only be set on FTS or hybrid queries.
    fast_search: Optional[bool]
        Skip a flat search of unindexed data. This will improve
        search performance but search results will not include unindexed data.

        The default is False
    """

    # The name of the vector column to use for vector search.
    vector_column: Optional[str] = None

    # vector to search for
    #
    # Note: today this will be floats on the sync path and pa.Array on the async
    # path though in the future we should unify this to pa.Array everywhere
    vector: Annotated[
        Optional[Union[List[float], List[List[float]], pa.Array, List[pa.Array]]],
        ensure_vector_query,
    ] = None

    # sql filter to refine the query with
    filter: Optional[str] = None

    # if True then apply the filter after vector search
    postfilter: Optional[bool] = None

    # full text search query
    full_text_query: Optional[FullTextSearchQuery] = None

    # top k results to return
    limit: Optional[int] = None

    # distance type to use for vector search
    distance_type: Optional[str] = None

    # which columns to return in the results
    columns: Optional[Union[List[str], Dict[str, str]]] = None

    # minimum number of IVF partitions to search
    #
    # If None then a default value (20) will be used.
    minimum_nprobes: Optional[int] = None

    # maximum number of IVF partitions to search
    #
    # If None then a default value (20) will be used.
    #
    # If 0 then no limit will be applied and all partitions could be searched
    # if needed to satisfy the limit.
    maximum_nprobes: Optional[int] = None

    # lower bound for distance search
    lower_bound: Optional[float] = None

    # upper bound for distance search
    upper_bound: Optional[float] = None

    # multiplier for the number of results to inspect for reranking
    refine_factor: Optional[int] = None

    # if true, include the row id in the results
    with_row_id: Optional[bool] = None

    # offset to start fetching results from
    offset: Optional[int] = None

    # if true, will only search the indexed data
    fast_search: Optional[bool] = None

    # size of the nearest neighbor list maintained during HNSW search
    ef: Optional[int] = None

    # Bypass the vector index and use a brute force search
    bypass_vector_index: Optional[bool] = None

    @classmethod
    def from_inner(cls, req: PyQueryRequest) -> Self:
        query = cls()
        query.limit = req.limit
        query.offset = req.offset
        query.filter = req.filter
        query.full_text_query = req.full_text_search
        query.columns = req.select
        query.with_row_id = req.with_row_id
        query.vector_column = req.column
        query.vector = req.query_vector
        query.distance_type = req.distance_type
        query.minimum_nprobes = req.minimum_nprobes
        query.maximum_nprobes = req.maximum_nprobes
        query.lower_bound = req.lower_bound
        query.upper_bound = req.upper_bound
        query.ef = req.ef
        query.refine_factor = req.refine_factor
        query.bypass_vector_index = req.bypass_vector_index
        query.postfilter = req.postfilter
        if req.full_text_search is not None:
            query.full_text_query = FullTextSearchQuery(
                columns=None,
                query=req.full_text_search,
            )
        return query

    # This tells pydantic to allow custom types (needed for the `vector` query since
    # pa.Array wouln't be allowed otherwise)
    if PYDANTIC_VERSION.major < 2:  # Pydantic 1.x compat

        class Config:
            arbitrary_types_allowed = True
    else:
        model_config = {"arbitrary_types_allowed": True}

              

  

  

    

            lancedb.query.LanceQueryBuilder

¶

    
            

              Bases: `ABC`

      
An abstract query builder. Subclasses are defined for vector search,
full text search, hybrid, and plain SQL filtering.

              
                Source code in `lancedb/query.py`
                
 544
 545
 546
 547
 548
 549
 550
 551
 552
 553
 554
 555
 556
 557
 558
 559
 560
 561
 562
 563
 564
 565
 566
 567
 568
 569
 570
 571
 572
 573
 574
 575
 576
 577
 578
 579
 580
 581
 582
 583
 584
 585
 586
 587
 588
 589
 590
 591
 592
 593
 594
 595
 596
 597
 598
 599
 600
 601
 602
 603
 604
 605
 606
 607
 608
 609
 610
 611
 612
 613
 614
 615
 616
 617
 618
 619
 620
 621
 622
 623
 624
 625
 626
 627
 628
 629
 630
 631
 632
 633
 634
 635
 636
 637
 638
 639
 640
 641
 642
 643
 644
 645
 646
 647
 648
 649
 650
 651
 652
 653
 654
 655
 656
 657
 658
 659
 660
 661
 662
 663
 664
 665
 666
 667
 668
 669
 670
 671
 672
 673
 674
 675
 676
 677
 678
 679
 680
 681
 682
 683
 684
 685
 686
 687
 688
 689
 690
 691
 692
 693
 694
 695
 696
 697
 698
 699
 700
 701
 702
 703
 704
 705
 706
 707
 708
 709
 710
 711
 712
 713
 714
 715
 716
 717
 718
 719
 720
 721
 722
 723
 724
 725
 726
 727
 728
 729
 730
 731
 732
 733
 734
 735
 736
 737
 738
 739
 740
 741
 742
 743
 744
 745
 746
 747
 748
 749
 750
 751
 752
 753
 754
 755
 756
 757
 758
 759
 760
 761
 762
 763
 764
 765
 766
 767
 768
 769
 770
 771
 772
 773
 774
 775
 776
 777
 778
 779
 780
 781
 782
 783
 784
 785
 786
 787
 788
 789
 790
 791
 792
 793
 794
 795
 796
 797
 798
 799
 800
 801
 802
 803
 804
 805
 806
 807
 808
 809
 810
 811
 812
 813
 814
 815
 816
 817
 818
 819
 820
 821
 822
 823
 824
 825
 826
 827
 828
 829
 830
 831
 832
 833
 834
 835
 836
 837
 838
 839
 840
 841
 842
 843
 844
 845
 846
 847
 848
 849
 850
 851
 852
 853
 854
 855
 856
 857
 858
 859
 860
 861
 862
 863
 864
 865
 866
 867
 868
 869
 870
 871
 872
 873
 874
 875
 876
 877
 878
 879
 880
 881
 882
 883
 884
 885
 886
 887
 888
 889
 890
 891
 892
 893
 894
 895
 896
 897
 898
 899
 900
 901
 902
 903
 904
 905
 906
 907
 908
 909
 910
 911
 912
 913
 914
 915
 916
 917
 918
 919
 920
 921
 922
 923
 924
 925
 926
 927
 928
 929
 930
 931
 932
 933
 934
 935
 936
 937
 938
 939
 940
 941
 942
 943
 944
 945
 946
 947
 948
 949
 950
 951
 952
 953
 954
 955
 956
 957
 958
 959
 960
 961
 962
 963
 964
 965
 966
 967
 968
 969
 970
 971
 972
 973
 974
 975
 976
 977
 978
 979
 980
 981
 982
 983
 984
 985
 986
 987
 988
 989
 990
 991
 992
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
class LanceQueryBuilder(ABC):
    """An abstract query builder. Subclasses are defined for vector search,
    full text search, hybrid, and plain SQL filtering.
    """

    @classmethod
    def create(
        cls,
        table: "Table",
        query: Optional[Union[np.ndarray, str, "PIL.Image.Image", Tuple]],
        query_type: str,
        vector_column_name: str,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
        fast_search: bool = None,
    ) -> Self:
        """
        Create a query builder based on the given query and query type.

        Parameters
        ----------
        table: Table
            The table to query.
        query: Optional[Union[np.ndarray, str, "PIL.Image.Image", Tuple]]
            The query to use. If None, an empty query builder is returned
            which performs simple SQL filtering.
        query_type: str
            The type of query to perform. One of "vector", "fts", "hybrid", or "auto".
            If "auto", the query type is inferred based on the query.
        vector_column_name: str
            The name of the vector column to use for vector search.
        fast_search: bool
            Skip flat search of unindexed data.
        """
        # Check hybrid search first as it supports empty query pattern
        if query_type == "hybrid":
            # hybrid fts and vector query
            return LanceHybridQueryBuilder(
                table, query, vector_column_name, fts_columns=fts_columns
            )

        if query is None:
            return LanceEmptyQueryBuilder(table)

        # remember the string query for reranking purpose
        str_query = query if isinstance(query, str) else None

        # convert "auto" query_type to "vector", "fts"
        # or "hybrid" and convert the query to vector if needed
        query, query_type = cls._resolve_query(
            table, query, query_type, vector_column_name
        )

        if query_type == "hybrid":
            return LanceHybridQueryBuilder(
                table, query, vector_column_name, fts_columns=fts_columns
            )

        if isinstance(query, (str, FullTextQuery)):
            # fts
            return LanceFtsQueryBuilder(
                table,
                query,
                ordering_field_name=ordering_field_name,
                fts_columns=fts_columns,
            )

        if isinstance(query, list):
            query = np.array(query, dtype=np.float32)
        elif isinstance(query, np.ndarray):
            query = query.astype(np.float32)
        else:
            raise TypeError(f"Unsupported query type: {type(query)}")

        return LanceVectorQueryBuilder(
            table, query, vector_column_name, str_query, fast_search
        )

    @classmethod
    def _resolve_query(cls, table, query, query_type, vector_column_name):
        # If query_type is fts, then query must be a string.
        # otherwise raise TypeError
        if query_type == "fts":
            if not isinstance(query, (str, FullTextQuery)):
                raise TypeError(
                    f"'fts' query must be a string or FullTextQuery: {type(query)}"
                )
            return query, query_type
        elif query_type == "vector":
            query = cls._query_to_vector(table, query, vector_column_name)
            return query, query_type
        elif query_type == "auto":
            if isinstance(query, (list, np.ndarray)):
                return query, "vector"
            else:
                conf = table.embedding_functions.get(vector_column_name)
                if conf is not None:
                    query = conf.function.compute_query_embeddings_with_retry(query)[0]
                    return query, "vector"
                else:
                    return query, "fts"
        else:
            raise ValueError(
                f"Invalid query_type, must be 'vector', 'fts', or 'auto': {query_type}"
            )

    @classmethod
    def _query_to_vector(cls, table, query, vector_column_name):
        if isinstance(query, (list, np.ndarray)):
            return query
        conf = table.embedding_functions.get(vector_column_name)
        if conf is not None:
            return conf.function.compute_query_embeddings_with_retry(query)[0]
        else:
            msg = f"No embedding function for {vector_column_name}"
            raise ValueError(msg)

    def __init__(self, table: "Table"):
        self._table = table
        self._limit = None
        self._offset = None
        self._columns = None
        self._where = None
        self._postfilter = None
        self._with_row_id = None
        self._vector = None
        self._text = None
        self._ef = None
        self._bypass_vector_index = None

    @deprecation.deprecated(
        deprecated_in="0.3.1",
        removed_in="0.4.0",
        current_version=__version__,
        details="Use to_pandas() instead",
    )
    def to_df(self) -> "pd.DataFrame":
        """
        *Deprecated alias for `to_pandas()`. Please use `to_pandas()` instead.*

        Execute the query and return the results as a pandas DataFrame.
        In addition to the selected columns, LanceDB also returns a vector
        and also the "_distance" column which is the distance between the query
        vector and the returned vector.
        """
        return self.to_pandas()

    def to_pandas(
        self,
        flatten: Optional[Union[int, bool]] = None,
        *,
        timeout: Optional[timedelta] = None,
    ) -> "pd.DataFrame":
        """
        Execute the query and return the results as a pandas DataFrame.
        In addition to the selected columns, LanceDB also returns a vector
        and also the "_distance" column which is the distance between the query
        vector and the returned vector.

        Parameters
        ----------
        flatten: Optional[Union[int, bool]]
            If flatten is True, flatten all nested columns.
            If flatten is an integer, flatten the nested columns up to the
            specified depth.
            If unspecified, do not flatten the nested columns.
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        tbl = flatten_columns(self.to_arrow(timeout=timeout), flatten)
        return tbl.to_pandas()

    @abstractmethod
    def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
        """
        Execute the query and return the results as an
        [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

        In addition to the selected columns, LanceDB also returns a vector
        and also the "_distance" column which is the distance between the query
        vector and the returned vectors.

        Parameters
        ----------
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        raise NotImplementedError

    @abstractmethod
    def to_batches(
        self,
        /,
        batch_size: Optional[int] = None,
        *,
        timeout: Optional[timedelta] = None,
    ) -> pa.RecordBatchReader:
        """
        Execute the query and return the results as a pyarrow
        [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html)

        Parameters
        ----------
        batch_size: int
            The maximum number of selected records in a RecordBatch object.
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        raise NotImplementedError

    def to_list(self, *, timeout: Optional[timedelta] = None) -> List[dict]:
        """
        Execute the query and return the results as a list of dictionaries.

        Each list entry is a dictionary with the selected column names as keys,
        or all table columns if `select` is not called. The vector and the "_distance"
        fields are returned whether or not they're explicitly selected.

        Parameters
        ----------
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        return self.to_arrow(timeout=timeout).to_pylist()

    def to_pydantic(
        self, model: type[T], *, timeout: Optional[timedelta] = None
    ) -> list[T]:
        """Return the table as a list of pydantic models.

        Parameters
        ----------
        model: Type[LanceModel]
            The pydantic model to use.
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.

        Returns
        -------
        List[LanceModel]
        """
        return [model(**row) for row in self.to_arrow(timeout=timeout).to_pylist()]

    def to_polars(self, *, timeout: Optional[timedelta] = None) -> "pl.DataFrame":
        """
        Execute the query and return the results as a Polars DataFrame.
        In addition to the selected columns, LanceDB also returns a vector
        and also the "_distance" column which is the distance between the query
        vector and the returned vector.

        Parameters
        ----------
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        import polars as pl

        return pl.from_arrow(self.to_arrow(timeout=timeout))

    def limit(self, limit: Union[int, None]) -> Self:
        """Set the maximum number of results to return.

        Parameters
        ----------
        limit: int
            The maximum number of results to return.
            The default query limit is 10 results.
            For ANN/KNN queries, you must specify a limit.
            For plain searches, all records are returned if limit not set.
            *WARNING* if you have a large dataset, setting
            the limit to a large number, e.g. the table size,
            can potentially result in reading a
            large amount of data into memory and cause
            out of memory issues.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        if limit is None or limit <= 0:
            if isinstance(self, LanceVectorQueryBuilder):
                raise ValueError("Limit is required for ANN/KNN queries")
            else:
                self._limit = None
        else:
            self._limit = limit
        return self

    def offset(self, offset: int) -> Self:
        """Set the offset for the results.

        Parameters
        ----------
        offset: int
            The offset to start fetching results from.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        if offset is None or offset <= 0:
            self._offset = 0
        else:
            self._offset = offset
        return self

    def select(self, columns: Union[list[str], dict[str, str]]) -> Self:
        """Set the columns to return.

        Parameters
        ----------
        columns: list of str, or dict of str to str default None
            List of column names to be fetched.
            Or a dictionary of column names to SQL expressions.
            All columns are fetched if None or unspecified.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        if isinstance(columns, list) or isinstance(columns, dict):
            self._columns = columns
        else:
            raise ValueError("columns must be a list or a dictionary")
        return self

    def where(self, where: str, prefilter: bool = True) -> Self:
        """Set the where clause.

        Parameters
        ----------
        where: str
            The where clause which is a valid SQL where clause. See
            `Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
            for valid SQL expressions.
        prefilter: bool, default True
            If True, apply the filter before vector search, otherwise the
            filter is applied on the result of vector search.
            This feature is **EXPERIMENTAL** and may be removed and modified
            without warning in the future.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        self._where = where
        self._postfilter = not prefilter
        return self

    def with_row_id(self, with_row_id: bool) -> Self:
        """Set whether to return row ids.

        Parameters
        ----------
        with_row_id: bool
            If True, return _rowid column in the results.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        self._with_row_id = with_row_id
        return self

    def explain_plan(self, verbose: Optional[bool] = False) -> str:
        """Return the execution plan for this query.

        Examples
        --------
        >>> import lancedb
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
        >>> query = [100, 100]
        >>> plan = table.search(query).explain_plan(True)
        >>> print(plan) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
          GlobalLimitExec: skip=0, fetch=10
            FilterExec: _distance@2 IS NOT NULL
              SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                KNNVectorDistance: metric=l2
                  LanceRead: uri=..., projection=[vector], ...

        Parameters
        ----------
        verbose : bool, default False
            Use a verbose output format.

        Returns
        -------
        plan : str
        """  # noqa: E501
        return self._table._explain_plan(self.to_query_object(), verbose=verbose)

    def analyze_plan(self) -> str:
        """
        Run the query and return its execution plan with runtime metrics.

        This returns detailed metrics for each step, such as elapsed time,
        rows processed, bytes read, and I/O stats. It is useful for debugging
        and performance tuning.

        Examples
        --------
        >>> import lancedb
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
        >>> query = [100, 100]
        >>> plan = table.search(query).analyze_plan()
        >>> print(plan)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        AnalyzeExec verbose=true, elapsed=..., metrics=...
          TracedExec, elapsed=..., metrics=...
            ProjectionExec: elapsed=..., expr=[...],
            metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
              GlobalLimitExec: elapsed=..., skip=0, fetch=10,
              metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
                FilterExec: elapsed=..., _distance@2 IS NOT NULL, metrics=[...]
                  SortExec: elapsed=..., TopK(fetch=10), expr=[...],
                  preserve_partitioning=[...],
                  metrics=[output_rows=..., elapsed_compute=...,
                  output_bytes=..., row_replacements=...]
                    KNNVectorDistance: elapsed=..., metric=l2,
                    metrics=[output_rows=..., elapsed_compute=...,
                    output_bytes=..., output_batches=...]
                      LanceRead: elapsed=..., uri=..., projection=[vector],
                      num_fragments=..., range_before=None, range_after=None,
                      row_id=true, row_addr=false,
                      full_filter=--, refine_filter=--,
                      metrics=[output_rows=..., elapsed_compute=..., output_bytes=...,
                      fragments_scanned=..., ranges_scanned=1, rows_scanned=1,
                      bytes_read=..., iops=..., requests=..., task_wait_time=...]

        Returns
        -------
        plan : str
            The physical query execution plan with runtime metrics.
        """
        return self._table._analyze_plan(self.to_query_object())

    def vector(self, vector: Union[np.ndarray, list]) -> Self:
        """Set the vector to search for.

        Parameters
        ----------
        vector: np.ndarray or list
            The vector to search for.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        raise NotImplementedError

    def text(self, text: str | FullTextQuery) -> Self:
        """Set the text to search for.

        Parameters
        ----------
        text: str | FullTextQuery
            If a string, it is treated as a MatchQuery.
            If a FullTextQuery object, it is used directly.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        raise NotImplementedError

    @abstractmethod
    def rerank(self, reranker: Reranker) -> Self:
        """Rerank the results using the specified reranker.

        Parameters
        ----------
        reranker: Reranker
            The reranker to use.

        Returns
        -------

        The LanceQueryBuilder object.
        """
        raise NotImplementedError

    @abstractmethod
    def to_query_object(self) -> Query:
        """Return a serializable representation of the query

        Returns
        -------
        Query
            The serializable representation of the query
        """
        raise NotImplementedError

              

  

            create

  
      `classmethod`
  

¶

create(table: 'Table', query: Optional[Union[ndarray, str, 'PIL.Image.Image', Tuple]], query_type: str, vector_column_name: str, ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None, fast_search: bool = None) -> Self

    

      
Create a query builder based on the given query and query type.

Parameters:

    
        
- 
          `table`
              (`'Table'`)
          –
          
            
The table to query.

          
        
        
- 
          `query`
              (`Optional[Union[ndarray, str, 'PIL.Image.Image', Tuple]]`)
          –
          
            
The query to use. If None, an empty query builder is returned
which performs simple SQL filtering.

          
        
        
- 
          `query_type`
              (`str`)
          –
          
            
The type of query to perform. One of "vector", "fts", "hybrid", or "auto".
If "auto", the query type is inferred based on the query.

          
        
        
- 
          `vector_column_name`
              (`str`)
          –
          
            
The name of the vector column to use for vector search.

          
        
        
- 
          `fast_search`
              (`bool`, default:
                  `None`
)
          –
          
            
Skip flat search of unindexed data.

          
        
    

            
              Source code in `lancedb/query.py`
              
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
@classmethod
def create(
    cls,
    table: "Table",
    query: Optional[Union[np.ndarray, str, "PIL.Image.Image", Tuple]],
    query_type: str,
    vector_column_name: str,
    ordering_field_name: Optional[str] = None,
    fts_columns: Optional[Union[str, List[str]]] = None,
    fast_search: bool = None,
) -> Self:
    """
    Create a query builder based on the given query and query type.

    Parameters
    ----------
    table: Table
        The table to query.
    query: Optional[Union[np.ndarray, str, "PIL.Image.Image", Tuple]]
        The query to use. If None, an empty query builder is returned
        which performs simple SQL filtering.
    query_type: str
        The type of query to perform. One of "vector", "fts", "hybrid", or "auto".
        If "auto", the query type is inferred based on the query.
    vector_column_name: str
        The name of the vector column to use for vector search.
    fast_search: bool
        Skip flat search of unindexed data.
    """
    # Check hybrid search first as it supports empty query pattern
    if query_type == "hybrid":
        # hybrid fts and vector query
        return LanceHybridQueryBuilder(
            table, query, vector_column_name, fts_columns=fts_columns
        )

    if query is None:
        return LanceEmptyQueryBuilder(table)

    # remember the string query for reranking purpose
    str_query = query if isinstance(query, str) else None

    # convert "auto" query_type to "vector", "fts"
    # or "hybrid" and convert the query to vector if needed
    query, query_type = cls._resolve_query(
        table, query, query_type, vector_column_name
    )

    if query_type == "hybrid":
        return LanceHybridQueryBuilder(
            table, query, vector_column_name, fts_columns=fts_columns
        )

    if isinstance(query, (str, FullTextQuery)):
        # fts
        return LanceFtsQueryBuilder(
            table,
            query,
            ordering_field_name=ordering_field_name,
            fts_columns=fts_columns,
        )

    if isinstance(query, list):
        query = np.array(query, dtype=np.float32)
    elif isinstance(query, np.ndarray):
        query = query.astype(np.float32)
    else:
        raise TypeError(f"Unsupported query type: {type(query)}")

    return LanceVectorQueryBuilder(
        table, query, vector_column_name, str_query, fast_search
    )

            
    

            to_df

¶

to_df() -> 'pd.DataFrame'

    

      
Deprecated alias for `to_pandas()`. Please use `to_pandas()` instead.

Execute the query and return the results as a pandas DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "_distance" column which is the distance between the query
vector and the returned vector.

            
              Source code in `lancedb/query.py`
              
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
@deprecation.deprecated(
    deprecated_in="0.3.1",
    removed_in="0.4.0",
    current_version=__version__,
    details="Use to_pandas() instead",
)
def to_df(self) -> "pd.DataFrame":
    """
    *Deprecated alias for `to_pandas()`. Please use `to_pandas()` instead.*

    Execute the query and return the results as a pandas DataFrame.
    In addition to the selected columns, LanceDB also returns a vector
    and also the "_distance" column which is the distance between the query
    vector and the returned vector.
    """
    return self.to_pandas()

            
    

            to_pandas

¶

to_pandas(flatten: Optional[Union[int, bool]] = None, *, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'

    

      
Execute the query and return the results as a pandas DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "_distance" column which is the distance between the query
vector and the returned vector.

Parameters:

    
        
- 
          `flatten`
              (`Optional[Union[int, bool]]`, default:
                  `None`
)
          –
          
            
If flatten is True, flatten all nested columns.
If flatten is an integer, flatten the nested columns up to the
specified depth.
If unspecified, do not flatten the nested columns.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
def to_pandas(
    self,
    flatten: Optional[Union[int, bool]] = None,
    *,
    timeout: Optional[timedelta] = None,
) -> "pd.DataFrame":
    """
    Execute the query and return the results as a pandas DataFrame.
    In addition to the selected columns, LanceDB also returns a vector
    and also the "_distance" column which is the distance between the query
    vector and the returned vector.

    Parameters
    ----------
    flatten: Optional[Union[int, bool]]
        If flatten is True, flatten all nested columns.
        If flatten is an integer, flatten the nested columns up to the
        specified depth.
        If unspecified, do not flatten the nested columns.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    tbl = flatten_columns(self.to_arrow(timeout=timeout), flatten)
    return tbl.to_pandas()

            
    

            to_arrow

  
      `abstractmethod`
  

¶

to_arrow(*, timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and return the results as an
Apache Arrow Table.

In addition to the selected columns, LanceDB also returns a vector
and also the "_distance" column which is the distance between the query
vector and the returned vectors.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
@abstractmethod
def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and return the results as an
    [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

    In addition to the selected columns, LanceDB also returns a vector
    and also the "_distance" column which is the distance between the query
    vector and the returned vectors.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    raise NotImplementedError

            
    

            to_batches

  
      `abstractmethod`
  

¶

to_batches(batch_size: Optional[int] = None, *, timeout: Optional[timedelta] = None) -> RecordBatchReader

    

      
Execute the query and return the results as a pyarrow
RecordBatchReader

Parameters:

    
        
- 
          `batch_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of selected records in a RecordBatch object.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
@abstractmethod
def to_batches(
    self,
    /,
    batch_size: Optional[int] = None,
    *,
    timeout: Optional[timedelta] = None,
) -> pa.RecordBatchReader:
    """
    Execute the query and return the results as a pyarrow
    [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html)

    Parameters
    ----------
    batch_size: int
        The maximum number of selected records in a RecordBatch object.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    raise NotImplementedError

            
    

            to_list

¶

to_list(*, timeout: Optional[timedelta] = None) -> List[dict]

    

      
Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
def to_list(self, *, timeout: Optional[timedelta] = None) -> List[dict]:
    """
    Execute the query and return the results as a list of dictionaries.

    Each list entry is a dictionary with the selected column names as keys,
    or all table columns if `select` is not called. The vector and the "_distance"
    fields are returned whether or not they're explicitly selected.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    return self.to_arrow(timeout=timeout).to_pylist()

            
    

            to_pydantic

¶

to_pydantic(model: type[T], *, timeout: Optional[timedelta] = None) -> list[T]

    

      
Return the table as a list of pydantic models.

Parameters:

    
        
- 
          `model`
              (`type[T]`)
          –
          
            
The pydantic model to use.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `List[LanceModel]`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
def to_pydantic(
    self, model: type[T], *, timeout: Optional[timedelta] = None
) -> list[T]:
    """Return the table as a list of pydantic models.

    Parameters
    ----------
    model: Type[LanceModel]
        The pydantic model to use.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    List[LanceModel]
    """
    return [model(**row) for row in self.to_arrow(timeout=timeout).to_pylist()]

            
    

            to_polars

¶

to_polars(*, timeout: Optional[timedelta] = None) -> 'pl.DataFrame'

    

      
Execute the query and return the results as a Polars DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "_distance" column which is the distance between the query
vector and the returned vector.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
def to_polars(self, *, timeout: Optional[timedelta] = None) -> "pl.DataFrame":
    """
    Execute the query and return the results as a Polars DataFrame.
    In addition to the selected columns, LanceDB also returns a vector
    and also the "_distance" column which is the distance between the query
    vector and the returned vector.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    import polars as pl

    return pl.from_arrow(self.to_arrow(timeout=timeout))

            
    

            limit

¶

limit(limit: Union[int, None]) -> Self

    

      
Set the maximum number of results to return.

Parameters:

    
        
- 
          `limit`
              (`Union[int, None]`)
          –
          
            
The maximum number of results to return.
The default query limit is 10 results.
For ANN/KNN queries, you must specify a limit.
For plain searches, all records are returned if limit not set.
WARNING if you have a large dataset, setting
the limit to a large number, e.g. the table size,
can potentially result in reading a
large amount of data into memory and cause
out of memory issues.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
def limit(self, limit: Union[int, None]) -> Self:
    """Set the maximum number of results to return.

    Parameters
    ----------
    limit: int
        The maximum number of results to return.
        The default query limit is 10 results.
        For ANN/KNN queries, you must specify a limit.
        For plain searches, all records are returned if limit not set.
        *WARNING* if you have a large dataset, setting
        the limit to a large number, e.g. the table size,
        can potentially result in reading a
        large amount of data into memory and cause
        out of memory issues.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    if limit is None or limit <= 0:
        if isinstance(self, LanceVectorQueryBuilder):
            raise ValueError("Limit is required for ANN/KNN queries")
        else:
            self._limit = None
    else:
        self._limit = limit
    return self

            
    

            offset

¶

offset(offset: int) -> Self

    

      
Set the offset for the results.

Parameters:

    
        
- 
          `offset`
              (`int`)
          –
          
            
The offset to start fetching results from.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
def offset(self, offset: int) -> Self:
    """Set the offset for the results.

    Parameters
    ----------
    offset: int
        The offset to start fetching results from.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    if offset is None or offset <= 0:
        self._offset = 0
    else:
        self._offset = offset
    return self

            
    

            select

¶

select(columns: Union[list[str], dict[str, str]]) -> Self

    

      
Set the columns to return.

Parameters:

    
        
- 
          `columns`
              (`Union[list[str], dict[str, str]]`)
          –
          
            
List of column names to be fetched.
Or a dictionary of column names to SQL expressions.
All columns are fetched if None or unspecified.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
def select(self, columns: Union[list[str], dict[str, str]]) -> Self:
    """Set the columns to return.

    Parameters
    ----------
    columns: list of str, or dict of str to str default None
        List of column names to be fetched.
        Or a dictionary of column names to SQL expressions.
        All columns are fetched if None or unspecified.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    if isinstance(columns, list) or isinstance(columns, dict):
        self._columns = columns
    else:
        raise ValueError("columns must be a list or a dictionary")
    return self

            
    

            where

¶

where(where: str, prefilter: bool = True) -> Self

    

      
Set the where clause.

Parameters:

    
        
- 
          `where`
              (`str`)
          –
          
            
The where clause which is a valid SQL where clause. See
`Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
for valid SQL expressions.

          
        
        
- 
          `prefilter`
              (`bool`, default:
                  `True`
)
          –
          
            
If True, apply the filter before vector search, otherwise the
filter is applied on the result of vector search.
This feature is EXPERIMENTAL and may be removed and modified
without warning in the future.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
def where(self, where: str, prefilter: bool = True) -> Self:
    """Set the where clause.

    Parameters
    ----------
    where: str
        The where clause which is a valid SQL where clause. See
        `Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
        for valid SQL expressions.
    prefilter: bool, default True
        If True, apply the filter before vector search, otherwise the
        filter is applied on the result of vector search.
        This feature is **EXPERIMENTAL** and may be removed and modified
        without warning in the future.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    self._where = where
    self._postfilter = not prefilter
    return self

            
    

            with_row_id

¶

with_row_id(with_row_id: bool) -> Self

    

      
Set whether to return row ids.

Parameters:

    
        
- 
          `with_row_id`
              (`bool`)
          –
          
            
If True, return _rowid column in the results.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
def with_row_id(self, with_row_id: bool) -> Self:
    """Set whether to return row ids.

    Parameters
    ----------
    with_row_id: bool
        If True, return _rowid column in the results.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    self._with_row_id = with_row_id
    return self

            
    

            explain_plan

¶

explain_plan(verbose: Optional[bool] = False) -> str

    

      
Return the execution plan for this query.

Examples:

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).explain_plan(True)
>>> print(plan)
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
def explain_plan(self, verbose: Optional[bool] = False) -> str:
    """Return the execution plan for this query.

    Examples
    --------
    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
    >>> query = [100, 100]
    >>> plan = table.search(query).explain_plan(True)
    >>> print(plan) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
      GlobalLimitExec: skip=0, fetch=10
        FilterExec: _distance@2 IS NOT NULL
          SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
            KNNVectorDistance: metric=l2
              LanceRead: uri=..., projection=[vector], ...

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501
    return self._table._explain_plan(self.to_query_object(), verbose=verbose)

            
    

            analyze_plan

¶

analyze_plan() -> str

    

      
Run the query and return its execution plan with runtime metrics.

This returns detailed metrics for each step, such as elapsed time,
rows processed, bytes read, and I/O stats. It is useful for debugging
and performance tuning.

Examples:

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).analyze_plan()
>>> print(plan)
AnalyzeExec verbose=true, elapsed=..., metrics=...
  TracedExec, elapsed=..., metrics=...
    ProjectionExec: elapsed=..., expr=[...],
    metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
      GlobalLimitExec: elapsed=..., skip=0, fetch=10,
      metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
        FilterExec: elapsed=..., _distance@2 IS NOT NULL, metrics=[...]
          SortExec: elapsed=..., TopK(fetch=10), expr=[...],
          preserve_partitioning=[...],
          metrics=[output_rows=..., elapsed_compute=...,
          output_bytes=..., row_replacements=...]
            KNNVectorDistance: elapsed=..., metric=l2,
            metrics=[output_rows=..., elapsed_compute=...,
            output_bytes=..., output_batches=...]
              LanceRead: elapsed=..., uri=..., projection=[vector],
              num_fragments=..., range_before=None, range_after=None,
              row_id=true, row_addr=false,
              full_filter=--, refine_filter=--,
              metrics=[output_rows=..., elapsed_compute=..., output_bytes=...,
              fragments_scanned=..., ranges_scanned=1, rows_scanned=1,
              bytes_read=..., iops=..., requests=..., task_wait_time=...]

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
The physical query execution plan with runtime metrics.

          
        
    

            
              Source code in `lancedb/query.py`
              
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
971
972
973
974
975
976
977
978
979
980
981
982
983
984
985
986
987
988
989
990
991
def analyze_plan(self) -> str:
    """
    Run the query and return its execution plan with runtime metrics.

    This returns detailed metrics for each step, such as elapsed time,
    rows processed, bytes read, and I/O stats. It is useful for debugging
    and performance tuning.

    Examples
    --------
    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
    >>> query = [100, 100]
    >>> plan = table.search(query).analyze_plan()
    >>> print(plan)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    AnalyzeExec verbose=true, elapsed=..., metrics=...
      TracedExec, elapsed=..., metrics=...
        ProjectionExec: elapsed=..., expr=[...],
        metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
          GlobalLimitExec: elapsed=..., skip=0, fetch=10,
          metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
            FilterExec: elapsed=..., _distance@2 IS NOT NULL, metrics=[...]
              SortExec: elapsed=..., TopK(fetch=10), expr=[...],
              preserve_partitioning=[...],
              metrics=[output_rows=..., elapsed_compute=...,
              output_bytes=..., row_replacements=...]
                KNNVectorDistance: elapsed=..., metric=l2,
                metrics=[output_rows=..., elapsed_compute=...,
                output_bytes=..., output_batches=...]
                  LanceRead: elapsed=..., uri=..., projection=[vector],
                  num_fragments=..., range_before=None, range_after=None,
                  row_id=true, row_addr=false,
                  full_filter=--, refine_filter=--,
                  metrics=[output_rows=..., elapsed_compute=..., output_bytes=...,
                  fragments_scanned=..., ranges_scanned=1, rows_scanned=1,
                  bytes_read=..., iops=..., requests=..., task_wait_time=...]

    Returns
    -------
    plan : str
        The physical query execution plan with runtime metrics.
    """
    return self._table._analyze_plan(self.to_query_object())

            
    

            vector

¶

vector(vector: Union[ndarray, list]) -> Self

    

      
Set the vector to search for.

Parameters:

    
        
- 
          `vector`
              (`Union[ndarray, list]`)
          –
          
            
The vector to search for.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
 993
 994
 995
 996
 997
 998
 999
1000
1001
1002
1003
1004
1005
1006
def vector(self, vector: Union[np.ndarray, list]) -> Self:
    """Set the vector to search for.

    Parameters
    ----------
    vector: np.ndarray or list
        The vector to search for.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    raise NotImplementedError

            
    

            text

¶

text(text: str | FullTextQuery) -> Self

    

      
Set the text to search for.

Parameters:

    
        
- 
          `text`
              (`str | FullTextQuery`)
          –
          
            
If a string, it is treated as a MatchQuery.
If a FullTextQuery object, it is used directly.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
def text(self, text: str | FullTextQuery) -> Self:
    """Set the text to search for.

    Parameters
    ----------
    text: str | FullTextQuery
        If a string, it is treated as a MatchQuery.
        If a FullTextQuery object, it is used directly.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    raise NotImplementedError

            
    

            rerank

  
      `abstractmethod`
  

¶

rerank(reranker: Reranker) -> Self

    

      
Rerank the results using the specified reranker.

Parameters:

    
        
- 
          `reranker`
              (`Reranker`)
          –
          
            
The reranker to use.

          
        
    

Returns:

    
        
- 
              `The LanceQueryBuilder object.`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
@abstractmethod
def rerank(self, reranker: Reranker) -> Self:
    """Rerank the results using the specified reranker.

    Parameters
    ----------
    reranker: Reranker
        The reranker to use.

    Returns
    -------

    The LanceQueryBuilder object.
    """
    raise NotImplementedError

            
    

            to_query_object

  
      `abstractmethod`
  

¶

to_query_object() -> Query

    

      
Return a serializable representation of the query

Returns:

    
        
- 
              `Query`
          –
          
            
The serializable representation of the query

          
        
    

            
              Source code in `lancedb/query.py`
              
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
@abstractmethod
def to_query_object(self) -> Query:
    """Return a serializable representation of the query

    Returns
    -------
    Query
        The serializable representation of the query
    """
    raise NotImplementedError

            
    

  

    

            lancedb.query.LanceVectorQueryBuilder

¶

    
            

              Bases: `LanceQueryBuilder`

Examples:

    
>>> import lancedb
>>> data = [{"vector": [1.1, 1.2], "b": 2},
...         {"vector": [0.5, 1.3], "b": 4},
...         {"vector": [0.4, 0.4], "b": 6},
...         {"vector": [0.4, 0.4], "b": 10}]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data=data)
>>> (table.search([0.4, 0.4])
...       .distance_type("cosine")
...       .where("b < 10")
...       .select(["b", "vector"])
...       .limit(2)
...       .to_pandas())
   b      vector  _distance
0  6  [0.4, 0.4]   0.000000
1  2  [1.1, 1.2]   0.000944

              
                Source code in `lancedb/query.py`
                
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
class LanceVectorQueryBuilder(LanceQueryBuilder):
    """
    Examples
    --------
    >>> import lancedb
    >>> data = [{"vector": [1.1, 1.2], "b": 2},
    ...         {"vector": [0.5, 1.3], "b": 4},
    ...         {"vector": [0.4, 0.4], "b": 6},
    ...         {"vector": [0.4, 0.4], "b": 10}]
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data=data)
    >>> (table.search([0.4, 0.4])
    ...       .distance_type("cosine")
    ...       .where("b < 10")
    ...       .select(["b", "vector"])
    ...       .limit(2)
    ...       .to_pandas())
       b      vector  _distance
    0  6  [0.4, 0.4]   0.000000
    1  2  [1.1, 1.2]   0.000944
    """

    def __init__(
        self,
        table: "Table",
        query: Union[np.ndarray, list, "PIL.Image.Image"],
        vector_column: str,
        str_query: Optional[str] = None,
        fast_search: bool = None,
    ):
        super().__init__(table)
        self._query = query
        self._distance_type = None
        self._minimum_nprobes = None
        self._maximum_nprobes = None
        self._lower_bound = None
        self._upper_bound = None
        self._refine_factor = None
        self._vector_column = vector_column
        self._postfilter = None
        self._reranker = None
        self._str_query = str_query
        self._fast_search = fast_search

    def metric(self, metric: Literal["l2", "cosine", "dot"]) -> LanceVectorQueryBuilder:
        """Set the distance metric to use.

        This is an alias for distance_type() and may be deprecated in the future.
        Please use distance_type() instead.

        Parameters
        ----------
        metric: "l2" or "cosine" or "dot"
            The distance metric to use. By default "l2" is used.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        return self.distance_type(metric)

    def distance_type(
        self, distance_type: Literal["l2", "cosine", "dot"]
    ) -> "LanceVectorQueryBuilder":
        """Set the distance metric to use.

        When performing a vector search we try and find the "nearest" vectors according
        to some kind of distance metric. This parameter controls which distance metric
        to use.

        Note: if there is a vector index then the distance type used MUST match the
        distance type used to train the vector index. If this is not done then the
        results will be invalid.

        Parameters
        ----------
        distance_type: "l2" or "cosine" or "dot"
            The distance metric to use. By default "l2" is used.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._distance_type = distance_type.lower()
        return self

    def nprobes(self, nprobes: int) -> LanceVectorQueryBuilder:
        """Set the number of probes to use.

        Higher values will yield better recall (more likely to find vectors if
        they exist) at the expense of latency.

        See discussion in [Querying an ANN Index][querying-an-ann-index] for
        tuning advice.

        This method sets both the minimum and maximum number of probes to the same
        value. See `minimum_nprobes` and `maximum_nprobes` for more fine-grained
        control.

        Parameters
        ----------
        nprobes: int
            The number of probes to use.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._minimum_nprobes = nprobes
        self._maximum_nprobes = nprobes
        return self

    def minimum_nprobes(self, minimum_nprobes: int) -> LanceVectorQueryBuilder:
        """Set the minimum number of probes to use.

        See `nprobes` for more details.

        These partitions will be searched on every vector query and will increase recall
        at the expense of latency.
        """
        self._minimum_nprobes = minimum_nprobes
        return self

    def maximum_nprobes(self, maximum_nprobes: int) -> LanceVectorQueryBuilder:
        """Set the maximum number of probes to use.

        See `nprobes` for more details.

        If this value is greater than `minimum_nprobes` then the excess partitions
        will be searched only if we have not found enough results.

        This can be useful when there is a narrow filter to allow these queries to
        spend more time searching and avoid potential false negatives.

        If this value is 0 then no limit will be applied and all partitions could be
        searched if needed to satisfy the limit.
        """
        self._maximum_nprobes = maximum_nprobes
        return self

    def distance_range(
        self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
    ) -> LanceVectorQueryBuilder:
        """Set the distance range to use.

        Only rows with distances within range [lower_bound, upper_bound)
        will be returned.

        Parameters
        ----------
        lower_bound: Optional[float]
            The lower bound of the distance range.
        upper_bound: Optional[float]
            The upper bound of the distance range.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        return self

    def ef(self, ef: int) -> LanceVectorQueryBuilder:
        """Set the number of candidates to consider during search.

        Higher values will yield better recall (more likely to find vectors if
        they exist) at the expense of latency.

        This only applies to the HNSW-related index.
        The default value is 1.5 * limit.

        Parameters
        ----------
        ef: int
            The number of candidates to consider during search.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._ef = ef
        return self

    def refine_factor(self, refine_factor: int) -> LanceVectorQueryBuilder:
        """Set the refine factor to use, increasing the number of vectors sampled.

        As an example, a refine factor of 2 will sample 2x as many vectors as
        requested, re-ranks them, and returns the top half most relevant results.

        See discussion in [Querying an ANN Index][querying-an-ann-index] for
        tuning advice.

        Parameters
        ----------
        refine_factor: int
            The refine factor to use.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._refine_factor = refine_factor
        return self

    def output_schema(self) -> pa.Schema:
        """
        Return the output schema for the query

        This does not execute the query.
        """
        return self._table._output_schema(self.to_query_object())

    def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
        """
        Execute the query and return the results as an
        [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

        In addition to the selected columns, LanceDB also returns a vector
        and also the "_distance" column which is the distance between the query
        vector and the returned vectors.

        Parameters
        ----------
        timeout: Optional[timedelta]
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.
        """
        return self.to_batches(timeout=timeout).read_all()

    def to_query_object(self) -> Query:
        """
        Build a Query object

        This can be used to serialize a query
        """
        vector = self._query if isinstance(self._query, list) else self._query.tolist()
        if isinstance(vector[0], np.ndarray):
            vector = [v.tolist() for v in vector]
        return Query(
            vector=vector,
            filter=self._where,
            postfilter=self._postfilter,
            limit=self._limit,
            distance_type=self._distance_type,
            columns=self._columns,
            minimum_nprobes=self._minimum_nprobes,
            maximum_nprobes=self._maximum_nprobes,
            lower_bound=self._lower_bound,
            upper_bound=self._upper_bound,
            refine_factor=self._refine_factor,
            vector_column=self._vector_column,
            with_row_id=self._with_row_id,
            offset=self._offset,
            fast_search=self._fast_search,
            ef=self._ef,
            bypass_vector_index=self._bypass_vector_index,
        )

    def to_batches(
        self,
        /,
        batch_size: Optional[int] = None,
        *,
        timeout: Optional[timedelta] = None,
    ) -> pa.RecordBatchReader:
        """
        Execute the query and return the result as a RecordBatchReader object.

        Parameters
        ----------
        batch_size: int
            The maximum number of selected records in a RecordBatch object.
        timeout: timedelta, default None
            The maximum time to wait for the query to complete.
            If None, wait indefinitely.

        Returns
        -------
        pa.RecordBatchReader
        """
        vector = self._query if isinstance(self._query, list) else self._query.tolist()
        if isinstance(vector[0], np.ndarray):
            vector = [v.tolist() for v in vector]
        query = self.to_query_object()
        result_set = self._table._execute_query(
            query, batch_size=batch_size, timeout=timeout
        )
        if self._reranker is not None:
            rs_table = result_set.read_all()
            result_set = self._reranker.rerank_vector(self._str_query, rs_table)
            check_reranker_result(result_set)
            # convert result_set back to RecordBatchReader
            result_set = pa.RecordBatchReader.from_batches(
                result_set.schema, result_set.to_batches()
            )

        return result_set

    def where(self, where: str, prefilter: bool = None) -> LanceVectorQueryBuilder:
        """Set the where clause.

        Parameters
        ----------
        where: str
            The where clause which is a valid SQL where clause. See
            `Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
            for valid SQL expressions.
        prefilter: bool, default True
            If True, apply the filter before vector search, otherwise the
            filter is applied on the result of vector search.

        Returns
        -------
        LanceQueryBuilder
            The LanceQueryBuilder object.
        """
        self._where = where
        if prefilter is not None:
            self._postfilter = not prefilter
        return self

    def rerank(
        self, reranker: Reranker, query_string: Optional[str] = None
    ) -> LanceVectorQueryBuilder:
        """Rerank the results using the specified reranker.

        Parameters
        ----------
        reranker: Reranker
            The reranker to use.

        query_string: Optional[str]
            The query to use for reranking. This needs to be specified explicitly here
            as the query used for vector search may already be vectorized and the
            reranker requires a string query.
            This is only required if the query used for vector search is not a string.
            Note: This doesn't yet support the case where the query is multimodal or a
            list of vectors.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._reranker = reranker
        if self._str_query is None and query_string is None:
            raise ValueError(
                """
                The query used for vector search is not a string.
                In this case, the reranker query needs to be specified explicitly.
                """
            )
        if query_string is not None and not isinstance(query_string, str):
            raise ValueError("Reranking currently only supports string queries")
        self._str_query = query_string if query_string is not None else self._str_query
        if reranker.score == "all":
            self.with_row_id(True)
        return self

    def bypass_vector_index(self) -> LanceVectorQueryBuilder:
        """
        If this is called then any vector index is skipped

        An exhaustive (flat) search will be performed.  The query vector will
        be compared to every vector in the table.  At high scales this can be
        expensive.  However, this is often still useful.  For example, skipping
        the vector index can give you ground truth results which you can use to
        calculate your recall to select an appropriate value for nprobes.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceVectorQueryBuilder object.
        """
        self._bypass_vector_index = True
        return self

    def fast_search(self) -> LanceVectorQueryBuilder:
        """
        Skip a flat search of unindexed data. This will improve
        search performance but search results will not include unindexed data.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceVectorQueryBuilder object.
        """
        self._fast_search = True
        return self

              

  

            metric

¶

metric(metric: Literal['l2', 'cosine', 'dot']) -> LanceVectorQueryBuilder

    

      
Set the distance metric to use.

This is an alias for distance_type() and may be deprecated in the future.
Please use distance_type() instead.

Parameters:

    
        
- 
          `metric`
              (`Literal['l2', 'cosine', 'dot']`)
          –
          
            
The distance metric to use. By default "l2" is used.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
def metric(self, metric: Literal["l2", "cosine", "dot"]) -> LanceVectorQueryBuilder:
    """Set the distance metric to use.

    This is an alias for distance_type() and may be deprecated in the future.
    Please use distance_type() instead.

    Parameters
    ----------
    metric: "l2" or "cosine" or "dot"
        The distance metric to use. By default "l2" is used.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    return self.distance_type(metric)

            
    

            distance_type

¶

distance_type(distance_type: Literal['l2', 'cosine', 'dot']) -> 'LanceVectorQueryBuilder'

    

      
Set the distance metric to use.

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

Parameters:

    
        
- 
          `distance_type`
              (`Literal['l2', 'cosine', 'dot']`)
          –
          
            
The distance metric to use. By default "l2" is used.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
def distance_type(
    self, distance_type: Literal["l2", "cosine", "dot"]
) -> "LanceVectorQueryBuilder":
    """Set the distance metric to use.

    When performing a vector search we try and find the "nearest" vectors according
    to some kind of distance metric. This parameter controls which distance metric
    to use.

    Note: if there is a vector index then the distance type used MUST match the
    distance type used to train the vector index. If this is not done then the
    results will be invalid.

    Parameters
    ----------
    distance_type: "l2" or "cosine" or "dot"
        The distance metric to use. By default "l2" is used.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._distance_type = distance_type.lower()
    return self

            
    

            nprobes

¶

nprobes(nprobes: int) -> LanceVectorQueryBuilder

    

      
Set the number of probes to use.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

See discussion in [Querying an ANN Index][querying-an-ann-index] for
tuning advice.

This method sets both the minimum and maximum number of probes to the same
value. See `minimum_nprobes` and `maximum_nprobes` for more fine-grained
control.

Parameters:

    
        
- 
          `nprobes`
              (`int`)
          –
          
            
The number of probes to use.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
def nprobes(self, nprobes: int) -> LanceVectorQueryBuilder:
    """Set the number of probes to use.

    Higher values will yield better recall (more likely to find vectors if
    they exist) at the expense of latency.

    See discussion in [Querying an ANN Index][querying-an-ann-index] for
    tuning advice.

    This method sets both the minimum and maximum number of probes to the same
    value. See `minimum_nprobes` and `maximum_nprobes` for more fine-grained
    control.

    Parameters
    ----------
    nprobes: int
        The number of probes to use.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._minimum_nprobes = nprobes
    self._maximum_nprobes = nprobes
    return self

            
    

            minimum_nprobes

¶

minimum_nprobes(minimum_nprobes: int) -> LanceVectorQueryBuilder

    

      
Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every vector query and will increase recall
at the expense of latency.

            
              Source code in `lancedb/query.py`
              
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
def minimum_nprobes(self, minimum_nprobes: int) -> LanceVectorQueryBuilder:
    """Set the minimum number of probes to use.

    See `nprobes` for more details.

    These partitions will be searched on every vector query and will increase recall
    at the expense of latency.
    """
    self._minimum_nprobes = minimum_nprobes
    return self

            
    

            maximum_nprobes

¶

maximum_nprobes(maximum_nprobes: int) -> LanceVectorQueryBuilder

    

      
Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

            
              Source code in `lancedb/query.py`
              
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
def maximum_nprobes(self, maximum_nprobes: int) -> LanceVectorQueryBuilder:
    """Set the maximum number of probes to use.

    See `nprobes` for more details.

    If this value is greater than `minimum_nprobes` then the excess partitions
    will be searched only if we have not found enough results.

    This can be useful when there is a narrow filter to allow these queries to
    spend more time searching and avoid potential false negatives.

    If this value is 0 then no limit will be applied and all partitions could be
    searched if needed to satisfy the limit.
    """
    self._maximum_nprobes = maximum_nprobes
    return self

            
    

            distance_range

¶

distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> LanceVectorQueryBuilder

    

      
Set the distance range to use.

Only rows with distances within range [lower_bound, upper_bound)
will be returned.

Parameters:

    
        
- 
          `lower_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The lower bound of the distance range.

          
        
        
- 
          `upper_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The upper bound of the distance range.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
def distance_range(
    self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
) -> LanceVectorQueryBuilder:
    """Set the distance range to use.

    Only rows with distances within range [lower_bound, upper_bound)
    will be returned.

    Parameters
    ----------
    lower_bound: Optional[float]
        The lower bound of the distance range.
    upper_bound: Optional[float]
        The upper bound of the distance range.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._lower_bound = lower_bound
    self._upper_bound = upper_bound
    return self

            
    

            ef

¶

ef(ef: int) -> LanceVectorQueryBuilder

    

      
Set the number of candidates to consider during search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

This only applies to the HNSW-related index.
The default value is 1.5 * limit.

Parameters:

    
        
- 
          `ef`
              (`int`)
          –
          
            
The number of candidates to consider during search.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
def ef(self, ef: int) -> LanceVectorQueryBuilder:
    """Set the number of candidates to consider during search.

    Higher values will yield better recall (more likely to find vectors if
    they exist) at the expense of latency.

    This only applies to the HNSW-related index.
    The default value is 1.5 * limit.

    Parameters
    ----------
    ef: int
        The number of candidates to consider during search.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._ef = ef
    return self

            
    

            refine_factor

¶

refine_factor(refine_factor: int) -> LanceVectorQueryBuilder

    

      
Set the refine factor to use, increasing the number of vectors sampled.

As an example, a refine factor of 2 will sample 2x as many vectors as
requested, re-ranks them, and returns the top half most relevant results.

See discussion in [Querying an ANN Index][querying-an-ann-index] for
tuning advice.

Parameters:

    
        
- 
          `refine_factor`
              (`int`)
          –
          
            
The refine factor to use.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
def refine_factor(self, refine_factor: int) -> LanceVectorQueryBuilder:
    """Set the refine factor to use, increasing the number of vectors sampled.

    As an example, a refine factor of 2 will sample 2x as many vectors as
    requested, re-ranks them, and returns the top half most relevant results.

    See discussion in [Querying an ANN Index][querying-an-ann-index] for
    tuning advice.

    Parameters
    ----------
    refine_factor: int
        The refine factor to use.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._refine_factor = refine_factor
    return self

            
    

            output_schema

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
1263
1264
1265
1266
1267
1268
1269
def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return self._table._output_schema(self.to_query_object())

            
    

            to_arrow

¶

to_arrow(*, timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and return the results as an
Apache Arrow Table.

In addition to the selected columns, LanceDB also returns a vector
and also the "_distance" column which is the distance between the query
vector and the returned vectors.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

            
              Source code in `lancedb/query.py`
              
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and return the results as an
    [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

    In addition to the selected columns, LanceDB also returns a vector
    and also the "_distance" column which is the distance between the query
    vector and the returned vectors.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.
    """
    return self.to_batches(timeout=timeout).read_all()

            
    

            to_query_object

¶

to_query_object() -> Query

    

      
Build a Query object

This can be used to serialize a query

            
              Source code in `lancedb/query.py`
              
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
def to_query_object(self) -> Query:
    """
    Build a Query object

    This can be used to serialize a query
    """
    vector = self._query if isinstance(self._query, list) else self._query.tolist()
    if isinstance(vector[0], np.ndarray):
        vector = [v.tolist() for v in vector]
    return Query(
        vector=vector,
        filter=self._where,
        postfilter=self._postfilter,
        limit=self._limit,
        distance_type=self._distance_type,
        columns=self._columns,
        minimum_nprobes=self._minimum_nprobes,
        maximum_nprobes=self._maximum_nprobes,
        lower_bound=self._lower_bound,
        upper_bound=self._upper_bound,
        refine_factor=self._refine_factor,
        vector_column=self._vector_column,
        with_row_id=self._with_row_id,
        offset=self._offset,
        fast_search=self._fast_search,
        ef=self._ef,
        bypass_vector_index=self._bypass_vector_index,
    )

            
    

            to_batches

¶

to_batches(batch_size: Optional[int] = None, *, timeout: Optional[timedelta] = None) -> RecordBatchReader

    

      
Execute the query and return the result as a RecordBatchReader object.

Parameters:

    
        
- 
          `batch_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of selected records in a RecordBatch object.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `RecordBatchReader`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
def to_batches(
    self,
    /,
    batch_size: Optional[int] = None,
    *,
    timeout: Optional[timedelta] = None,
) -> pa.RecordBatchReader:
    """
    Execute the query and return the result as a RecordBatchReader object.

    Parameters
    ----------
    batch_size: int
        The maximum number of selected records in a RecordBatch object.
    timeout: timedelta, default None
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    pa.RecordBatchReader
    """
    vector = self._query if isinstance(self._query, list) else self._query.tolist()
    if isinstance(vector[0], np.ndarray):
        vector = [v.tolist() for v in vector]
    query = self.to_query_object()
    result_set = self._table._execute_query(
        query, batch_size=batch_size, timeout=timeout
    )
    if self._reranker is not None:
        rs_table = result_set.read_all()
        result_set = self._reranker.rerank_vector(self._str_query, rs_table)
        check_reranker_result(result_set)
        # convert result_set back to RecordBatchReader
        result_set = pa.RecordBatchReader.from_batches(
            result_set.schema, result_set.to_batches()
        )

    return result_set

            
    

            where

¶

where(where: str, prefilter: bool = None) -> LanceVectorQueryBuilder

    

      
Set the where clause.

Parameters:

    
        
- 
          `where`
              (`str`)
          –
          
            
The where clause which is a valid SQL where clause. See
`Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
for valid SQL expressions.

          
        
        
- 
          `prefilter`
              (`bool`, default:
                  `None`
)
          –
          
            
If True, apply the filter before vector search, otherwise the
filter is applied on the result of vector search.

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
def where(self, where: str, prefilter: bool = None) -> LanceVectorQueryBuilder:
    """Set the where clause.

    Parameters
    ----------
    where: str
        The where clause which is a valid SQL where clause. See
        `Lance filter pushdown <https://lance.org/guide/read_and_write#filter-push-down>`_
        for valid SQL expressions.
    prefilter: bool, default True
        If True, apply the filter before vector search, otherwise the
        filter is applied on the result of vector search.

    Returns
    -------
    LanceQueryBuilder
        The LanceQueryBuilder object.
    """
    self._where = where
    if prefilter is not None:
        self._postfilter = not prefilter
    return self

            
    

            rerank

¶

rerank(reranker: Reranker, query_string: Optional[str] = None) -> LanceVectorQueryBuilder

    

      
Rerank the results using the specified reranker.

Parameters:

    
        
- 
          `reranker`
              (`Reranker`)
          –
          
            
The reranker to use.

          
        
        
- 
          `query_string`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The query to use for reranking. This needs to be specified explicitly here
as the query used for vector search may already be vectorized and the
reranker requires a string query.
This is only required if the query used for vector search is not a string.
Note: This doesn't yet support the case where the query is multimodal or a
list of vectors.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
def rerank(
    self, reranker: Reranker, query_string: Optional[str] = None
) -> LanceVectorQueryBuilder:
    """Rerank the results using the specified reranker.

    Parameters
    ----------
    reranker: Reranker
        The reranker to use.

    query_string: Optional[str]
        The query to use for reranking. This needs to be specified explicitly here
        as the query used for vector search may already be vectorized and the
        reranker requires a string query.
        This is only required if the query used for vector search is not a string.
        Note: This doesn't yet support the case where the query is multimodal or a
        list of vectors.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._reranker = reranker
    if self._str_query is None and query_string is None:
        raise ValueError(
            """
            The query used for vector search is not a string.
            In this case, the reranker query needs to be specified explicitly.
            """
        )
    if query_string is not None and not isinstance(query_string, str):
        raise ValueError("Reranking currently only supports string queries")
    self._str_query = query_string if query_string is not None else self._str_query
    if reranker.score == "all":
        self.with_row_id(True)
    return self

            
    

            bypass_vector_index

¶

bypass_vector_index() -> LanceVectorQueryBuilder

    

      
If this is called then any vector index is skipped

An exhaustive (flat) search will be performed.  The query vector will
be compared to every vector in the table.  At high scales this can be
expensive.  However, this is often still useful.  For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceVectorQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
def bypass_vector_index(self) -> LanceVectorQueryBuilder:
    """
    If this is called then any vector index is skipped

    An exhaustive (flat) search will be performed.  The query vector will
    be compared to every vector in the table.  At high scales this can be
    expensive.  However, this is often still useful.  For example, skipping
    the vector index can give you ground truth results which you can use to
    calculate your recall to select an appropriate value for nprobes.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceVectorQueryBuilder object.
    """
    self._bypass_vector_index = True
    return self

            
    

            fast_search

¶

fast_search() -> LanceVectorQueryBuilder

    

      
Skip a flat search of unindexed data. This will improve
search performance but search results will not include unindexed data.

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceVectorQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
def fast_search(self) -> LanceVectorQueryBuilder:
    """
    Skip a flat search of unindexed data. This will improve
    search performance but search results will not include unindexed data.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceVectorQueryBuilder object.
    """
    self._fast_search = True
    return self

            
    

  

    

            lancedb.query.LanceFtsQueryBuilder

¶

    
            

              Bases: `LanceQueryBuilder`

      
A builder for full text search for LanceDB.

              
                Source code in `lancedb/query.py`
                
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
class LanceFtsQueryBuilder(LanceQueryBuilder):
    """A builder for full text search for LanceDB."""

    def __init__(
        self,
        table: "Table",
        query: str | FullTextQuery,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ):
        super().__init__(table)
        self._query = query
        self._phrase_query = False
        self.ordering_field_name = ordering_field_name
        self._reranker = None
        if isinstance(fts_columns, str):
            fts_columns = [fts_columns]
        self._fts_columns = fts_columns

    def phrase_query(self, phrase_query: bool = True) -> LanceFtsQueryBuilder:
        """Set whether to use phrase query.

        Parameters
        ----------
        phrase_query: bool, default True
            If True, then the query will be wrapped in quotes and
            double quotes replaced by single quotes.

        Returns
        -------
        LanceFtsQueryBuilder
            The LanceFtsQueryBuilder object.
        """
        self._phrase_query = phrase_query
        return self

    def to_query_object(self) -> Query:
        return Query(
            columns=self._columns,
            filter=self._where,
            limit=self._limit,
            postfilter=self._postfilter,
            with_row_id=self._with_row_id,
            full_text_query=FullTextSearchQuery(
                query=self._query, columns=self._fts_columns
            ),
            offset=self._offset,
        )

    def output_schema(self) -> pa.Schema:
        """
        Return the output schema for the query

        This does not execute the query.
        """
        return self._table._output_schema(self.to_query_object())

    def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
        path, fs, exist = self._table._get_fts_index_path()
        if exist:
            return self.tantivy_to_arrow()

        query = self._query
        if self._phrase_query:
            if isinstance(query, str):
                if not query.startswith('"') or not query.endswith('"'):
                    self._query = f'"{query}"'
            elif isinstance(query, FullTextQuery) and not isinstance(
                query, PhraseQuery
            ):
                raise TypeError("Please use PhraseQuery for phrase queries.")
        query = self.to_query_object()
        results = self._table._execute_query(query, timeout=timeout)
        results = results.read_all()
        if self._reranker is not None:
            results = self._reranker.rerank_fts(self._query, results)
            check_reranker_result(results)
        return results

    def to_batches(
        self, /, batch_size: Optional[int] = None, timeout: Optional[timedelta] = None
    ):
        raise NotImplementedError("to_batches on an FTS query")

    def tantivy_to_arrow(self) -> pa.Table:
        try:
            import tantivy
        except ImportError:
            raise ImportError(
                "Please install tantivy-py `pip install tantivy` to use the full text search feature."  # noqa: E501
            )

        from .fts import search_index

        # get the index path
        path, fs, exist = self._table._get_fts_index_path()

        # check if the index exist
        if not exist:
            raise FileNotFoundError(
                "Fts index does not exist. "
                "Please first call table.create_fts_index(['<field_names>']) to "
                "create the fts index."
            )

        # Check that we are on local filesystem
        if not isinstance(fs, pa_fs.LocalFileSystem):
            raise NotImplementedError(
                "Tantivy-based full text search "
                "is only supported on the local filesystem"
            )
        # open the index
        index = tantivy.Index.open(path)
        # get the scores and doc ids
        query = self._query
        if self._phrase_query:
            query = query.replace('"', "'")
            query = f'"{query}"'
        limit = self._limit if self._limit is not None else 10
        row_ids, scores = search_index(
            index, query, limit, ordering_field=self.ordering_field_name
        )
        if len(row_ids) == 0:
            empty_schema = pa.schema([pa.field("_score", pa.float32())])
            return pa.Table.from_batches([], schema=empty_schema)
        scores = pa.array(scores)
        output_tbl = self._table.to_lance().take(row_ids, columns=self._columns)
        output_tbl = output_tbl.append_column("_score", scores)
        # this needs to match vector search results which are uint64
        row_ids = pa.array(row_ids, type=pa.uint64())

        if self._where is not None:
            tmp_name = "__lancedb__duckdb__indexer__"
            output_tbl = output_tbl.append_column(
                tmp_name, pa.array(range(len(output_tbl)))
            )
            try:
                # TODO would be great to have Substrait generate pyarrow compute
                # expressions or conversely have pyarrow support SQL expressions
                # using Substrait
                import duckdb

                indexer = duckdb.sql(
                    f"SELECT {tmp_name} FROM output_tbl WHERE {self._where}"
                ).to_arrow_table()[tmp_name]
                output_tbl = output_tbl.take(indexer).drop([tmp_name])
                row_ids = row_ids.take(indexer)

            except ImportError:
                import tempfile

                import lance

                # TODO Use "memory://" instead once that's supported
                with tempfile.TemporaryDirectory() as tmp:
                    ds = lance.write_dataset(output_tbl, tmp)
                    output_tbl = ds.to_table(filter=self._where)
                    indexer = output_tbl[tmp_name]
                    row_ids = row_ids.take(indexer)
                    output_tbl = output_tbl.drop([tmp_name])

        if self._with_row_id:
            output_tbl = output_tbl.append_column("_rowid", row_ids)

        if self._reranker is not None:
            output_tbl = self._reranker.rerank_fts(self._query, output_tbl)
        return output_tbl

    def rerank(self, reranker: Reranker) -> LanceFtsQueryBuilder:
        """Rerank the results using the specified reranker.

        Parameters
        ----------
        reranker: Reranker
            The reranker to use.

        Returns
        -------
        LanceFtsQueryBuilder
            The LanceQueryBuilder object.
        """
        self._reranker = reranker
        if reranker.score == "all":
            self.with_row_id(True)
        return self

              

  

            phrase_query

¶

phrase_query(phrase_query: bool = True) -> LanceFtsQueryBuilder

    

      
Set whether to use phrase query.

Parameters:

    
        
- 
          `phrase_query`
              (`bool`, default:
                  `True`
)
          –
          
            
If True, then the query will be wrapped in quotes and
double quotes replaced by single quotes.

          
        
    

Returns:

    
        
- 
              `LanceFtsQueryBuilder`
          –
          
            
The LanceFtsQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
def phrase_query(self, phrase_query: bool = True) -> LanceFtsQueryBuilder:
    """Set whether to use phrase query.

    Parameters
    ----------
    phrase_query: bool, default True
        If True, then the query will be wrapped in quotes and
        double quotes replaced by single quotes.

    Returns
    -------
    LanceFtsQueryBuilder
        The LanceFtsQueryBuilder object.
    """
    self._phrase_query = phrase_query
    return self

            
    

            output_schema

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
1499
1500
1501
1502
1503
1504
1505
def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return self._table._output_schema(self.to_query_object())

            
    

            rerank

¶

rerank(reranker: Reranker) -> LanceFtsQueryBuilder

    

      
Rerank the results using the specified reranker.

Parameters:

    
        
- 
          `reranker`
              (`Reranker`)
          –
          
            
The reranker to use.

          
        
    

Returns:

    
        
- 
              `LanceFtsQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
def rerank(self, reranker: Reranker) -> LanceFtsQueryBuilder:
    """Rerank the results using the specified reranker.

    Parameters
    ----------
    reranker: Reranker
        The reranker to use.

    Returns
    -------
    LanceFtsQueryBuilder
        The LanceQueryBuilder object.
    """
    self._reranker = reranker
    if reranker.score == "all":
        self.with_row_id(True)
    return self

            
    

  

    

            lancedb.query.LanceHybridQueryBuilder

¶

    
            

              Bases: `LanceQueryBuilder`

      
A query builder that performs hybrid vector and full text search.
Results are combined and reranked based on the specified reranker.
By default, the results are reranked using the RRFReranker, which
uses reciprocal rank fusion score for reranking.

To make the vector and fts results comparable, the scores are normalized.
Instead of normalizing scores, the `normalize` parameter can be set to "rank"
in the `rerank` method to convert the scores to ranks and then normalize them.

              
                Source code in `lancedb/query.py`
                
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
1720
1721
1722
1723
1724
1725
1726
1727
1728
1729
1730
1731
1732
1733
1734
1735
1736
1737
1738
1739
1740
1741
1742
1743
1744
1745
1746
1747
1748
1749
1750
1751
1752
1753
1754
1755
1756
1757
1758
1759
1760
1761
1762
1763
1764
1765
1766
1767
1768
1769
1770
1771
1772
1773
1774
1775
1776
1777
1778
1779
1780
1781
1782
1783
1784
1785
1786
1787
1788
1789
1790
1791
1792
1793
1794
1795
1796
1797
1798
1799
1800
1801
1802
1803
1804
1805
1806
1807
1808
1809
1810
1811
1812
1813
1814
1815
1816
1817
1818
1819
1820
1821
1822
1823
1824
1825
1826
1827
1828
1829
1830
1831
1832
1833
1834
1835
1836
1837
1838
1839
1840
1841
1842
1843
1844
1845
1846
1847
1848
1849
1850
1851
1852
1853
1854
1855
1856
1857
1858
1859
1860
1861
1862
1863
1864
1865
1866
1867
1868
1869
1870
1871
1872
1873
1874
1875
1876
1877
1878
1879
1880
1881
1882
1883
1884
1885
1886
1887
1888
1889
1890
1891
1892
1893
1894
1895
1896
1897
1898
1899
1900
1901
1902
1903
1904
1905
1906
1907
1908
1909
1910
1911
1912
1913
1914
1915
1916
1917
1918
1919
1920
1921
1922
1923
1924
1925
1926
1927
1928
1929
1930
1931
1932
1933
1934
1935
1936
1937
1938
1939
1940
1941
1942
1943
1944
1945
1946
1947
1948
1949
1950
1951
1952
1953
1954
1955
1956
1957
1958
1959
1960
1961
1962
1963
1964
1965
1966
1967
1968
1969
1970
1971
1972
1973
1974
1975
1976
1977
1978
1979
1980
1981
1982
1983
1984
1985
1986
1987
1988
1989
1990
1991
1992
1993
1994
1995
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014
2015
2016
2017
2018
2019
2020
2021
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2032
2033
2034
2035
2036
2037
2038
2039
2040
2041
2042
2043
2044
2045
2046
2047
2048
2049
2050
2051
2052
2053
2054
2055
2056
2057
2058
2059
2060
2061
2062
2063
2064
2065
2066
2067
2068
2069
2070
2071
2072
2073
2074
2075
2076
2077
2078
2079
2080
2081
2082
2083
2084
2085
2086
2087
2088
2089
2090
2091
2092
2093
2094
2095
2096
2097
2098
2099
2100
2101
2102
2103
2104
2105
2106
2107
2108
2109
2110
2111
2112
2113
2114
2115
2116
2117
2118
2119
2120
2121
2122
2123
2124
2125
2126
2127
2128
2129
2130
2131
2132
2133
2134
2135
2136
2137
2138
2139
2140
2141
2142
2143
2144
2145
2146
2147
2148
2149
2150
2151
2152
2153
2154
2155
2156
2157
2158
2159
2160
2161
2162
2163
2164
2165
2166
2167
2168
2169
2170
2171
2172
2173
2174
2175
2176
2177
2178
2179
2180
2181
2182
2183
2184
2185
2186
2187
2188
2189
2190
2191
2192
2193
2194
2195
2196
class LanceHybridQueryBuilder(LanceQueryBuilder):
    """
    A query builder that performs hybrid vector and full text search.
    Results are combined and reranked based on the specified reranker.
    By default, the results are reranked using the RRFReranker, which
    uses reciprocal rank fusion score for reranking.

    To make the vector and fts results comparable, the scores are normalized.
    Instead of normalizing scores, the `normalize` parameter can be set to "rank"
    in the `rerank` method to convert the scores to ranks and then normalize them.
    """

    def __init__(
        self,
        table: "Table",
        query: Optional[Union[str, FullTextQuery]] = None,
        vector_column: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ):
        super().__init__(table)
        self._query = query
        self._vector_column = vector_column
        self._fts_columns = fts_columns
        self._norm = None
        self._reranker = None
        self._minimum_nprobes = None
        self._maximum_nprobes = None
        self._refine_factor = None
        self._distance_type = None
        self._phrase_query = None
        self._lower_bound = None
        self._upper_bound = None

    def _validate_query(self, query, vector=None, text=None):
        if query is not None and (vector is not None or text is not None):
            raise ValueError(
                "You can either provide a string query in search() method"
                "or set `vector()` and `text()` explicitly for hybrid search."
                "But not both."
            )

        vector_query = vector if vector is not None else query
        if not isinstance(vector_query, (str, list, np.ndarray)):
            raise ValueError("Vector query must be either a string or a vector")

        text_query = text or query
        if text_query is None:
            raise ValueError("Text query must be provided for hybrid search.")
        if not isinstance(text_query, (str, FullTextQuery)):
            raise ValueError("Text query must be a string or FullTextQuery")

        return vector_query, text_query

    def phrase_query(self, phrase_query: bool = None) -> LanceHybridQueryBuilder:
        """Set whether to use phrase query.

        Parameters
        ----------
        phrase_query: bool, default True
            If True, then the query will be wrapped in quotes and
            double quotes replaced by single quotes.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._phrase_query = phrase_query
        return self

    def to_query_object(self) -> Query:
        raise NotImplementedError("to_query_object not yet supported on a hybrid query")

    def to_arrow(self, *, timeout: Optional[timedelta] = None) -> pa.Table:
        self._create_query_builders()
        with ThreadPoolExecutor() as executor:
            fts_future = executor.submit(
                self._fts_query.with_row_id(True).to_arrow, timeout=timeout
            )
            vector_future = executor.submit(
                self._vector_query.with_row_id(True).to_arrow, timeout=timeout
            )
            fts_results = fts_future.result()
            vector_results = vector_future.result()

        return self._combine_hybrid_results(
            fts_results=fts_results,
            vector_results=vector_results,
            norm=self._norm,
            fts_query=self._fts_query._query,
            reranker=self._reranker,
            limit=self._limit,
            with_row_ids=self._with_row_id,
        )

    @staticmethod
    def _combine_hybrid_results(
        fts_results: pa.Table,
        vector_results: pa.Table,
        norm: str,
        fts_query: str,
        reranker,
        limit: int,
        with_row_ids: bool,
    ) -> pa.Table:
        if norm == "rank":
            vector_results = LanceHybridQueryBuilder._rank(vector_results, "_distance")
            fts_results = LanceHybridQueryBuilder._rank(fts_results, "_score")

        original_distances = None
        original_scores = None
        original_distance_row_ids = None
        original_score_row_ids = None
        # normalize the scores to be between 0 and 1, 0 being most relevant
        # We check whether the results (vector and FTS) are empty, because when
        # they are, they often are missing the _rowid column, which causes an error
        if vector_results.num_rows > 0:
            distance_i = vector_results.column_names.index("_distance")
            original_distances = vector_results.column(distance_i)
            original_distance_row_ids = vector_results.column("_rowid")
            vector_results = vector_results.set_column(
                distance_i,
                vector_results.field(distance_i),
                LanceHybridQueryBuilder._normalize_scores(original_distances),
            )

        # In fts higher scores represent relevance. Not inverting them here as
        # rerankers might need to preserve this score to support `return_score="all"`
        if fts_results.num_rows > 0:
            score_i = fts_results.column_names.index("_score")
            original_scores = fts_results.column(score_i)
            original_score_row_ids = fts_results.column("_rowid")
            fts_results = fts_results.set_column(
                score_i,
                fts_results.field(score_i),
                LanceHybridQueryBuilder._normalize_scores(original_scores),
            )

        results = reranker.rerank_hybrid(fts_query, vector_results, fts_results)

        check_reranker_result(results)

        if "_distance" in results.column_names and original_distances is not None:
            # restore the original distances
            indices = pc.index_in(
                results["_rowid"], original_distance_row_ids, skip_nulls=True
            )
            original_distances = pc.take(original_distances, indices)
            distance_i = results.column_names.index("_distance")
            results = results.set_column(distance_i, "_distance", original_distances)

        if "_score" in results.column_names and original_scores is not None:
            # restore the original scores
            indices = pc.index_in(
                results["_rowid"], original_score_row_ids, skip_nulls=True
            )
            original_scores = pc.take(original_scores, indices)
            score_i = results.column_names.index("_score")
            results = results.set_column(score_i, "_score", original_scores)

        results = results.slice(length=limit)

        if not with_row_ids:
            results = results.drop(["_rowid"])

        return results

    def to_batches(
        self, /, batch_size: Optional[int] = None, timeout: Optional[timedelta] = None
    ):
        raise NotImplementedError("to_batches not yet supported on a hybrid query")

    @staticmethod
    def _rank(results: pa.Table, column: str, ascending: bool = True):
        if len(results) == 0:
            return results
        # Get the _score column from results
        scores = results.column(column).to_numpy()
        sort_indices = np.argsort(scores)
        if not ascending:
            sort_indices = sort_indices[::-1]
        ranks = np.empty_like(sort_indices)
        ranks[sort_indices] = np.arange(len(scores)) + 1
        # replace the _score column with the ranks
        _score_idx = results.column_names.index(column)
        results = results.set_column(
            _score_idx, column, pa.array(ranks, type=pa.float32())
        )
        return results

    @staticmethod
    def _normalize_scores(scores: pa.Array, invert=False) -> pa.Array:
        if len(scores) == 0:
            return scores
        # normalize the scores by subtracting the min and dividing by the max
        min, max = pc.min_max(scores).values()
        rng = pc.subtract(max, min)

        if not pc.equal(rng, pa.scalar(0.0)).as_py():
            scores = pc.divide(pc.subtract(scores, min), rng)
        elif not pc.equal(max, pa.scalar(0.0)).as_py():
            # If rng is 0, then we at least want the scores to be 0
            scores = pc.subtract(scores, min)

        if invert:
            scores = pc.subtract(1, scores)

        return scores

    def rerank(
        self,
        reranker: Reranker = RRFReranker(),
        normalize: str = "score",
    ) -> LanceHybridQueryBuilder:
        """
        Rerank the hybrid search results using the specified reranker. The reranker
        must be an instance of Reranker class.

        Parameters
        ----------
        reranker: Reranker, default RRFReranker()
            The reranker to use. Must be an instance of Reranker class.
        normalize: str, default "score"
            The method to normalize the scores. Can be "rank" or "score". If "rank",
            the scores are converted to ranks and then normalized. If "score", the
            scores are normalized directly.
        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        if normalize not in ["rank", "score"]:
            raise ValueError("normalize must be 'rank' or 'score'.")
        if reranker and not isinstance(reranker, Reranker):
            raise ValueError("reranker must be an instance of Reranker class.")

        self._norm = normalize
        self._reranker = reranker
        if reranker.score == "all":
            self.with_row_id(True)

        return self

    def nprobes(self, nprobes: int) -> LanceHybridQueryBuilder:
        """
        Set the number of probes to use for vector search.

        Higher values will yield better recall (more likely to find vectors if
        they exist) at the expense of latency.

        Parameters
        ----------
        nprobes: int
            The number of probes to use.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._minimum_nprobes = nprobes
        self._maximum_nprobes = nprobes
        return self

    def minimum_nprobes(self, minimum_nprobes: int) -> LanceHybridQueryBuilder:
        """Set the minimum number of probes to use.

        See `nprobes` for more details.
        """
        self._minimum_nprobes = minimum_nprobes
        return self

    def maximum_nprobes(self, maximum_nprobes: int) -> LanceHybridQueryBuilder:
        """Set the maximum number of probes to use.

        See `nprobes` for more details.
        """
        self._maximum_nprobes = maximum_nprobes
        return self

    def distance_range(
        self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
    ) -> LanceHybridQueryBuilder:
        """
        Set the distance range to use.

        Only rows with distances within range [lower_bound, upper_bound)
        will be returned.

        Parameters
        ----------
        lower_bound: Optional[float]
            The lower bound of the distance range.
        upper_bound: Optional[float]
            The upper bound of the distance range.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        return self

    def ef(self, ef: int) -> LanceHybridQueryBuilder:
        """
        Set the number of candidates to consider during search.

        Higher values will yield better recall (more likely to find vectors if
        they exist) at the expense of latency.

        This only applies to the HNSW-related index.
        The default value is 1.5 * limit.

        Parameters
        ----------
        ef: int
            The number of candidates to consider during search.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._ef = ef
        return self

    def metric(self, metric: Literal["l2", "cosine", "dot"]) -> LanceHybridQueryBuilder:
        """Set the distance metric to use.

        This is an alias for distance_type() and may be deprecated in the future.
        Please use distance_type() instead.

        Parameters
        ----------
        metric: "l2" or "cosine" or "dot"
            The distance metric to use. By default "l2" is used.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        return self.distance_type(metric)

    def distance_type(
        self, distance_type: Literal["l2", "cosine", "dot"]
    ) -> "LanceHybridQueryBuilder":
        """Set the distance metric to use.

        When performing a vector search we try and find the "nearest" vectors according
        to some kind of distance metric. This parameter controls which distance metric
        to use.

        Note: if there is a vector index then the distance type used MUST match the
        distance type used to train the vector index. If this is not done then the
        results will be invalid.

        Parameters
        ----------
        distance_type: "l2" or "cosine" or "dot"
            The distance metric to use. By default "l2" is used.

        Returns
        -------
        LanceVectorQueryBuilder
            The LanceQueryBuilder object.
        """
        self._distance_type = distance_type.lower()
        return self

    def refine_factor(self, refine_factor: int) -> LanceHybridQueryBuilder:
        """
        Refine the vector search results by reading extra elements and
        re-ranking them in memory.

        Parameters
        ----------
        refine_factor: int
            The refine factor to use.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._refine_factor = refine_factor
        return self

    def vector(self, vector: Union[np.ndarray, list]) -> LanceHybridQueryBuilder:
        self._vector = vector
        return self

    def text(self, text: str | FullTextQuery) -> LanceHybridQueryBuilder:
        self._text = text
        return self

    def bypass_vector_index(self) -> LanceHybridQueryBuilder:
        """
        If this is called then any vector index is skipped

        An exhaustive (flat) search will be performed.  The query vector will
        be compared to every vector in the table.  At high scales this can be
        expensive.  However, this is often still useful.  For example, skipping
        the vector index can give you ground truth results which you can use to
        calculate your recall to select an appropriate value for nprobes.

        Returns
        -------
        LanceHybridQueryBuilder
            The LanceHybridQueryBuilder object.
        """
        self._bypass_vector_index = True
        return self

    def explain_plan(self, verbose: Optional[bool] = False) -> str:
        """Return the execution plan for this query.

        Examples
        --------
        >>> import lancedb
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
        >>> query = [100, 100]
        >>> plan = table.search(query).explain_plan(True)
        >>> print(plan) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
          GlobalLimitExec: skip=0, fetch=10
            FilterExec: _distance@2 IS NOT NULL
              SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                KNNVectorDistance: metric=l2
                  LanceRead: uri=..., projection=[vector], ...

        Parameters
        ----------
        verbose : bool, default False
            Use a verbose output format.

        Returns
        -------
        plan : str
        """  # noqa: E501
        self._create_query_builders()

        reranker_label = str(self._reranker) if self._reranker else "No reranker"
        vector_plan = self._table._explain_plan(
            self._vector_query.to_query_object(), verbose=verbose
        )
        fts_plan = self._table._explain_plan(
            self._fts_query.to_query_object(), verbose=verbose
        )
        # Indent sub-plans under the reranker
        indented_vector = "\n".join("  " + line for line in vector_plan.splitlines())
        indented_fts = "\n".join("  " + line for line in fts_plan.splitlines())
        return f"{reranker_label}\n  {indented_vector}\n  {indented_fts}"

    def analyze_plan(self):
        """Execute the query and display with runtime metrics.

        Returns
        -------
        plan : str
        """
        self._create_query_builders()

        results = ["Vector Search Plan:"]
        results.append(self._table._analyze_plan(self._vector_query.to_query_object()))
        results.append("FTS Search Plan:")
        results.append(self._table._analyze_plan(self._fts_query.to_query_object()))
        return "\n".join(results)

    def _create_query_builders(self):
        """Set up and configure the vector and FTS query builders."""
        vector_query, fts_query = self._validate_query(
            self._query, self._vector, self._text
        )
        self._fts_query = LanceFtsQueryBuilder(
            self._table, fts_query, fts_columns=self._fts_columns
        )
        vector_query = self._query_to_vector(
            self._table, vector_query, self._vector_column
        )
        self._vector_query = LanceVectorQueryBuilder(
            self._table, vector_query, self._vector_column
        )

        # Apply common configurations
        if self._limit:
            self._vector_query.limit(self._limit)
            self._fts_query.limit(self._limit)
        if self._columns:
            self._vector_query.select(self._columns)
            self._fts_query.select(self._columns)
        if self._where:
            self._vector_query.where(self._where, self._postfilter)
            self._fts_query.where(self._where, self._postfilter)
        if self._with_row_id:
            self._vector_query.with_row_id(True)
            self._fts_query.with_row_id(True)
        if self._phrase_query:
            self._fts_query.phrase_query(True)
        if self._distance_type:
            self._vector_query.metric(self._distance_type)
        if self._minimum_nprobes:
            self._vector_query.minimum_nprobes(self._minimum_nprobes)
        if self._maximum_nprobes is not None:
            self._vector_query.maximum_nprobes(self._maximum_nprobes)
        if self._refine_factor:
            self._vector_query.refine_factor(self._refine_factor)
        if self._ef:
            self._vector_query.ef(self._ef)
        if self._bypass_vector_index:
            self._vector_query.bypass_vector_index()
        if self._lower_bound or self._upper_bound:
            self._vector_query.distance_range(
                lower_bound=self._lower_bound, upper_bound=self._upper_bound
            )

        if self._reranker is None:
            self._reranker = RRFReranker()

              

  

            phrase_query

¶

phrase_query(phrase_query: bool = None) -> LanceHybridQueryBuilder

    

      
Set whether to use phrase query.

Parameters:

    
        
- 
          `phrase_query`
              (`bool`, default:
                  `None`
)
          –
          
            
If True, then the query will be wrapped in quotes and
double quotes replaced by single quotes.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1729
1730
1731
1732
1733
1734
1735
1736
1737
1738
1739
1740
1741
1742
1743
1744
def phrase_query(self, phrase_query: bool = None) -> LanceHybridQueryBuilder:
    """Set whether to use phrase query.

    Parameters
    ----------
    phrase_query: bool, default True
        If True, then the query will be wrapped in quotes and
        double quotes replaced by single quotes.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._phrase_query = phrase_query
    return self

            
    

            rerank

¶

rerank(reranker: Reranker = RRFReranker(), normalize: str = 'score') -> LanceHybridQueryBuilder

    

      
Rerank the hybrid search results using the specified reranker. The reranker
must be an instance of Reranker class.

Parameters:

    
        
- 
          `reranker`
              (`Reranker`, default:
                  `RRFReranker()`
)
          –
          
            
The reranker to use. Must be an instance of Reranker class.

          
        
        
- 
          `normalize`
              (`str`, default:
                  `'score'`
)
          –
          
            
The method to normalize the scores. Can be "rank" or "score". If "rank",
the scores are converted to ranks and then normalized. If "score", the
scores are normalized directly.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1885
1886
1887
1888
1889
1890
1891
1892
1893
1894
1895
1896
1897
1898
1899
1900
1901
1902
1903
1904
1905
1906
1907
1908
1909
1910
1911
1912
1913
1914
1915
1916
1917
def rerank(
    self,
    reranker: Reranker = RRFReranker(),
    normalize: str = "score",
) -> LanceHybridQueryBuilder:
    """
    Rerank the hybrid search results using the specified reranker. The reranker
    must be an instance of Reranker class.

    Parameters
    ----------
    reranker: Reranker, default RRFReranker()
        The reranker to use. Must be an instance of Reranker class.
    normalize: str, default "score"
        The method to normalize the scores. Can be "rank" or "score". If "rank",
        the scores are converted to ranks and then normalized. If "score", the
        scores are normalized directly.
    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    if normalize not in ["rank", "score"]:
        raise ValueError("normalize must be 'rank' or 'score'.")
    if reranker and not isinstance(reranker, Reranker):
        raise ValueError("reranker must be an instance of Reranker class.")

    self._norm = normalize
    self._reranker = reranker
    if reranker.score == "all":
        self.with_row_id(True)

    return self

            
    

            nprobes

¶

nprobes(nprobes: int) -> LanceHybridQueryBuilder

    

      
Set the number of probes to use for vector search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

Parameters:

    
        
- 
          `nprobes`
              (`int`)
          –
          
            
The number of probes to use.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1919
1920
1921
1922
1923
1924
1925
1926
1927
1928
1929
1930
1931
1932
1933
1934
1935
1936
1937
1938
def nprobes(self, nprobes: int) -> LanceHybridQueryBuilder:
    """
    Set the number of probes to use for vector search.

    Higher values will yield better recall (more likely to find vectors if
    they exist) at the expense of latency.

    Parameters
    ----------
    nprobes: int
        The number of probes to use.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._minimum_nprobes = nprobes
    self._maximum_nprobes = nprobes
    return self

            
    

            minimum_nprobes

¶

minimum_nprobes(minimum_nprobes: int) -> LanceHybridQueryBuilder

    

      
Set the minimum number of probes to use.

See `nprobes` for more details.

            
              Source code in `lancedb/query.py`
              
1940
1941
1942
1943
1944
1945
1946
def minimum_nprobes(self, minimum_nprobes: int) -> LanceHybridQueryBuilder:
    """Set the minimum number of probes to use.

    See `nprobes` for more details.
    """
    self._minimum_nprobes = minimum_nprobes
    return self

            
    

            maximum_nprobes

¶

maximum_nprobes(maximum_nprobes: int) -> LanceHybridQueryBuilder

    

      
Set the maximum number of probes to use.

See `nprobes` for more details.

            
              Source code in `lancedb/query.py`
              
1948
1949
1950
1951
1952
1953
1954
def maximum_nprobes(self, maximum_nprobes: int) -> LanceHybridQueryBuilder:
    """Set the maximum number of probes to use.

    See `nprobes` for more details.
    """
    self._maximum_nprobes = maximum_nprobes
    return self

            
    

            distance_range

¶

distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> LanceHybridQueryBuilder

    

      
Set the distance range to use.

Only rows with distances within range [lower_bound, upper_bound)
will be returned.

Parameters:

    
        
- 
          `lower_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The lower bound of the distance range.

          
        
        
- 
          `upper_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The upper bound of the distance range.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1956
1957
1958
1959
1960
1961
1962
1963
1964
1965
1966
1967
1968
1969
1970
1971
1972
1973
1974
1975
1976
1977
1978
1979
def distance_range(
    self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
) -> LanceHybridQueryBuilder:
    """
    Set the distance range to use.

    Only rows with distances within range [lower_bound, upper_bound)
    will be returned.

    Parameters
    ----------
    lower_bound: Optional[float]
        The lower bound of the distance range.
    upper_bound: Optional[float]
        The upper bound of the distance range.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._lower_bound = lower_bound
    self._upper_bound = upper_bound
    return self

            
    

            ef

¶

ef(ef: int) -> LanceHybridQueryBuilder

    

      
Set the number of candidates to consider during search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

This only applies to the HNSW-related index.
The default value is 1.5 * limit.

Parameters:

    
        
- 
          `ef`
              (`int`)
          –
          
            
The number of candidates to consider during search.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
1981
1982
1983
1984
1985
1986
1987
1988
1989
1990
1991
1992
1993
1994
1995
1996
1997
1998
1999
2000
2001
2002
def ef(self, ef: int) -> LanceHybridQueryBuilder:
    """
    Set the number of candidates to consider during search.

    Higher values will yield better recall (more likely to find vectors if
    they exist) at the expense of latency.

    This only applies to the HNSW-related index.
    The default value is 1.5 * limit.

    Parameters
    ----------
    ef: int
        The number of candidates to consider during search.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._ef = ef
    return self

            
    

            metric

¶

metric(metric: Literal['l2', 'cosine', 'dot']) -> LanceHybridQueryBuilder

    

      
Set the distance metric to use.

This is an alias for distance_type() and may be deprecated in the future.
Please use distance_type() instead.

Parameters:

    
        
- 
          `metric`
              (`Literal['l2', 'cosine', 'dot']`)
          –
          
            
The distance metric to use. By default "l2" is used.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014
2015
2016
2017
2018
2019
2020
def metric(self, metric: Literal["l2", "cosine", "dot"]) -> LanceHybridQueryBuilder:
    """Set the distance metric to use.

    This is an alias for distance_type() and may be deprecated in the future.
    Please use distance_type() instead.

    Parameters
    ----------
    metric: "l2" or "cosine" or "dot"
        The distance metric to use. By default "l2" is used.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    return self.distance_type(metric)

            
    

            distance_type

¶

distance_type(distance_type: Literal['l2', 'cosine', 'dot']) -> 'LanceHybridQueryBuilder'

    

      
Set the distance metric to use.

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

Parameters:

    
        
- 
          `distance_type`
              (`Literal['l2', 'cosine', 'dot']`)
          –
          
            
The distance metric to use. By default "l2" is used.

          
        
    

Returns:

    
        
- 
              `LanceVectorQueryBuilder`
          –
          
            
The LanceQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2032
2033
2034
2035
2036
2037
2038
2039
2040
2041
2042
2043
2044
2045
2046
def distance_type(
    self, distance_type: Literal["l2", "cosine", "dot"]
) -> "LanceHybridQueryBuilder":
    """Set the distance metric to use.

    When performing a vector search we try and find the "nearest" vectors according
    to some kind of distance metric. This parameter controls which distance metric
    to use.

    Note: if there is a vector index then the distance type used MUST match the
    distance type used to train the vector index. If this is not done then the
    results will be invalid.

    Parameters
    ----------
    distance_type: "l2" or "cosine" or "dot"
        The distance metric to use. By default "l2" is used.

    Returns
    -------
    LanceVectorQueryBuilder
        The LanceQueryBuilder object.
    """
    self._distance_type = distance_type.lower()
    return self

            
    

            refine_factor

¶

refine_factor(refine_factor: int) -> LanceHybridQueryBuilder

    

      
Refine the vector search results by reading extra elements and
re-ranking them in memory.

Parameters:

    
        
- 
          `refine_factor`
              (`int`)
          –
          
            
The refine factor to use.

          
        
    

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2048
2049
2050
2051
2052
2053
2054
2055
2056
2057
2058
2059
2060
2061
2062
2063
2064
def refine_factor(self, refine_factor: int) -> LanceHybridQueryBuilder:
    """
    Refine the vector search results by reading extra elements and
    re-ranking them in memory.

    Parameters
    ----------
    refine_factor: int
        The refine factor to use.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._refine_factor = refine_factor
    return self

            
    

            bypass_vector_index

¶

bypass_vector_index() -> LanceHybridQueryBuilder

    

      
If this is called then any vector index is skipped

An exhaustive (flat) search will be performed.  The query vector will
be compared to every vector in the table.  At high scales this can be
expensive.  However, this is often still useful.  For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

Returns:

    
        
- 
              `LanceHybridQueryBuilder`
          –
          
            
The LanceHybridQueryBuilder object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2074
2075
2076
2077
2078
2079
2080
2081
2082
2083
2084
2085
2086
2087
2088
2089
2090
def bypass_vector_index(self) -> LanceHybridQueryBuilder:
    """
    If this is called then any vector index is skipped

    An exhaustive (flat) search will be performed.  The query vector will
    be compared to every vector in the table.  At high scales this can be
    expensive.  However, this is often still useful.  For example, skipping
    the vector index can give you ground truth results which you can use to
    calculate your recall to select an appropriate value for nprobes.

    Returns
    -------
    LanceHybridQueryBuilder
        The LanceHybridQueryBuilder object.
    """
    self._bypass_vector_index = True
    return self

            
    

            explain_plan

¶

explain_plan(verbose: Optional[bool] = False) -> str

    

      
Return the execution plan for this query.

Examples:

    
>>> import lancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).explain_plan(True)
>>> print(plan)
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2092
2093
2094
2095
2096
2097
2098
2099
2100
2101
2102
2103
2104
2105
2106
2107
2108
2109
2110
2111
2112
2113
2114
2115
2116
2117
2118
2119
2120
2121
2122
2123
2124
2125
2126
2127
2128
2129
2130
2131
def explain_plan(self, verbose: Optional[bool] = False) -> str:
    """Return the execution plan for this query.

    Examples
    --------
    >>> import lancedb
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
    >>> query = [100, 100]
    >>> plan = table.search(query).explain_plan(True)
    >>> print(plan) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
      GlobalLimitExec: skip=0, fetch=10
        FilterExec: _distance@2 IS NOT NULL
          SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
            KNNVectorDistance: metric=l2
              LanceRead: uri=..., projection=[vector], ...

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501
    self._create_query_builders()

    reranker_label = str(self._reranker) if self._reranker else "No reranker"
    vector_plan = self._table._explain_plan(
        self._vector_query.to_query_object(), verbose=verbose
    )
    fts_plan = self._table._explain_plan(
        self._fts_query.to_query_object(), verbose=verbose
    )
    # Indent sub-plans under the reranker
    indented_vector = "\n".join("  " + line for line in vector_plan.splitlines())
    indented_fts = "\n".join("  " + line for line in fts_plan.splitlines())
    return f"{reranker_label}\n  {indented_vector}\n  {indented_fts}"

            
    

            analyze_plan

¶

analyze_plan()

    

      
Execute the query and display with runtime metrics.

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2133
2134
2135
2136
2137
2138
2139
2140
2141
2142
2143
2144
2145
2146
def analyze_plan(self):
    """Execute the query and display with runtime metrics.

    Returns
    -------
    plan : str
    """
    self._create_query_builders()

    results = ["Vector Search Plan:"]
    results.append(self._table._analyze_plan(self._vector_query.to_query_object()))
    results.append("FTS Search Plan:")
    results.append(self._table._analyze_plan(self._fts_query.to_query_object()))
    return "\n".join(results)

            
    

  

    

## Embeddings¶

            lancedb.embeddings.registry.EmbeddingFunctionRegistry

¶

    

      
This is a singleton class used to register embedding functions
and fetch them by name. It also handles serializing and deserializing.
You can implement your own embedding function by subclassing EmbeddingFunction
or TextEmbeddingFunction and registering it with the registry.

NOTE: Here TEXT is a type alias for Union[str, List[str], pa.Array,
      pa.ChunkedArray, np.ndarray]

Examples:

    
>>> registry = EmbeddingFunctionRegistry.get_instance()
>>> @registry.register("my-embedding-function")
... class MyEmbeddingFunction(EmbeddingFunction):
...     def ndims(self) -> int:
...         return 128
...
...     def compute_query_embeddings(self, query: str, *args, **kwargs):
...         return self.compute_source_embeddings(query, *args, **kwargs)
...
...     def compute_source_embeddings(self, texts, *args, **kwargs):
...         return [np.random.rand(self.ndims()) for _ in range(len(texts))]
...
>>> registry.get("my-embedding-function")
<class 'lancedb.embeddings.registry.MyEmbeddingFunction'>

              
                Source code in `lancedb/embeddings/registry.py`
                
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
class EmbeddingFunctionRegistry:
    """
    This is a singleton class used to register embedding functions
    and fetch them by name. It also handles serializing and deserializing.
    You can implement your own embedding function by subclassing EmbeddingFunction
    or TextEmbeddingFunction and registering it with the registry.

    NOTE: Here TEXT is a type alias for Union[str, List[str], pa.Array,
          pa.ChunkedArray, np.ndarray]

    Examples
    --------
    >>> registry = EmbeddingFunctionRegistry.get_instance()
    >>> @registry.register("my-embedding-function")
    ... class MyEmbeddingFunction(EmbeddingFunction):
    ...     def ndims(self) -> int:
    ...         return 128
    ...
    ...     def compute_query_embeddings(self, query: str, *args, **kwargs):
    ...         return self.compute_source_embeddings(query, *args, **kwargs)
    ...
    ...     def compute_source_embeddings(self, texts, *args, **kwargs):
    ...         return [np.random.rand(self.ndims()) for _ in range(len(texts))]
    ...
    >>> registry.get("my-embedding-function")
    <class 'lancedb.embeddings.registry.MyEmbeddingFunction'>
    """

    @classmethod
    def get_instance(cls):
        return __REGISTRY__

    def __init__(self):
        self._functions = {}
        self._variables = {}

    def register(self, alias: Optional[str] = None):
        """
        This creates a decorator that can be used to register
        an EmbeddingFunction.

        Parameters
        ----------
        alias : Optional[str]
            a human friendly name for the embedding function. If not
            provided, the class name will be used.
        """

        # This is a decorator for a class that inherits from BaseModel
        # It adds the class to the registry
        def decorator(cls):
            if not issubclass(cls, EmbeddingFunction):
                raise TypeError("Must be a subclass of EmbeddingFunction")
            if cls.__name__ in self._functions:
                raise KeyError(f"{cls.__name__} was already registered")
            key = alias or cls.__name__
            self._functions[key] = cls
            cls.__embedding_function_registry_alias__ = alias
            return cls

        return decorator

    def reset(self):
        """
        Reset the registry to its initial state
        """
        self._functions = {}

    def get(self, name: str) -> Type[EmbeddingFunction]:
        """
        Fetch an embedding function class by name

        Parameters
        ----------
        name : str
            The name of the embedding function to fetch
            Either the alias or the class name if no alias was provided
            during registration
        """
        return self._functions[name]

    def parse_functions(
        self, metadata: Optional[Dict[bytes, bytes]]
    ) -> Dict[str, "EmbeddingFunctionConfig"]:
        """
        Parse the metadata from an arrow table and
        return a mapping of the vector column to the
        embedding function and source column

        Parameters
        ----------
        metadata : Optional[Dict[bytes, bytes]]
            The metadata from an arrow table. Note that
            the keys and values are bytes (pyarrow api)

        Returns
        -------
        functions : dict
            A mapping of vector column name to embedding function.
            An empty dict is returned if input is None or does not
            contain b"embedding_functions".
        """
        if metadata is None:
            return {}
        # Look at both bytes and string keys, since we might use either
        serialized = metadata.get(
            b"embedding_functions", metadata.get("embedding_functions")
        )
        if serialized is None:
            return {}
        raw_list = json.loads(serialized.decode("utf-8"))
        return {
            obj["vector_column"]: EmbeddingFunctionConfig(
                vector_column=obj["vector_column"],
                source_column=obj["source_column"],
                function=self.get(obj["name"]).create(**obj["model"]),
            )
            for obj in raw_list
        }

    def function_to_metadata(self, conf: "EmbeddingFunctionConfig"):
        """
        Convert the given embedding function and source / vector column configs
        into a config dictionary that can be serialized into arrow metadata
        """
        func = conf.function
        name = getattr(
            func, "__embedding_function_registry_alias__", func.__class__.__name__
        )
        json_data = func.safe_model_dump()
        return {
            "name": name,
            "model": json_data,
            "source_column": conf.source_column,
            "vector_column": conf.vector_column,
        }

    def get_table_metadata(self, func_list):
        """
        Convert a list of embedding functions and source / vector configs
        into a config dictionary that can be serialized into arrow metadata
        """
        if func_list is None or len(func_list) == 0:
            return None
        json_data = [self.function_to_metadata(func) for func in func_list]
        # Note that metadata dictionary values must be bytes
        # so we need to json dump then utf8 encode
        metadata = json.dumps(json_data, indent=2).encode("utf-8")
        return {"embedding_functions": metadata}

    def set_var(self, name: str, value: str) -> None:
        """
        Set a variable. These can be accessed in embedding configuration using
        the syntax `$var:variable_name`. If they are not set, an error will be
        thrown letting you know which variable is missing. If you want to supply
        a default value, you can add an additional part in the configuration
        like so: `$var:variable_name:default_value`. Default values can be
        used for runtime configurations that are not sensitive, such as
        whether to use a GPU for inference.

        The name must not contain a colon. Default values can contain colons.
        """
        if ":" in name:
            raise ValueError("Variable names cannot contain colons")
        self._variables[name] = value

    def get_var(self, name: str) -> str:
        """
        Get a variable.
        """
        return self._variables[name]

              

  

            register

¶

register(alias: Optional[str] = None)

    

      
This creates a decorator that can be used to register
an EmbeddingFunction.

Parameters:

    
        
- 
          `alias`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
a human friendly name for the embedding function. If not
provided, the class name will be used.

          
        
    

            
              Source code in `lancedb/embeddings/registry.py`
              
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
def register(self, alias: Optional[str] = None):
    """
    This creates a decorator that can be used to register
    an EmbeddingFunction.

    Parameters
    ----------
    alias : Optional[str]
        a human friendly name for the embedding function. If not
        provided, the class name will be used.
    """

    # This is a decorator for a class that inherits from BaseModel
    # It adds the class to the registry
    def decorator(cls):
        if not issubclass(cls, EmbeddingFunction):
            raise TypeError("Must be a subclass of EmbeddingFunction")
        if cls.__name__ in self._functions:
            raise KeyError(f"{cls.__name__} was already registered")
        key = alias or cls.__name__
        self._functions[key] = cls
        cls.__embedding_function_registry_alias__ = alias
        return cls

    return decorator

            
    

            reset

¶

reset()

    

      
Reset the registry to its initial state

            
              Source code in `lancedb/embeddings/registry.py`
              
72
73
74
75
76
def reset(self):
    """
    Reset the registry to its initial state
    """
    self._functions = {}

            
    

            get

¶

get(name: str) -> Type[EmbeddingFunction]

    

      
Fetch an embedding function class by name

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the embedding function to fetch
Either the alias or the class name if no alias was provided
during registration

          
        
    

            
              Source code in `lancedb/embeddings/registry.py`
              
78
79
80
81
82
83
84
85
86
87
88
89
def get(self, name: str) -> Type[EmbeddingFunction]:
    """
    Fetch an embedding function class by name

    Parameters
    ----------
    name : str
        The name of the embedding function to fetch
        Either the alias or the class name if no alias was provided
        during registration
    """
    return self._functions[name]

            
    

            parse_functions

¶

parse_functions(metadata: Optional[Dict[bytes, bytes]]) -> Dict[str, EmbeddingFunctionConfig]

    

      
Parse the metadata from an arrow table and
return a mapping of the vector column to the
embedding function and source column

Parameters:

    
        
- 
          `metadata`
              (`Optional[Dict[bytes, bytes]]`)
          –
          
            
The metadata from an arrow table. Note that
the keys and values are bytes (pyarrow api)

          
        
    

Returns:

    
        
- 
`functions` (              `dict`
)          –
          
            
A mapping of vector column name to embedding function.
An empty dict is returned if input is None or does not
contain b"embedding_functions".

          
        
    

            
              Source code in `lancedb/embeddings/registry.py`
              
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
def parse_functions(
    self, metadata: Optional[Dict[bytes, bytes]]
) -> Dict[str, "EmbeddingFunctionConfig"]:
    """
    Parse the metadata from an arrow table and
    return a mapping of the vector column to the
    embedding function and source column

    Parameters
    ----------
    metadata : Optional[Dict[bytes, bytes]]
        The metadata from an arrow table. Note that
        the keys and values are bytes (pyarrow api)

    Returns
    -------
    functions : dict
        A mapping of vector column name to embedding function.
        An empty dict is returned if input is None or does not
        contain b"embedding_functions".
    """
    if metadata is None:
        return {}
    # Look at both bytes and string keys, since we might use either
    serialized = metadata.get(
        b"embedding_functions", metadata.get("embedding_functions")
    )
    if serialized is None:
        return {}
    raw_list = json.loads(serialized.decode("utf-8"))
    return {
        obj["vector_column"]: EmbeddingFunctionConfig(
            vector_column=obj["vector_column"],
            source_column=obj["source_column"],
            function=self.get(obj["name"]).create(**obj["model"]),
        )
        for obj in raw_list
    }

            
    

            function_to_metadata

¶

function_to_metadata(conf: EmbeddingFunctionConfig)

    

      
Convert the given embedding function and source / vector column configs
into a config dictionary that can be serialized into arrow metadata

            
              Source code in `lancedb/embeddings/registry.py`
              
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
def function_to_metadata(self, conf: "EmbeddingFunctionConfig"):
    """
    Convert the given embedding function and source / vector column configs
    into a config dictionary that can be serialized into arrow metadata
    """
    func = conf.function
    name = getattr(
        func, "__embedding_function_registry_alias__", func.__class__.__name__
    )
    json_data = func.safe_model_dump()
    return {
        "name": name,
        "model": json_data,
        "source_column": conf.source_column,
        "vector_column": conf.vector_column,
    }

            
    

            get_table_metadata

¶

get_table_metadata(func_list)

    

      
Convert a list of embedding functions and source / vector configs
into a config dictionary that can be serialized into arrow metadata

            
              Source code in `lancedb/embeddings/registry.py`
              
147
148
149
150
151
152
153
154
155
156
157
158
def get_table_metadata(self, func_list):
    """
    Convert a list of embedding functions and source / vector configs
    into a config dictionary that can be serialized into arrow metadata
    """
    if func_list is None or len(func_list) == 0:
        return None
    json_data = [self.function_to_metadata(func) for func in func_list]
    # Note that metadata dictionary values must be bytes
    # so we need to json dump then utf8 encode
    metadata = json.dumps(json_data, indent=2).encode("utf-8")
    return {"embedding_functions": metadata}

            
    

            set_var

¶

set_var(name: str, value: str) -> None

    

      
Set a variable. These can be accessed in embedding configuration using
the syntax `$var:variable_name`. If they are not set, an error will be
thrown letting you know which variable is missing. If you want to supply
a default value, you can add an additional part in the configuration
like so: `$var:variable_name:default_value`. Default values can be
used for runtime configurations that are not sensitive, such as
whether to use a GPU for inference.

The name must not contain a colon. Default values can contain colons.

            
              Source code in `lancedb/embeddings/registry.py`
              
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
def set_var(self, name: str, value: str) -> None:
    """
    Set a variable. These can be accessed in embedding configuration using
    the syntax `$var:variable_name`. If they are not set, an error will be
    thrown letting you know which variable is missing. If you want to supply
    a default value, you can add an additional part in the configuration
    like so: `$var:variable_name:default_value`. Default values can be
    used for runtime configurations that are not sensitive, such as
    whether to use a GPU for inference.

    The name must not contain a colon. Default values can contain colons.
    """
    if ":" in name:
        raise ValueError("Variable names cannot contain colons")
    self._variables[name] = value

            
    

            get_var

¶

get_var(name: str) -> str

    

      
Get a variable.

            
              Source code in `lancedb/embeddings/registry.py`
              
176
177
178
179
180
def get_var(self, name: str) -> str:
    """
    Get a variable.
    """
    return self._variables[name]

            
    

  

    

            lancedb.embeddings.base.EmbeddingFunctionConfig

¶

    
            

              Bases: `BaseModel`

      
This model encapsulates the configuration for a embedding function
in a lancedb table. It holds the embedding function, the source column,
and the vector column

              
                Source code in `lancedb/embeddings/base.py`
                
199
200
201
202
203
204
205
206
207
208
class EmbeddingFunctionConfig(BaseModel):
    """
    This model encapsulates the configuration for a embedding function
    in a lancedb table. It holds the embedding function, the source column,
    and the vector column
    """

    vector_column: str
    source_column: str
    function: EmbeddingFunction

              

  

  

    

            lancedb.embeddings.base.EmbeddingFunction

¶

    
            

              Bases: `BaseModel`, `ABC`

      
An ABC for embedding functions.

All concrete embedding functions must implement the following methods:
1. compute_query_embeddings() which takes a query and returns a list of embeddings
2. compute_source_embeddings() which returns a list of embeddings for
   the source column
For text data, the two will be the same. For multi-modal data, the source column
might be images and the vector column might be text.
3. ndims() which returns the number of dimensions of the vector column

              
                Source code in `lancedb/embeddings/base.py`
                
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
class EmbeddingFunction(BaseModel, ABC):
    """
    An ABC for embedding functions.

    All concrete embedding functions must implement the following methods:
    1. compute_query_embeddings() which takes a query and returns a list of embeddings
    2. compute_source_embeddings() which returns a list of embeddings for
       the source column
    For text data, the two will be the same. For multi-modal data, the source column
    might be images and the vector column might be text.
    3. ndims() which returns the number of dimensions of the vector column
    """

    __slots__ = ("__weakref__",)  # pydantic 1.x compatibility
    max_retries: int = (
        7  # Setting 0 disables retires. Maybe this should not be enabled by default,
    )
    _ndims: int = PrivateAttr()
    _original_args: dict = PrivateAttr()

    @classmethod
    def create(cls, **kwargs):
        """
        Create an instance of the embedding function
        """
        resolved_kwargs = cls.__resolveVariables(kwargs)
        instance = cls(**resolved_kwargs)
        instance._original_args = kwargs
        return instance

    @classmethod
    def __resolveVariables(cls, args: dict) -> dict:
        """
        Resolve variables in the args
        """
        from .registry import EmbeddingFunctionRegistry

        new_args = copy.deepcopy(args)

        registry = EmbeddingFunctionRegistry.get_instance()
        sensitive_keys = cls.sensitive_keys()
        for k, v in new_args.items():
            if isinstance(v, str) and not v.startswith("$var:") and k in sensitive_keys:
                exc = ValueError(
                    f"Sensitive key '{k}' cannot be set to a hardcoded value"
                )
                add_note(exc, "Help: Use $var: to set sensitive keys to variables")
                raise exc

            if isinstance(v, str) and v.startswith("$var:"):
                parts = v[5:].split(":", maxsplit=1)
                if len(parts) == 1:
                    try:
                        new_args[k] = registry.get_var(parts[0])
                    except KeyError:
                        exc = ValueError(
                            "Variable '{}' not found in registry".format(parts[0])
                        )
                        add_note(
                            exc,
                            "Help: Variables are reset in new Python sessions. "
                            "Use `registry.set_var` to set variables.",
                        )
                        raise exc
                else:
                    name, default = parts
                    try:
                        new_args[k] = registry.get_var(name)
                    except KeyError:
                        new_args[k] = default
        return new_args

    @staticmethod
    def sensitive_keys() -> List[str]:
        """
        Return a list of keys that are sensitive and should not be allowed
        to be set to hardcoded values in the config. For example, API keys.
        """
        return []

    @abstractmethod
    def compute_query_embeddings(self, *args, **kwargs) -> list[Union[np.array, None]]:
        """
        Compute the embeddings for a given user query

        Returns
        -------
        A list of embeddings for each input. The embedding of each input can be None
        when the embedding is not valid.
        """
        pass

    @abstractmethod
    def compute_source_embeddings(self, *args, **kwargs) -> list[Union[np.array, None]]:
        """Compute the embeddings for the source column in the database

        Returns
        -------
        A list of embeddings for each input. The embedding of each input can be None
        when the embedding is not valid.
        """
        pass

    def compute_query_embeddings_with_retry(
        self, *args, **kwargs
    ) -> list[Union[np.array, None]]:
        """Compute the embeddings for a given user query with retries

        Returns
        -------
        A list of embeddings for each input. The embedding of each input can be None
        when the embedding is not valid.
        """
        return retry_with_exponential_backoff(
            self.compute_query_embeddings, max_retries=self.max_retries
        )(
            *args,
            **kwargs,
        )

    def compute_source_embeddings_with_retry(
        self, *args, **kwargs
    ) -> list[Union[np.array, None]]:
        """Compute the embeddings for the source column in the database with retries.

        Returns
        -------
        A list of embeddings for each input. The embedding of each input can be None
        when the embedding is not valid.
        """
        return retry_with_exponential_backoff(
            self.compute_source_embeddings, max_retries=self.max_retries
        )(*args, **kwargs)

    def sanitize_input(self, texts: TEXT) -> Union[List[str], np.ndarray]:
        """
        Sanitize the input to the embedding function.
        """
        if isinstance(texts, str):
            texts = [texts]
        elif isinstance(texts, pa.Array):
            texts = texts.to_pylist()
        elif isinstance(texts, pa.ChunkedArray):
            texts = texts.combine_chunks().to_pylist()
        return texts

    def safe_model_dump(self):
        if not hasattr(self, "_original_args"):
            raise ValueError(
                "EmbeddingFunction was not created with EmbeddingFunction.create()"
            )
        return self._original_args

    @abstractmethod
    def ndims(self) -> int:
        """
        Return the dimensions of the vector column
        """
        pass

    def SourceField(self, **kwargs):
        """
        Creates a pydantic Field that can automatically annotate
        the source column for this embedding function
        """
        return Field(json_schema_extra={"source_column_for": self}, **kwargs)

    def VectorField(self, **kwargs):
        """
        Creates a pydantic Field that can automatically annotate
        the target vector column for this embedding function
        """
        return Field(json_schema_extra={"vector_column_for": self}, **kwargs)

    def __eq__(self, __value: object) -> bool:
        if not hasattr(__value, "__dict__"):
            return False
        return vars(self) == vars(__value)

    def __hash__(self) -> int:
        return hash(frozenset(vars(self).items()))

              

  

            create

  
      `classmethod`
  

¶

create(**kwargs)

    

      
Create an instance of the embedding function

            
              Source code in `lancedb/embeddings/base.py`
              
36
37
38
39
40
41
42
43
44
@classmethod
def create(cls, **kwargs):
    """
    Create an instance of the embedding function
    """
    resolved_kwargs = cls.__resolveVariables(kwargs)
    instance = cls(**resolved_kwargs)
    instance._original_args = kwargs
    return instance

            
    

            __resolveVariables

  
      `classmethod`
  

¶

__resolveVariables(args: dict) -> dict

    

      
Resolve variables in the args

            
              Source code in `lancedb/embeddings/base.py`
              
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
@classmethod
def __resolveVariables(cls, args: dict) -> dict:
    """
    Resolve variables in the args
    """
    from .registry import EmbeddingFunctionRegistry

    new_args = copy.deepcopy(args)

    registry = EmbeddingFunctionRegistry.get_instance()
    sensitive_keys = cls.sensitive_keys()
    for k, v in new_args.items():
        if isinstance(v, str) and not v.startswith("$var:") and k in sensitive_keys:
            exc = ValueError(
                f"Sensitive key '{k}' cannot be set to a hardcoded value"
            )
            add_note(exc, "Help: Use $var: to set sensitive keys to variables")
            raise exc

        if isinstance(v, str) and v.startswith("$var:"):
            parts = v[5:].split(":", maxsplit=1)
            if len(parts) == 1:
                try:
                    new_args[k] = registry.get_var(parts[0])
                except KeyError:
                    exc = ValueError(
                        "Variable '{}' not found in registry".format(parts[0])
                    )
                    add_note(
                        exc,
                        "Help: Variables are reset in new Python sessions. "
                        "Use `registry.set_var` to set variables.",
                    )
                    raise exc
            else:
                name, default = parts
                try:
                    new_args[k] = registry.get_var(name)
                except KeyError:
                    new_args[k] = default
    return new_args

            
    

            sensitive_keys

  
      `staticmethod`
  

¶

sensitive_keys() -> List[str]

    

      
Return a list of keys that are sensitive and should not be allowed
to be set to hardcoded values in the config. For example, API keys.

            
              Source code in `lancedb/embeddings/base.py`
              
88
89
90
91
92
93
94
@staticmethod
def sensitive_keys() -> List[str]:
    """
    Return a list of keys that are sensitive and should not be allowed
    to be set to hardcoded values in the config. For example, API keys.
    """
    return []

            
    

            compute_query_embeddings

  
      `abstractmethod`
  

¶

compute_query_embeddings(*args, **kwargs) -> list[Union[array, None]]

    

      
Compute the embeddings for a given user query

Returns:

    
        
- 
              `A list of embeddings for each input. The embedding of each input can be None`
          –
          
            
          
        
        
- 
              `when the embedding is not valid.`
          –
          
            
          
        
    

            
              Source code in `lancedb/embeddings/base.py`
              
 96
 97
 98
 99
100
101
102
103
104
105
106
@abstractmethod
def compute_query_embeddings(self, *args, **kwargs) -> list[Union[np.array, None]]:
    """
    Compute the embeddings for a given user query

    Returns
    -------
    A list of embeddings for each input. The embedding of each input can be None
    when the embedding is not valid.
    """
    pass

            
    

            compute_source_embeddings

  
      `abstractmethod`
  

¶

compute_source_embeddings(*args, **kwargs) -> list[Union[array, None]]

    

      
Compute the embeddings for the source column in the database

Returns:

    
        
- 
              `A list of embeddings for each input. The embedding of each input can be None`
          –
          
            
          
        
        
- 
              `when the embedding is not valid.`
          –
          
            
          
        
    

            
              Source code in `lancedb/embeddings/base.py`
              
108
109
110
111
112
113
114
115
116
117
@abstractmethod
def compute_source_embeddings(self, *args, **kwargs) -> list[Union[np.array, None]]:
    """Compute the embeddings for the source column in the database

    Returns
    -------
    A list of embeddings for each input. The embedding of each input can be None
    when the embedding is not valid.
    """
    pass

            
    

            compute_query_embeddings_with_retry

¶

compute_query_embeddings_with_retry(*args, **kwargs) -> list[Union[array, None]]

    

      
Compute the embeddings for a given user query with retries

Returns:

    
        
- 
              `A list of embeddings for each input. The embedding of each input can be None`
          –
          
            
          
        
        
- 
              `when the embedding is not valid.`
          –
          
            
          
        
    

            
              Source code in `lancedb/embeddings/base.py`
              
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
def compute_query_embeddings_with_retry(
    self, *args, **kwargs
) -> list[Union[np.array, None]]:
    """Compute the embeddings for a given user query with retries

    Returns
    -------
    A list of embeddings for each input. The embedding of each input can be None
    when the embedding is not valid.
    """
    return retry_with_exponential_backoff(
        self.compute_query_embeddings, max_retries=self.max_retries
    )(
        *args,
        **kwargs,
    )

            
    

            compute_source_embeddings_with_retry

¶

compute_source_embeddings_with_retry(*args, **kwargs) -> list[Union[array, None]]

    

      
Compute the embeddings for the source column in the database with retries.

Returns:

    
        
- 
              `A list of embeddings for each input. The embedding of each input can be None`
          –
          
            
          
        
        
- 
              `when the embedding is not valid.`
          –
          
            
          
        
    

            
              Source code in `lancedb/embeddings/base.py`
              
136
137
138
139
140
141
142
143
144
145
146
147
148
def compute_source_embeddings_with_retry(
    self, *args, **kwargs
) -> list[Union[np.array, None]]:
    """Compute the embeddings for the source column in the database with retries.

    Returns
    -------
    A list of embeddings for each input. The embedding of each input can be None
    when the embedding is not valid.
    """
    return retry_with_exponential_backoff(
        self.compute_source_embeddings, max_retries=self.max_retries
    )(*args, **kwargs)

            
    

            sanitize_input

¶

sanitize_input(texts: TEXT) -> Union[List[str], ndarray]

    

      
Sanitize the input to the embedding function.

            
              Source code in `lancedb/embeddings/base.py`
              
150
151
152
153
154
155
156
157
158
159
160
def sanitize_input(self, texts: TEXT) -> Union[List[str], np.ndarray]:
    """
    Sanitize the input to the embedding function.
    """
    if isinstance(texts, str):
        texts = [texts]
    elif isinstance(texts, pa.Array):
        texts = texts.to_pylist()
    elif isinstance(texts, pa.ChunkedArray):
        texts = texts.combine_chunks().to_pylist()
    return texts

            
    

            ndims

  
      `abstractmethod`
  

¶

ndims() -> int

    

      
Return the dimensions of the vector column

            
              Source code in `lancedb/embeddings/base.py`
              
169
170
171
172
173
174
@abstractmethod
def ndims(self) -> int:
    """
    Return the dimensions of the vector column
    """
    pass

            
    

            SourceField

¶

SourceField(**kwargs)

    

      
Creates a pydantic Field that can automatically annotate
the source column for this embedding function

            
              Source code in `lancedb/embeddings/base.py`
              
176
177
178
179
180
181
def SourceField(self, **kwargs):
    """
    Creates a pydantic Field that can automatically annotate
    the source column for this embedding function
    """
    return Field(json_schema_extra={"source_column_for": self}, **kwargs)

            
    

            VectorField

¶

VectorField(**kwargs)

    

      
Creates a pydantic Field that can automatically annotate
the target vector column for this embedding function

            
              Source code in `lancedb/embeddings/base.py`
              
183
184
185
186
187
188
def VectorField(self, **kwargs):
    """
    Creates a pydantic Field that can automatically annotate
    the target vector column for this embedding function
    """
    return Field(json_schema_extra={"vector_column_for": self}, **kwargs)

            
    

  

    

            lancedb.embeddings.base.TextEmbeddingFunction

¶

    
            

              Bases: `EmbeddingFunction`

      
A callable ABC for embedding functions that take text as input

              
                Source code in `lancedb/embeddings/base.py`
                
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
class TextEmbeddingFunction(EmbeddingFunction):
    """
    A callable ABC for embedding functions that take text as input
    """

    def compute_query_embeddings(
        self, query: str, *args, **kwargs
    ) -> list[Union[np.array, None]]:
        return self.compute_source_embeddings(query, *args, **kwargs)

    def compute_source_embeddings(
        self, texts: TEXT, *args, **kwargs
    ) -> list[Union[np.array, None]]:
        texts = self.sanitize_input(texts)
        return self.generate_embeddings(texts)

    @abstractmethod
    def generate_embeddings(
        self, texts: Union[List[str], np.ndarray], *args, **kwargs
    ) -> list[Union[np.array, None]]:
        """Generate the embeddings for the given texts"""
        pass

              

  

            generate_embeddings

  
      `abstractmethod`
  

¶

generate_embeddings(texts: Union[List[str], ndarray], *args, **kwargs) -> list[Union[array, None]]

    

      
Generate the embeddings for the given texts

            
              Source code in `lancedb/embeddings/base.py`
              
227
228
229
230
231
232
@abstractmethod
def generate_embeddings(
    self, texts: Union[List[str], np.ndarray], *args, **kwargs
) -> list[Union[np.array, None]]:
    """Generate the embeddings for the given texts"""
    pass

            
    

  

    

            lancedb.embeddings.sentence_transformers.SentenceTransformerEmbeddings

¶

    
            

              Bases: `TextEmbeddingFunction`

      
An embedding function that uses the sentence-transformers library

https://huggingface.co/sentence-transformers

Parameters:

    
        
- 
          `name`
          –
          
            
The name of the model to use.

          
        
        
- 
          `device`
          –
          
            
The device to use for the model

          
        
        
- 
          `normalize`
          –
          
            
Whether to normalize the embeddings

          
        
        
- 
          `trust_remote_code`
          –
          
            
Whether to trust the remote code

          
        
    

              
                Source code in `lancedb/embeddings/sentence_transformers.py`
                
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
@register("sentence-transformers")
class SentenceTransformerEmbeddings(TextEmbeddingFunction):
    """
    An embedding function that uses the sentence-transformers library

    https://huggingface.co/sentence-transformers

    Parameters
    ----------
    name: str, default "all-MiniLM-L6-v2"
        The name of the model to use.
    device: str, default "cpu"
        The device to use for the model
    normalize: bool, default True
        Whether to normalize the embeddings
    trust_remote_code: bool, default True
        Whether to trust the remote code
    """

    name: str = "all-MiniLM-L6-v2"
    device: str = "cpu"
    normalize: bool = True
    trust_remote_code: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ndims = None

    @property
    def embedding_model(self):
        """
        Get the sentence-transformers embedding model specified by the
        name, device, and trust_remote_code. This is cached so that the
        model is only loaded once per process.
        """
        return self.get_embedding_model()

    def ndims(self):
        if self._ndims is None:
            self._ndims = len(self.generate_embeddings("foo")[0])
        return self._ndims

    def generate_embeddings(
        self, texts: Union[List[str], np.ndarray]
    ) -> List[np.array]:
        """
        Get the embeddings for the given texts

        Parameters
        ----------
        texts: list[str] or np.ndarray (of str)
            The texts to embed
        """
        return self.embedding_model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
        ).tolist()

    @weak_lru(maxsize=1)
    def get_embedding_model(self):
        """
        Get the sentence-transformers embedding model specified by the
        name, device, and trust_remote_code. This is cached so that the
        model is only loaded once per process.

        TODO: use lru_cache instead with a reasonable/configurable maxsize
        """
        sentence_transformers = attempt_import_or_raise(
            "sentence_transformers", "sentence-transformers"
        )
        return sentence_transformers.SentenceTransformer(
            self.name, device=self.device, trust_remote_code=self.trust_remote_code
        )

              

  

            embedding_model

  
      `property`
  

¶

embedding_model

    

      
Get the sentence-transformers embedding model specified by the
name, device, and trust_remote_code. This is cached so that the
model is only loaded once per process.

    

            generate_embeddings

¶

generate_embeddings(texts: Union[List[str], ndarray]) -> List[array]

    

      
Get the embeddings for the given texts

Parameters:

    
        
- 
          `texts`
              (`Union[List[str], ndarray]`)
          –
          
            
The texts to embed

          
        
    

            
              Source code in `lancedb/embeddings/sentence_transformers.py`
              
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
def generate_embeddings(
    self, texts: Union[List[str], np.ndarray]
) -> List[np.array]:
    """
    Get the embeddings for the given texts

    Parameters
    ----------
    texts: list[str] or np.ndarray (of str)
        The texts to embed
    """
    return self.embedding_model.encode(
        list(texts),
        convert_to_numpy=True,
        normalize_embeddings=self.normalize,
    ).tolist()

            
    

            get_embedding_model

¶

get_embedding_model()

    

      
Get the sentence-transformers embedding model specified by the
name, device, and trust_remote_code. This is cached so that the
model is only loaded once per process.

TODO: use lru_cache instead with a reasonable/configurable maxsize

            
              Source code in `lancedb/embeddings/sentence_transformers.py`
              
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
@weak_lru(maxsize=1)
def get_embedding_model(self):
    """
    Get the sentence-transformers embedding model specified by the
    name, device, and trust_remote_code. This is cached so that the
    model is only loaded once per process.

    TODO: use lru_cache instead with a reasonable/configurable maxsize
    """
    sentence_transformers = attempt_import_or_raise(
        "sentence_transformers", "sentence-transformers"
    )
    return sentence_transformers.SentenceTransformer(
        self.name, device=self.device, trust_remote_code=self.trust_remote_code
    )

            
    

  

    

            lancedb.embeddings.openai.OpenAIEmbeddings

¶

    
            

              Bases: `TextEmbeddingFunction`

      
An embedding function that uses the OpenAI API

https://platform.openai.com/docs/guides/embeddings

This can also be used for open source models that
are compatible with the OpenAI API.

  Notes
  
If you're running an Ollama server locally,
you can just override the `base_url` parameter
and provide the Ollama embedding model you want
to use (https://ollama.com/library):

from lancedb.embeddings import get_registry
openai = get_registry().get("openai")
embedding_function = openai.create(
    name="<ollama-embedding-model-name>",
    base_url="http://localhost:11434",
    )

              
                Source code in `lancedb/embeddings/openai.py`
                
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
@register("openai")
class OpenAIEmbeddings(TextEmbeddingFunction):
    """
    An embedding function that uses the OpenAI API

    https://platform.openai.com/docs/guides/embeddings

    This can also be used for open source models that
    are compatible with the OpenAI API.

    Notes
    -----
    If you're running an Ollama server locally,
    you can just override the `base_url` parameter
    and provide the Ollama embedding model you want
    to use (https://ollama.com/library):

    ```python
    from lancedb.embeddings import get_registry
    openai = get_registry().get("openai")
    embedding_function = openai.create(
        name="<ollama-embedding-model-name>",
        base_url="http://localhost:11434",
        )
    ```

    """

    name: str = "text-embedding-ada-002"
    dim: Optional[int] = None
    base_url: Optional[str] = None
    default_headers: Optional[dict] = None
    organization: Optional[str] = None
    api_key: Optional[str] = None

    # Set true to use Azure OpenAI API
    use_azure: bool = False

    def ndims(self):
        return self._ndims

    @staticmethod
    def sensitive_keys():
        return ["api_key"]

    @staticmethod
    def model_names():
        return [
            "text-embedding-ada-002",
            "text-embedding-3-large",
            "text-embedding-3-small",
        ]

    @cached_property
    def _ndims(self):
        if self.name == "text-embedding-ada-002":
            return 1536
        elif self.name == "text-embedding-3-large":
            return self.dim or 3072
        elif self.name == "text-embedding-3-small":
            return self.dim or 1536
        else:
            raise ValueError(f"Unknown model name {self.name}")

    def generate_embeddings(
        self, texts: Union[List[str], "np.ndarray"]
    ) -> List["np.array"]:
        """
        Get the embeddings for the given texts

        Parameters
        ----------
        texts: list[str] or np.ndarray (of str)
            The texts to embed
        """
        openai = attempt_import_or_raise("openai")

        valid_texts = []
        valid_indices = []
        for idx, text in enumerate(texts):
            if text:
                valid_texts.append(text)
                valid_indices.append(idx)

        # TODO retry, rate limit, token limit
        try:
            kwargs = {
                "input": valid_texts,
                "model": self.name,
            }
            if self.name != "text-embedding-ada-002":
                kwargs["dimensions"] = self.dim

            rs = self._openai_client.embeddings.create(**kwargs)
            valid_embeddings = {
                idx: v.embedding for v, idx in zip(rs.data, valid_indices)
            }
        except openai.BadRequestError:
            logging.exception("Bad request: %s", texts)
            return [None] * len(texts)
        except Exception:
            logging.exception("OpenAI embeddings error")
            raise
        return [valid_embeddings.get(idx, None) for idx in range(len(texts))]

    @cached_property
    def _openai_client(self):
        openai = attempt_import_or_raise("openai")
        kwargs = {}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        if self.default_headers:
            kwargs["default_headers"] = self.default_headers
        if self.organization:
            kwargs["organization"] = self.organization
        if self.api_key:
            kwargs["api_key"] = self.api_key

        if self.use_azure:
            return openai.AzureOpenAI(**kwargs)
        else:
            return openai.OpenAI(**kwargs)

              

  

            generate_embeddings

¶

generate_embeddings(texts: Union[List[str], ndarray]) -> List[array]

    

      
Get the embeddings for the given texts

Parameters:

    
        
- 
          `texts`
              (`Union[List[str], ndarray]`)
          –
          
            
The texts to embed

          
        
    

            
              Source code in `lancedb/embeddings/openai.py`
              
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
def generate_embeddings(
    self, texts: Union[List[str], "np.ndarray"]
) -> List["np.array"]:
    """
    Get the embeddings for the given texts

    Parameters
    ----------
    texts: list[str] or np.ndarray (of str)
        The texts to embed
    """
    openai = attempt_import_or_raise("openai")

    valid_texts = []
    valid_indices = []
    for idx, text in enumerate(texts):
        if text:
            valid_texts.append(text)
            valid_indices.append(idx)

    # TODO retry, rate limit, token limit
    try:
        kwargs = {
            "input": valid_texts,
            "model": self.name,
        }
        if self.name != "text-embedding-ada-002":
            kwargs["dimensions"] = self.dim

        rs = self._openai_client.embeddings.create(**kwargs)
        valid_embeddings = {
            idx: v.embedding for v, idx in zip(rs.data, valid_indices)
        }
    except openai.BadRequestError:
        logging.exception("Bad request: %s", texts)
        return [None] * len(texts)
    except Exception:
        logging.exception("OpenAI embeddings error")
        raise
    return [valid_embeddings.get(idx, None) for idx in range(len(texts))]

            
    

  

    

            lancedb.embeddings.open_clip.OpenClipEmbeddings

¶

    
            

              Bases: `EmbeddingFunction`

      
An embedding function that uses the OpenClip API
For multi-modal text-to-image search

https://github.com/mlfoundations/open_clip

              
                Source code in `lancedb/embeddings/open_clip.py`
                
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
@register("open-clip")
class OpenClipEmbeddings(EmbeddingFunction):
    """
    An embedding function that uses the OpenClip API
    For multi-modal text-to-image search

    https://github.com/mlfoundations/open_clip
    """

    name: str = "ViT-B-32"
    pretrained: str = "laion2b_s34b_b79k"
    device: str = "cpu"
    batch_size: int = 64
    normalize: bool = True
    _model = PrivateAttr()
    _preprocess = PrivateAttr()
    _tokenizer = PrivateAttr()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        open_clip = attempt_import_or_raise("open_clip", "open-clip")
        model, _, preprocess = open_clip.create_model_and_transforms(
            self.name, pretrained=self.pretrained
        )
        model.to(self.device)
        self._model, self._preprocess = model, preprocess
        self._tokenizer = open_clip.get_tokenizer(self.name)
        self._ndims = None

    def ndims(self):
        if self._ndims is None:
            self._ndims = self.generate_text_embeddings("foo").shape[0]
        return self._ndims

    def compute_query_embeddings(
        self, query: Union[str, "PIL.Image.Image"], *args, **kwargs
    ) -> List[np.ndarray]:
        """
        Compute the embeddings for a given user query

        Parameters
        ----------
        query : Union[str, PIL.Image.Image]
            The query to embed. A query can be either text or an image.
        """
        if isinstance(query, str):
            return [self.generate_text_embeddings(query)]
        else:
            PIL_Image = attempt_import_or_raise("PIL.Image", "pillow")
            if isinstance(query, PIL_Image.Image):
                return [self.generate_image_embedding(query)]
            else:
                raise TypeError("OpenClip supports str or PIL Image as query")

    def generate_text_embeddings(self, text: str) -> np.ndarray:
        torch = attempt_import_or_raise("torch")
        text = self.sanitize_input(text)
        text = self._tokenizer(text)
        text.to(self.device)
        with torch.no_grad():
            text_features = self._model.encode_text(text.to(self.device))
            if self.normalize:
                text_features /= text_features.norm(dim=-1, keepdim=True)
            return text_features.cpu().numpy().squeeze()

    def sanitize_input(self, images: IMAGES) -> Union[List[bytes], np.ndarray]:
        """
        Sanitize the input to the embedding function.
        """
        if isinstance(images, (str, bytes)):
            images = [images]
        elif isinstance(images, pa.Array):
            images = images.to_pylist()
        elif isinstance(images, pa.ChunkedArray):
            images = images.combine_chunks().to_pylist()
        return images

    def compute_source_embeddings(
        self, images: IMAGES, *args, **kwargs
    ) -> List[np.array]:
        """
        Get the embeddings for the given images
        """
        images = self.sanitize_input(images)
        embeddings = []
        for i in range(0, len(images), self.batch_size):
            j = min(i + self.batch_size, len(images))
            batch = images[i:j]
            embeddings.extend(self._parallel_get(batch))
        return embeddings

    def _parallel_get(self, images: Union[List[str], List[bytes]]) -> List[np.ndarray]:
        """
        Issue concurrent requests to retrieve the image data
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.generate_image_embedding, image)
                for image in images
            ]
            return [future.result() for future in tqdm(futures)]

    def generate_image_embedding(
        self, image: Union[str, bytes, "PIL.Image.Image"]
    ) -> np.ndarray:
        """
        Generate the embedding for a single image

        Parameters
        ----------
        image : Union[str, bytes, PIL.Image.Image]
            The image to embed. If the image is a str, it is treated as a uri.
            If the image is bytes, it is treated as the raw image bytes.
        """
        torch = attempt_import_or_raise("torch")
        # TODO handle retry and errors for https
        image = self._to_pil(image)
        image = self._preprocess(image).unsqueeze(0)
        with torch.no_grad():
            return self._encode_and_normalize_image(image)

    def _to_pil(self, image: Union[str, bytes]):
        PIL_Image = attempt_import_or_raise("PIL.Image", "pillow")
        if isinstance(image, bytes):
            return PIL_Image.open(io.BytesIO(image))
        if isinstance(image, PIL_Image.Image):
            return image
        elif isinstance(image, str):
            parsed = urlparse.urlparse(image)
            # TODO handle drive letter on windows.
            if parsed.scheme == "file":
                return PIL_Image.open(parsed.path)
            elif parsed.scheme == "":
                return PIL_Image.open(image if os.name == "nt" else parsed.path)
            elif parsed.scheme.startswith("http"):
                return PIL_Image.open(io.BytesIO(url_retrieve(image)))
            else:
                raise NotImplementedError("Only local and http(s) urls are supported")

    def _encode_and_normalize_image(self, image_tensor: "torch.Tensor"):
        """
        encode a single image tensor and optionally normalize the output
        """
        image_features = self._model.encode_image(image_tensor.to(self.device))
        if self.normalize:
            image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy().squeeze()

              

  

            compute_query_embeddings

¶

compute_query_embeddings(query: Union[str, Image], *args, **kwargs) -> List[ndarray]

    

      
Compute the embeddings for a given user query

Parameters:

    
        
- 
          `query`
              (`Union[str, Image]`)
          –
          
            
The query to embed. A query can be either text or an image.

          
        
    

            
              Source code in `lancedb/embeddings/open_clip.py`
              
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
def compute_query_embeddings(
    self, query: Union[str, "PIL.Image.Image"], *args, **kwargs
) -> List[np.ndarray]:
    """
    Compute the embeddings for a given user query

    Parameters
    ----------
    query : Union[str, PIL.Image.Image]
        The query to embed. A query can be either text or an image.
    """
    if isinstance(query, str):
        return [self.generate_text_embeddings(query)]
    else:
        PIL_Image = attempt_import_or_raise("PIL.Image", "pillow")
        if isinstance(query, PIL_Image.Image):
            return [self.generate_image_embedding(query)]
        else:
            raise TypeError("OpenClip supports str or PIL Image as query")

            
    

            sanitize_input

¶

sanitize_input(images: IMAGES) -> Union[List[bytes], ndarray]

    

      
Sanitize the input to the embedding function.

            
              Source code in `lancedb/embeddings/open_clip.py`
              
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
def sanitize_input(self, images: IMAGES) -> Union[List[bytes], np.ndarray]:
    """
    Sanitize the input to the embedding function.
    """
    if isinstance(images, (str, bytes)):
        images = [images]
    elif isinstance(images, pa.Array):
        images = images.to_pylist()
    elif isinstance(images, pa.ChunkedArray):
        images = images.combine_chunks().to_pylist()
    return images

            
    

            compute_source_embeddings

¶

compute_source_embeddings(images: IMAGES, *args, **kwargs) -> List[array]

    

      
Get the embeddings for the given images

            
              Source code in `lancedb/embeddings/open_clip.py`
              
103
104
105
106
107
108
109
110
111
112
113
114
115
def compute_source_embeddings(
    self, images: IMAGES, *args, **kwargs
) -> List[np.array]:
    """
    Get the embeddings for the given images
    """
    images = self.sanitize_input(images)
    embeddings = []
    for i in range(0, len(images), self.batch_size):
        j = min(i + self.batch_size, len(images))
        batch = images[i:j]
        embeddings.extend(self._parallel_get(batch))
    return embeddings

            
    

            generate_image_embedding

¶

generate_image_embedding(image: Union[str, bytes, Image]) -> ndarray

    

      
Generate the embedding for a single image

Parameters:

    
        
- 
          `image`
              (`Union[str, bytes, Image]`)
          –
          
            
The image to embed. If the image is a str, it is treated as a uri.
If the image is bytes, it is treated as the raw image bytes.

          
        
    

            
              Source code in `lancedb/embeddings/open_clip.py`
              
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
def generate_image_embedding(
    self, image: Union[str, bytes, "PIL.Image.Image"]
) -> np.ndarray:
    """
    Generate the embedding for a single image

    Parameters
    ----------
    image : Union[str, bytes, PIL.Image.Image]
        The image to embed. If the image is a str, it is treated as a uri.
        If the image is bytes, it is treated as the raw image bytes.
    """
    torch = attempt_import_or_raise("torch")
    # TODO handle retry and errors for https
    image = self._to_pil(image)
    image = self._preprocess(image).unsqueeze(0)
    with torch.no_grad():
        return self._encode_and_normalize_image(image)

            
    

  

    

## Remote configuration¶

            lancedb.remote.ClientConfig

  
      `dataclass`
  

¶

    

              
                Source code in `lancedb/remote/__init__.py`
                
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
@dataclass
class ClientConfig:
    user_agent: str = f"LanceDB-Python-Client/{__version__}"
    retry_config: RetryConfig = field(default_factory=RetryConfig)
    timeout_config: Optional[TimeoutConfig] = field(default_factory=TimeoutConfig)
    extra_headers: Optional[dict] = None
    id_delimiter: Optional[str] = None
    tls_config: Optional[TlsConfig] = None
    header_provider: Optional["HeaderProvider"] = None

    def __post_init__(self):
        if isinstance(self.retry_config, dict):
            self.retry_config = RetryConfig(**self.retry_config)
        if isinstance(self.timeout_config, dict):
            self.timeout_config = TimeoutConfig(**self.timeout_config)
        if isinstance(self.tls_config, dict):
            self.tls_config = TlsConfig(**self.tls_config)

              

  

  

    

            lancedb.remote.TimeoutConfig

  
      `dataclass`
  

¶

    

      
Timeout configuration for remote HTTP client.

Attributes:

    
        
- 
          `timeout`
              (`Optional[timedelta]`)
          –
          
            
The overall timeout for the entire request. This includes connection,
send, and read time. If the entire request doesn't complete within
this time, it will fail. Default is None (no overall timeout).
This can also be set via the environment variable
`LANCE_CLIENT_TIMEOUT`, as an integer number of seconds.

          
        
        
- 
          `connect_timeout`
              (`Optional[timedelta]`)
          –
          
            
The timeout for establishing a connection. Default is 120 seconds (2 minutes).
This can also be set via the environment variable
`LANCE_CLIENT_CONNECT_TIMEOUT`, as an integer number of seconds.

          
        
        
- 
          `read_timeout`
              (`Optional[timedelta]`)
          –
          
            
The timeout for reading data from the server. Default is 300 seconds
(5 minutes). This can also be set via the environment variable
`LANCE_CLIENT_READ_TIMEOUT`, as an integer number of seconds.

          
        
        
- 
          `pool_idle_timeout`
              (`Optional[timedelta]`)
          –
          
            
The timeout for keeping idle connections in the connection pool. Default
is 300 seconds (5 minutes). This can also be set via the environment variable
`LANCE_CLIENT_CONNECTION_TIMEOUT`, as an integer number of seconds.

          
        
    

              
                Source code in `lancedb/remote/__init__.py`
                
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
@dataclass
class TimeoutConfig:
    """Timeout configuration for remote HTTP client.

    Attributes
    ----------
    timeout: Optional[timedelta]
        The overall timeout for the entire request. This includes connection,
        send, and read time. If the entire request doesn't complete within
        this time, it will fail. Default is None (no overall timeout).
        This can also be set via the environment variable
        `LANCE_CLIENT_TIMEOUT`, as an integer number of seconds.
    connect_timeout: Optional[timedelta]
        The timeout for establishing a connection. Default is 120 seconds (2 minutes).
        This can also be set via the environment variable
        `LANCE_CLIENT_CONNECT_TIMEOUT`, as an integer number of seconds.
    read_timeout: Optional[timedelta]
        The timeout for reading data from the server. Default is 300 seconds
        (5 minutes). This can also be set via the environment variable
        `LANCE_CLIENT_READ_TIMEOUT`, as an integer number of seconds.
    pool_idle_timeout: Optional[timedelta]
        The timeout for keeping idle connections in the connection pool. Default
        is 300 seconds (5 minutes). This can also be set via the environment variable
        `LANCE_CLIENT_CONNECTION_TIMEOUT`, as an integer number of seconds.
    """

    timeout: Optional[timedelta] = None
    connect_timeout: Optional[timedelta] = None
    read_timeout: Optional[timedelta] = None
    pool_idle_timeout: Optional[timedelta] = None

    @staticmethod
    def __to_timedelta(value) -> Optional[timedelta]:
        if value is None:
            return None
        elif isinstance(value, timedelta):
            return value
        elif isinstance(value, (int, float)):
            return timedelta(seconds=value)
        else:
            raise ValueError(
                f"Invalid value for timeout: {value}, must be a timedelta "
                "or number of seconds"
            )

    def __post_init__(self):
        self.timeout = self.__to_timedelta(self.timeout)
        self.connect_timeout = self.__to_timedelta(self.connect_timeout)
        self.read_timeout = self.__to_timedelta(self.read_timeout)
        self.pool_idle_timeout = self.__to_timedelta(self.pool_idle_timeout)

              

  

  

    

            lancedb.remote.RetryConfig

  
      `dataclass`
  

¶

    

      
Retry configuration for the remote HTTP client.

Attributes:

    
        
- 
          `retries`
              (`Optional[int]`)
          –
          
            
The maximum number of retries for a request. Default is 3. You can also set this
via the environment variable `LANCE_CLIENT_MAX_RETRIES`.

          
        
        
- 
          `connect_retries`
              (`Optional[int]`)
          –
          
            
The maximum number of retries for connection errors. Default is 3. You can also
set this via the environment variable `LANCE_CLIENT_CONNECT_RETRIES`.

          
        
        
- 
          `read_retries`
              (`Optional[int]`)
          –
          
            
The maximum number of retries for read errors. Default is 3. You can also set
this via the environment variable `LANCE_CLIENT_READ_RETRIES`.

          
        
        
- 
          `backoff_factor`
              (`Optional[float]`)
          –
          
            
The backoff factor to apply between retries. Default is 0.25. Between each retry
the client will wait for the amount of seconds:
`{backoff factor} * (2 ** ({number of previous retries}))`. So for the default
of 0.25, the first retry will wait 0.25 seconds, the second retry will wait 0.5
seconds, the third retry will wait 1 second, etc.

You can also set this via the environment variable
`LANCE_CLIENT_RETRY_BACKOFF_FACTOR`.

          
        
        
- 
          `backoff_jitter`
              (`Optional[float]`)
          –
          
            
The jitter to apply to the backoff factor, in seconds. Default is 0.25.

A random value between 0 and `backoff_jitter` will be added to the backoff
factor in seconds. So for the default of 0.25 seconds, between 0 and 250
milliseconds will be added to the sleep between each retry.

You can also set this via the environment variable
`LANCE_CLIENT_RETRY_BACKOFF_JITTER`.

          
        
        
- 
          `statuses`
              (`Optional[List[int]`)
          –
          
            
The HTTP status codes for which to retry the request. Default is
[429, 500, 502, 503].

You can also set this via the environment variable
`LANCE_CLIENT_RETRY_STATUSES`. Use a comma-separated list of integers.

          
        
    

              
                Source code in `lancedb/remote/__init__.py`
                
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
@dataclass
class RetryConfig:
    """Retry configuration for the remote HTTP client.

    Attributes
    ----------
    retries: Optional[int]
        The maximum number of retries for a request. Default is 3. You can also set this
        via the environment variable `LANCE_CLIENT_MAX_RETRIES`.
    connect_retries: Optional[int]
        The maximum number of retries for connection errors. Default is 3. You can also
        set this via the environment variable `LANCE_CLIENT_CONNECT_RETRIES`.
    read_retries: Optional[int]
        The maximum number of retries for read errors. Default is 3. You can also set
        this via the environment variable `LANCE_CLIENT_READ_RETRIES`.
    backoff_factor: Optional[float]
        The backoff factor to apply between retries. Default is 0.25. Between each retry
        the client will wait for the amount of seconds:
        `{backoff factor} * (2 ** ({number of previous retries}))`. So for the default
        of 0.25, the first retry will wait 0.25 seconds, the second retry will wait 0.5
        seconds, the third retry will wait 1 second, etc.

        You can also set this via the environment variable
        `LANCE_CLIENT_RETRY_BACKOFF_FACTOR`.
    backoff_jitter: Optional[float]
        The jitter to apply to the backoff factor, in seconds. Default is 0.25.

        A random value between 0 and `backoff_jitter` will be added to the backoff
        factor in seconds. So for the default of 0.25 seconds, between 0 and 250
        milliseconds will be added to the sleep between each retry.

        You can also set this via the environment variable
        `LANCE_CLIENT_RETRY_BACKOFF_JITTER`.
    statuses: Optional[List[int]
        The HTTP status codes for which to retry the request. Default is
        [429, 500, 502, 503].

        You can also set this via the environment variable
        `LANCE_CLIENT_RETRY_STATUSES`. Use a comma-separated list of integers.
    """

    retries: Optional[int] = None
    connect_retries: Optional[int] = None
    read_retries: Optional[int] = None
    backoff_factor: Optional[float] = None
    backoff_jitter: Optional[float] = None
    statuses: Optional[List[int]] = None

              

  

  

    

## Context¶

            lancedb.context.contextualize

¶

contextualize(raw_df: 'pd.DataFrame') -> Contextualizer

    

      
Create a Contextualizer object for the given DataFrame.

Used to create context windows. Context windows are rolling subsets of text
data.

The input text column should already be separated into rows that will be the
unit of the window. So to create a context window over tokens, start with
a DataFrame with one token per row. To create a context window over sentences,
start with a DataFrame with one sentence per row.

Examples:

    
>>> from lancedb.context import contextualize
>>> import pandas as pd
>>> data = pd.DataFrame({
...    'token': ['The', 'quick', 'brown', 'fox', 'jumped', 'over',
...              'the', 'lazy', 'dog', 'I', 'love', 'sandwiches'],
...    'document_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
... })

    
`window` determines how many rows to include in each window. In our case
this how many tokens, but depending on the input data, it could be sentences,
paragraphs, messages, etc.

    
>>> contextualize(data).window(3).stride(1).text_col('token').to_pandas()
                token  document_id
0     The quick brown            1
1     quick brown fox            1
2    brown fox jumped            1
3     fox jumped over            1
4     jumped over the            1
5       over the lazy            1
6        the lazy dog            1
7          lazy dog I            1
8          dog I love            1
9   I love sandwiches            2
10    love sandwiches            2
>>> (contextualize(data).window(7).stride(1).min_window_size(7)
...   .text_col('token').to_pandas())
                                  token  document_id
0   The quick brown fox jumped over the            1
1  quick brown fox jumped over the lazy            1
2    brown fox jumped over the lazy dog            1
3        fox jumped over the lazy dog I            1
4       jumped over the lazy dog I love            1
5   over the lazy dog I love sandwiches            1

    
`stride` determines how many rows to skip between each window start. This can
be used to reduce the total number of windows generated.

    
>>> contextualize(data).window(4).stride(2).text_col('token').to_pandas()
                    token  document_id
0     The quick brown fox            1
2   brown fox jumped over            1
4    jumped over the lazy            1
6          the lazy dog I            1
8   dog I love sandwiches            1
10        love sandwiches            2

    
`groupby` determines how to group the rows. For example, we would like to have
context windows that don't cross document boundaries. In this case, we can
pass `document_id` as the group by.

    
>>> (contextualize(data)
...     .window(4).stride(2).text_col('token').groupby('document_id')
...     .to_pandas())
                   token  document_id
0    The quick brown fox            1
2  brown fox jumped over            1
4   jumped over the lazy            1
6           the lazy dog            1
9      I love sandwiches            2

    
`min_window_size` determines the minimum size of the context windows
that are generated.This can be used to trim the last few context windows
which have size less than `min_window_size`.
By default context windows of size 1 are skipped.

    
>>> (contextualize(data)
...     .window(6).stride(3).text_col('token').groupby('document_id')
...     .to_pandas())
                             token  document_id
0  The quick brown fox jumped over            1
3     fox jumped over the lazy dog            1
6                     the lazy dog            1
9                I love sandwiches            2

    
>>> (contextualize(data)
...     .window(6).stride(3).min_window_size(4).text_col('token')
...     .groupby('document_id')
...     .to_pandas())
                             token  document_id
0  The quick brown fox jumped over            1
3     fox jumped over the lazy dog            1

            
              Source code in `lancedb/context.py`
              
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
def contextualize(raw_df: "pd.DataFrame") -> Contextualizer:
    """Create a Contextualizer object for the given DataFrame.

    Used to create context windows. Context windows are rolling subsets of text
    data.

    The input text column should already be separated into rows that will be the
    unit of the window. So to create a context window over tokens, start with
    a DataFrame with one token per row. To create a context window over sentences,
    start with a DataFrame with one sentence per row.

    Examples
    --------
    >>> from lancedb.context import contextualize
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...    'token': ['The', 'quick', 'brown', 'fox', 'jumped', 'over',
    ...              'the', 'lazy', 'dog', 'I', 'love', 'sandwiches'],
    ...    'document_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
    ... })

    ``window`` determines how many rows to include in each window. In our case
    this how many tokens, but depending on the input data, it could be sentences,
    paragraphs, messages, etc.

    >>> contextualize(data).window(3).stride(1).text_col('token').to_pandas()
                    token  document_id
    0     The quick brown            1
    1     quick brown fox            1
    2    brown fox jumped            1
    3     fox jumped over            1
    4     jumped over the            1
    5       over the lazy            1
    6        the lazy dog            1
    7          lazy dog I            1
    8          dog I love            1
    9   I love sandwiches            2
    10    love sandwiches            2
    >>> (contextualize(data).window(7).stride(1).min_window_size(7)
    ...   .text_col('token').to_pandas())
                                      token  document_id
    0   The quick brown fox jumped over the            1
    1  quick brown fox jumped over the lazy            1
    2    brown fox jumped over the lazy dog            1
    3        fox jumped over the lazy dog I            1
    4       jumped over the lazy dog I love            1
    5   over the lazy dog I love sandwiches            1

    ``stride`` determines how many rows to skip between each window start. This can
    be used to reduce the total number of windows generated.

    >>> contextualize(data).window(4).stride(2).text_col('token').to_pandas()
                        token  document_id
    0     The quick brown fox            1
    2   brown fox jumped over            1
    4    jumped over the lazy            1
    6          the lazy dog I            1
    8   dog I love sandwiches            1
    10        love sandwiches            2

    ``groupby`` determines how to group the rows. For example, we would like to have
    context windows that don't cross document boundaries. In this case, we can
    pass ``document_id`` as the group by.

    >>> (contextualize(data)
    ...     .window(4).stride(2).text_col('token').groupby('document_id')
    ...     .to_pandas())
                       token  document_id
    0    The quick brown fox            1
    2  brown fox jumped over            1
    4   jumped over the lazy            1
    6           the lazy dog            1
    9      I love sandwiches            2

    ``min_window_size`` determines the minimum size of the context windows
    that are generated.This can be used to trim the last few context windows
    which have size less than ``min_window_size``.
    By default context windows of size 1 are skipped.

    >>> (contextualize(data)
    ...     .window(6).stride(3).text_col('token').groupby('document_id')
    ...     .to_pandas())
                                 token  document_id
    0  The quick brown fox jumped over            1
    3     fox jumped over the lazy dog            1
    6                     the lazy dog            1
    9                I love sandwiches            2

    >>> (contextualize(data)
    ...     .window(6).stride(3).min_window_size(4).text_col('token')
    ...     .groupby('document_id')
    ...     .to_pandas())
                                 token  document_id
    0  The quick brown fox jumped over            1
    3     fox jumped over the lazy dog            1

    """
    return Contextualizer(raw_df)

            
    

            lancedb.context.Contextualizer

¶

    

      
Create context windows from a DataFrame.
See lancedb.context.contextualize.

              
                Source code in `lancedb/context.py`
                
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
class Contextualizer:
    """Create context windows from a DataFrame.
    See [lancedb.context.contextualize][].
    """

    def __init__(self, raw_df):
        self._text_col = None
        self._groupby = None
        self._stride = None
        self._window = None
        self._min_window_size = 2
        self._raw_df = raw_df

    def window(self, window: int) -> Contextualizer:
        """Set the window size. i.e., how many rows to include in each window.

        Parameters
        ----------
        window: int
            The window size.
        """
        self._window = window
        return self

    def stride(self, stride: int) -> Contextualizer:
        """Set the stride. i.e., how many rows to skip between each window.

        Parameters
        ----------
        stride: int
            The stride.
        """
        self._stride = stride
        return self

    def groupby(self, groupby: str) -> Contextualizer:
        """Set the groupby column. i.e., how to group the rows.
        Windows don't cross groups

        Parameters
        ----------
        groupby: str
            The groupby column.
        """
        self._groupby = groupby
        return self

    def text_col(self, text_col: str) -> Contextualizer:
        """Set the text column used to make the context window.

        Parameters
        ----------
        text_col: str
            The text column.
        """
        self._text_col = text_col
        return self

    def min_window_size(self, min_window_size: int) -> Contextualizer:
        """Set the (optional) min_window_size size for the context window.

        Parameters
        ----------
        min_window_size: int
            The min_window_size.
        """
        self._min_window_size = min_window_size
        return self

    @deprecation.deprecated(
        deprecated_in="0.3.1",
        removed_in="0.4.0",
        current_version=__version__,
        details="Use to_pandas() instead",
    )
    def to_df(self) -> "pd.DataFrame":
        return self.to_pandas()

    def to_pandas(self) -> "pd.DataFrame":
        """Create the context windows and return a DataFrame."""
        if pd is None:
            raise ImportError(
                "pandas is required to create context windows using lancedb"
            )

        if self._text_col not in self._raw_df.columns.tolist():
            raise MissingColumnError(self._text_col)

        if self._window is None or self._window < 1:
            raise MissingValueError(
                "The value of window is None or less than 1. Specify the "
                "window size (number of rows to include in each window)"
            )

        if self._stride is None or self._stride < 1:
            raise MissingValueError(
                "The value of stride is None or less than 1. Specify the "
                "stride (number of rows to skip between each window)"
            )

        def process_group(grp):
            # For each group, create the text rolling window
            # with values of size >= min_window_size
            text = grp[self._text_col].values
            contexts = grp.iloc[:: self._stride, :].copy()
            windows = [
                " ".join(text[start_i : min(start_i + self._window, len(grp))])
                for start_i in range(0, len(grp), self._stride)
                if start_i + self._window <= len(grp)
                or len(grp) - start_i >= self._min_window_size
            ]
            # if last few rows dropped
            if len(windows) < len(contexts):
                contexts = contexts.iloc[: len(windows)]
            contexts[self._text_col] = windows
            return contexts

        if self._groupby is None:
            return process_group(self._raw_df)
        # concat result from all groups
        return pd.concat(
            [process_group(grp) for _, grp in self._raw_df.groupby(self._groupby)]
        )

              

  

            window

¶

window(window: int) -> Contextualizer

    

      
Set the window size. i.e., how many rows to include in each window.

Parameters:

    
        
- 
          `window`
              (`int`)
          –
          
            
The window size.

          
        
    

            
              Source code in `lancedb/context.py`
              
127
128
129
130
131
132
133
134
135
136
def window(self, window: int) -> Contextualizer:
    """Set the window size. i.e., how many rows to include in each window.

    Parameters
    ----------
    window: int
        The window size.
    """
    self._window = window
    return self

            
    

            stride

¶

stride(stride: int) -> Contextualizer

    

      
Set the stride. i.e., how many rows to skip between each window.

Parameters:

    
        
- 
          `stride`
              (`int`)
          –
          
            
The stride.

          
        
    

            
              Source code in `lancedb/context.py`
              
138
139
140
141
142
143
144
145
146
147
def stride(self, stride: int) -> Contextualizer:
    """Set the stride. i.e., how many rows to skip between each window.

    Parameters
    ----------
    stride: int
        The stride.
    """
    self._stride = stride
    return self

            
    

            groupby

¶

groupby(groupby: str) -> Contextualizer

    

      
Set the groupby column. i.e., how to group the rows.
Windows don't cross groups

Parameters:

    
        
- 
          `groupby`
              (`str`)
          –
          
            
The groupby column.

          
        
    

            
              Source code in `lancedb/context.py`
              
149
150
151
152
153
154
155
156
157
158
159
def groupby(self, groupby: str) -> Contextualizer:
    """Set the groupby column. i.e., how to group the rows.
    Windows don't cross groups

    Parameters
    ----------
    groupby: str
        The groupby column.
    """
    self._groupby = groupby
    return self

            
    

            text_col

¶

text_col(text_col: str) -> Contextualizer

    

      
Set the text column used to make the context window.

Parameters:

    
        
- 
          `text_col`
              (`str`)
          –
          
            
The text column.

          
        
    

            
              Source code in `lancedb/context.py`
              
161
162
163
164
165
166
167
168
169
170
def text_col(self, text_col: str) -> Contextualizer:
    """Set the text column used to make the context window.

    Parameters
    ----------
    text_col: str
        The text column.
    """
    self._text_col = text_col
    return self

            
    

            min_window_size

¶

min_window_size(min_window_size: int) -> Contextualizer

    

      
Set the (optional) min_window_size size for the context window.

Parameters:

    
        
- 
          `min_window_size`
              (`int`)
          –
          
            
The min_window_size.

          
        
    

            
              Source code in `lancedb/context.py`
              
172
173
174
175
176
177
178
179
180
181
def min_window_size(self, min_window_size: int) -> Contextualizer:
    """Set the (optional) min_window_size size for the context window.

    Parameters
    ----------
    min_window_size: int
        The min_window_size.
    """
    self._min_window_size = min_window_size
    return self

            
    

            to_pandas

¶

to_pandas() -> 'pd.DataFrame'

    

      
Create the context windows and return a DataFrame.

            
              Source code in `lancedb/context.py`
              
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
def to_pandas(self) -> "pd.DataFrame":
    """Create the context windows and return a DataFrame."""
    if pd is None:
        raise ImportError(
            "pandas is required to create context windows using lancedb"
        )

    if self._text_col not in self._raw_df.columns.tolist():
        raise MissingColumnError(self._text_col)

    if self._window is None or self._window < 1:
        raise MissingValueError(
            "The value of window is None or less than 1. Specify the "
            "window size (number of rows to include in each window)"
        )

    if self._stride is None or self._stride < 1:
        raise MissingValueError(
            "The value of stride is None or less than 1. Specify the "
            "stride (number of rows to skip between each window)"
        )

    def process_group(grp):
        # For each group, create the text rolling window
        # with values of size >= min_window_size
        text = grp[self._text_col].values
        contexts = grp.iloc[:: self._stride, :].copy()
        windows = [
            " ".join(text[start_i : min(start_i + self._window, len(grp))])
            for start_i in range(0, len(grp), self._stride)
            if start_i + self._window <= len(grp)
            or len(grp) - start_i >= self._min_window_size
        ]
        # if last few rows dropped
        if len(windows) < len(contexts):
            contexts = contexts.iloc[: len(windows)]
        contexts[self._text_col] = windows
        return contexts

    if self._groupby is None:
        return process_group(self._raw_df)
    # concat result from all groups
    return pd.concat(
        [process_group(grp) for _, grp in self._raw_df.groupby(self._groupby)]
    )

            
    

  

    

## Full text search¶

            lancedb.fts.create_index

¶

create_index(index_path: str, text_fields: List[str], ordering_fields: Optional[List[str]] = None, tokenizer_name: str = 'default') -> Index

    

      
Create a new Index (not populated)

Parameters:

    
        
- 
          `index_path`
              (`str`)
          –
          
            
Path to the index directory

          
        
        
- 
          `text_fields`
              (`List[str]`)
          –
          
            
List of text fields to index

          
        
        
- 
          `ordering_fields`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
List of unsigned type fields to order by at search time

          
        
        
- 
          `tokenizer_name`
              (`str`, default:
                  `"default"`
)
          –
          
            
The tokenizer to use

          
        
    

Returns:

    
        
- 
`index` (              `Index`
)          –
          
            
The index object (not yet populated)

          
        
    

            
              Source code in `lancedb/fts.py`
              
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
def create_index(
    index_path: str,
    text_fields: List[str],
    ordering_fields: Optional[List[str]] = None,
    tokenizer_name: str = "default",
) -> tantivy.Index:
    """
    Create a new Index (not populated)

    Parameters
    ----------
    index_path : str
        Path to the index directory
    text_fields : List[str]
        List of text fields to index
    ordering_fields: List[str]
        List of unsigned type fields to order by at search time
    tokenizer_name : str, default "default"
        The tokenizer to use

    Returns
    -------
    index : tantivy.Index
        The index object (not yet populated)
    """
    if ordering_fields is None:
        ordering_fields = []
    # Declaring our schema.
    schema_builder = tantivy.SchemaBuilder()
    # special field that we'll populate with row_id
    schema_builder.add_integer_field("doc_id", stored=True)
    # data fields
    for name in text_fields:
        schema_builder.add_text_field(name, stored=True, tokenizer_name=tokenizer_name)
    if ordering_fields:
        for name in ordering_fields:
            schema_builder.add_unsigned_field(name, fast=True)
    schema = schema_builder.build()
    os.makedirs(index_path, exist_ok=True)
    index = tantivy.Index(schema, path=index_path)
    return index

            
    

            lancedb.fts.populate_index

¶

populate_index(index: Index, table: LanceTable, fields: List[str], writer_heap_size: Optional[int] = None, ordering_fields: Optional[List[str]] = None) -> int

    

      
Populate an index with data from a LanceTable

Parameters:

    
        
- 
          `index`
              (`Index`)
          –
          
            
The index object

          
        
        
- 
          `table`
              (`LanceTable`)
          –
          
            
The table to index

          
        
        
- 
          `fields`
              (`List[str]`)
          –
          
            
List of fields to index

          
        
        
- 
          `writer_heap_size`
              (`int`, default:
                  `None`
)
          –
          
            
The writer heap size in bytes, defaults to 1GB

          
        
    

Returns:

    
        
- 
              `int`
          –
          
            
The number of rows indexed

          
        
    

            
              Source code in `lancedb/fts.py`
              
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
def populate_index(
    index: tantivy.Index,
    table: LanceTable,
    fields: List[str],
    writer_heap_size: Optional[int] = None,
    ordering_fields: Optional[List[str]] = None,
) -> int:
    """
    Populate an index with data from a LanceTable

    Parameters
    ----------
    index : tantivy.Index
        The index object
    table : LanceTable
        The table to index
    fields : List[str]
        List of fields to index
    writer_heap_size : int
        The writer heap size in bytes, defaults to 1GB

    Returns
    -------
    int
        The number of rows indexed
    """
    if ordering_fields is None:
        ordering_fields = []
    writer_heap_size = writer_heap_size or 1024 * 1024 * 1024
    # first check the fields exist and are string or large string type
    nested = []

    for name in fields:
        try:
            f = table.schema.field(name)  # raises KeyError if not found
        except KeyError:
            f = resolve_path(table.schema, name)
            nested.append(name)

        if not pa.types.is_string(f.type) and not pa.types.is_large_string(f.type):
            raise TypeError(f"Field {name} is not a string type")

    # create a tantivy writer
    writer = index.writer(heap_size=writer_heap_size)
    # write data into index
    dataset = table.to_lance()
    row_id = 0

    max_nested_level = 0
    if len(nested) > 0:
        max_nested_level = max([len(name.split(".")) for name in nested])

    for b in dataset.to_batches(columns=fields + ordering_fields):
        if max_nested_level > 0:
            b = pa.Table.from_batches([b])
            for _ in range(max_nested_level - 1):
                b = b.flatten()
        for i in range(b.num_rows):
            doc = tantivy.Document()
            for name in fields:
                value = b[name][i].as_py()
                if value is not None:
                    doc.add_text(name, value)
            for name in ordering_fields:
                value = b[name][i].as_py()
                if value is not None:
                    doc.add_unsigned(name, value)
            if not doc.is_empty:
                doc.add_integer("doc_id", row_id)
                writer.add_document(doc)
            row_id += 1
    # commit changes
    writer.commit()
    return row_id

            
    

            lancedb.fts.search_index

¶

search_index(index: Index, query: str, limit: int = 10, ordering_field=None) -> Tuple[Tuple[int], Tuple[float]]

    

      
Search an index for a query

Parameters:

    
        
- 
          `index`
              (`Index`)
          –
          
            
The index object

          
        
        
- 
          `query`
              (`str`)
          –
          
            
The query string

          
        
        
- 
          `limit`
              (`int`, default:
                  `10`
)
          –
          
            
The maximum number of results to return

          
        
    

Returns:

    
        
- 
`ids_and_score` (              `list[tuple[int], tuple[float]]`
)          –
          
            
A tuple of two tuples, the first containing the document ids
and the second containing the scores

          
        
    

            
              Source code in `lancedb/fts.py`
              
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
def search_index(
    index: tantivy.Index, query: str, limit: int = 10, ordering_field=None
) -> Tuple[Tuple[int], Tuple[float]]:
    """
    Search an index for a query

    Parameters
    ----------
    index : tantivy.Index
        The index object
    query : str
        The query string
    limit : int
        The maximum number of results to return

    Returns
    -------
    ids_and_score: list[tuple[int], tuple[float]]
        A tuple of two tuples, the first containing the document ids
        and the second containing the scores
    """
    searcher = index.searcher()
    query = index.parse_query(query)
    # get top results
    if ordering_field:
        results = searcher.search(query, limit, order_by_field=ordering_field)
    else:
        results = searcher.search(query, limit)
    if results.count == 0:
        return tuple(), tuple()
    return tuple(
        zip(
            *[
                (searcher.doc(doc_address)["doc_id"][0], score)
                for score, doc_address in results.hits
            ]
        )
    )

            
    

## Utilities¶

            lancedb.schema.vector

¶

vector(dimension: int, value_type: DataType = pa.float32()) -> DataType

    

      
A help function to create a vector type.

Parameters:

    
        
- 
          `dimension`
              (`int`)
          –
          
            
          
        
        
- 
          `value_type`
              (`DataType`, default:
                  `float32()`
)
          –
          
            
The type of the value in the vector.

          
        
    

Returns:

    
        
- 
              `A PyArrow DataType for vectors.`
          –
          
            
          
        
    

Examples:

    
>>> import pyarrow as pa
>>> import lancedb
>>> schema = pa.schema([
...     pa.field("id", pa.int64()),
...     pa.field("vector", lancedb.vector(756)),
... ])

            
              Source code in `lancedb/schema.py`
              
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
def vector(dimension: int, value_type: pa.DataType = pa.float32()) -> pa.DataType:
    """A help function to create a vector type.

    Parameters
    ----------
    dimension: The dimension of the vector.
    value_type: pa.DataType, optional
        The type of the value in the vector.

    Returns
    -------
    A PyArrow DataType for vectors.

    Examples
    --------

    >>> import pyarrow as pa
    >>> import lancedb
    >>> schema = pa.schema([
    ...     pa.field("id", pa.int64()),
    ...     pa.field("vector", lancedb.vector(756)),
    ... ])
    """
    return pa.list_(value_type, dimension)

            
    

            lancedb.merge.LanceMergeInsertBuilder

¶

    
            

              Bases: `object`

      
Builder for a LanceDB merge insert operation

See `merge_insert` for
more context

              
                Source code in `lancedb/merge.py`
                
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
class LanceMergeInsertBuilder(object):
    """Builder for a LanceDB merge insert operation

    See [`merge_insert`][lancedb.table.Table.merge_insert] for
    more context
    """

    def __init__(self, table: "Table", on: List[str]):  # noqa: F821
        # Do not put a docstring here.  This method should be hidden
        # from API docs.  Users should use merge_insert to create
        # this object.
        self._table = table
        self._on = on
        self._when_matched_update_all = False
        self._when_matched_update_all_condition = None
        self._when_not_matched_insert_all = False
        self._when_not_matched_by_source_delete = False
        self._when_not_matched_by_source_condition = None
        self._timeout = None
        self._use_index = True

    def when_matched_update_all(
        self, *, where: Optional[str] = None
    ) -> LanceMergeInsertBuilder:
        """
        Rows that exist in both the source table (new data) and
        the target table (old data) will be updated, replacing
        the old row with the corresponding matching row.

        If there are multiple matches then the behavior is undefined.
        Currently this causes multiple copies of the row to be created
        but that behavior is subject to change.
        """
        self._when_matched_update_all = True
        self._when_matched_update_all_condition = where
        return self

    def when_not_matched_insert_all(self) -> LanceMergeInsertBuilder:
        """
        Rows that exist only in the source table (new data) should
        be inserted into the target table.
        """
        self._when_not_matched_insert_all = True
        return self

    def when_not_matched_by_source_delete(
        self, condition: Optional[str] = None
    ) -> LanceMergeInsertBuilder:
        """
        Rows that exist only in the target table (old data) will be
        deleted.  An optional condition can be provided to limit what
        data is deleted.

        Parameters
        ----------
        condition: Optional[str], default None
            If None then all such rows will be deleted.  Otherwise the
            condition will be used as an SQL filter to limit what rows
            are deleted.
        """
        self._when_not_matched_by_source_delete = True
        if condition is not None:
            self._when_not_matched_by_source_condition = condition
        return self

    def use_index(self, use_index: bool) -> LanceMergeInsertBuilder:
        """
        Controls whether to use indexes for the merge operation.

        When set to `True` (the default), the operation will use an index if available
        on the join key for improved performance. When set to `False`, it forces a full
        table scan even if an index exists. This can be useful for benchmarking or when
        the query optimizer chooses a suboptimal path.

        Parameters
        ----------
        use_index: bool
            Whether to use indices for the merge operation. Defaults to `True`.
        """
        self._use_index = use_index
        return self

    def execute(
        self,
        new_data: DATA,
        on_bad_vectors: str = "error",
        fill_value: float = 0.0,
        timeout: Optional[timedelta] = None,
    ) -> MergeInsertResult:
        """
        Executes the merge insert operation

        Nothing is returned but the [`Table`][lancedb.table.Table] is updated

        Parameters
        ----------
        new_data: DATA
            New records which will be matched against the existing records
            to potentially insert or update into the table.  This parameter
            can be anything you use for [`add`][lancedb.table.Table.add]
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contains NaNs.
            One of "error", "drop", "fill".
        fill_value: float, default 0.
            The value to use when filling vectors. Only used if on_bad_vectors="fill".
        timeout: Optional[timedelta], default None
            Maximum time to run the operation before cancelling it.

            By default, there is a 30-second timeout that is only enforced after the
            first attempt. This is to prevent spending too long retrying to resolve
            conflicts. For example, if a write attempt takes 20 seconds and fails,
            the second attempt will be cancelled after 10 seconds, hitting the
            30-second timeout. However, a write that takes one hour and succeeds on the
            first attempt will not be cancelled.

            When this is set, the timeout is enforced on all attempts, including
            the first.

        Returns
        -------
        MergeInsertResult
            version: the new version number of the table after doing merge insert.
        """
        if timeout is not None:
            self._timeout = timeout
        return self._table._do_merge(self, new_data, on_bad_vectors, fill_value)

              

  

            when_matched_update_all

¶

when_matched_update_all(*, where: Optional[str] = None) -> LanceMergeInsertBuilder

    

      
Rows that exist in both the source table (new data) and
the target table (old data) will be updated, replacing
the old row with the corresponding matching row.

If there are multiple matches then the behavior is undefined.
Currently this causes multiple copies of the row to be created
but that behavior is subject to change.

            
              Source code in `lancedb/merge.py`
              
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
def when_matched_update_all(
    self, *, where: Optional[str] = None
) -> LanceMergeInsertBuilder:
    """
    Rows that exist in both the source table (new data) and
    the target table (old data) will be updated, replacing
    the old row with the corresponding matching row.

    If there are multiple matches then the behavior is undefined.
    Currently this causes multiple copies of the row to be created
    but that behavior is subject to change.
    """
    self._when_matched_update_all = True
    self._when_matched_update_all_condition = where
    return self

            
    

            when_not_matched_insert_all

¶

when_not_matched_insert_all() -> LanceMergeInsertBuilder

    

      
Rows that exist only in the source table (new data) should
be inserted into the target table.

            
              Source code in `lancedb/merge.py`
              
54
55
56
57
58
59
60
def when_not_matched_insert_all(self) -> LanceMergeInsertBuilder:
    """
    Rows that exist only in the source table (new data) should
    be inserted into the target table.
    """
    self._when_not_matched_insert_all = True
    return self

            
    

            when_not_matched_by_source_delete

¶

when_not_matched_by_source_delete(condition: Optional[str] = None) -> LanceMergeInsertBuilder

    

      
Rows that exist only in the target table (old data) will be
deleted.  An optional condition can be provided to limit what
data is deleted.

Parameters:

    
        
- 
          `condition`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
If None then all such rows will be deleted.  Otherwise the
condition will be used as an SQL filter to limit what rows
are deleted.

          
        
    

            
              Source code in `lancedb/merge.py`
              
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
def when_not_matched_by_source_delete(
    self, condition: Optional[str] = None
) -> LanceMergeInsertBuilder:
    """
    Rows that exist only in the target table (old data) will be
    deleted.  An optional condition can be provided to limit what
    data is deleted.

    Parameters
    ----------
    condition: Optional[str], default None
        If None then all such rows will be deleted.  Otherwise the
        condition will be used as an SQL filter to limit what rows
        are deleted.
    """
    self._when_not_matched_by_source_delete = True
    if condition is not None:
        self._when_not_matched_by_source_condition = condition
    return self

            
    

            use_index

¶

use_index(use_index: bool) -> LanceMergeInsertBuilder

    

      
Controls whether to use indexes for the merge operation.

When set to `True` (the default), the operation will use an index if available
on the join key for improved performance. When set to `False`, it forces a full
table scan even if an index exists. This can be useful for benchmarking or when
the query optimizer chooses a suboptimal path.

Parameters:

    
        
- 
          `use_index`
              (`bool`)
          –
          
            
Whether to use indices for the merge operation. Defaults to `True`.

          
        
    

            
              Source code in `lancedb/merge.py`
              
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
def use_index(self, use_index: bool) -> LanceMergeInsertBuilder:
    """
    Controls whether to use indexes for the merge operation.

    When set to `True` (the default), the operation will use an index if available
    on the join key for improved performance. When set to `False`, it forces a full
    table scan even if an index exists. This can be useful for benchmarking or when
    the query optimizer chooses a suboptimal path.

    Parameters
    ----------
    use_index: bool
        Whether to use indices for the merge operation. Defaults to `True`.
    """
    self._use_index = use_index
    return self

            
    

            execute

¶

execute(new_data: DATA, on_bad_vectors: str = 'error', fill_value: float = 0.0, timeout: Optional[timedelta] = None) -> MergeInsertResult

    

      
Executes the merge insert operation

Nothing is returned but the `Table` is updated

Parameters:

    
        
- 
          `new_data`
              (`DATA`)
          –
          
            
New records which will be matched against the existing records
to potentially insert or update into the table.  This parameter
can be anything you use for `add`

          
        
        
- 
          `on_bad_vectors`
              (`str`, default:
                  `'error'`
)
          –
          
            
What to do if any of the vectors are not the same size or contains NaNs.
One of "error", "drop", "fill".

          
        
        
- 
          `fill_value`
              (`float`, default:
                  `0.0`
)
          –
          
            
The value to use when filling vectors. Only used if on_bad_vectors="fill".

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
Maximum time to run the operation before cancelling it.

By default, there is a 30-second timeout that is only enforced after the
first attempt. This is to prevent spending too long retrying to resolve
conflicts. For example, if a write attempt takes 20 seconds and fails,
the second attempt will be cancelled after 10 seconds, hitting the
30-second timeout. However, a write that takes one hour and succeeds on the
first attempt will not be cancelled.

When this is set, the timeout is enforced on all attempts, including
the first.

          
        
    

Returns:

    
        
- 
              `MergeInsertResult`
          –
          
            
version: the new version number of the table after doing merge insert.

          
        
    

            
              Source code in `lancedb/merge.py`
              
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
def execute(
    self,
    new_data: DATA,
    on_bad_vectors: str = "error",
    fill_value: float = 0.0,
    timeout: Optional[timedelta] = None,
) -> MergeInsertResult:
    """
    Executes the merge insert operation

    Nothing is returned but the [`Table`][lancedb.table.Table] is updated

    Parameters
    ----------
    new_data: DATA
        New records which will be matched against the existing records
        to potentially insert or update into the table.  This parameter
        can be anything you use for [`add`][lancedb.table.Table.add]
    on_bad_vectors: str, default "error"
        What to do if any of the vectors are not the same size or contains NaNs.
        One of "error", "drop", "fill".
    fill_value: float, default 0.
        The value to use when filling vectors. Only used if on_bad_vectors="fill".
    timeout: Optional[timedelta], default None
        Maximum time to run the operation before cancelling it.

        By default, there is a 30-second timeout that is only enforced after the
        first attempt. This is to prevent spending too long retrying to resolve
        conflicts. For example, if a write attempt takes 20 seconds and fails,
        the second attempt will be cancelled after 10 seconds, hitting the
        30-second timeout. However, a write that takes one hour and succeeds on the
        first attempt will not be cancelled.

        When this is set, the timeout is enforced on all attempts, including
        the first.

    Returns
    -------
    MergeInsertResult
        version: the new version number of the table after doing merge insert.
    """
    if timeout is not None:
        self._timeout = timeout
    return self._table._do_merge(self, new_data, on_bad_vectors, fill_value)

            
    

  

    

## Integrations¶

## Pydantic¶

            lancedb.pydantic.pydantic_to_schema

¶

pydantic_to_schema(model: Type[BaseModel]) -> Schema

    

      
Convert a Pydantic Model to a
   PyArrow Schema.

Parameters:

    
        
- 
          `model`
              (`Type[BaseModel]`)
          –
          
            
The Pydantic BaseModel to convert to Arrow Schema.

          
        
    

Returns:

    
        
- 
              `Schema`
          –
          
            
The Arrow Schema

          
        
    

Examples:

    
>>> from typing import List, Optional
>>> import pydantic
>>> from lancedb.pydantic import pydantic_to_schema, Vector
>>> class FooModel(pydantic.BaseModel):
...     id: int
...     s: str
...     vec: Vector(1536)  # fixed_size_list<item: float32>[1536]
...     li: List[int]
...
>>> schema = pydantic_to_schema(FooModel)
>>> assert schema == pa.schema([
...     pa.field("id", pa.int64(), False),
...     pa.field("s", pa.utf8(), False),
...     pa.field("vec", pa.list_(pa.float32(), 1536)),
...     pa.field("li", pa.list_(pa.int64()), False),
... ])

            
              Source code in `lancedb/pydantic.py`
              
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
def pydantic_to_schema(model: Type[pydantic.BaseModel]) -> pa.Schema:
    """Convert a [Pydantic Model][pydantic.BaseModel] to a
       [PyArrow Schema][pyarrow.Schema].

    Parameters
    ----------
    model : Type[pydantic.BaseModel]
        The Pydantic BaseModel to convert to Arrow Schema.

    Returns
    -------
    pyarrow.Schema
        The Arrow Schema

    Examples
    --------

    >>> from typing import List, Optional
    >>> import pydantic
    >>> from lancedb.pydantic import pydantic_to_schema, Vector
    >>> class FooModel(pydantic.BaseModel):
    ...     id: int
    ...     s: str
    ...     vec: Vector(1536)  # fixed_size_list<item: float32>[1536]
    ...     li: List[int]
    ...
    >>> schema = pydantic_to_schema(FooModel)
    >>> assert schema == pa.schema([
    ...     pa.field("id", pa.int64(), False),
    ...     pa.field("s", pa.utf8(), False),
    ...     pa.field("vec", pa.list_(pa.float32(), 1536)),
    ...     pa.field("li", pa.list_(pa.int64()), False),
    ... ])
    """
    fields = _pydantic_model_to_fields(model)
    return pa.schema(fields)

            
    

            lancedb.pydantic.vector

¶

vector(dim: int, value_type: DataType = pa.float32())

    

            
              Source code in `lancedb/pydantic.py`
              
56
57
58
59
60
61
62
63
64
65
def vector(dim: int, value_type: pa.DataType = pa.float32()):
    # TODO: remove in future release
    from warnings import warn

    warn(
        "lancedb.pydantic.vector() is deprecated, use lancedb.pydantic.Vector instead."
        "This function will be removed in future release",
        DeprecationWarning,
    )
    return Vector(dim, value_type)

            
    

            lancedb.pydantic.LanceModel

¶

    
            

              Bases: `BaseModel`

      
A Pydantic Model base class that can be converted to a LanceDB Table.

Examples:

    
>>> import lancedb
>>> from lancedb.pydantic import LanceModel, Vector
>>>
>>> class TestModel(LanceModel):
...     name: str
...     vector: Vector(2)
...
>>> db = lancedb.connect("./example")
>>> table = db.create_table("test", schema=TestModel)
>>> table.add([
...     TestModel(name="test", vector=[1.0, 2.0])
... ])
AddResult(version=2)
>>> table.search([0., 0.]).limit(1).to_pydantic(TestModel)
[TestModel(name='test', vector=FixedSizeList(dim=2))]

              
                Source code in `lancedb/pydantic.py`
                
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
class LanceModel(pydantic.BaseModel):
    """
    A Pydantic Model base class that can be converted to a LanceDB Table.

    Examples
    --------
    >>> import lancedb
    >>> from lancedb.pydantic import LanceModel, Vector
    >>>
    >>> class TestModel(LanceModel):
    ...     name: str
    ...     vector: Vector(2)
    ...
    >>> db = lancedb.connect("./example")
    >>> table = db.create_table("test", schema=TestModel)
    >>> table.add([
    ...     TestModel(name="test", vector=[1.0, 2.0])
    ... ])
    AddResult(version=2)
    >>> table.search([0., 0.]).limit(1).to_pydantic(TestModel)
    [TestModel(name='test', vector=FixedSizeList(dim=2))]
    """

    @classmethod
    def to_arrow_schema(cls):
        """
        Get the Arrow Schema for this model.
        """
        schema = pydantic_to_schema(cls)
        functions = cls.parse_embedding_functions()
        if len(functions) > 0:
            # Prevent circular import
            from .embeddings import EmbeddingFunctionRegistry

            metadata = EmbeddingFunctionRegistry.get_instance().get_table_metadata(
                functions
            )
            schema = schema.with_metadata(metadata)
        return schema

    @classmethod
    def field_names(cls) -> List[str]:
        """
        Get the field names of this model.
        """
        return list(cls.safe_get_fields().keys())

    @classmethod
    def safe_get_fields(cls):
        if PYDANTIC_VERSION.major < 2:
            return cls.__fields__
        return cls.model_fields

    @classmethod
    def parse_embedding_functions(cls) -> List["EmbeddingFunctionConfig"]:
        """
        Parse the embedding functions from this model.
        """
        from .embeddings import EmbeddingFunctionConfig

        vec_and_function = []
        for name, field_info in cls.safe_get_fields().items():
            func = get_extras(field_info, "vector_column_for")
            if func is not None:
                vec_and_function.append([name, func])

        configs = []
        for vec, func in vec_and_function:
            for source, field_info in cls.safe_get_fields().items():
                src_func = get_extras(field_info, "source_column_for")
                if src_func is func:
                    # note we can't use == here since the function is a pydantic
                    # model so two instances of the same function are ==, so if you
                    # have multiple vector columns from multiple sources, both will
                    # be mapped to the same source column
                    # GH594
                    configs.append(
                        EmbeddingFunctionConfig(
                            source_column=source, vector_column=vec, function=func
                        )
                    )
        return configs

              

  

            to_arrow_schema

  
      `classmethod`
  

¶

to_arrow_schema()

    

      
Get the Arrow Schema for this model.

            
              Source code in `lancedb/pydantic.py`
              
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
@classmethod
def to_arrow_schema(cls):
    """
    Get the Arrow Schema for this model.
    """
    schema = pydantic_to_schema(cls)
    functions = cls.parse_embedding_functions()
    if len(functions) > 0:
        # Prevent circular import
        from .embeddings import EmbeddingFunctionRegistry

        metadata = EmbeddingFunctionRegistry.get_instance().get_table_metadata(
            functions
        )
        schema = schema.with_metadata(metadata)
    return schema

            
    

            field_names

  
      `classmethod`
  

¶

field_names() -> List[str]

    

      
Get the field names of this model.

            
              Source code in `lancedb/pydantic.py`
              
468
469
470
471
472
473
@classmethod
def field_names(cls) -> List[str]:
    """
    Get the field names of this model.
    """
    return list(cls.safe_get_fields().keys())

            
    

            parse_embedding_functions

  
      `classmethod`
  

¶

parse_embedding_functions() -> List['EmbeddingFunctionConfig']

    

      
Parse the embedding functions from this model.

            
              Source code in `lancedb/pydantic.py`
              
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
@classmethod
def parse_embedding_functions(cls) -> List["EmbeddingFunctionConfig"]:
    """
    Parse the embedding functions from this model.
    """
    from .embeddings import EmbeddingFunctionConfig

    vec_and_function = []
    for name, field_info in cls.safe_get_fields().items():
        func = get_extras(field_info, "vector_column_for")
        if func is not None:
            vec_and_function.append([name, func])

    configs = []
    for vec, func in vec_and_function:
        for source, field_info in cls.safe_get_fields().items():
            src_func = get_extras(field_info, "source_column_for")
            if src_func is func:
                # note we can't use == here since the function is a pydantic
                # model so two instances of the same function are ==, so if you
                # have multiple vector columns from multiple sources, both will
                # be mapped to the same source column
                # GH594
                configs.append(
                    EmbeddingFunctionConfig(
                        source_column=source, vector_column=vec, function=func
                    )
                )
    return configs

            
    

  

    

## Reranking¶

            lancedb.rerankers.linear_combination.LinearCombinationReranker

¶

    
            

              Bases: `Reranker`

      
Reranks the results using a linear combination of the scores from the
vector and FTS search. For missing scores, fill with `fill` value.

Parameters:

    
        
- 
          `weight`
              (`float`, default:
                  `0.7`
)
          –
          
            
The weight to give to the vector score. Must be between 0 and 1.

          
        
        
- 
          `fill`
              (`float`, default:
                  `1.0`
)
          –
          
            
The score to give to results that are only in one of the two result sets.
This is treated as penalty, so a higher value means a lower score.
TODO: We should just hardcode this--
its pretty confusing as we invert scores to calculate final score

          
        
        
- 
          `return_score`
              (`str`, default:
                  `"relevance"`
)
          –
          
            
opntions are "relevance" or "all"
The type of score to return. If "relevance", will return only the relevance
score. If "all", will return all scores from the vector and FTS search along
with the relevance score.

          
        
    

              
                Source code in `lancedb/rerankers/linear_combination.py`
                
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
class LinearCombinationReranker(Reranker):
    """
    Reranks the results using a linear combination of the scores from the
    vector and FTS search. For missing scores, fill with `fill` value.
    Parameters
    ----------
    weight : float, default 0.7
        The weight to give to the vector score. Must be between 0 and 1.
    fill : float, default 1.0
        The score to give to results that are only in one of the two result sets.
        This is treated as penalty, so a higher value means a lower score.
        TODO: We should just hardcode this--
        its pretty confusing as we invert scores to calculate final score
    return_score : str, default "relevance"
        opntions are "relevance" or "all"
        The type of score to return. If "relevance", will return only the relevance
        score. If "all", will return all scores from the vector and FTS search along
        with the relevance score.
    """

    def __init__(
        self, weight: float = 0.7, fill: float = 1.0, return_score="relevance"
    ):
        if weight < 0 or weight > 1:
            raise ValueError("weight must be between 0 and 1.")
        super().__init__(return_score)
        self.weight = weight
        self.fill = fill

    def __str__(self):
        return f"LinearCombinationReranker(weight={self.weight}, fill={self.fill})"

    def rerank_hybrid(
        self,
        query: str,  # noqa: F821
        vector_results: pa.Table,
        fts_results: pa.Table,
    ):
        combined_results = self.merge_results(vector_results, fts_results, self.fill)

        return combined_results

    def merge_results(
        self, vector_results: pa.Table, fts_results: pa.Table, fill: float
    ):
        # If one is empty then return the other and add _relevance_score
        # column equal the existing vector or fts score
        if len(vector_results) == 0:
            results = fts_results.append_column(
                "_relevance_score",
                pa.array(fts_results["_score"], type=pa.float32()),
            )
            if self.score == "relevance":
                results = self._keep_relevance_score(results)
            elif self.score == "all":
                results = results.append_column(
                    "_distance",
                    pa.array([nan] * len(fts_results), type=pa.float32()),
                )
            return results

        if len(fts_results) == 0:
            # invert the distance to relevance score
            results = vector_results.append_column(
                "_relevance_score",
                pa.array(
                    [
                        self._invert_score(distance)
                        for distance in vector_results["_distance"].to_pylist()
                    ],
                    type=pa.float32(),
                ),
            )
            if self.score == "relevance":
                results = self._keep_relevance_score(results)
            elif self.score == "all":
                results = results.append_column(
                    "_score",
                    pa.array([nan] * len(vector_results), type=pa.float32()),
                )
            return results
        results = defaultdict()
        for vector_result in vector_results.to_pylist():
            results[vector_result["_rowid"]] = vector_result
        for fts_result in fts_results.to_pylist():
            row_id = fts_result["_rowid"]
            if row_id in results:
                results[row_id]["_score"] = fts_result["_score"]
            else:
                results[row_id] = fts_result

        combined_list = []
        for row_id, result in results.items():
            vector_score = self._invert_score(result.get("_distance", fill))
            fts_score = result.get("_score", fill)
            result["_relevance_score"] = self._combine_score(vector_score, fts_score)
            combined_list.append(result)

        relevance_score_schema = pa.schema(
            [
                pa.field("_relevance_score", pa.float32()),
            ]
        )
        combined_schema = pa.unify_schemas(
            [vector_results.schema, fts_results.schema, relevance_score_schema]
        )
        tbl = pa.Table.from_pylist(combined_list, schema=combined_schema).sort_by(
            [("_relevance_score", "descending")]
        )
        if self.score == "relevance":
            tbl = self._keep_relevance_score(tbl)
        return tbl

    def _combine_score(self, vector_score, fts_score):
        # these scores represent distance
        return 1 - (self.weight * vector_score + (1 - self.weight) * fts_score)

    def _invert_score(self, dist: float):
        # Invert the score between relevance and distance
        return 1 - dist

              

  

  

    

            lancedb.rerankers.cohere.CohereReranker

¶

    
            

              Bases: `Reranker`

      
Reranks the results using the Cohere Rerank API.
https://docs.cohere.com/docs/rerank-guide

Parameters:

    
        
- 
          `model_name`
              (`str`, default:
                  `"rerank-english-v2.0"`
)
          –
          
            
The name of the cross encoder model to use. Available cohere models are:
- rerank-english-v2.0
- rerank-multilingual-v2.0

          
        
        
- 
          `column`
              (`str`, default:
                  `"text"`
)
          –
          
            
The name of the column to use as input to the cross encoder model.

          
        
        
- 
          `top_n`
              (`str`, default:
                  `None`
)
          –
          
            
The number of results to return. If None, will return all results.

          
        
    

              
                Source code in `lancedb/rerankers/cohere.py`
                
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
class CohereReranker(Reranker):
    """
    Reranks the results using the Cohere Rerank API.
    https://docs.cohere.com/docs/rerank-guide

    Parameters
    ----------
    model_name : str, default "rerank-english-v2.0"
        The name of the cross encoder model to use. Available cohere models are:
        - rerank-english-v2.0
        - rerank-multilingual-v2.0
    column : str, default "text"
        The name of the column to use as input to the cross encoder model.
    top_n : str, default None
        The number of results to return. If None, will return all results.
    """

    def __init__(
        self,
        model_name: str = "rerank-english-v3.0",
        column: str = "text",
        top_n: Union[int, None] = None,
        return_score="relevance",
        api_key: Union[str, None] = None,
    ):
        super().__init__(return_score)
        self.model_name = model_name
        self.column = column
        self.top_n = top_n
        self.api_key = api_key

    def __str__(self):
        return f"CohereReranker(model_name={self.model_name})"

    @cached_property
    def _client(self):
        cohere = attempt_import_or_raise("cohere")
        # ensure version is at least 0.5.0
        if hasattr(cohere, "__version__") and Version(cohere.__version__) < Version(
            "0.5.0"
        ):
            raise ValueError(
                f"cohere version must be at least 0.5.0, found {cohere.__version__}"
            )
        if os.environ.get("COHERE_API_KEY") is None and self.api_key is None:
            raise ValueError(
                "COHERE_API_KEY not set. Either set it in your environment or \
                pass it as `api_key` argument to the CohereReranker."
            )
        return cohere.Client(os.environ.get("COHERE_API_KEY") or self.api_key)

    def _rerank(self, result_set: pa.Table, query: str):
        result_set = self._handle_empty_results(result_set)
        if len(result_set) == 0:
            return result_set
        docs = result_set[self.column].to_pylist()
        response = self._client.rerank(
            query=query,
            documents=docs,
            top_n=self.top_n,
            model=self.model_name,
        )
        results = (
            response.results
        )  # returns list (text, idx, relevance) attributes sorted descending by score
        indices, scores = list(
            zip(*[(result.index, result.relevance_score) for result in results])
        )  # tuples
        result_set = result_set.take(list(indices))
        # add the scores
        result_set = result_set.append_column(
            "_relevance_score", pa.array(scores, type=pa.float32())
        )

        return result_set

    def rerank_hybrid(
        self,
        query: str,
        vector_results: pa.Table,
        fts_results: pa.Table,
    ):
        if self.score == "all":
            combined_results = self._merge_and_keep_scores(vector_results, fts_results)
        else:
            combined_results = self.merge_results(vector_results, fts_results)
        combined_results = self._rerank(combined_results, query)
        if self.score == "relevance":
            combined_results = self._keep_relevance_score(combined_results)

        return combined_results

    def rerank_vector(self, query: str, vector_results: pa.Table):
        vector_results = self._rerank(vector_results, query)
        if self.score == "relevance":
            vector_results = vector_results.drop_columns(["_distance"])
        return vector_results

    def rerank_fts(self, query: str, fts_results: pa.Table):
        fts_results = self._rerank(fts_results, query)
        if self.score == "relevance":
            fts_results = fts_results.drop_columns(["_score"])
        return fts_results

              

  

  

    

            lancedb.rerankers.colbert.ColbertReranker

¶

    
            

              Bases: `AnswerdotaiRerankers`

      
Reranks the results using the ColBERT model.

Parameters:

    
        
- 
          `model_name`
              (`str`, default:
                  `"colbert" (colbert-ir/colbert-v2.0)`
)
          –
          
            
The name of the cross encoder model to use.

          
        
        
- 
          `column`
              (`str`, default:
                  `"text"`
)
          –
          
            
The name of the column to use as input to the cross encoder model.

          
        
        
- 
          `return_score`
              (`str`, default:
                  `"relevance"`
)
          –
          
            
options are "relevance" or "all". Only "relevance" is supported for now.

          
        
        
- 
          `**kwargs`
          –
          
            
Additional keyword arguments to pass to the model, for example, 'device'.
See AnswerDotAI/rerankers for more information.

          
        
    

              
                Source code in `lancedb/rerankers/colbert.py`
                
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
class ColbertReranker(AnswerdotaiRerankers):
    """
    Reranks the results using the ColBERT model.

    Parameters
    ----------
    model_name : str, default "colbert" (colbert-ir/colbert-v2.0)
        The name of the cross encoder model to use.
    column : str, default "text"
        The name of the column to use as input to the cross encoder model.
    return_score : str, default "relevance"
        options are "relevance" or "all". Only "relevance" is supported for now.
    **kwargs
        Additional keyword arguments to pass to the model, for example, 'device'.
        See AnswerDotAI/rerankers for more information.
    """

    def __init__(
        self,
        model_name: str = "colbert-ir/colbertv2.0",
        column: str = "text",
        return_score="relevance",
        **kwargs,
    ):
        super().__init__(
            model_type="colbert",
            model_name=model_name,
            column=column,
            return_score=return_score,
            **kwargs,
        )

              

  

  

    

            lancedb.rerankers.cross_encoder.CrossEncoderReranker

¶

    
            

              Bases: `Reranker`

      
Reranks the results using a cross encoder model. The cross encoder model is
used to score the query and each result. The results are then sorted by the score.

Parameters:

    
        
- 
          `model_name`
              (`str`, default:
                  `"cross-encoder/ms-marco-TinyBERT-L-6"`
)
          –
          
            
The name of the cross encoder model to use. See the sentence transformers
documentation for a list of available models.

          
        
        
- 
          `column`
              (`str`, default:
                  `"text"`
)
          –
          
            
The name of the column to use as input to the cross encoder model.

          
        
        
- 
          `device`
              (`str`, default:
                  `None`
)
          –
          
            
The device to use for the cross encoder model. If None, will use "cuda"
if available, otherwise "cpu".

          
        
        
- 
          `return_score`
              (`str`, default:
                  `"relevance"`
)
          –
          
            
options are "relevance" or "all". Only "relevance" is supported for now.

          
        
        
- 
          `trust_remote_code`
              (`bool`, default:
                  `True`
)
          –
          
            
If True, will trust the remote code to be safe. If False, will not trust
the remote code and will not run it

          
        
    

              
                Source code in `lancedb/rerankers/cross_encoder.py`
                
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
class CrossEncoderReranker(Reranker):
    """
    Reranks the results using a cross encoder model. The cross encoder model is
    used to score the query and each result. The results are then sorted by the score.

    Parameters
    ----------
    model_name : str, default "cross-encoder/ms-marco-TinyBERT-L-6"
        The name of the cross encoder model to use. See the sentence transformers
        documentation for a list of available models.
    column : str, default "text"
        The name of the column to use as input to the cross encoder model.
    device : str, default None
        The device to use for the cross encoder model. If None, will use "cuda"
        if available, otherwise "cpu".
    return_score : str, default "relevance"
        options are "relevance" or "all". Only "relevance" is supported for now.
    trust_remote_code : bool, default True
        If True, will trust the remote code to be safe. If False, will not trust
        the remote code and will not run it
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-TinyBERT-L-6",
        column: str = "text",
        device: Union[str, None] = None,
        return_score="relevance",
        trust_remote_code: bool = True,
    ):
        super().__init__(return_score)
        torch = attempt_import_or_raise("torch")
        self.model_name = model_name
        self.column = column
        self.device = device
        self.trust_remote_code = trust_remote_code
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def __str__(self):
        return f"CrossEncoderReranker(model_name={self.model_name})"

    @cached_property
    def model(self):
        sbert = attempt_import_or_raise("sentence_transformers")
        # Allows overriding the automatically selected device
        cross_encoder = sbert.CrossEncoder(
            self.model_name,
            device=self.device,
            trust_remote_code=self.trust_remote_code,
        )

        return cross_encoder

    def _rerank(self, result_set: pa.Table, query: str):
        result_set = self._handle_empty_results(result_set)
        if len(result_set) == 0:
            return result_set
        passages = result_set[self.column].to_pylist()
        cross_inp = [[query, passage] for passage in passages]
        cross_scores = self.model.predict(cross_inp)
        result_set = result_set.append_column(
            "_relevance_score", pa.array(cross_scores, type=pa.float32())
        )

        return result_set

    def rerank_hybrid(
        self,
        query: str,
        vector_results: pa.Table,
        fts_results: pa.Table,
    ):
        if self.score == "all":
            combined_results = self._merge_and_keep_scores(vector_results, fts_results)
        else:
            combined_results = self.merge_results(vector_results, fts_results)
        combined_results = self._rerank(combined_results, query)
        # sort the results by _score
        if self.score == "relevance":
            combined_results = self._keep_relevance_score(combined_results)

        combined_results = combined_results.sort_by(
            [("_relevance_score", "descending")]
        )

        return combined_results

    def rerank_vector(self, query: str, vector_results: pa.Table):
        vector_results = self._rerank(vector_results, query)
        if self.score == "relevance":
            vector_results = vector_results.drop_columns(["_distance"])

        vector_results = vector_results.sort_by([("_relevance_score", "descending")])
        return vector_results

    def rerank_fts(self, query: str, fts_results: pa.Table):
        fts_results = self._rerank(fts_results, query)
        if self.score == "relevance":
            fts_results = fts_results.drop_columns(["_score"])

        fts_results = fts_results.sort_by([("_relevance_score", "descending")])
        return fts_results

              

  

  

    

            lancedb.rerankers.openai.OpenaiReranker

¶

    
            

              Bases: `Reranker`

      
Reranks the results using the OpenAI API.
WARNING: This is a prompt based reranker that uses chat model that is
not a dedicated reranker API. This should be treated as experimental.

Parameters:

    
        
- 
          `model_name`
              (`str`, default:
                  `"gpt-4-turbo-preview"`
)
          –
          
            
The name of the cross encoder model to use.

          
        
        
- 
          `column`
              (`str`, default:
                  `"text"`
)
          –
          
            
The name of the column to use as input to the cross encoder model.

          
        
        
- 
          `return_score`
              (`str`, default:
                  `"relevance"`
)
          –
          
            
options are "relevance" or "all". Only "relevance" is supported for now.

          
        
        
- 
          `api_key`
              (`str`, default:
                  `None`
)
          –
          
            
The API key to use. If None, will use the OPENAI_API_KEY environment variable.

          
        
    

              
                Source code in `lancedb/rerankers/openai.py`
                
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
class OpenaiReranker(Reranker):
    """
    Reranks the results using the OpenAI API.
    WARNING: This is a prompt based reranker that uses chat model that is
    not a dedicated reranker API. This should be treated as experimental.

    Parameters
    ----------
    model_name : str, default "gpt-4-turbo-preview"
        The name of the cross encoder model to use.
    column : str, default "text"
        The name of the column to use as input to the cross encoder model.
    return_score : str, default "relevance"
        options are "relevance" or "all". Only "relevance" is supported for now.
    api_key : str, default None
        The API key to use. If None, will use the OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        model_name: str = "gpt-4-turbo-preview",
        column: str = "text",
        return_score="relevance",
        api_key: Optional[str] = None,
    ):
        super().__init__(return_score)
        self.model_name = model_name
        self.column = column
        self.api_key = api_key

    def __str__(self):
        return f"OpenaiReranker(model_name={self.model_name})"

    def _rerank(self, result_set: pa.Table, query: str):
        result_set = self._handle_empty_results(result_set)
        if len(result_set) == 0:
            return result_set
        docs = result_set[self.column].to_pylist()
        response = self._client.chat.completions.create(
            model=self.model_name,
            response_format={"type": "json_object"},
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert relevance ranker. Given a list of\
                        documents and a query, your job is to determine the relevance\
                        each document is for answering the query. Your output is JSON,\
                        which is a list of documents. Each document has two fields,\
                        content and relevance_score.  relevance_score is from 0.0 to\
                        1.0 indicating the relevance of the text to the given query.\
                        Make sure to include all documents in the response.",
                },
                {"role": "user", "content": f"Query: {query} Docs: {docs}"},
            ],
        )
        results = json.loads(response.choices[0].message.content)["documents"]
        docs, scores = list(
            zip(*[(result["content"], result["relevance_score"]) for result in results])
        )  # tuples
        # replace the self.column column with the docs
        result_set = result_set.drop(self.column)
        result_set = result_set.append_column(
            self.column, pa.array(docs, type=pa.string())
        )
        # add the scores
        result_set = result_set.append_column(
            "_relevance_score", pa.array(scores, type=pa.float32())
        )

        return result_set

    def rerank_hybrid(
        self,
        query: str,
        vector_results: pa.Table,
        fts_results: pa.Table,
    ):
        if self.score == "all":
            combined_results = self._merge_and_keep_scores(vector_results, fts_results)
        else:
            combined_results = self.merge_results(vector_results, fts_results)
        combined_results = self._rerank(combined_results, query)
        if self.score == "relevance":
            combined_results = self._keep_relevance_score(combined_results)

        combined_results = combined_results.sort_by(
            [("_relevance_score", "descending")]
        )

        return combined_results

    def rerank_vector(self, query: str, vector_results: pa.Table):
        vector_results = self._rerank(vector_results, query)
        if self.score == "relevance":
            vector_results = vector_results.drop_columns(["_distance"])
        vector_results = vector_results.sort_by([("_relevance_score", "descending")])
        return vector_results

    def rerank_fts(self, query: str, fts_results: pa.Table):
        fts_results = self._rerank(fts_results, query)
        if self.score == "relevance":
            fts_results = fts_results.drop_columns(["_score"])
        fts_results = fts_results.sort_by([("_relevance_score", "descending")])
        return fts_results

    @cached_property
    def _client(self):
        openai = attempt_import_or_raise(
            "openai"
        )  # TODO: force version or handle versions < 1.0
        if os.environ.get("OPENAI_API_KEY") is None and self.api_key is None:
            raise ValueError(
                "OPENAI_API_KEY not set. Either set it in your environment or \
                pass it as `api_key` argument to the CohereReranker."
            )
        return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or self.api_key)

              

  

  

    

## Connections (Asynchronous)¶

Connections represent a connection to a LanceDb database and
can be used to create, list, or open tables.

            lancedb.connect_async

  
      `async`
  

¶

connect_async(uri: URI, *, api_key: Optional[str] = None, region: str = 'us-east-1', host_override: Optional[str] = None, read_consistency_interval: Optional[timedelta] = None, client_config: Optional[Union[ClientConfig, Dict[str, Any]]] = None, storage_options: Optional[Dict[str, str]] = None, session: Optional[Session] = None) -> AsyncConnection

    

      
Connect to a LanceDB database.

Parameters:

    
        
- 
          `uri`
              (`URI`)
          –
          
            
The uri of the database.

          
        
        
- 
          `api_key`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
If present, connect to LanceDB cloud.
Otherwise, connect to a database on file system or cloud storage.
Can be set via environment variable `LANCEDB_API_KEY`.

          
        
        
- 
          `region`
              (`str`, default:
                  `'us-east-1'`
)
          –
          
            
The region to use for LanceDB Cloud.

          
        
        
- 
          `host_override`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The override url for LanceDB Cloud.

          
        
        
- 
          `read_consistency_interval`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
(For LanceDB OSS only)
The interval at which to check for updates to the table from other
processes. If None, then consistency is not checked. For performance
reasons, this is the default. For strong consistency, set this to
zero seconds. Then every read will check for updates from other
processes. As a compromise, you can set this to a non-zero timedelta
for eventual consistency. If more than that interval has passed since
the last check, then the table will be checked for updates. Note: this
consistency only applies to read operations. Write operations are
always consistent.

          
        
        
- 
          `client_config`
              (`Optional[Union[ClientConfig, Dict[str, Any]]]`, default:
                  `None`
)
          –
          
            
Configuration options for the LanceDB Cloud HTTP client. If a dict, then
the keys are the attributes of the ClientConfig class. If None, then the
default configuration is used.

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. See available options at
https://lancedb.com/docs/storage/

          
        
        
- 
          `session`
              (`Optional[Session]`, default:
                  `None`
)
          –
          
            
(For LanceDB OSS only)
A session to use for this connection. Sessions allow you to configure
cache sizes for index and metadata caches, which can significantly
impact memory use and performance. They can also be re-used across
multiple connections to share the same cache state.

          
        
    

Examples:

    
>>> import lancedb
>>> async def doctest_example():
...     # For a local directory, provide a path to the database
...     db = await lancedb.connect_async("~/.lancedb")
...     # For object storage, use a URI prefix
...     db = await lancedb.connect_async("s3://my-bucket/lancedb",
...                                      storage_options={
...                                          "aws_access_key_id": "***"})
...     # Connect to LanceDB cloud
...     db = await lancedb.connect_async("db://my_database", api_key="ldb_...",
...                                      client_config={
...                                          "retry_config": {"retries": 5}})

Returns:

    
        
- 
`conn` (              `AsyncConnection`
)          –
          
            
A connection to a LanceDB database.

          
        
    

            
              Source code in `lancedb/__init__.py`
              
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
async def connect_async(
    uri: URI,
    *,
    api_key: Optional[str] = None,
    region: str = "us-east-1",
    host_override: Optional[str] = None,
    read_consistency_interval: Optional[timedelta] = None,
    client_config: Optional[Union[ClientConfig, Dict[str, Any]]] = None,
    storage_options: Optional[Dict[str, str]] = None,
    session: Optional[Session] = None,
) -> AsyncConnection:
    """Connect to a LanceDB database.

    Parameters
    ----------
    uri: str or Path
        The uri of the database.
    api_key: str, optional
        If present, connect to LanceDB cloud.
        Otherwise, connect to a database on file system or cloud storage.
        Can be set via environment variable `LANCEDB_API_KEY`.
    region: str, default "us-east-1"
        The region to use for LanceDB Cloud.
    host_override: str, optional
        The override url for LanceDB Cloud.
    read_consistency_interval: timedelta, default None
        (For LanceDB OSS only)
        The interval at which to check for updates to the table from other
        processes. If None, then consistency is not checked. For performance
        reasons, this is the default. For strong consistency, set this to
        zero seconds. Then every read will check for updates from other
        processes. As a compromise, you can set this to a non-zero timedelta
        for eventual consistency. If more than that interval has passed since
        the last check, then the table will be checked for updates. Note: this
        consistency only applies to read operations. Write operations are
        always consistent.
    client_config: ClientConfig or dict, optional
        Configuration options for the LanceDB Cloud HTTP client. If a dict, then
        the keys are the attributes of the ClientConfig class. If None, then the
        default configuration is used.
    storage_options: dict, optional
        Additional options for the storage backend. See available options at
        <https://lancedb.com/docs/storage/>
    session: Session, optional
        (For LanceDB OSS only)
        A session to use for this connection. Sessions allow you to configure
        cache sizes for index and metadata caches, which can significantly
        impact memory use and performance. They can also be re-used across
        multiple connections to share the same cache state.

    Examples
    --------

    >>> import lancedb
    >>> async def doctest_example():
    ...     # For a local directory, provide a path to the database
    ...     db = await lancedb.connect_async("~/.lancedb")
    ...     # For object storage, use a URI prefix
    ...     db = await lancedb.connect_async("s3://my-bucket/lancedb",
    ...                                      storage_options={
    ...                                          "aws_access_key_id": "***"})
    ...     # Connect to LanceDB cloud
    ...     db = await lancedb.connect_async("db://my_database", api_key="ldb_...",
    ...                                      client_config={
    ...                                          "retry_config": {"retries": 5}})

    Returns
    -------
    conn : AsyncConnection
        A connection to a LanceDB database.
    """
    if read_consistency_interval is not None:
        read_consistency_interval_secs = read_consistency_interval.total_seconds()
    else:
        read_consistency_interval_secs = None

    if isinstance(client_config, dict):
        client_config = ClientConfig(**client_config)

    _check_s3_bucket_with_dots(str(uri), storage_options)

    return AsyncConnection(
        await lancedb_connect(
            sanitize_uri(uri),
            api_key,
            region,
            host_override,
            read_consistency_interval_secs,
            client_config,
            storage_options,
            session,
        )
    )

            
    

            lancedb.db.AsyncConnection

¶

    
            

              Bases: `object`

      
An active LanceDB connection

To obtain a connection you can use the connect_async
function.

This could be a native connection (using lance) or a remote connection (e.g. for
connecting to LanceDb Cloud)

Local connections do not currently hold any open resources but they may do so in the
future (for example, for shared cache or connections to catalog services) Remote
connections represent an open connection to the remote server.  The
close method can be used to release any
underlying resources eagerly.  The connection can also be used as a context manager.

Connections can be shared on multiple threads and are expected to be long lived.
Connections can also be used as a context manager, however, in many cases a single
connection can be used for the lifetime of the application and so this is often
not needed.  Closing a connection is optional.  If it is not closed then it will
be automatically closed when the connection object is deleted.

Examples:

    
>>> import lancedb
>>> async def doctest_example():
...   with await lancedb.connect_async("/tmp/my_dataset") as conn:
...     # do something with the connection
...     pass
...   # conn is closed here

              
                Source code in `lancedb/db.py`
                
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
1672
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
1720
1721
1722
1723
1724
1725
1726
class AsyncConnection(object):
    """An active LanceDB connection

    To obtain a connection you can use the [connect_async][lancedb.connect_async]
    function.

    This could be a native connection (using lance) or a remote connection (e.g. for
    connecting to LanceDb Cloud)

    Local connections do not currently hold any open resources but they may do so in the
    future (for example, for shared cache or connections to catalog services) Remote
    connections represent an open connection to the remote server.  The
    [close][lancedb.db.AsyncConnection.close] method can be used to release any
    underlying resources eagerly.  The connection can also be used as a context manager.

    Connections can be shared on multiple threads and are expected to be long lived.
    Connections can also be used as a context manager, however, in many cases a single
    connection can be used for the lifetime of the application and so this is often
    not needed.  Closing a connection is optional.  If it is not closed then it will
    be automatically closed when the connection object is deleted.

    Examples
    --------

    >>> import lancedb
    >>> async def doctest_example():
    ...   with await lancedb.connect_async("/tmp/my_dataset") as conn:
    ...     # do something with the connection
    ...     pass
    ...   # conn is closed here
    """

    def __init__(self, connection: LanceDbConnection):
        self._inner = connection

    def __repr__(self):
        return self._inner.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def is_open(self):
        """Return True if the connection is open."""
        return self._inner.is_open()

    def close(self):
        """Close the connection, releasing any underlying resources.

        It is safe to call this method multiple times.

        Any attempt to use the connection after it is closed will result in an error."""
        self._inner.close()

    @property
    def uri(self) -> str:
        return self._inner.uri

    async def get_read_consistency_interval(self) -> Optional[timedelta]:
        interval_secs = await self._inner.get_read_consistency_interval()
        if interval_secs is not None:
            return timedelta(seconds=interval_secs)
        else:
            return None

    async def list_namespaces(
        self,
        namespace: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ListNamespacesResponse:
        """List immediate child namespace names in the given namespace.

        Parameters
        ----------
        namespace: List[str], optional
            The parent namespace to list namespaces in.
            None or empty list represents root namespace.
        page_token: str, optional
            The token to use for pagination. If not present, start from the beginning.
        limit: int, optional
            The maximum number of results to return.

        Returns
        -------
        ListNamespacesResponse
            Response containing namespace names and optional pagination token
        """
        if namespace is None:
            namespace = []
        result = await self._inner.list_namespaces(
            namespace=namespace, page_token=page_token, limit=limit
        )
        return ListNamespacesResponse(**result)

    async def create_namespace(
        self,
        namespace: List[str],
        mode: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> CreateNamespaceResponse:
        """Create a new namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to create.
        mode: str, optional
            Creation mode - "create", "exist_ok", or "overwrite". Case insensitive.
        properties: Dict[str, str], optional
            Properties to associate with the namespace

        Returns
        -------
        CreateNamespaceResponse
            Response containing namespace properties
        """
        result = await self._inner.create_namespace(
            namespace,
            mode=_normalize_create_namespace_mode(mode),
            properties=properties,
        )
        return CreateNamespaceResponse(**result)

    async def drop_namespace(
        self,
        namespace: List[str],
        mode: Optional[str] = None,
        behavior: Optional[str] = None,
    ) -> DropNamespaceResponse:
        """Drop a namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to drop.
        mode: str, optional
            Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
        behavior: str, optional
            Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
            Case insensitive.

        Returns
        -------
        DropNamespaceResponse
            Response containing properties and transaction_id if applicable.
        """
        result = await self._inner.drop_namespace(
            namespace,
            mode=_normalize_drop_namespace_mode(mode),
            behavior=_normalize_drop_namespace_behavior(behavior),
        )
        return DropNamespaceResponse(**result)

    async def describe_namespace(
        self, namespace: List[str]
    ) -> DescribeNamespaceResponse:
        """Describe a namespace.

        Parameters
        ----------
        namespace: List[str]
            The namespace identifier to describe.

        Returns
        -------
        DescribeNamespaceResponse
            Response containing the namespace properties.
        """
        result = await self._inner.describe_namespace(namespace)
        return DescribeNamespaceResponse(**result)

    async def list_tables(
        self,
        namespace: Optional[List[str]] = None,
        page_token: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ListTablesResponse:
        """List all tables in this database with pagination support.

        Parameters
        ----------
        namespace: List[str], optional
            The namespace to list tables in.
            None or empty list represents root namespace.
        page_token: str, optional
            Token for pagination. Use the token from a previous response
            to get the next page of results.
        limit: int, optional
            The maximum number of results to return.

        Returns
        -------
        ListTablesResponse
            Response containing table names and optional page_token for pagination.
        """
        if namespace is None:
            namespace = []
        result = await self._inner.list_tables(
            namespace=namespace, page_token=page_token, limit=limit
        )
        return ListTablesResponse(**result)

    async def table_names(
        self,
        *,
        namespace: Optional[List[str]] = None,
        start_after: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Iterable[str]:
        """List all tables in this database, in sorted order

        .. deprecated::
            Use :meth:`list_tables` instead, which provides proper pagination support.

        Parameters
        ----------
        namespace: List[str], optional
            The namespace to list tables in.
            None or empty list represents root namespace.
        start_after: str, optional
            If present, only return names that come lexicographically after the supplied
            value.

            This can be combined with limit to implement pagination by setting this to
            the last table name from the previous page.
        limit: int, default 10
            The number of results to return.

        Returns
        -------
        Iterable of str
        """
        import warnings

        warnings.warn(
            "table_names() is deprecated, use list_tables() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        if namespace is None:
            namespace = []
        return await self._inner.table_names(
            namespace=namespace, start_after=start_after, limit=limit
        )

    async def create_table(
        self,
        name: str,
        data: Optional[DATA] = None,
        schema: Optional[Union[pa.Schema, LanceModel]] = None,
        mode: Optional[Literal["create", "overwrite"]] = None,
        exist_ok: Optional[bool] = None,
        on_bad_vectors: Optional[str] = None,
        fill_value: Optional[float] = None,
        storage_options: Optional[Dict[str, str]] = None,
        storage_options_provider: Optional["StorageOptionsProvider"] = None,
        *,
        namespace: Optional[List[str]] = None,
        embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None,
        location: Optional[str] = None,
    ) -> AsyncTable:
        """Create an [AsyncTable][lancedb.table.AsyncTable] in the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], default []
            The namespace to create the table in.
            Empty list represents root namespace.
        data: The data to initialize the table, *optional*
            User must provide at least one of `data` or `schema`.
            Acceptable types are:

            - list-of-dict

            - pandas.DataFrame

            - pyarrow.Table or pyarrow.RecordBatch
        schema: The schema of the table, *optional*
            Acceptable types are:

            - pyarrow.Schema

            - [LanceModel][lancedb.pydantic.LanceModel]
        mode: Literal["create", "overwrite"]; default "create"
            The mode to use when creating the table.
            Can be either "create" or "overwrite".
            By default, if the table already exists, an exception is raised.
            If you want to overwrite the table, use mode="overwrite".
        exist_ok: bool, default False
            If a table by the same name already exists, then raise an exception
            if exist_ok=False. If exist_ok=True, then open the existing table;
            it will not add the provided data but will validate against any
            schema that's specified.
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contains NaNs.
            One of "error", "drop", "fill".
        fill_value: float
            The value to use when filling vectors. Only used if on_bad_vectors="fill".
        storage_options: dict, optional
            Additional options for the storage backend. Options already set on the
            connection will be inherited by the table, but can be overridden here.
            See available options at
            <https://lancedb.com/docs/storage/>

            To enable stable row IDs (row IDs remain stable after compaction,
            update, delete, and merges), set `new_table_enable_stable_row_ids`
            to `"true"` in storage_options when connecting to the database.

        Returns
        -------
        AsyncTable
            A reference to the newly created table.

        !!! note

            The vector index won't be created by default.
            To create the index, call the `create_index` method on the table.

        Examples
        --------

        Can create with list of tuples or dictionaries:

        >>> import lancedb
        >>> async def doctest_example():
        ...     db = await lancedb.connect_async("./.lancedb")
        ...     data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
        ...             {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
        ...     my_table = await db.create_table("my_table", data)
        ...     print(await my_table.query().limit(5).to_arrow())
        >>> import asyncio
        >>> asyncio.run(doctest_example())
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: double
        long: double
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        You can also pass a pandas DataFrame:

        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...    "vector": [[1.1, 1.2], [0.2, 1.8]],
        ...    "lat": [45.5, 40.1],
        ...    "long": [-122.7, -74.1]
        ... })
        >>> async def pandas_example():
        ...     db = await lancedb.connect_async("./.lancedb")
        ...     my_table = await db.create_table("table2", data)
        ...     print(await my_table.query().limit(5).to_arrow())
        >>> asyncio.run(pandas_example())
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: double
        long: double
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        Data is converted to Arrow before being written to disk. For maximum
        control over how data is saved, either provide the PyArrow schema to
        convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

        >>> import pyarrow as pa
        >>> custom_schema = pa.schema([
        ...   pa.field("vector", pa.list_(pa.float32(), 2)),
        ...   pa.field("lat", pa.float32()),
        ...   pa.field("long", pa.float32())
        ... ])
        >>> async def with_schema():
        ...     db = await lancedb.connect_async("./.lancedb")
        ...     my_table = await db.create_table("table3", data, schema = custom_schema)
        ...     print(await my_table.query().limit(5).to_arrow())
        >>> asyncio.run(with_schema())
        pyarrow.Table
        vector: fixed_size_list<item: float>[2]
          child 0, item: float
        lat: float
        long: float
        ----
        vector: [[[1.1,1.2],[0.2,1.8]]]
        lat: [[45.5,40.1]]
        long: [[-122.7,-74.1]]

        It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

        >>> import pyarrow as pa
        >>> def make_batches():
        ...     for i in range(5):
        ...         yield pa.RecordBatch.from_arrays(
        ...             [
        ...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
        ...                     pa.list_(pa.float32(), 2)),
        ...                 pa.array(["foo", "bar"]),
        ...                 pa.array([10.0, 20.0]),
        ...             ],
        ...             ["vector", "item", "price"],
        ...         )
        >>> schema=pa.schema([
        ...     pa.field("vector", pa.list_(pa.float32(), 2)),
        ...     pa.field("item", pa.utf8()),
        ...     pa.field("price", pa.float32()),
        ... ])
        >>> async def iterable_example():
        ...     db = await lancedb.connect_async("./.lancedb")
        ...     await db.create_table("table4", make_batches(), schema=schema)
        >>> asyncio.run(iterable_example())
        """
        if namespace is None:
            namespace = []
        metadata = None

        if embedding_functions is not None:
            # If we passed in embedding functions explicitly
            # then we'll override any schema metadata that
            # may was implicitly specified by the LanceModel schema
            registry = EmbeddingFunctionRegistry.get_instance()
            metadata = registry.get_table_metadata(embedding_functions)

        # Defining defaults here and not in function prototype.  In the future
        # these defaults will move into rust so better to keep them as None.
        if on_bad_vectors is None:
            on_bad_vectors = "error"

        if fill_value is None:
            fill_value = 0.0

        data, schema = sanitize_create_table(
            data, schema, metadata, on_bad_vectors, fill_value
        )
        validate_schema(schema)

        if exist_ok is None:
            exist_ok = False
        if mode is None:
            mode = "create"
        if mode == "create" and exist_ok:
            mode = "exist_ok"

        if data is None:
            new_table = await self._inner.create_empty_table(
                name,
                mode,
                schema,
                namespace=namespace,
                storage_options=storage_options,
                storage_options_provider=storage_options_provider,
                location=location,
            )
        else:
            data = data_to_reader(data, schema)
            new_table = await self._inner.create_table(
                name,
                mode,
                data,
                namespace=namespace,
                storage_options=storage_options,
                storage_options_provider=storage_options_provider,
                location=location,
            )

        return AsyncTable(new_table)

    async def open_table(
        self,
        name: str,
        *,
        namespace: Optional[List[str]] = None,
        storage_options: Optional[Dict[str, str]] = None,
        storage_options_provider: Optional["StorageOptionsProvider"] = None,
        index_cache_size: Optional[int] = None,
        location: Optional[str] = None,
    ) -> AsyncTable:
        """Open a Lance Table in the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], optional
            The namespace to open the table from.
            None or empty list represents root namespace.
        storage_options: dict, optional
            Additional options for the storage backend. Options already set on the
            connection will be inherited by the table, but can be overridden here.
            See available options at
            <https://lancedb.com/docs/storage/>
        index_cache_size: int, default 256
            **Deprecated**: Use session-level cache configuration instead.
            Create a Session with custom cache sizes and pass it to lancedb.connect().

            Set the size of the index cache, specified as a number of entries

            The exact meaning of an "entry" will depend on the type of index:
            * IVF - there is one entry for each IVF partition
            * BTREE - there is one entry for the entire index

            This cache applies to the entire opened table, across all indices.
            Setting this value higher will increase performance on larger datasets
            at the expense of more RAM
        location: str, optional
            The explicit location (URI) of the table. If provided, the table will be
            opened from this location instead of deriving it from the database URI
            and table name.

        Returns
        -------
        A LanceTable object representing the table.
        """
        if namespace is None:
            namespace = []
        table = await self._inner.open_table(
            name,
            namespace=namespace,
            storage_options=storage_options,
            storage_options_provider=storage_options_provider,
            index_cache_size=index_cache_size,
            location=location,
        )
        return AsyncTable(table)

    async def clone_table(
        self,
        target_table_name: str,
        source_uri: str,
        *,
        target_namespace: Optional[List[str]] = None,
        source_version: Optional[int] = None,
        source_tag: Optional[str] = None,
        is_shallow: bool = True,
    ) -> AsyncTable:
        """Clone a table from a source table.

        A shallow clone creates a new table that shares the underlying data files
        with the source table but has its own independent manifest. This allows
        both the source and cloned tables to evolve independently while initially
        sharing the same data, deletion, and index files.

        Parameters
        ----------
        target_table_name: str
            The name of the target table to create.
        source_uri: str
            The URI of the source table to clone from.
        target_namespace: List[str], optional
            The namespace for the target table.
            None or empty list represents root namespace.
        source_version: int, optional
            The version of the source table to clone.
        source_tag: str, optional
            The tag of the source table to clone.
        is_shallow: bool, default True
            Whether to perform a shallow clone (True) or deep clone (False).
            Currently only shallow clone is supported.

        Returns
        -------
        An AsyncTable object representing the cloned table.
        """
        if target_namespace is None:
            target_namespace = []
        table = await self._inner.clone_table(
            target_table_name,
            source_uri,
            target_namespace=target_namespace,
            source_version=source_version,
            source_tag=source_tag,
            is_shallow=is_shallow,
        )
        return AsyncTable(table)

    async def rename_table(
        self,
        cur_name: str,
        new_name: str,
        cur_namespace: Optional[List[str]] = None,
        new_namespace: Optional[List[str]] = None,
    ):
        """Rename a table in the database.

        Parameters
        ----------
        cur_name: str
            The current name of the table.
        new_name: str
            The new name of the table.
        cur_namespace: List[str], optional
            The namespace of the current table.
            None or empty list represents root namespace.
        new_namespace: List[str], optional
            The namespace to move the table to.
            If not specified, defaults to the same as cur_namespace.
        """
        if cur_namespace is None:
            cur_namespace = []
        if new_namespace is None:
            new_namespace = []
        await self._inner.rename_table(
            cur_name, new_name, cur_namespace=cur_namespace, new_namespace=new_namespace
        )

    async def drop_table(
        self,
        name: str,
        *,
        namespace: Optional[List[str]] = None,
        ignore_missing: bool = False,
    ):
        """Drop a table from the database.

        Parameters
        ----------
        name: str
            The name of the table.
        namespace: List[str], default []
            The namespace to drop the table from.
            Empty list represents root namespace.
        ignore_missing: bool, default False
            If True, ignore if the table does not exist.
        """
        if namespace is None:
            namespace = []
        try:
            await self._inner.drop_table(name, namespace=namespace)
        except ValueError as e:
            if not ignore_missing:
                raise e
            if f"Table '{name}' was not found" not in str(e):
                raise e

    async def drop_all_tables(self, namespace: Optional[List[str]] = None):
        """Drop all tables from the database.

        Parameters
        ----------
        namespace: List[str], optional
            The namespace to drop all tables from.
            None or empty list represents root namespace.
        """
        if namespace is None:
            namespace = []
        await self._inner.drop_all_tables(namespace=namespace)

    @deprecation.deprecated(
        deprecated_in="0.15.1",
        removed_in="0.17",
        current_version=__version__,
        details="Use drop_all_tables() instead",
    )
    async def drop_database(self):
        """
        Drop database
        This is the same thing as dropping all the tables
        """
        await self._inner.drop_all_tables()

              

  

            is_open

¶

is_open()

    

      
Return True if the connection is open.

            
              Source code in `lancedb/db.py`
              
1103
1104
1105
def is_open(self):
    """Return True if the connection is open."""
    return self._inner.is_open()

            
    

            close

¶

close()

    

      
Close the connection, releasing any underlying resources.

It is safe to call this method multiple times.

Any attempt to use the connection after it is closed will result in an error.

            
              Source code in `lancedb/db.py`
              
1107
1108
1109
1110
1111
1112
1113
def close(self):
    """Close the connection, releasing any underlying resources.

    It is safe to call this method multiple times.

    Any attempt to use the connection after it is closed will result in an error."""
    self._inner.close()

            
    

            list_namespaces

  
      `async`
  

¶

list_namespaces(namespace: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListNamespacesResponse

    

      
List immediate child namespace names in the given namespace.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The parent namespace to list namespaces in.
None or empty list represents root namespace.

          
        
        
- 
          `page_token`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The token to use for pagination. If not present, start from the beginning.

          
        
        
- 
          `limit`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of results to return.

          
        
    

Returns:

    
        
- 
              `ListNamespacesResponse`
          –
          
            
Response containing namespace names and optional pagination token

          
        
    

            
              Source code in `lancedb/db.py`
              
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
async def list_namespaces(
    self,
    namespace: Optional[List[str]] = None,
    page_token: Optional[str] = None,
    limit: Optional[int] = None,
) -> ListNamespacesResponse:
    """List immediate child namespace names in the given namespace.

    Parameters
    ----------
    namespace: List[str], optional
        The parent namespace to list namespaces in.
        None or empty list represents root namespace.
    page_token: str, optional
        The token to use for pagination. If not present, start from the beginning.
    limit: int, optional
        The maximum number of results to return.

    Returns
    -------
    ListNamespacesResponse
        Response containing namespace names and optional pagination token
    """
    if namespace is None:
        namespace = []
    result = await self._inner.list_namespaces(
        namespace=namespace, page_token=page_token, limit=limit
    )
    return ListNamespacesResponse(**result)

            
    

            create_namespace

  
      `async`
  

¶

create_namespace(namespace: List[str], mode: Optional[str] = None, properties: Optional[Dict[str, str]] = None) -> CreateNamespaceResponse

    

      
Create a new namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to create.

          
        
        
- 
          `mode`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Creation mode - "create", "exist_ok", or "overwrite". Case insensitive.

          
        
        
- 
          `properties`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Properties to associate with the namespace

          
        
    

Returns:

    
        
- 
              `CreateNamespaceResponse`
          –
          
            
Response containing namespace properties

          
        
    

            
              Source code in `lancedb/db.py`
              
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
async def create_namespace(
    self,
    namespace: List[str],
    mode: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
) -> CreateNamespaceResponse:
    """Create a new namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to create.
    mode: str, optional
        Creation mode - "create", "exist_ok", or "overwrite". Case insensitive.
    properties: Dict[str, str], optional
        Properties to associate with the namespace

    Returns
    -------
    CreateNamespaceResponse
        Response containing namespace properties
    """
    result = await self._inner.create_namespace(
        namespace,
        mode=_normalize_create_namespace_mode(mode),
        properties=properties,
    )
    return CreateNamespaceResponse(**result)

            
    

            drop_namespace

  
      `async`
  

¶

drop_namespace(namespace: List[str], mode: Optional[str] = None, behavior: Optional[str] = None) -> DropNamespaceResponse

    

      
Drop a namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to drop.

          
        
        
- 
          `mode`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.

          
        
        
- 
          `behavior`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
Case insensitive.

          
        
    

Returns:

    
        
- 
              `DropNamespaceResponse`
          –
          
            
Response containing properties and transaction_id if applicable.

          
        
    

            
              Source code in `lancedb/db.py`
              
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
async def drop_namespace(
    self,
    namespace: List[str],
    mode: Optional[str] = None,
    behavior: Optional[str] = None,
) -> DropNamespaceResponse:
    """Drop a namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to drop.
    mode: str, optional
        Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
    behavior: str, optional
        Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
        Case insensitive.

    Returns
    -------
    DropNamespaceResponse
        Response containing properties and transaction_id if applicable.
    """
    result = await self._inner.drop_namespace(
        namespace,
        mode=_normalize_drop_namespace_mode(mode),
        behavior=_normalize_drop_namespace_behavior(behavior),
    )
    return DropNamespaceResponse(**result)

            
    

            describe_namespace

  
      `async`
  

¶

describe_namespace(namespace: List[str]) -> DescribeNamespaceResponse

    

      
Describe a namespace.

Parameters:

    
        
- 
          `namespace`
              (`List[str]`)
          –
          
            
The namespace identifier to describe.

          
        
    

Returns:

    
        
- 
              `DescribeNamespaceResponse`
          –
          
            
Response containing the namespace properties.

          
        
    

            
              Source code in `lancedb/db.py`
              
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227
1228
1229
1230
1231
async def describe_namespace(
    self, namespace: List[str]
) -> DescribeNamespaceResponse:
    """Describe a namespace.

    Parameters
    ----------
    namespace: List[str]
        The namespace identifier to describe.

    Returns
    -------
    DescribeNamespaceResponse
        Response containing the namespace properties.
    """
    result = await self._inner.describe_namespace(namespace)
    return DescribeNamespaceResponse(**result)

            
    

            list_tables

  
      `async`
  

¶

list_tables(namespace: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListTablesResponse

    

      
List all tables in this database with pagination support.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to list tables in.
None or empty list represents root namespace.

          
        
        
- 
          `page_token`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
Token for pagination. Use the token from a previous response
to get the next page of results.

          
        
        
- 
          `limit`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of results to return.

          
        
    

Returns:

    
        
- 
              `ListTablesResponse`
          –
          
            
Response containing table names and optional page_token for pagination.

          
        
    

            
              Source code in `lancedb/db.py`
              
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
async def list_tables(
    self,
    namespace: Optional[List[str]] = None,
    page_token: Optional[str] = None,
    limit: Optional[int] = None,
) -> ListTablesResponse:
    """List all tables in this database with pagination support.

    Parameters
    ----------
    namespace: List[str], optional
        The namespace to list tables in.
        None or empty list represents root namespace.
    page_token: str, optional
        Token for pagination. Use the token from a previous response
        to get the next page of results.
    limit: int, optional
        The maximum number of results to return.

    Returns
    -------
    ListTablesResponse
        Response containing table names and optional page_token for pagination.
    """
    if namespace is None:
        namespace = []
    result = await self._inner.list_tables(
        namespace=namespace, page_token=page_token, limit=limit
    )
    return ListTablesResponse(**result)

            
    

            table_names

  
      `async`
  

¶

table_names(*, namespace: Optional[List[str]] = None, start_after: Optional[str] = None, limit: Optional[int] = None) -> Iterable[str]

    

      
List all tables in this database, in sorted order

.. deprecated::
    Use :meth:`list_tables` instead, which provides proper pagination support.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to list tables in.
None or empty list represents root namespace.

          
        
        
- 
          `start_after`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
If present, only return names that come lexicographically after the supplied
value.

This can be combined with limit to implement pagination by setting this to
the last table name from the previous page.

          
        
        
- 
          `limit`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The number of results to return.

          
        
    

Returns:

    
        
- 
              `Iterable of str`
          –
          
            
          
        
    

            
              Source code in `lancedb/db.py`
              
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
async def table_names(
    self,
    *,
    namespace: Optional[List[str]] = None,
    start_after: Optional[str] = None,
    limit: Optional[int] = None,
) -> Iterable[str]:
    """List all tables in this database, in sorted order

    .. deprecated::
        Use :meth:`list_tables` instead, which provides proper pagination support.

    Parameters
    ----------
    namespace: List[str], optional
        The namespace to list tables in.
        None or empty list represents root namespace.
    start_after: str, optional
        If present, only return names that come lexicographically after the supplied
        value.

        This can be combined with limit to implement pagination by setting this to
        the last table name from the previous page.
    limit: int, default 10
        The number of results to return.

    Returns
    -------
    Iterable of str
    """
    import warnings

    warnings.warn(
        "table_names() is deprecated, use list_tables() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    if namespace is None:
        namespace = []
    return await self._inner.table_names(
        namespace=namespace, start_after=start_after, limit=limit
    )

            
    

            create_table

  
      `async`
  

¶

create_table(name: str, data: Optional[DATA] = None, schema: Optional[Union[Schema, LanceModel]] = None, mode: Optional[Literal['create', 'overwrite']] = None, exist_ok: Optional[bool] = None, on_bad_vectors: Optional[str] = None, fill_value: Optional[float] = None, storage_options: Optional[Dict[str, str]] = None, storage_options_provider: Optional['StorageOptionsProvider'] = None, *, namespace: Optional[List[str]] = None, embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None, location: Optional[str] = None) -> AsyncTable

    

      
Create an AsyncTable in the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to create the table in.
Empty list represents root namespace.

          
        
        
- 
          `data`
              (`Optional[DATA]`, default:
                  `None`
)
          –
          
            
User must provide at least one of `data` or `schema`.
Acceptable types are:

- 

list-of-dict

- 

pandas.DataFrame

- 

pyarrow.Table or pyarrow.RecordBatch

          
        
        
- 
          `schema`
              (`Optional[Union[Schema, LanceModel]]`, default:
                  `None`
)
          –
          
            
Acceptable types are:

- 

pyarrow.Schema

- 

LanceModel

          
        
        
- 
          `mode`
              (`Optional[Literal['create', 'overwrite']]`, default:
                  `None`
)
          –
          
            
The mode to use when creating the table.
Can be either "create" or "overwrite".
By default, if the table already exists, an exception is raised.
If you want to overwrite the table, use mode="overwrite".

          
        
        
- 
          `exist_ok`
              (`Optional[bool]`, default:
                  `None`
)
          –
          
            
If a table by the same name already exists, then raise an exception
if exist_ok=False. If exist_ok=True, then open the existing table;
it will not add the provided data but will validate against any
schema that's specified.

          
        
        
- 
          `on_bad_vectors`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
What to do if any of the vectors are not the same size or contains NaNs.
One of "error", "drop", "fill".

          
        
        
- 
          `fill_value`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The value to use when filling vectors. Only used if on_bad_vectors="fill".

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. Options already set on the
connection will be inherited by the table, but can be overridden here.
See available options at
https://lancedb.com/docs/storage/

To enable stable row IDs (row IDs remain stable after compaction,
update, delete, and merges), set `new_table_enable_stable_row_ids`
to `"true"` in storage_options when connecting to the database.

          
        
    

Returns:

    
        
- 
              `AsyncTable`
          –
          
            
A reference to the newly created table.

          
        
        
- 
              `!!! note`
          –
          
            
The vector index won't be created by default.
To create the index, call the `create_index` method on the table.

          
        
    

Examples:

    
Can create with list of tuples or dictionaries:

    
>>> import lancedb
>>> async def doctest_example():
...     db = await lancedb.connect_async("./.lancedb")
...     data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
...             {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
...     my_table = await db.create_table("my_table", data)
...     print(await my_table.query().limit(5).to_arrow())
>>> import asyncio
>>> asyncio.run(doctest_example())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
You can also pass a pandas DataFrame:

    
>>> import pandas as pd
>>> data = pd.DataFrame({
...    "vector": [[1.1, 1.2], [0.2, 1.8]],
...    "lat": [45.5, 40.1],
...    "long": [-122.7, -74.1]
... })
>>> async def pandas_example():
...     db = await lancedb.connect_async("./.lancedb")
...     my_table = await db.create_table("table2", data)
...     print(await my_table.query().limit(5).to_arrow())
>>> asyncio.run(pandas_example())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
Data is converted to Arrow before being written to disk. For maximum
control over how data is saved, either provide the PyArrow schema to
convert to or else provide a PyArrow Table directly.

    
>>> import pyarrow as pa
>>> custom_schema = pa.schema([
...   pa.field("vector", pa.list_(pa.float32(), 2)),
...   pa.field("lat", pa.float32()),
...   pa.field("long", pa.float32())
... ])
>>> async def with_schema():
...     db = await lancedb.connect_async("./.lancedb")
...     my_table = await db.create_table("table3", data, schema = custom_schema)
...     print(await my_table.query().limit(5).to_arrow())
>>> asyncio.run(with_schema())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: float
long: float
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]

    
It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

    
>>> import pyarrow as pa
>>> def make_batches():
...     for i in range(5):
...         yield pa.RecordBatch.from_arrays(
...             [
...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
...                     pa.list_(pa.float32(), 2)),
...                 pa.array(["foo", "bar"]),
...                 pa.array([10.0, 20.0]),
...             ],
...             ["vector", "item", "price"],
...         )
>>> schema=pa.schema([
...     pa.field("vector", pa.list_(pa.float32(), 2)),
...     pa.field("item", pa.utf8()),
...     pa.field("price", pa.float32()),
... ])
>>> async def iterable_example():
...     db = await lancedb.connect_async("./.lancedb")
...     await db.create_table("table4", make_batches(), schema=schema)
>>> asyncio.run(iterable_example())

            
              Source code in `lancedb/db.py`
              
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
async def create_table(
    self,
    name: str,
    data: Optional[DATA] = None,
    schema: Optional[Union[pa.Schema, LanceModel]] = None,
    mode: Optional[Literal["create", "overwrite"]] = None,
    exist_ok: Optional[bool] = None,
    on_bad_vectors: Optional[str] = None,
    fill_value: Optional[float] = None,
    storage_options: Optional[Dict[str, str]] = None,
    storage_options_provider: Optional["StorageOptionsProvider"] = None,
    *,
    namespace: Optional[List[str]] = None,
    embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None,
    location: Optional[str] = None,
) -> AsyncTable:
    """Create an [AsyncTable][lancedb.table.AsyncTable] in the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], default []
        The namespace to create the table in.
        Empty list represents root namespace.
    data: The data to initialize the table, *optional*
        User must provide at least one of `data` or `schema`.
        Acceptable types are:

        - list-of-dict

        - pandas.DataFrame

        - pyarrow.Table or pyarrow.RecordBatch
    schema: The schema of the table, *optional*
        Acceptable types are:

        - pyarrow.Schema

        - [LanceModel][lancedb.pydantic.LanceModel]
    mode: Literal["create", "overwrite"]; default "create"
        The mode to use when creating the table.
        Can be either "create" or "overwrite".
        By default, if the table already exists, an exception is raised.
        If you want to overwrite the table, use mode="overwrite".
    exist_ok: bool, default False
        If a table by the same name already exists, then raise an exception
        if exist_ok=False. If exist_ok=True, then open the existing table;
        it will not add the provided data but will validate against any
        schema that's specified.
    on_bad_vectors: str, default "error"
        What to do if any of the vectors are not the same size or contains NaNs.
        One of "error", "drop", "fill".
    fill_value: float
        The value to use when filling vectors. Only used if on_bad_vectors="fill".
    storage_options: dict, optional
        Additional options for the storage backend. Options already set on the
        connection will be inherited by the table, but can be overridden here.
        See available options at
        <https://lancedb.com/docs/storage/>

        To enable stable row IDs (row IDs remain stable after compaction,
        update, delete, and merges), set `new_table_enable_stable_row_ids`
        to `"true"` in storage_options when connecting to the database.

    Returns
    -------
    AsyncTable
        A reference to the newly created table.

    !!! note

        The vector index won't be created by default.
        To create the index, call the `create_index` method on the table.

    Examples
    --------

    Can create with list of tuples or dictionaries:

    >>> import lancedb
    >>> async def doctest_example():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
    ...             {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
    ...     my_table = await db.create_table("my_table", data)
    ...     print(await my_table.query().limit(5).to_arrow())
    >>> import asyncio
    >>> asyncio.run(doctest_example())
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: double
    long: double
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    You can also pass a pandas DataFrame:

    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...    "vector": [[1.1, 1.2], [0.2, 1.8]],
    ...    "lat": [45.5, 40.1],
    ...    "long": [-122.7, -74.1]
    ... })
    >>> async def pandas_example():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     my_table = await db.create_table("table2", data)
    ...     print(await my_table.query().limit(5).to_arrow())
    >>> asyncio.run(pandas_example())
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: double
    long: double
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    Data is converted to Arrow before being written to disk. For maximum
    control over how data is saved, either provide the PyArrow schema to
    convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

    >>> import pyarrow as pa
    >>> custom_schema = pa.schema([
    ...   pa.field("vector", pa.list_(pa.float32(), 2)),
    ...   pa.field("lat", pa.float32()),
    ...   pa.field("long", pa.float32())
    ... ])
    >>> async def with_schema():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     my_table = await db.create_table("table3", data, schema = custom_schema)
    ...     print(await my_table.query().limit(5).to_arrow())
    >>> asyncio.run(with_schema())
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    lat: float
    long: float
    ----
    vector: [[[1.1,1.2],[0.2,1.8]]]
    lat: [[45.5,40.1]]
    long: [[-122.7,-74.1]]

    It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

    >>> import pyarrow as pa
    >>> def make_batches():
    ...     for i in range(5):
    ...         yield pa.RecordBatch.from_arrays(
    ...             [
    ...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
    ...                     pa.list_(pa.float32(), 2)),
    ...                 pa.array(["foo", "bar"]),
    ...                 pa.array([10.0, 20.0]),
    ...             ],
    ...             ["vector", "item", "price"],
    ...         )
    >>> schema=pa.schema([
    ...     pa.field("vector", pa.list_(pa.float32(), 2)),
    ...     pa.field("item", pa.utf8()),
    ...     pa.field("price", pa.float32()),
    ... ])
    >>> async def iterable_example():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     await db.create_table("table4", make_batches(), schema=schema)
    >>> asyncio.run(iterable_example())
    """
    if namespace is None:
        namespace = []
    metadata = None

    if embedding_functions is not None:
        # If we passed in embedding functions explicitly
        # then we'll override any schema metadata that
        # may was implicitly specified by the LanceModel schema
        registry = EmbeddingFunctionRegistry.get_instance()
        metadata = registry.get_table_metadata(embedding_functions)

    # Defining defaults here and not in function prototype.  In the future
    # these defaults will move into rust so better to keep them as None.
    if on_bad_vectors is None:
        on_bad_vectors = "error"

    if fill_value is None:
        fill_value = 0.0

    data, schema = sanitize_create_table(
        data, schema, metadata, on_bad_vectors, fill_value
    )
    validate_schema(schema)

    if exist_ok is None:
        exist_ok = False
    if mode is None:
        mode = "create"
    if mode == "create" and exist_ok:
        mode = "exist_ok"

    if data is None:
        new_table = await self._inner.create_empty_table(
            name,
            mode,
            schema,
            namespace=namespace,
            storage_options=storage_options,
            storage_options_provider=storage_options_provider,
            location=location,
        )
    else:
        data = data_to_reader(data, schema)
        new_table = await self._inner.create_table(
            name,
            mode,
            data,
            namespace=namespace,
            storage_options=storage_options,
            storage_options_provider=storage_options_provider,
            location=location,
        )

    return AsyncTable(new_table)

            
    

            open_table

  
      `async`
  

¶

open_table(name: str, *, namespace: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, storage_options_provider: Optional['StorageOptionsProvider'] = None, index_cache_size: Optional[int] = None, location: Optional[str] = None) -> AsyncTable

    

      
Open a Lance Table in the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to open the table from.
None or empty list represents root namespace.

          
        
        
- 
          `storage_options`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
Additional options for the storage backend. Options already set on the
connection will be inherited by the table, but can be overridden here.
See available options at
https://lancedb.com/docs/storage/

          
        
        
- 
          `index_cache_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
Deprecated: Use session-level cache configuration instead.
Create a Session with custom cache sizes and pass it to lancedb.connect().

Set the size of the index cache, specified as a number of entries

The exact meaning of an "entry" will depend on the type of index:
* IVF - there is one entry for each IVF partition
* BTREE - there is one entry for the entire index

This cache applies to the entire opened table, across all indices.
Setting this value higher will increase performance on larger datasets
at the expense of more RAM

          
        
        
- 
          `location`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The explicit location (URI) of the table. If provided, the table will be
opened from this location instead of deriving it from the database URI
and table name.

          
        
    

Returns:

    
        
- 
              `A LanceTable object representing the table.`
          –
          
            
          
        
    

            
              Source code in `lancedb/db.py`
              
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
async def open_table(
    self,
    name: str,
    *,
    namespace: Optional[List[str]] = None,
    storage_options: Optional[Dict[str, str]] = None,
    storage_options_provider: Optional["StorageOptionsProvider"] = None,
    index_cache_size: Optional[int] = None,
    location: Optional[str] = None,
) -> AsyncTable:
    """Open a Lance Table in the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], optional
        The namespace to open the table from.
        None or empty list represents root namespace.
    storage_options: dict, optional
        Additional options for the storage backend. Options already set on the
        connection will be inherited by the table, but can be overridden here.
        See available options at
        <https://lancedb.com/docs/storage/>
    index_cache_size: int, default 256
        **Deprecated**: Use session-level cache configuration instead.
        Create a Session with custom cache sizes and pass it to lancedb.connect().

        Set the size of the index cache, specified as a number of entries

        The exact meaning of an "entry" will depend on the type of index:
        * IVF - there is one entry for each IVF partition
        * BTREE - there is one entry for the entire index

        This cache applies to the entire opened table, across all indices.
        Setting this value higher will increase performance on larger datasets
        at the expense of more RAM
    location: str, optional
        The explicit location (URI) of the table. If provided, the table will be
        opened from this location instead of deriving it from the database URI
        and table name.

    Returns
    -------
    A LanceTable object representing the table.
    """
    if namespace is None:
        namespace = []
    table = await self._inner.open_table(
        name,
        namespace=namespace,
        storage_options=storage_options,
        storage_options_provider=storage_options_provider,
        index_cache_size=index_cache_size,
        location=location,
    )
    return AsyncTable(table)

            
    

            clone_table

  
      `async`
  

¶

clone_table(target_table_name: str, source_uri: str, *, target_namespace: Optional[List[str]] = None, source_version: Optional[int] = None, source_tag: Optional[str] = None, is_shallow: bool = True) -> AsyncTable

    

      
Clone a table from a source table.

A shallow clone creates a new table that shares the underlying data files
with the source table but has its own independent manifest. This allows
both the source and cloned tables to evolve independently while initially
sharing the same data, deletion, and index files.

Parameters:

    
        
- 
          `target_table_name`
              (`str`)
          –
          
            
The name of the target table to create.

          
        
        
- 
          `source_uri`
              (`str`)
          –
          
            
The URI of the source table to clone from.

          
        
        
- 
          `target_namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace for the target table.
None or empty list represents root namespace.

          
        
        
- 
          `source_version`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The version of the source table to clone.

          
        
        
- 
          `source_tag`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The tag of the source table to clone.

          
        
        
- 
          `is_shallow`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to perform a shallow clone (True) or deep clone (False).
Currently only shallow clone is supported.

          
        
    

Returns:

    
        
- 
              `An AsyncTable object representing the cloned table.`
          –
          
            
          
        
    

            
              Source code in `lancedb/db.py`
              
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
async def clone_table(
    self,
    target_table_name: str,
    source_uri: str,
    *,
    target_namespace: Optional[List[str]] = None,
    source_version: Optional[int] = None,
    source_tag: Optional[str] = None,
    is_shallow: bool = True,
) -> AsyncTable:
    """Clone a table from a source table.

    A shallow clone creates a new table that shares the underlying data files
    with the source table but has its own independent manifest. This allows
    both the source and cloned tables to evolve independently while initially
    sharing the same data, deletion, and index files.

    Parameters
    ----------
    target_table_name: str
        The name of the target table to create.
    source_uri: str
        The URI of the source table to clone from.
    target_namespace: List[str], optional
        The namespace for the target table.
        None or empty list represents root namespace.
    source_version: int, optional
        The version of the source table to clone.
    source_tag: str, optional
        The tag of the source table to clone.
    is_shallow: bool, default True
        Whether to perform a shallow clone (True) or deep clone (False).
        Currently only shallow clone is supported.

    Returns
    -------
    An AsyncTable object representing the cloned table.
    """
    if target_namespace is None:
        target_namespace = []
    table = await self._inner.clone_table(
        target_table_name,
        source_uri,
        target_namespace=target_namespace,
        source_version=source_version,
        source_tag=source_tag,
        is_shallow=is_shallow,
    )
    return AsyncTable(table)

            
    

            rename_table

  
      `async`
  

¶

rename_table(cur_name: str, new_name: str, cur_namespace: Optional[List[str]] = None, new_namespace: Optional[List[str]] = None)

    

      
Rename a table in the database.

Parameters:

    
        
- 
          `cur_name`
              (`str`)
          –
          
            
The current name of the table.

          
        
        
- 
          `new_name`
              (`str`)
          –
          
            
The new name of the table.

          
        
        
- 
          `cur_namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace of the current table.
None or empty list represents root namespace.

          
        
        
- 
          `new_namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to move the table to.
If not specified, defaults to the same as cur_namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
async def rename_table(
    self,
    cur_name: str,
    new_name: str,
    cur_namespace: Optional[List[str]] = None,
    new_namespace: Optional[List[str]] = None,
):
    """Rename a table in the database.

    Parameters
    ----------
    cur_name: str
        The current name of the table.
    new_name: str
        The new name of the table.
    cur_namespace: List[str], optional
        The namespace of the current table.
        None or empty list represents root namespace.
    new_namespace: List[str], optional
        The namespace to move the table to.
        If not specified, defaults to the same as cur_namespace.
    """
    if cur_namespace is None:
        cur_namespace = []
    if new_namespace is None:
        new_namespace = []
    await self._inner.rename_table(
        cur_name, new_name, cur_namespace=cur_namespace, new_namespace=new_namespace
    )

            
    

            drop_table

  
      `async`
  

¶

drop_table(name: str, *, namespace: Optional[List[str]] = None, ignore_missing: bool = False)

    

      
Drop a table from the database.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the table.

          
        
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to drop the table from.
Empty list represents root namespace.

          
        
        
- 
          `ignore_missing`
              (`bool`, default:
                  `False`
)
          –
          
            
If True, ignore if the table does not exist.

          
        
    

            
              Source code in `lancedb/db.py`
              
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
async def drop_table(
    self,
    name: str,
    *,
    namespace: Optional[List[str]] = None,
    ignore_missing: bool = False,
):
    """Drop a table from the database.

    Parameters
    ----------
    name: str
        The name of the table.
    namespace: List[str], default []
        The namespace to drop the table from.
        Empty list represents root namespace.
    ignore_missing: bool, default False
        If True, ignore if the table does not exist.
    """
    if namespace is None:
        namespace = []
    try:
        await self._inner.drop_table(name, namespace=namespace)
    except ValueError as e:
        if not ignore_missing:
            raise e
        if f"Table '{name}' was not found" not in str(e):
            raise e

            
    

            drop_all_tables

  
      `async`
  

¶

drop_all_tables(namespace: Optional[List[str]] = None)

    

      
Drop all tables from the database.

Parameters:

    
        
- 
          `namespace`
              (`Optional[List[str]]`, default:
                  `None`
)
          –
          
            
The namespace to drop all tables from.
None or empty list represents root namespace.

          
        
    

            
              Source code in `lancedb/db.py`
              
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
async def drop_all_tables(self, namespace: Optional[List[str]] = None):
    """Drop all tables from the database.

    Parameters
    ----------
    namespace: List[str], optional
        The namespace to drop all tables from.
        None or empty list represents root namespace.
    """
    if namespace is None:
        namespace = []
    await self._inner.drop_all_tables(namespace=namespace)

            
    

            drop_database

  
      `async`
  

¶

drop_database()

    

      
Drop database
This is the same thing as dropping all the tables

            
              Source code in `lancedb/db.py`
              
1715
1716
1717
1718
1719
1720
1721
1722
1723
1724
1725
1726
@deprecation.deprecated(
    deprecated_in="0.15.1",
    removed_in="0.17",
    current_version=__version__,
    details="Use drop_all_tables() instead",
)
async def drop_database(self):
    """
    Drop database
    This is the same thing as dropping all the tables
    """
    await self._inner.drop_all_tables()

            
    

  

    

## Tables (Asynchronous)¶

Table hold your actual data as a collection of records / rows.

            lancedb.table.AsyncTable

¶

    

      
An AsyncTable is a collection of Records in a LanceDB Database.

An AsyncTable can be obtained from the
AsyncConnection.create_table and
AsyncConnection.open_table methods.

An AsyncTable object is expected to be long lived and reused for multiple
operations. AsyncTable objects will cache a certain amount of index data in memory.
This cache will be freed when the Table is garbage collected.  To eagerly free the
cache you can call the close method.  Once the
AsyncTable is closed, it cannot be used for any further operations.

An AsyncTable can also be used as a context manager, and will automatically close
when the context is exited.  Closing a table is optional.  If you do not close the
table, it will be closed when the AsyncTable object is garbage collected.

Examples:

    
Create using AsyncConnection.create_table
(more examples in that method's documentation).

    
>>> import lancedb
>>> async def create_a_table():
...     db = await lancedb.connect_async("./.lancedb")
...     data = [{"vector": [1.1, 1.2], "b": 2}]
...     table = await db.create_table("my_table", data=data)
...     print(await table.query().limit(5).to_arrow())
>>> import asyncio
>>> asyncio.run(create_a_table())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
b: int64
----
vector: [[[1.1,1.2]]]
b: [[2]]

    
Can append new data with AsyncTable.add().

    
>>> async def add_to_table():
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.open_table("my_table")
...     await table.add([{"vector": [0.5, 1.3], "b": 4}])
>>> asyncio.run(add_to_table())

    
Can query the table with
AsyncTable.vector_search.

    
>>> async def search_table_for_vector():
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.open_table("my_table")
...     results = (
...       await table.vector_search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
...     )
...     print(results)
>>> asyncio.run(search_table_for_vector())
   b      vector  _distance
0  4  [0.5, 1.3]       0.82
1  2  [1.1, 1.2]       1.13

    
Search queries are much faster when an index is created. See
AsyncTable.create_index.

              
                Source code in `lancedb/table.py`
                
3337
3338
3339
3340
3341
3342
3343
3344
3345
3346
3347
3348
3349
3350
3351
3352
3353
3354
3355
3356
3357
3358
3359
3360
3361
3362
3363
3364
3365
3366
3367
3368
3369
3370
3371
3372
3373
3374
3375
3376
3377
3378
3379
3380
3381
3382
3383
3384
3385
3386
3387
3388
3389
3390
3391
3392
3393
3394
3395
3396
3397
3398
3399
3400
3401
3402
3403
3404
3405
3406
3407
3408
3409
3410
3411
3412
3413
3414
3415
3416
3417
3418
3419
3420
3421
3422
3423
3424
3425
3426
3427
3428
3429
3430
3431
3432
3433
3434
3435
3436
3437
3438
3439
3440
3441
3442
3443
3444
3445
3446
3447
3448
3449
3450
3451
3452
3453
3454
3455
3456
3457
3458
3459
3460
3461
3462
3463
3464
3465
3466
3467
3468
3469
3470
3471
3472
3473
3474
3475
3476
3477
3478
3479
3480
3481
3482
3483
3484
3485
3486
3487
3488
3489
3490
3491
3492
3493
3494
3495
3496
3497
3498
3499
3500
3501
3502
3503
3504
3505
3506
3507
3508
3509
3510
3511
3512
3513
3514
3515
3516
3517
3518
3519
3520
3521
3522
3523
3524
3525
3526
3527
3528
3529
3530
3531
3532
3533
3534
3535
3536
3537
3538
3539
3540
3541
3542
3543
3544
3545
3546
3547
3548
3549
3550
3551
3552
3553
3554
3555
3556
3557
3558
3559
3560
3561
3562
3563
3564
3565
3566
3567
3568
3569
3570
3571
3572
3573
3574
3575
3576
3577
3578
3579
3580
3581
3582
3583
3584
3585
3586
3587
3588
3589
3590
3591
3592
3593
3594
3595
3596
3597
3598
3599
3600
3601
3602
3603
3604
3605
3606
3607
3608
3609
3610
3611
3612
3613
3614
3615
3616
3617
3618
3619
3620
3621
3622
3623
3624
3625
3626
3627
3628
3629
3630
3631
3632
3633
3634
3635
3636
3637
3638
3639
3640
3641
3642
3643
3644
3645
3646
3647
3648
3649
3650
3651
3652
3653
3654
3655
3656
3657
3658
3659
3660
3661
3662
3663
3664
3665
3666
3667
3668
3669
3670
3671
3672
3673
3674
3675
3676
3677
3678
3679
3680
3681
3682
3683
3684
3685
3686
3687
3688
3689
3690
3691
3692
3693
3694
3695
3696
3697
3698
3699
3700
3701
3702
3703
3704
3705
3706
3707
3708
3709
3710
3711
3712
3713
3714
3715
3716
3717
3718
3719
3720
3721
3722
3723
3724
3725
3726
3727
3728
3729
3730
3731
3732
3733
3734
3735
3736
3737
3738
3739
3740
3741
3742
3743
3744
3745
3746
3747
3748
3749
3750
3751
3752
3753
3754
3755
3756
3757
3758
3759
3760
3761
3762
3763
3764
3765
3766
3767
3768
3769
3770
3771
3772
3773
3774
3775
3776
3777
3778
3779
3780
3781
3782
3783
3784
3785
3786
3787
3788
3789
3790
3791
3792
3793
3794
3795
3796
3797
3798
3799
3800
3801
3802
3803
3804
3805
3806
3807
3808
3809
3810
3811
3812
3813
3814
3815
3816
3817
3818
3819
3820
3821
3822
3823
3824
3825
3826
3827
3828
3829
3830
3831
3832
3833
3834
3835
3836
3837
3838
3839
3840
3841
3842
3843
3844
3845
3846
3847
3848
3849
3850
3851
3852
3853
3854
3855
3856
3857
3858
3859
3860
3861
3862
3863
3864
3865
3866
3867
3868
3869
3870
3871
3872
3873
3874
3875
3876
3877
3878
3879
3880
3881
3882
3883
3884
3885
3886
3887
3888
3889
3890
3891
3892
3893
3894
3895
3896
3897
3898
3899
3900
3901
3902
3903
3904
3905
3906
3907
3908
3909
3910
3911
3912
3913
3914
3915
3916
3917
3918
3919
3920
3921
3922
3923
3924
3925
3926
3927
3928
3929
3930
3931
3932
3933
3934
3935
3936
3937
3938
3939
3940
3941
3942
3943
3944
3945
3946
3947
3948
3949
3950
3951
3952
3953
3954
3955
3956
3957
3958
3959
3960
3961
3962
3963
3964
3965
3966
3967
3968
3969
3970
3971
3972
3973
3974
3975
3976
3977
3978
3979
3980
3981
3982
3983
3984
3985
3986
3987
3988
3989
3990
3991
3992
3993
3994
3995
3996
3997
3998
3999
4000
4001
4002
4003
4004
4005
4006
4007
4008
4009
4010
4011
4012
4013
4014
4015
4016
4017
4018
4019
4020
4021
4022
4023
4024
4025
4026
4027
4028
4029
4030
4031
4032
4033
4034
4035
4036
4037
4038
4039
4040
4041
4042
4043
4044
4045
4046
4047
4048
4049
4050
4051
4052
4053
4054
4055
4056
4057
4058
4059
4060
4061
4062
4063
4064
4065
4066
4067
4068
4069
4070
4071
4072
4073
4074
4075
4076
4077
4078
4079
4080
4081
4082
4083
4084
4085
4086
4087
4088
4089
4090
4091
4092
4093
4094
4095
4096
4097
4098
4099
4100
4101
4102
4103
4104
4105
4106
4107
4108
4109
4110
4111
4112
4113
4114
4115
4116
4117
4118
4119
4120
4121
4122
4123
4124
4125
4126
4127
4128
4129
4130
4131
4132
4133
4134
4135
4136
4137
4138
4139
4140
4141
4142
4143
4144
4145
4146
4147
4148
4149
4150
4151
4152
4153
4154
4155
4156
4157
4158
4159
4160
4161
4162
4163
4164
4165
4166
4167
4168
4169
4170
4171
4172
4173
4174
4175
4176
4177
4178
4179
4180
4181
4182
4183
4184
4185
4186
4187
4188
4189
4190
4191
4192
4193
4194
4195
4196
4197
4198
4199
4200
4201
4202
4203
4204
4205
4206
4207
4208
4209
4210
4211
4212
4213
4214
4215
4216
4217
4218
4219
4220
4221
4222
4223
4224
4225
4226
4227
4228
4229
4230
4231
4232
4233
4234
4235
4236
4237
4238
4239
4240
4241
4242
4243
4244
4245
4246
4247
4248
4249
4250
4251
4252
4253
4254
4255
4256
4257
4258
4259
4260
4261
4262
4263
4264
4265
4266
4267
4268
4269
4270
4271
4272
4273
4274
4275
4276
4277
4278
4279
4280
4281
4282
4283
4284
4285
4286
4287
4288
4289
4290
4291
4292
4293
4294
4295
4296
4297
4298
4299
4300
4301
4302
4303
4304
4305
4306
4307
4308
4309
4310
4311
4312
4313
4314
4315
4316
4317
4318
4319
4320
4321
4322
4323
4324
4325
4326
4327
4328
4329
4330
4331
4332
4333
4334
4335
4336
4337
4338
4339
4340
4341
4342
4343
4344
4345
4346
4347
4348
4349
4350
4351
4352
4353
4354
4355
4356
4357
4358
4359
4360
4361
4362
4363
4364
4365
4366
4367
4368
4369
4370
4371
4372
4373
4374
4375
4376
4377
4378
4379
4380
4381
4382
4383
4384
4385
4386
4387
4388
4389
4390
4391
4392
4393
4394
4395
4396
4397
4398
4399
4400
4401
4402
4403
4404
4405
4406
4407
4408
4409
4410
4411
4412
4413
4414
4415
4416
4417
4418
4419
4420
4421
4422
4423
4424
4425
4426
4427
4428
4429
4430
4431
4432
4433
4434
4435
4436
4437
4438
4439
4440
4441
4442
4443
4444
4445
4446
4447
4448
4449
4450
4451
4452
4453
4454
4455
4456
4457
4458
4459
4460
4461
4462
4463
4464
4465
4466
4467
4468
4469
4470
4471
4472
4473
4474
4475
4476
4477
4478
4479
4480
4481
4482
4483
4484
4485
4486
4487
4488
4489
4490
4491
4492
4493
4494
4495
4496
4497
4498
4499
4500
4501
4502
4503
4504
4505
4506
4507
4508
4509
4510
4511
4512
4513
4514
4515
4516
4517
4518
4519
4520
4521
4522
4523
4524
4525
4526
4527
4528
4529
4530
4531
4532
4533
4534
4535
4536
4537
4538
4539
4540
4541
4542
4543
4544
4545
4546
4547
4548
4549
4550
4551
4552
4553
4554
4555
4556
4557
4558
4559
4560
4561
4562
4563
4564
4565
4566
4567
4568
4569
4570
4571
4572
4573
4574
4575
4576
4577
4578
4579
4580
4581
4582
4583
4584
4585
4586
4587
4588
4589
4590
4591
4592
4593
4594
4595
4596
4597
4598
4599
4600
4601
4602
4603
4604
4605
4606
4607
4608
4609
4610
4611
4612
4613
4614
4615
4616
4617
4618
4619
4620
4621
4622
4623
4624
4625
4626
4627
4628
4629
4630
4631
4632
4633
4634
4635
4636
4637
4638
4639
4640
4641
4642
4643
4644
4645
4646
4647
4648
4649
class AsyncTable:
    """
    An AsyncTable is a collection of Records in a LanceDB Database.

    An AsyncTable can be obtained from the
    [AsyncConnection.create_table][lancedb.AsyncConnection.create_table] and
    [AsyncConnection.open_table][lancedb.AsyncConnection.open_table] methods.

    An AsyncTable object is expected to be long lived and reused for multiple
    operations. AsyncTable objects will cache a certain amount of index data in memory.
    This cache will be freed when the Table is garbage collected.  To eagerly free the
    cache you can call the [close][lancedb.AsyncTable.close] method.  Once the
    AsyncTable is closed, it cannot be used for any further operations.

    An AsyncTable can also be used as a context manager, and will automatically close
    when the context is exited.  Closing a table is optional.  If you do not close the
    table, it will be closed when the AsyncTable object is garbage collected.

    Examples
    --------

    Create using [AsyncConnection.create_table][lancedb.AsyncConnection.create_table]
    (more examples in that method's documentation).

    >>> import lancedb
    >>> async def create_a_table():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     data = [{"vector": [1.1, 1.2], "b": 2}]
    ...     table = await db.create_table("my_table", data=data)
    ...     print(await table.query().limit(5).to_arrow())
    >>> import asyncio
    >>> asyncio.run(create_a_table())
    pyarrow.Table
    vector: fixed_size_list<item: float>[2]
      child 0, item: float
    b: int64
    ----
    vector: [[[1.1,1.2]]]
    b: [[2]]

    Can append new data with [AsyncTable.add()][lancedb.table.AsyncTable.add].

    >>> async def add_to_table():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     table = await db.open_table("my_table")
    ...     await table.add([{"vector": [0.5, 1.3], "b": 4}])
    >>> asyncio.run(add_to_table())

    Can query the table with
    [AsyncTable.vector_search][lancedb.table.AsyncTable.vector_search].

    >>> async def search_table_for_vector():
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     table = await db.open_table("my_table")
    ...     results = (
    ...       await table.vector_search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
    ...     )
    ...     print(results)
    >>> asyncio.run(search_table_for_vector())
       b      vector  _distance
    0  4  [0.5, 1.3]       0.82
    1  2  [1.1, 1.2]       1.13

    Search queries are much faster when an index is created. See
    [AsyncTable.create_index][lancedb.table.AsyncTable.create_index].
    """

    def __init__(self, table: LanceDBTable):
        """Create a new AsyncTable object.

        You should not create AsyncTable objects directly.

        Use [AsyncConnection.create_table][lancedb.AsyncConnection.create_table] and
        [AsyncConnection.open_table][lancedb.AsyncConnection.open_table] to obtain
        Table objects."""
        self._inner = table

    def __repr__(self):
        return self._inner.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def is_open(self) -> bool:
        """Return True if the table is open."""
        return self._inner.is_open()

    def close(self):
        """Close the table and free any resources associated with it.

        It is safe to call this method multiple times.

        Any attempt to use the table after it has been closed will raise an error."""
        return self._inner.close()

    @property
    def name(self) -> str:
        """The name of the table."""
        return self._inner.name()

    async def schema(self) -> pa.Schema:
        """The [Arrow Schema](https://arrow.apache.org/docs/python/api/datatypes.html#)
        of this Table

        """
        return await self._inner.schema()

    async def embedding_functions(self) -> Dict[str, EmbeddingFunctionConfig]:
        """
        Get the embedding functions for the table

        Returns
        -------
        funcs: Dict[str, EmbeddingFunctionConfig]
            A mapping of the vector column to the embedding function
            or empty dict if not configured.
        """
        schema = await self.schema()
        return EmbeddingFunctionRegistry.get_instance().parse_functions(schema.metadata)

    async def count_rows(self, filter: Optional[str] = None) -> int:
        """
        Count the number of rows in the table.

        Parameters
        ----------
        filter: str, optional
            A SQL where clause to filter the rows to count.
        """
        return await self._inner.count_rows(filter)

    async def head(self, n=5) -> pa.Table:
        """
        Return the first `n` rows of the table.

        Parameters
        ----------
        n: int, default 5
            The number of rows to return.
        """
        return await self.query().limit(n).to_arrow()

    def query(self) -> AsyncQuery:
        """
        Returns an [AsyncQuery][lancedb.query.AsyncQuery] that can be used
        to search the table.

        Use methods on the returned query to control query behavior.  The query
        can be executed with methods like [to_arrow][lancedb.query.AsyncQuery.to_arrow],
        [to_pandas][lancedb.query.AsyncQuery.to_pandas] and more.
        """
        return AsyncQuery(self._inner.query())

    async def to_pandas(self) -> "pd.DataFrame":
        """Return the table as a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
        """
        return (await self.to_arrow()).to_pandas()

    async def to_arrow(self) -> pa.Table:
        """Return the table as a pyarrow Table.

        Returns
        -------
        pa.Table
        """
        return await self.query().to_arrow()

    async def create_index(
        self,
        column: str,
        *,
        replace: Optional[bool] = None,
        config: Optional[
            Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]
        ] = None,
        wait_timeout: Optional[timedelta] = None,
        name: Optional[str] = None,
        train: bool = True,
    ):
        """Create an index to speed up queries

        Indices can be created on vector columns or scalar columns.
        Indices on vector columns will speed up vector searches.
        Indices on scalar columns will speed up filtering (in both
        vector and non-vector searches)

        Parameters
        ----------
        column: str
            The column to index.
        replace: bool, default True
            Whether to replace the existing index

            If this is false, and another index already exists on the same columns
            and the same name, then an error will be returned.  This is true even if
            that index is out of date.

            The default is True
        config: default None
            For advanced configuration you can specify the type of index you would
            like to create.   You can also specify index-specific parameters when
            creating an index object.
        wait_timeout: timedelta, optional
            The timeout to wait if indexing is asynchronous.
        name: str, optional
            The name of the index. If not provided, a default name will be generated.
        train: bool, default True
            Whether to train the index with existing data. Vector indices always train
            with existing data.
        """
        if config is not None:
            if not isinstance(
                config,
                (
                    IvfFlat,
                    IvfSq,
                    IvfPq,
                    IvfRq,
                    HnswPq,
                    HnswSq,
                    BTree,
                    Bitmap,
                    LabelList,
                    FTS,
                ),
            ):
                raise TypeError(
                    "config must be an instance of IvfSq, IvfPq, IvfRq, HnswPq, HnswSq,"
                    " BTree, Bitmap, LabelList, or FTS, but got " + str(type(config))
                )
        try:
            await self._inner.create_index(
                column,
                index=config,
                replace=replace,
                wait_timeout=wait_timeout,
                name=name,
                train=train,
            )
        except ValueError as e:
            if "not support the requested language" in str(e):
                supported_langs = ", ".join(lang_mapping.values())
                help_msg = f"Supported languages: {supported_langs}"
                add_note(e, help_msg)
            raise e

    async def drop_index(self, name: str) -> None:
        """
        Drop an index from the table.

        Parameters
        ----------
        name: str
            The name of the index to drop.

        Notes
        -----
        This does not delete the index from disk, it just removes it from the table.
        To delete the index, run [optimize][lancedb.table.AsyncTable.optimize]
        after dropping the index.

        Use [list_indices][lancedb.table.AsyncTable.list_indices] to find the names
        of the indices.
        """
        await self._inner.drop_index(name)

    async def prewarm_index(self, name: str) -> None:
        """
        Prewarm an index in the table.

        Parameters
        ----------
        name: str
            The name of the index to prewarm

        Notes
        -----
        This will load the index into memory.  This may reduce the cold-start time for
        future queries.  If the index does not fit in the cache then this call may be
        wasteful.
        """
        await self._inner.prewarm_index(name)

    async def wait_for_index(
        self, index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)
    ) -> None:
        """
        Wait for indexing to complete for the given index names.
        This will poll the table until all the indices are fully indexed,
        or raise a timeout exception if the timeout is reached.

        Parameters
        ----------
        index_names: str
            The name of the indices to poll
        timeout: timedelta
            Timeout to wait for asynchronous indexing. The default is 5 minutes.
        """
        await self._inner.wait_for_index(index_names, timeout)

    async def stats(self) -> TableStatistics:
        """
        Retrieve table and fragment statistics.
        """
        return await self._inner.stats()

    async def uri(self) -> str:
        """
        Get the table URI (storage location).

        For remote tables, this fetches the location from the server via describe.
        For local tables, this returns the dataset URI.

        Returns
        -------
        str
            The full storage location of the table (e.g., S3/GCS path).
        """
        return await self._inner.uri()

    async def initial_storage_options(self) -> Optional[Dict[str, str]]:
        """Get the initial storage options that were passed in when opening this table.

        For dynamically refreshed options (e.g., credential vending), use
        :meth:`latest_storage_options`.

        Warning: This is an internal API and the return value is subject to change.

        Returns
        -------
        Optional[Dict[str, str]]
            The storage options, or None if no storage options were configured.
        """
        return await self._inner.initial_storage_options()

    async def latest_storage_options(self) -> Optional[Dict[str, str]]:
        """Get the latest storage options, refreshing from provider if configured.

        This method is useful for credential vending scenarios where storage options
        may be refreshed dynamically. If no dynamic provider is configured, this
        returns the initial static options.

        Warning: This is an internal API and the return value is subject to change.

        Returns
        -------
        Optional[Dict[str, str]]
            The storage options, or None if no storage options were configured.
        """
        return await self._inner.latest_storage_options()

    async def add(
        self,
        data: DATA,
        *,
        mode: Optional[Literal["append", "overwrite"]] = "append",
        on_bad_vectors: Optional[OnBadVectorsType] = None,
        fill_value: Optional[float] = None,
    ) -> AddResult:
        """Add more data to the [Table](Table).

        Parameters
        ----------
        data: DATA
            The data to insert into the table. Acceptable types are:

            - list-of-dict

            - pandas.DataFrame

            - pyarrow.Table or pyarrow.RecordBatch
        mode: str
            The mode to use when writing the data. Valid values are
            "append" and "overwrite".
        on_bad_vectors: str, default "error"
            What to do if any of the vectors are not the same size or contains NaNs.
            One of "error", "drop", "fill", "null".
        fill_value: float, default 0.
            The value to use when filling vectors. Only used if on_bad_vectors="fill".

        """
        schema = await self.schema()
        if on_bad_vectors is None:
            on_bad_vectors = "error"
        if fill_value is None:
            fill_value = 0.0
        data = _sanitize_data(
            data,
            schema,
            metadata=schema.metadata,
            on_bad_vectors=on_bad_vectors,
            fill_value=fill_value,
            allow_subschema=True,
        )
        if isinstance(data, pa.Table):
            data = data.to_reader()

        return await self._inner.add(data, mode or "append")

    def merge_insert(self, on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder:
        """
        Returns a [`LanceMergeInsertBuilder`][lancedb.merge.LanceMergeInsertBuilder]
        that can be used to create a "merge insert" operation

        This operation can add rows, update rows, and remove rows all in a single
        transaction. It is a very generic tool that can be used to create
        behaviors like "insert if not exists", "update or insert (i.e. upsert)",
        or even replace a portion of existing data with new data (e.g. replace
        all data where month="january")

        The merge insert operation works by combining new data from a
        **source table** with existing data in a **target table** by using a
        join.  There are three categories of records.

        "Matched" records are records that exist in both the source table and
        the target table. "Not matched" records exist only in the source table
        (e.g. these are new data) "Not matched by source" records exist only
        in the target table (this is old data)

        The builder returned by this method can be used to customize what
        should happen for each category of data.

        Please note that the data may appear to be reordered as part of this
        operation.  This is because updated rows will be deleted from the
        dataset and then reinserted at the end with the new values.

        Parameters
        ----------

        on: Union[str, Iterable[str]]
            A column (or columns) to join on.  This is how records from the
            source table and target table are matched.  Typically this is some
            kind of key or id column.

        Examples
        --------
        >>> import lancedb
        >>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", data)
        >>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
        >>> # Perform a "upsert" operation
        >>> res = table.merge_insert("a")     \\
        ...      .when_matched_update_all()     \\
        ...      .when_not_matched_insert_all() \\
        ...      .execute(new_data)
        >>> res
        MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
        >>> # The order of new rows is non-deterministic since we use
        >>> # a hash-join as part of this operation and so we sort here
        >>> table.to_arrow().sort_by("a").to_pandas()
           a  b
        0  1  b
        1  2  x
        2  3  y
        3  4  z
        """  # noqa: E501
        on = [on] if isinstance(on, str) else list(iter(on))

        return LanceMergeInsertBuilder(self, on)

    @overload
    async def search(
        self,
        query: Optional[str] = None,
        vector_column_name: Optional[str] = None,
        query_type: Literal["auto"] = ...,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> Union[AsyncHybridQuery, AsyncFTSQuery, AsyncVectorQuery]: ...

    @overload
    async def search(
        self,
        query: Optional[str] = None,
        vector_column_name: Optional[str] = None,
        query_type: Literal["hybrid"] = ...,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> AsyncHybridQuery: ...

    @overload
    async def search(
        self,
        query: Optional[Union[VEC, "PIL.Image.Image", Tuple]] = None,
        vector_column_name: Optional[str] = None,
        query_type: Literal["auto"] = ...,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> AsyncVectorQuery: ...

    @overload
    async def search(
        self,
        query: Optional[str] = None,
        vector_column_name: Optional[str] = None,
        query_type: Literal["fts"] = ...,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> AsyncFTSQuery: ...

    @overload
    async def search(
        self,
        query: Optional[
            Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]
        ] = None,
        vector_column_name: Optional[str] = None,
        query_type: Literal["vector"] = ...,
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> AsyncVectorQuery: ...

    async def search(
        self,
        query: Optional[
            Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]
        ] = None,
        vector_column_name: Optional[str] = None,
        query_type: QueryType = "auto",
        ordering_field_name: Optional[str] = None,
        fts_columns: Optional[Union[str, List[str]]] = None,
    ) -> Union[AsyncHybridQuery, AsyncFTSQuery, AsyncVectorQuery]:
        """Create a search query to find the nearest neighbors
        of the given query vector. We currently support [vector search][search]
        and [full-text search][experimental-full-text-search].

        All query options are defined in [AsyncQuery][lancedb.query.AsyncQuery].

        Parameters
        ----------
        query: list/np.ndarray/str/PIL.Image.Image, default None
            The targetted vector to search for.

            - *default None*.
            Acceptable types are: list, np.ndarray, PIL.Image.Image

            - If None then the select/where/limit clauses are applied to filter
            the table
        vector_column_name: str, optional
            The name of the vector column to search.

            The vector column needs to be a pyarrow fixed size list type

            - If not specified then the vector column is inferred from
            the table schema

            - If the table has multiple vector columns then the *vector_column_name*
            needs to be specified. Otherwise, an error is raised.
        query_type: str
            *default "auto"*.
            Acceptable types are: "vector", "fts", "hybrid", or "auto"

            - If "auto" then the query type is inferred from the query;

                - If `query` is a list/np.ndarray then the query type is
                "vector";

                - If `query` is a PIL.Image.Image then either do vector search,
                or raise an error if no corresponding embedding function is found.

            - If `query` is a string, then the query type is "vector" if the
              table has embedding functions else the query type is "fts"

        Returns
        -------
        LanceQueryBuilder
            A query builder object representing the query.
        """

        def is_embedding(query):
            return isinstance(query, (list, np.ndarray, pa.Array, pa.ChunkedArray))

        async def get_embedding_func(
            vector_column_name: Optional[str],
            query_type: QueryType,
            query: Optional[Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]],
        ) -> Tuple[str, EmbeddingFunctionConfig]:
            if isinstance(query, FullTextQuery):
                query_type = "fts"
            schema = await self.schema()
            vector_column_name = infer_vector_column_name(
                schema=schema,
                query_type=query_type,
                query=query,
                vector_column_name=vector_column_name,
            )
            funcs = EmbeddingFunctionRegistry.get_instance().parse_functions(
                schema.metadata
            )
            func = funcs.get(vector_column_name)
            if func is None:
                error = ValueError(
                    f"Column '{vector_column_name}' has no registered "
                    "embedding function."
                )
                if len(funcs) > 0:
                    add_note(
                        error,
                        "Embedding functions are registered for columns: "
                        f"{list(funcs.keys())}",
                    )
                else:
                    add_note(
                        error, "No embedding functions are registered for any columns."
                    )
                raise error
            return vector_column_name, func

        async def make_embedding(embedding, query):
            if embedding is not None:
                loop = asyncio.get_running_loop()
                # This function is likely to block, since it either calls an expensive
                # function or makes an HTTP request to an embeddings REST API.
                return (
                    await loop.run_in_executor(
                        None,
                        embedding.function.compute_query_embeddings_with_retry,
                        query,
                    )
                )[0]
            else:
                return None

        if query_type == "auto":
            # Infer the query type.
            if is_embedding(query):
                vector_query = query
                query_type = "vector"
            elif isinstance(query, FullTextQuery):
                query_type = "fts"
            elif isinstance(query, str):
                try:
                    (
                        indices,
                        (vector_column_name, embedding_conf),
                    ) = await asyncio.gather(
                        self.list_indices(),
                        get_embedding_func(vector_column_name, "auto", query),
                    )
                except ValueError as e:
                    if "Column" in str(
                        e
                    ) and "has no registered embedding function" in str(e):
                        # If the column has no registered embedding function,
                        # then it's an FTS query.
                        query_type = "fts"
                    else:
                        raise e
                else:
                    if embedding_conf is not None:
                        vector_query = await make_embedding(embedding_conf, query)
                        if any(
                            i.columns[0] == embedding_conf.source_column
                            and i.index_type == "FTS"
                            for i in indices
                        ):
                            query_type = "hybrid"
                        else:
                            query_type = "vector"
                    else:
                        query_type = "fts"
            else:
                # it's an image or something else embeddable.
                query_type = "vector"
        elif query_type == "vector":
            if is_embedding(query):
                vector_query = query
            else:
                vector_column_name, embedding_conf = await get_embedding_func(
                    vector_column_name, query_type, query
                )
                vector_query = await make_embedding(embedding_conf, query)
        elif query_type == "hybrid":
            if is_embedding(query):
                raise ValueError("Hybrid search requires a text query")
            else:
                vector_column_name, embedding_conf = await get_embedding_func(
                    vector_column_name, query_type, query
                )
                vector_query = await make_embedding(embedding_conf, query)

        if query_type == "vector":
            builder = self.query().nearest_to(vector_query)
            if vector_column_name:
                builder = builder.column(vector_column_name)
            return builder
        elif query_type == "fts":
            return self.query().nearest_to_text(query, columns=fts_columns)
        elif query_type == "hybrid":
            builder = self.query().nearest_to(vector_query)
            if vector_column_name:
                builder = builder.column(vector_column_name)
            return builder.nearest_to_text(query, columns=fts_columns)
        else:
            raise ValueError(f"Unknown query type: '{query_type}'")

    def vector_search(
        self,
        query_vector: Union[VEC, Tuple],
    ) -> AsyncVectorQuery:
        """
        Search the table with a given query vector.
        This is a convenience method for preparing a vector query and
        is the same thing as calling `nearestTo` on the builder returned
        by `query`.  Seer [nearest_to][lancedb.query.AsyncQuery.nearest_to] for more
        details.
        """
        return self.query().nearest_to(query_vector)

    def _sync_query_to_async(
        self, query: Query
    ) -> AsyncHybridQuery | AsyncFTSQuery | AsyncVectorQuery | AsyncQuery:
        async_query = self.query()
        if query.limit is not None:
            async_query = async_query.limit(query.limit)
        if query.offset is not None:
            async_query = async_query.offset(query.offset)
        if query.columns:
            async_query = async_query.select(query.columns)
        if query.filter:
            async_query = async_query.where(query.filter)
        if query.fast_search:
            async_query = async_query.fast_search()
        if query.with_row_id:
            async_query = async_query.with_row_id()

        if query.vector:
            async_query = async_query.nearest_to(query.vector).distance_range(
                query.lower_bound, query.upper_bound
            )
            if query.distance_type is not None:
                async_query = async_query.distance_type(query.distance_type)
            if query.minimum_nprobes is not None and query.maximum_nprobes is not None:
                # Set both to the minimum first to avoid min > max error.
                async_query = async_query.nprobes(
                    query.minimum_nprobes
                ).maximum_nprobes(query.maximum_nprobes)
            elif query.minimum_nprobes is not None:
                async_query = async_query.minimum_nprobes(query.minimum_nprobes)
            elif query.maximum_nprobes is not None:
                async_query = async_query.maximum_nprobes(query.maximum_nprobes)
            if query.refine_factor is not None:
                async_query = async_query.refine_factor(query.refine_factor)
            if query.vector_column:
                async_query = async_query.column(query.vector_column)
            if query.ef:
                async_query = async_query.ef(query.ef)
            if query.bypass_vector_index:
                async_query = async_query.bypass_vector_index()

        if query.postfilter:
            async_query = async_query.postfilter()

        if query.full_text_query:
            async_query = async_query.nearest_to_text(
                query.full_text_query.query, query.full_text_query.columns
            )

        return async_query

    async def _execute_query(
        self,
        query: Query,
        *,
        batch_size: Optional[int] = None,
        timeout: Optional[timedelta] = None,
    ) -> pa.RecordBatchReader:
        # The sync table calls into this method, so we need to map the
        # query to the async version of the query and run that here. This is only
        # used for that code path right now.

        async_query = self._sync_query_to_async(query)

        return await async_query.to_batches(
            max_batch_length=batch_size, timeout=timeout
        )

    async def _explain_plan(self, query: Query, verbose: Optional[bool]) -> str:
        # This method is used by the sync table
        async_query = self._sync_query_to_async(query)
        return await async_query.explain_plan(verbose)

    async def _analyze_plan(self, query: Query) -> str:
        # This method is used by the sync table
        async_query = self._sync_query_to_async(query)
        return await async_query.analyze_plan()

    async def _output_schema(self, query: Query) -> pa.Schema:
        async_query = self._sync_query_to_async(query)
        return await async_query.output_schema()

    async def _do_merge(
        self,
        merge: LanceMergeInsertBuilder,
        new_data: DATA,
        on_bad_vectors: OnBadVectorsType,
        fill_value: float,
    ) -> MergeResult:
        schema = await self.schema()
        if on_bad_vectors is None:
            on_bad_vectors = "error"
        if fill_value is None:
            fill_value = 0.0
        data = _sanitize_data(
            new_data,
            schema,
            metadata=schema.metadata,
            on_bad_vectors=on_bad_vectors,
            fill_value=fill_value,
            allow_subschema=True,
        )
        if isinstance(data, pa.Table):
            data = pa.RecordBatchReader.from_batches(data.schema, data.to_batches())
        return await self._inner.execute_merge_insert(
            data,
            dict(
                on=merge._on,
                when_matched_update_all=merge._when_matched_update_all,
                when_matched_update_all_condition=merge._when_matched_update_all_condition,
                when_not_matched_insert_all=merge._when_not_matched_insert_all,
                when_not_matched_by_source_delete=merge._when_not_matched_by_source_delete,
                when_not_matched_by_source_condition=merge._when_not_matched_by_source_condition,
                timeout=merge._timeout,
                use_index=merge._use_index,
            ),
        )

    async def delete(self, where: str) -> DeleteResult:
        """Delete rows from the table.

        This can be used to delete a single row, many rows, all rows, or
        sometimes no rows (if your predicate matches nothing).

        Parameters
        ----------
        where: str
            The SQL where clause to use when deleting rows.

            - For example, 'x = 2' or 'x IN (1, 2, 3)'.

            The filter must not be empty, or it will error.

        Examples
        --------
        >>> import lancedb
        >>> data = [
        ...    {"x": 1, "vector": [1.0, 2]},
        ...    {"x": 2, "vector": [3.0, 4]},
        ...    {"x": 3, "vector": [5.0, 6]}
        ... ]
        >>> db = lancedb.connect("./.lancedb")
        >>> table = db.create_table("my_table", data)
        >>> table.to_pandas()
           x      vector
        0  1  [1.0, 2.0]
        1  2  [3.0, 4.0]
        2  3  [5.0, 6.0]
        >>> table.delete("x = 2")
        DeleteResult(version=2)
        >>> table.to_pandas()
           x      vector
        0  1  [1.0, 2.0]
        1  3  [5.0, 6.0]

        If you have a list of values to delete, you can combine them into a
        stringified list and use the `IN` operator:

        >>> to_remove = [1, 5]
        >>> to_remove = ", ".join([str(v) for v in to_remove])
        >>> to_remove
        '1, 5'
        >>> table.delete(f"x IN ({to_remove})")
        DeleteResult(version=3)
        >>> table.to_pandas()
           x      vector
        0  3  [5.0, 6.0]
        """
        return await self._inner.delete(where)

    async def update(
        self,
        updates: Optional[Dict[str, Any]] = None,
        *,
        where: Optional[str] = None,
        updates_sql: Optional[Dict[str, str]] = None,
    ) -> UpdateResult:
        """
        This can be used to update zero to all rows in the table.

        If a filter is provided with `where` then only rows matching the
        filter will be updated.  Otherwise all rows will be updated.

        Parameters
        ----------
        updates: dict, optional
            The updates to apply.  The keys should be the name of the column to
            update.  The values should be the new values to assign.  This is
            required unless updates_sql is supplied.
        where: str, optional
            An SQL filter that controls which rows are updated. For example, 'x = 2'
            or 'x IN (1, 2, 3)'.  Only rows that satisfy this filter will be udpated.
        updates_sql: dict, optional
            The updates to apply, expressed as SQL expression strings.  The keys should
            be column names. The values should be SQL expressions.  These can be SQL
            literals (e.g. "7" or "'foo'") or they can be expressions based on the
            previous value of the row (e.g. "x + 1" to increment the x column by 1)

        Returns
        -------
        UpdateResult
            An object containing:
            - rows_updated: The number of rows that were updated
            - version: The new version number of the table after the update

        Examples
        --------
        >>> import asyncio
        >>> import lancedb
        >>> import pandas as pd
        >>> async def demo_update():
        ...     data = pd.DataFrame({"x": [1, 2], "vector": [[1, 2], [3, 4]]})
        ...     db = await lancedb.connect_async("./.lancedb")
        ...     table = await db.create_table("my_table", data)
        ...     # x is [1, 2], vector is [[1, 2], [3, 4]]
        ...     await table.update({"vector": [10, 10]}, where="x = 2")
        ...     # x is [1, 2], vector is [[1, 2], [10, 10]]
        ...     await table.update(updates_sql={"x": "x + 1"})
        ...     # x is [2, 3], vector is [[1, 2], [10, 10]]
        >>> asyncio.run(demo_update())
        """
        if updates is not None and updates_sql is not None:
            raise ValueError("Only one of updates or updates_sql can be provided")
        if updates is None and updates_sql is None:
            raise ValueError("Either updates or updates_sql must be provided")

        if updates is not None:
            updates_sql = {k: value_to_sql(v) for k, v in updates.items()}

        return await self._inner.update(updates_sql, where)

    async def add_columns(
        self, transforms: dict[str, str] | pa.field | List[pa.field] | pa.Schema
    ) -> AddColumnsResult:
        """
        Add new columns with defined values.

        Parameters
        ----------
        transforms: Dict[str, str]
            A map of column name to a SQL expression to use to calculate the
            value of the new column. These expressions will be evaluated for
            each row in the table, and can reference existing columns.
            Alternatively, you can pass a pyarrow field or schema to add
            new columns with NULLs.

        Returns
        -------
        AddColumnsResult
            version: the new version number of the table after adding columns.

        """
        if isinstance(transforms, pa.Field):
            transforms = [transforms]
        if isinstance(transforms, list) and all(
            {isinstance(f, pa.Field) for f in transforms}
        ):
            transforms = pa.schema(transforms)
        if isinstance(transforms, pa.Schema):
            return await self._inner.add_columns_with_schema(transforms)
        else:
            return await self._inner.add_columns(list(transforms.items()))

    async def alter_columns(
        self, *alterations: Iterable[dict[str, Any]]
    ) -> AlterColumnsResult:
        """
        Alter column names and nullability.

        alterations : Iterable[Dict[str, Any]]
            A sequence of dictionaries, each with the following keys:
            - "path": str
                The column path to alter. For a top-level column, this is the name.
                For a nested column, this is the dot-separated path, e.g. "a.b.c".
            - "rename": str, optional
                The new name of the column. If not specified, the column name is
                not changed.
            - "data_type": pyarrow.DataType, optional
               The new data type of the column. Existing values will be casted
               to this type. If not specified, the column data type is not changed.
            - "nullable": bool, optional
                Whether the column should be nullable. If not specified, the column
                nullability is not changed. Only non-nullable columns can be changed
                to nullable. Currently, you cannot change a nullable column to
                non-nullable.

        Returns
        -------
        AlterColumnsResult
            version: the new version number of the table after the alteration.
        """
        return await self._inner.alter_columns(alterations)

    async def drop_columns(self, columns: Iterable[str]):
        """
        Drop columns from the table.

        Parameters
        ----------
        columns : Iterable[str]
            The names of the columns to drop.
        """
        return await self._inner.drop_columns(columns)

    async def version(self) -> int:
        """
        Retrieve the version of the table

        LanceDb supports versioning.  Every operation that modifies the table increases
        version.  As long as a version hasn't been deleted you can `[Self::checkout]`
        that version to view the data at that point.  In addition, you can
        `[Self::restore]` the version to replace the current table with a previous
        version.
        """
        return await self._inner.version()

    async def list_versions(self):
        """
        List all versions of the table
        """
        versions = await self._inner.list_versions()
        for v in versions:
            ts_nanos = v["timestamp"]
            v["timestamp"] = datetime.fromtimestamp(ts_nanos // 1e9) + timedelta(
                microseconds=(ts_nanos % 1e9) // 1e3
            )

        return versions

    async def checkout(self, version: int | str):
        """
        Checks out a specific version of the Table

        Any read operation on the table will now access the data at the checked out
        version. As a consequence, calling this method will disable any read consistency
        interval that was previously set.

        This is a read-only operation that turns the table into a sort of "view"
        or "detached head".  Other table instances will not be affected.  To make the
        change permanent you can use the `[Self::restore]` method.

        Any operation that modifies the table will fail while the table is in a checked
        out state.

        Parameters
        ----------
        version: int | str,
            The version to check out. A version number (`int`) or a tag
            (`str`) can be provided.

        To return the table to a normal state use `[Self::checkout_latest]`
        """
        try:
            await self._inner.checkout(version)
        except RuntimeError as e:
            if "not found" in str(e):
                raise ValueError(
                    f"Version {version} no longer exists. Was it cleaned up?"
                )
            else:
                raise

    async def checkout_latest(self):
        """
        Ensures the table is pointing at the latest version

        This can be used to manually update a table when the read_consistency_interval
        is None
        It can also be used to undo a `[Self::checkout]` operation
        """
        await self._inner.checkout_latest()

    async def restore(self, version: Optional[int | str] = None):
        """
        Restore the table to the currently checked out version

        This operation will fail if checkout has not been called previously

        This operation will overwrite the latest version of the table with a
        previous version.  Any changes made since the checked out version will
        no longer be visible.

        Once the operation concludes the table will no longer be in a checked
        out state and the read_consistency_interval, if any, will apply.
        """
        await self._inner.restore(version)

    def take_offsets(self, offsets: list[int]) -> AsyncTakeQuery:
        """
        Take a list of offsets from the table.

        Offsets are 0-indexed and relative to the current version of the table.  Offsets
        are not stable.  A row with an offset of N may have a different offset in a
        different version of the table (e.g. if an earlier row is deleted).

        Offsets are mostly useful for sampling as the set of all valid offsets is easily
        known in advance to be [0, len(table)).

        Parameters
        ----------
        offsets: list[int]
            The offsets to take.

        Returns
        -------
        pa.RecordBatch
            A record batch containing the rows at the given offsets.
        """
        return AsyncTakeQuery(self._inner.take_offsets(offsets))

    def take_row_ids(self, row_ids: list[int]) -> AsyncTakeQuery:
        """
        Take a list of row ids from the table.

        Row ids are not stable and are relative to the current version of the table.
        They can change due to compaction and updates.

        Unlike offsets, row ids are not 0-indexed and no assumptions should be made
        about the possible range of row ids.  In order to use this method you must
        first obtain the row ids by scanning or searching the table.

        Even so, row ids are more stable than offsets and can be useful in some
        situations.

        There is an ongoing effort to make row ids stable which is tracked at
        https://github.com/lancedb/lancedb/issues/1120

        Parameters
        ----------
        row_ids: list[int]
            The row ids to take.

        Returns
        -------
        AsyncTakeQuery
            A query object that can be executed to get the rows.
        """
        return AsyncTakeQuery(self._inner.take_row_ids(row_ids))

    @property
    def tags(self) -> AsyncTags:
        """Tag management for the dataset.

        Similar to Git, tags are a way to add metadata to a specific version of the
        dataset.

        .. warning::

            Tagged versions are exempted from the
            :py:meth:`optimize(cleanup_older_than)` process.

            To remove a version that has been tagged, you must first
            :py:meth:`~Tags.delete` the associated tag.

        """
        return AsyncTags(self._inner)

    async def optimize(
        self,
        *,
        cleanup_older_than: Optional[timedelta] = None,
        delete_unverified: bool = False,
        retrain=False,
    ) -> OptimizeStats:
        """
        Optimize the on-disk data and indices for better performance.

        Modeled after ``VACUUM`` in PostgreSQL.

        Optimization covers three operations:

         * Compaction: Merges small files into larger ones
         * Prune: Removes old versions of the dataset
         * Index: Optimizes the indices, adding new data to existing indices

        Parameters
        ----------
        cleanup_older_than: timedelta, optional default 7 days
            All files belonging to versions older than this will be removed.  Set
            to 0 days to remove all versions except the latest.  The latest version
            is never removed.
        delete_unverified: bool, default False
            Files leftover from a failed transaction may appear to be part of an
            in-progress operation (e.g. appending new data) and these files will not
            be deleted unless they are at least 7 days old. If delete_unverified is True
            then these files will be deleted regardless of their age.
        retrain: bool, default False
            This parameter is no longer used and is deprecated.

        Experimental API
        ----------------

        The optimization process is undergoing active development and may change.
        Our goal with these changes is to improve the performance of optimization and
        reduce the complexity.

        That being said, it is essential today to run optimize if you want the best
        performance.  It should be stable and safe to use in production, but it our
        hope that the API may be simplified (or not even need to be called) in the
        future.

        The frequency an application shoudl call optimize is based on the frequency of
        data modifications.  If data is frequently added, deleted, or updated then
        optimize should be run frequently.  A good rule of thumb is to run optimize if
        you have added or modified 100,000 or more records or run more than 20 data
        modification operations.
        """
        cleanup_since_ms: Optional[int] = None
        if cleanup_older_than is not None:
            cleanup_since_ms = round(cleanup_older_than.total_seconds() * 1000)

        if retrain:
            import warnings

            warnings.warn(
                "The 'retrain' parameter is deprecated and will be removed in a "
                "future version.",
                DeprecationWarning,
            )

        return await self._inner.optimize(
            cleanup_since_ms=cleanup_since_ms,
            delete_unverified=delete_unverified,
        )

    async def list_indices(self) -> Iterable[IndexConfig]:
        """
        List all indices that have been created with Self::create_index
        """
        return await self._inner.list_indices()

    async def index_stats(self, index_name: str) -> Optional[IndexStatistics]:
        """
        Retrieve statistics about an index

        Parameters
        ----------
        index_name: str
            The name of the index to retrieve statistics for

        Returns
        -------
        IndexStatistics or None
            The statistics about the index. Returns None if the index does not exist.
        """
        stats = await self._inner.index_stats(index_name)
        if stats is None:
            return None
        else:
            return IndexStatistics(**stats)

    async def uses_v2_manifest_paths(self) -> bool:
        """
        Check if the table is using the new v2 manifest paths.

        Returns
        -------
        bool
            True if the table is using the new v2 manifest paths, False otherwise.
        """
        return await self._inner.uses_v2_manifest_paths()

    async def migrate_manifest_paths_v2(self):
        """
        Migrate the manifest paths to the new format.

        This will update the manifest to use the new v2 format for paths.

        This function is idempotent, and can be run multiple times without
        changing the state of the object store.

        !!! danger

            This should not be run while other concurrent operations are happening.
            And it should also run until completion before resuming other operations.

        You can use
        [AsyncTable.uses_v2_manifest_paths][lancedb.table.AsyncTable.uses_v2_manifest_paths]
        to check if the table is already using the new path style.
        """
        await self._inner.migrate_manifest_paths_v2()

    async def replace_field_metadata(
        self, field_name: str, new_metadata: dict[str, str]
    ):
        """
        Replace the metadata of a field in the schema

        Parameters
        ----------
        field_name: str
            The name of the field to replace the metadata for
        new_metadata: dict
            The new metadata to set
        """
        await self._inner.replace_field_metadata(field_name, new_metadata)

              

  

            name

  
      `property`
  

¶

name: str

    

      
The name of the table.

    

            tags

  
      `property`
  

¶

tags: AsyncTags

    

      
Tag management for the dataset.

Similar to Git, tags are a way to add metadata to a specific version of the
dataset.

.. warning::

Tagged versions are exempted from the
:py:meth:`optimize(cleanup_older_than)` process.

To remove a version that has been tagged, you must first
:py:meth:`~Tags.delete` the associated tag.

    

            __init__

¶

__init__(table: Table)

    

      
Create a new AsyncTable object.

You should not create AsyncTable objects directly.

Use AsyncConnection.create_table and
AsyncConnection.open_table to obtain
Table objects.

            
              Source code in `lancedb/table.py`
              
3404
3405
3406
3407
3408
3409
3410
3411
3412
def __init__(self, table: LanceDBTable):
    """Create a new AsyncTable object.

    You should not create AsyncTable objects directly.

    Use [AsyncConnection.create_table][lancedb.AsyncConnection.create_table] and
    [AsyncConnection.open_table][lancedb.AsyncConnection.open_table] to obtain
    Table objects."""
    self._inner = table

            
    

            is_open

¶

is_open() -> bool

    

      
Return True if the table is open.

            
              Source code in `lancedb/table.py`
              
3423
3424
3425
def is_open(self) -> bool:
    """Return True if the table is open."""
    return self._inner.is_open()

            
    

            close

¶

close()

    

      
Close the table and free any resources associated with it.

It is safe to call this method multiple times.

Any attempt to use the table after it has been closed will raise an error.

            
              Source code in `lancedb/table.py`
              
3427
3428
3429
3430
3431
3432
3433
def close(self):
    """Close the table and free any resources associated with it.

    It is safe to call this method multiple times.

    Any attempt to use the table after it has been closed will raise an error."""
    return self._inner.close()

            
    

            schema

  
      `async`
  

¶

schema() -> Schema

    

      
The Arrow Schema
of this Table

            
              Source code in `lancedb/table.py`
              
3440
3441
3442
3443
3444
3445
async def schema(self) -> pa.Schema:
    """The [Arrow Schema](https://arrow.apache.org/docs/python/api/datatypes.html#)
    of this Table

    """
    return await self._inner.schema()

            
    

            embedding_functions

  
      `async`
  

¶

embedding_functions() -> Dict[str, EmbeddingFunctionConfig]

    

      
Get the embedding functions for the table

Returns:

    
        
- 
`funcs` (              `Dict[str, EmbeddingFunctionConfig]`
)          –
          
            
A mapping of the vector column to the embedding function
or empty dict if not configured.

          
        
    

            
              Source code in `lancedb/table.py`
              
3447
3448
3449
3450
3451
3452
3453
3454
3455
3456
3457
3458
async def embedding_functions(self) -> Dict[str, EmbeddingFunctionConfig]:
    """
    Get the embedding functions for the table

    Returns
    -------
    funcs: Dict[str, EmbeddingFunctionConfig]
        A mapping of the vector column to the embedding function
        or empty dict if not configured.
    """
    schema = await self.schema()
    return EmbeddingFunctionRegistry.get_instance().parse_functions(schema.metadata)

            
    

            count_rows

  
      `async`
  

¶

count_rows(filter: Optional[str] = None) -> int

    

      
Count the number of rows in the table.

Parameters:

    
        
- 
          `filter`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
A SQL where clause to filter the rows to count.

          
        
    

            
              Source code in `lancedb/table.py`
              
3460
3461
3462
3463
3464
3465
3466
3467
3468
3469
async def count_rows(self, filter: Optional[str] = None) -> int:
    """
    Count the number of rows in the table.

    Parameters
    ----------
    filter: str, optional
        A SQL where clause to filter the rows to count.
    """
    return await self._inner.count_rows(filter)

            
    

            head

  
      `async`
  

¶

head(n=5) -> Table

    

      
Return the first `n` rows of the table.

Parameters:

    
        
- 
          `n`
          –
          
            
The number of rows to return.

          
        
    

            
              Source code in `lancedb/table.py`
              
3471
3472
3473
3474
3475
3476
3477
3478
3479
3480
async def head(self, n=5) -> pa.Table:
    """
    Return the first `n` rows of the table.

    Parameters
    ----------
    n: int, default 5
        The number of rows to return.
    """
    return await self.query().limit(n).to_arrow()

            
    

            query

¶

query() -> AsyncQuery

    

      
Returns an AsyncQuery that can be used
to search the table.

Use methods on the returned query to control query behavior.  The query
can be executed with methods like to_arrow,
to_pandas and more.

            
              Source code in `lancedb/table.py`
              
3482
3483
3484
3485
3486
3487
3488
3489
3490
3491
def query(self) -> AsyncQuery:
    """
    Returns an [AsyncQuery][lancedb.query.AsyncQuery] that can be used
    to search the table.

    Use methods on the returned query to control query behavior.  The query
    can be executed with methods like [to_arrow][lancedb.query.AsyncQuery.to_arrow],
    [to_pandas][lancedb.query.AsyncQuery.to_pandas] and more.
    """
    return AsyncQuery(self._inner.query())

            
    

            to_pandas

  
      `async`
  

¶

to_pandas() -> 'pd.DataFrame'

    

      
Return the table as a pandas DataFrame.

Returns:

    
        
- 
              `DataFrame`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
3493
3494
3495
3496
3497
3498
3499
3500
async def to_pandas(self) -> "pd.DataFrame":
    """Return the table as a pandas DataFrame.

    Returns
    -------
    pd.DataFrame
    """
    return (await self.to_arrow()).to_pandas()

            
    

            to_arrow

  
      `async`
  

¶

to_arrow() -> Table

    

      
Return the table as a pyarrow Table.

Returns:

    
        
- 
              `Table`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
3502
3503
3504
3505
3506
3507
3508
3509
async def to_arrow(self) -> pa.Table:
    """Return the table as a pyarrow Table.

    Returns
    -------
    pa.Table
    """
    return await self.query().to_arrow()

            
    

            create_index

  
      `async`
  

¶

create_index(column: str, *, replace: Optional[bool] = None, config: Optional[Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]] = None, wait_timeout: Optional[timedelta] = None, name: Optional[str] = None, train: bool = True)

    

      
Create an index to speed up queries

Indices can be created on vector columns or scalar columns.
Indices on vector columns will speed up vector searches.
Indices on scalar columns will speed up filtering (in both
vector and non-vector searches)

Parameters:

    
        
- 
          `column`
              (`str`)
          –
          
            
The column to index.

          
        
        
- 
          `replace`
              (`Optional[bool]`, default:
                  `None`
)
          –
          
            
Whether to replace the existing index

If this is false, and another index already exists on the same columns
and the same name, then an error will be returned.  This is true even if
that index is out of date.

The default is True

          
        
        
- 
          `config`
              (`Optional[Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]]`, default:
                  `None`
)
          –
          
            
For advanced configuration you can specify the type of index you would
like to create.   You can also specify index-specific parameters when
creating an index object.

          
        
        
- 
          `wait_timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The timeout to wait if indexing is asynchronous.

          
        
        
- 
          `name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the index. If not provided, a default name will be generated.

          
        
        
- 
          `train`
              (`bool`, default:
                  `True`
)
          –
          
            
Whether to train the index with existing data. Vector indices always train
with existing data.

          
        
    

            
              Source code in `lancedb/table.py`
              
3511
3512
3513
3514
3515
3516
3517
3518
3519
3520
3521
3522
3523
3524
3525
3526
3527
3528
3529
3530
3531
3532
3533
3534
3535
3536
3537
3538
3539
3540
3541
3542
3543
3544
3545
3546
3547
3548
3549
3550
3551
3552
3553
3554
3555
3556
3557
3558
3559
3560
3561
3562
3563
3564
3565
3566
3567
3568
3569
3570
3571
3572
3573
3574
3575
3576
3577
3578
3579
3580
3581
3582
3583
3584
3585
3586
3587
3588
async def create_index(
    self,
    column: str,
    *,
    replace: Optional[bool] = None,
    config: Optional[
        Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]
    ] = None,
    wait_timeout: Optional[timedelta] = None,
    name: Optional[str] = None,
    train: bool = True,
):
    """Create an index to speed up queries

    Indices can be created on vector columns or scalar columns.
    Indices on vector columns will speed up vector searches.
    Indices on scalar columns will speed up filtering (in both
    vector and non-vector searches)

    Parameters
    ----------
    column: str
        The column to index.
    replace: bool, default True
        Whether to replace the existing index

        If this is false, and another index already exists on the same columns
        and the same name, then an error will be returned.  This is true even if
        that index is out of date.

        The default is True
    config: default None
        For advanced configuration you can specify the type of index you would
        like to create.   You can also specify index-specific parameters when
        creating an index object.
    wait_timeout: timedelta, optional
        The timeout to wait if indexing is asynchronous.
    name: str, optional
        The name of the index. If not provided, a default name will be generated.
    train: bool, default True
        Whether to train the index with existing data. Vector indices always train
        with existing data.
    """
    if config is not None:
        if not isinstance(
            config,
            (
                IvfFlat,
                IvfSq,
                IvfPq,
                IvfRq,
                HnswPq,
                HnswSq,
                BTree,
                Bitmap,
                LabelList,
                FTS,
            ),
        ):
            raise TypeError(
                "config must be an instance of IvfSq, IvfPq, IvfRq, HnswPq, HnswSq,"
                " BTree, Bitmap, LabelList, or FTS, but got " + str(type(config))
            )
    try:
        await self._inner.create_index(
            column,
            index=config,
            replace=replace,
            wait_timeout=wait_timeout,
            name=name,
            train=train,
        )
    except ValueError as e:
        if "not support the requested language" in str(e):
            supported_langs = ", ".join(lang_mapping.values())
            help_msg = f"Supported languages: {supported_langs}"
            add_note(e, help_msg)
        raise e

            
    

            drop_index

  
      `async`
  

¶

drop_index(name: str) -> None

    

      
Drop an index from the table.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the index to drop.

          
        
    

  Notes
  
This does not delete the index from disk, it just removes it from the table.
To delete the index, run optimize
after dropping the index.

Use list_indices to find the names
of the indices.

            
              Source code in `lancedb/table.py`
              
3590
3591
3592
3593
3594
3595
3596
3597
3598
3599
3600
3601
3602
3603
3604
3605
3606
3607
3608
async def drop_index(self, name: str) -> None:
    """
    Drop an index from the table.

    Parameters
    ----------
    name: str
        The name of the index to drop.

    Notes
    -----
    This does not delete the index from disk, it just removes it from the table.
    To delete the index, run [optimize][lancedb.table.AsyncTable.optimize]
    after dropping the index.

    Use [list_indices][lancedb.table.AsyncTable.list_indices] to find the names
    of the indices.
    """
    await self._inner.drop_index(name)

            
    

            prewarm_index

  
      `async`
  

¶

prewarm_index(name: str) -> None

    

      
Prewarm an index in the table.

Parameters:

    
        
- 
          `name`
              (`str`)
          –
          
            
The name of the index to prewarm

          
        
    

  Notes
  
This will load the index into memory.  This may reduce the cold-start time for
future queries.  If the index does not fit in the cache then this call may be
wasteful.

            
              Source code in `lancedb/table.py`
              
3610
3611
3612
3613
3614
3615
3616
3617
3618
3619
3620
3621
3622
3623
3624
3625
async def prewarm_index(self, name: str) -> None:
    """
    Prewarm an index in the table.

    Parameters
    ----------
    name: str
        The name of the index to prewarm

    Notes
    -----
    This will load the index into memory.  This may reduce the cold-start time for
    future queries.  If the index does not fit in the cache then this call may be
    wasteful.
    """
    await self._inner.prewarm_index(name)

            
    

            wait_for_index

  
      `async`
  

¶

wait_for_index(index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)) -> None

    

      
Wait for indexing to complete for the given index names.
This will poll the table until all the indices are fully indexed,
or raise a timeout exception if the timeout is reached.

Parameters:

    
        
- 
          `index_names`
              (`Iterable[str]`)
          –
          
            
The name of the indices to poll

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `timedelta(seconds=300)`
)
          –
          
            
Timeout to wait for asynchronous indexing. The default is 5 minutes.

          
        
    

            
              Source code in `lancedb/table.py`
              
3627
3628
3629
3630
3631
3632
3633
3634
3635
3636
3637
3638
3639
3640
3641
3642
async def wait_for_index(
    self, index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)
) -> None:
    """
    Wait for indexing to complete for the given index names.
    This will poll the table until all the indices are fully indexed,
    or raise a timeout exception if the timeout is reached.

    Parameters
    ----------
    index_names: str
        The name of the indices to poll
    timeout: timedelta
        Timeout to wait for asynchronous indexing. The default is 5 minutes.
    """
    await self._inner.wait_for_index(index_names, timeout)

            
    

            stats

  
      `async`
  

¶

stats() -> TableStatistics

    

      
Retrieve table and fragment statistics.

            
              Source code in `lancedb/table.py`
              
3644
3645
3646
3647
3648
async def stats(self) -> TableStatistics:
    """
    Retrieve table and fragment statistics.
    """
    return await self._inner.stats()

            
    

            uri

  
      `async`
  

¶

uri() -> str

    

      
Get the table URI (storage location).

For remote tables, this fetches the location from the server via describe.
For local tables, this returns the dataset URI.

Returns:

    
        
- 
              `str`
          –
          
            
The full storage location of the table (e.g., S3/GCS path).

          
        
    

            
              Source code in `lancedb/table.py`
              
3650
3651
3652
3653
3654
3655
3656
3657
3658
3659
3660
3661
3662
async def uri(self) -> str:
    """
    Get the table URI (storage location).

    For remote tables, this fetches the location from the server via describe.
    For local tables, this returns the dataset URI.

    Returns
    -------
    str
        The full storage location of the table (e.g., S3/GCS path).
    """
    return await self._inner.uri()

            
    

            initial_storage_options

  
      `async`
  

¶

initial_storage_options() -> Optional[Dict[str, str]]

    

      
Get the initial storage options that were passed in when opening this table.

For dynamically refreshed options (e.g., credential vending), use
:meth:`latest_storage_options`.

Warning: This is an internal API and the return value is subject to change.

Returns:

    
        
- 
              `Optional[Dict[str, str]]`
          –
          
            
The storage options, or None if no storage options were configured.

          
        
    

            
              Source code in `lancedb/table.py`
              
3664
3665
3666
3667
3668
3669
3670
3671
3672
3673
3674
3675
3676
3677
async def initial_storage_options(self) -> Optional[Dict[str, str]]:
    """Get the initial storage options that were passed in when opening this table.

    For dynamically refreshed options (e.g., credential vending), use
    :meth:`latest_storage_options`.

    Warning: This is an internal API and the return value is subject to change.

    Returns
    -------
    Optional[Dict[str, str]]
        The storage options, or None if no storage options were configured.
    """
    return await self._inner.initial_storage_options()

            
    

            latest_storage_options

  
      `async`
  

¶

latest_storage_options() -> Optional[Dict[str, str]]

    

      
Get the latest storage options, refreshing from provider if configured.

This method is useful for credential vending scenarios where storage options
may be refreshed dynamically. If no dynamic provider is configured, this
returns the initial static options.

Warning: This is an internal API and the return value is subject to change.

Returns:

    
        
- 
              `Optional[Dict[str, str]]`
          –
          
            
The storage options, or None if no storage options were configured.

          
        
    

            
              Source code in `lancedb/table.py`
              
3679
3680
3681
3682
3683
3684
3685
3686
3687
3688
3689
3690
3691
3692
3693
async def latest_storage_options(self) -> Optional[Dict[str, str]]:
    """Get the latest storage options, refreshing from provider if configured.

    This method is useful for credential vending scenarios where storage options
    may be refreshed dynamically. If no dynamic provider is configured, this
    returns the initial static options.

    Warning: This is an internal API and the return value is subject to change.

    Returns
    -------
    Optional[Dict[str, str]]
        The storage options, or None if no storage options were configured.
    """
    return await self._inner.latest_storage_options()

            
    

            add

  
      `async`
  

¶

add(data: DATA, *, mode: Optional[Literal['append', 'overwrite']] = 'append', on_bad_vectors: Optional[OnBadVectorsType] = None, fill_value: Optional[float] = None) -> AddResult

    

      
Add more data to the Table.

Parameters:

    
        
- 
          `data`
              (`DATA`)
          –
          
            
The data to insert into the table. Acceptable types are:

- 

list-of-dict

- 

pandas.DataFrame

- 

pyarrow.Table or pyarrow.RecordBatch

          
        
        
- 
          `mode`
              (`Optional[Literal['append', 'overwrite']]`, default:
                  `'append'`
)
          –
          
            
The mode to use when writing the data. Valid values are
"append" and "overwrite".

          
        
        
- 
          `on_bad_vectors`
              (`Optional[OnBadVectorsType]`, default:
                  `None`
)
          –
          
            
What to do if any of the vectors are not the same size or contains NaNs.
One of "error", "drop", "fill", "null".

          
        
        
- 
          `fill_value`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The value to use when filling vectors. Only used if on_bad_vectors="fill".

          
        
    

            
              Source code in `lancedb/table.py`
              
3695
3696
3697
3698
3699
3700
3701
3702
3703
3704
3705
3706
3707
3708
3709
3710
3711
3712
3713
3714
3715
3716
3717
3718
3719
3720
3721
3722
3723
3724
3725
3726
3727
3728
3729
3730
3731
3732
3733
3734
3735
3736
3737
3738
3739
3740
3741
async def add(
    self,
    data: DATA,
    *,
    mode: Optional[Literal["append", "overwrite"]] = "append",
    on_bad_vectors: Optional[OnBadVectorsType] = None,
    fill_value: Optional[float] = None,
) -> AddResult:
    """Add more data to the [Table](Table).

    Parameters
    ----------
    data: DATA
        The data to insert into the table. Acceptable types are:

        - list-of-dict

        - pandas.DataFrame

        - pyarrow.Table or pyarrow.RecordBatch
    mode: str
        The mode to use when writing the data. Valid values are
        "append" and "overwrite".
    on_bad_vectors: str, default "error"
        What to do if any of the vectors are not the same size or contains NaNs.
        One of "error", "drop", "fill", "null".
    fill_value: float, default 0.
        The value to use when filling vectors. Only used if on_bad_vectors="fill".

    """
    schema = await self.schema()
    if on_bad_vectors is None:
        on_bad_vectors = "error"
    if fill_value is None:
        fill_value = 0.0
    data = _sanitize_data(
        data,
        schema,
        metadata=schema.metadata,
        on_bad_vectors=on_bad_vectors,
        fill_value=fill_value,
        allow_subschema=True,
    )
    if isinstance(data, pa.Table):
        data = data.to_reader()

    return await self._inner.add(data, mode or "append")

            
    

            merge_insert

¶

merge_insert(on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder

    

      
Returns a `LanceMergeInsertBuilder`
that can be used to create a "merge insert" operation

This operation can add rows, update rows, and remove rows all in a single
transaction. It is a very generic tool that can be used to create
behaviors like "insert if not exists", "update or insert (i.e. upsert)",
or even replace a portion of existing data with new data (e.g. replace
all data where month="january")

The merge insert operation works by combining new data from a
source table with existing data in a target table by using a
join.  There are three categories of records.

"Matched" records are records that exist in both the source table and
the target table. "Not matched" records exist only in the source table
(e.g. these are new data) "Not matched by source" records exist only
in the target table (this is old data)

The builder returned by this method can be used to customize what
should happen for each category of data.

Please note that the data may appear to be reordered as part of this
operation.  This is because updated rows will be deleted from the
dataset and then reinserted at the end with the new values.

Parameters:

    
        
- 
          `on`
              (`Union[str, Iterable[str]]`)
          –
          
            
A column (or columns) to join on.  This is how records from the
source table and target table are matched.  Typically this is some
kind of key or id column.

          
        
    

Examples:

    
>>> import lancedb
>>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
>>> # Perform a "upsert" operation
>>> res = table.merge_insert("a")     \
...      .when_matched_update_all()     \
...      .when_not_matched_insert_all() \
...      .execute(new_data)
>>> res
MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
>>> # The order of new rows is non-deterministic since we use
>>> # a hash-join as part of this operation and so we sort here
>>> table.to_arrow().sort_by("a").to_pandas()
   a  b
0  1  b
1  2  x
2  3  y
3  4  z

            
              Source code in `lancedb/table.py`
              
3743
3744
3745
3746
3747
3748
3749
3750
3751
3752
3753
3754
3755
3756
3757
3758
3759
3760
3761
3762
3763
3764
3765
3766
3767
3768
3769
3770
3771
3772
3773
3774
3775
3776
3777
3778
3779
3780
3781
3782
3783
3784
3785
3786
3787
3788
3789
3790
3791
3792
3793
3794
3795
3796
3797
3798
3799
3800
3801
3802
3803
def merge_insert(self, on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder:
    """
    Returns a [`LanceMergeInsertBuilder`][lancedb.merge.LanceMergeInsertBuilder]
    that can be used to create a "merge insert" operation

    This operation can add rows, update rows, and remove rows all in a single
    transaction. It is a very generic tool that can be used to create
    behaviors like "insert if not exists", "update or insert (i.e. upsert)",
    or even replace a portion of existing data with new data (e.g. replace
    all data where month="january")

    The merge insert operation works by combining new data from a
    **source table** with existing data in a **target table** by using a
    join.  There are three categories of records.

    "Matched" records are records that exist in both the source table and
    the target table. "Not matched" records exist only in the source table
    (e.g. these are new data) "Not matched by source" records exist only
    in the target table (this is old data)

    The builder returned by this method can be used to customize what
    should happen for each category of data.

    Please note that the data may appear to be reordered as part of this
    operation.  This is because updated rows will be deleted from the
    dataset and then reinserted at the end with the new values.

    Parameters
    ----------

    on: Union[str, Iterable[str]]
        A column (or columns) to join on.  This is how records from the
        source table and target table are matched.  Typically this is some
        kind of key or id column.

    Examples
    --------
    >>> import lancedb
    >>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data)
    >>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
    >>> # Perform a "upsert" operation
    >>> res = table.merge_insert("a")     \\
    ...      .when_matched_update_all()     \\
    ...      .when_not_matched_insert_all() \\
    ...      .execute(new_data)
    >>> res
    MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
    >>> # The order of new rows is non-deterministic since we use
    >>> # a hash-join as part of this operation and so we sort here
    >>> table.to_arrow().sort_by("a").to_pandas()
       a  b
    0  1  b
    1  2  x
    2  3  y
    3  4  z
    """  # noqa: E501
    on = [on] if isinstance(on, str) else list(iter(on))

    return LanceMergeInsertBuilder(self, on)

            
    

            search

  
      `async`
  

¶

search(query: Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]] = None, vector_column_name: Optional[str] = None, query_type: QueryType = 'auto', ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None) -> Union[AsyncHybridQuery, AsyncFTSQuery, AsyncVectorQuery]

    

      
Create a search query to find the nearest neighbors
of the given query vector. We currently support vector search
and [full-text search][experimental-full-text-search].

All query options are defined in AsyncQuery.

Parameters:

    
        
- 
          `query`
              (`Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]]`, default:
                  `None`
)
          –
          
            
The targetted vector to search for.

- 

default None.
Acceptable types are: list, np.ndarray, PIL.Image.Image

- 

If None then the select/where/limit clauses are applied to filter
the table

          
        
        
- 
          `vector_column_name`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
The name of the vector column to search.

The vector column needs to be a pyarrow fixed size list type

- 

If not specified then the vector column is inferred from
the table schema

- 

If the table has multiple vector columns then the vector_column_name
needs to be specified. Otherwise, an error is raised.

          
        
        
- 
          `query_type`
              (`QueryType`, default:
                  `'auto'`
)
          –
          
            
default "auto".
Acceptable types are: "vector", "fts", "hybrid", or "auto"

- 

If "auto" then the query type is inferred from the query;

- 

If `query` is a list/np.ndarray then the query type is
"vector";

- 

If `query` is a PIL.Image.Image then either do vector search,
or raise an error if no corresponding embedding function is found.

- 

If `query` is a string, then the query type is "vector" if the
  table has embedding functions else the query type is "fts"

          
        
    

Returns:

    
        
- 
              `LanceQueryBuilder`
          –
          
            
A query builder object representing the query.

          
        
    

            
              Source code in `lancedb/table.py`
              
3857
3858
3859
3860
3861
3862
3863
3864
3865
3866
3867
3868
3869
3870
3871
3872
3873
3874
3875
3876
3877
3878
3879
3880
3881
3882
3883
3884
3885
3886
3887
3888
3889
3890
3891
3892
3893
3894
3895
3896
3897
3898
3899
3900
3901
3902
3903
3904
3905
3906
3907
3908
3909
3910
3911
3912
3913
3914
3915
3916
3917
3918
3919
3920
3921
3922
3923
3924
3925
3926
3927
3928
3929
3930
3931
3932
3933
3934
3935
3936
3937
3938
3939
3940
3941
3942
3943
3944
3945
3946
3947
3948
3949
3950
3951
3952
3953
3954
3955
3956
3957
3958
3959
3960
3961
3962
3963
3964
3965
3966
3967
3968
3969
3970
3971
3972
3973
3974
3975
3976
3977
3978
3979
3980
3981
3982
3983
3984
3985
3986
3987
3988
3989
3990
3991
3992
3993
3994
3995
3996
3997
3998
3999
4000
4001
4002
4003
4004
4005
4006
4007
4008
4009
4010
4011
4012
4013
4014
4015
4016
4017
4018
4019
4020
4021
4022
4023
4024
4025
4026
4027
4028
4029
4030
4031
4032
4033
4034
4035
4036
4037
4038
4039
async def search(
    self,
    query: Optional[
        Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]
    ] = None,
    vector_column_name: Optional[str] = None,
    query_type: QueryType = "auto",
    ordering_field_name: Optional[str] = None,
    fts_columns: Optional[Union[str, List[str]]] = None,
) -> Union[AsyncHybridQuery, AsyncFTSQuery, AsyncVectorQuery]:
    """Create a search query to find the nearest neighbors
    of the given query vector. We currently support [vector search][search]
    and [full-text search][experimental-full-text-search].

    All query options are defined in [AsyncQuery][lancedb.query.AsyncQuery].

    Parameters
    ----------
    query: list/np.ndarray/str/PIL.Image.Image, default None
        The targetted vector to search for.

        - *default None*.
        Acceptable types are: list, np.ndarray, PIL.Image.Image

        - If None then the select/where/limit clauses are applied to filter
        the table
    vector_column_name: str, optional
        The name of the vector column to search.

        The vector column needs to be a pyarrow fixed size list type

        - If not specified then the vector column is inferred from
        the table schema

        - If the table has multiple vector columns then the *vector_column_name*
        needs to be specified. Otherwise, an error is raised.
    query_type: str
        *default "auto"*.
        Acceptable types are: "vector", "fts", "hybrid", or "auto"

        - If "auto" then the query type is inferred from the query;

            - If `query` is a list/np.ndarray then the query type is
            "vector";

            - If `query` is a PIL.Image.Image then either do vector search,
            or raise an error if no corresponding embedding function is found.

        - If `query` is a string, then the query type is "vector" if the
          table has embedding functions else the query type is "fts"

    Returns
    -------
    LanceQueryBuilder
        A query builder object representing the query.
    """

    def is_embedding(query):
        return isinstance(query, (list, np.ndarray, pa.Array, pa.ChunkedArray))

    async def get_embedding_func(
        vector_column_name: Optional[str],
        query_type: QueryType,
        query: Optional[Union[VEC, str, "PIL.Image.Image", Tuple, FullTextQuery]],
    ) -> Tuple[str, EmbeddingFunctionConfig]:
        if isinstance(query, FullTextQuery):
            query_type = "fts"
        schema = await self.schema()
        vector_column_name = infer_vector_column_name(
            schema=schema,
            query_type=query_type,
            query=query,
            vector_column_name=vector_column_name,
        )
        funcs = EmbeddingFunctionRegistry.get_instance().parse_functions(
            schema.metadata
        )
        func = funcs.get(vector_column_name)
        if func is None:
            error = ValueError(
                f"Column '{vector_column_name}' has no registered "
                "embedding function."
            )
            if len(funcs) > 0:
                add_note(
                    error,
                    "Embedding functions are registered for columns: "
                    f"{list(funcs.keys())}",
                )
            else:
                add_note(
                    error, "No embedding functions are registered for any columns."
                )
            raise error
        return vector_column_name, func

    async def make_embedding(embedding, query):
        if embedding is not None:
            loop = asyncio.get_running_loop()
            # This function is likely to block, since it either calls an expensive
            # function or makes an HTTP request to an embeddings REST API.
            return (
                await loop.run_in_executor(
                    None,
                    embedding.function.compute_query_embeddings_with_retry,
                    query,
                )
            )[0]
        else:
            return None

    if query_type == "auto":
        # Infer the query type.
        if is_embedding(query):
            vector_query = query
            query_type = "vector"
        elif isinstance(query, FullTextQuery):
            query_type = "fts"
        elif isinstance(query, str):
            try:
                (
                    indices,
                    (vector_column_name, embedding_conf),
                ) = await asyncio.gather(
                    self.list_indices(),
                    get_embedding_func(vector_column_name, "auto", query),
                )
            except ValueError as e:
                if "Column" in str(
                    e
                ) and "has no registered embedding function" in str(e):
                    # If the column has no registered embedding function,
                    # then it's an FTS query.
                    query_type = "fts"
                else:
                    raise e
            else:
                if embedding_conf is not None:
                    vector_query = await make_embedding(embedding_conf, query)
                    if any(
                        i.columns[0] == embedding_conf.source_column
                        and i.index_type == "FTS"
                        for i in indices
                    ):
                        query_type = "hybrid"
                    else:
                        query_type = "vector"
                else:
                    query_type = "fts"
        else:
            # it's an image or something else embeddable.
            query_type = "vector"
    elif query_type == "vector":
        if is_embedding(query):
            vector_query = query
        else:
            vector_column_name, embedding_conf = await get_embedding_func(
                vector_column_name, query_type, query
            )
            vector_query = await make_embedding(embedding_conf, query)
    elif query_type == "hybrid":
        if is_embedding(query):
            raise ValueError("Hybrid search requires a text query")
        else:
            vector_column_name, embedding_conf = await get_embedding_func(
                vector_column_name, query_type, query
            )
            vector_query = await make_embedding(embedding_conf, query)

    if query_type == "vector":
        builder = self.query().nearest_to(vector_query)
        if vector_column_name:
            builder = builder.column(vector_column_name)
        return builder
    elif query_type == "fts":
        return self.query().nearest_to_text(query, columns=fts_columns)
    elif query_type == "hybrid":
        builder = self.query().nearest_to(vector_query)
        if vector_column_name:
            builder = builder.column(vector_column_name)
        return builder.nearest_to_text(query, columns=fts_columns)
    else:
        raise ValueError(f"Unknown query type: '{query_type}'")

            
    

            vector_search

¶

vector_search(query_vector: Union[VEC, Tuple]) -> AsyncVectorQuery

    

      
Search the table with a given query vector.
This is a convenience method for preparing a vector query and
is the same thing as calling `nearestTo` on the builder returned
by `query`.  Seer nearest_to for more
details.

            
              Source code in `lancedb/table.py`
              
4041
4042
4043
4044
4045
4046
4047
4048
4049
4050
4051
4052
def vector_search(
    self,
    query_vector: Union[VEC, Tuple],
) -> AsyncVectorQuery:
    """
    Search the table with a given query vector.
    This is a convenience method for preparing a vector query and
    is the same thing as calling `nearestTo` on the builder returned
    by `query`.  Seer [nearest_to][lancedb.query.AsyncQuery.nearest_to] for more
    details.
    """
    return self.query().nearest_to(query_vector)

            
    

            delete

  
      `async`
  

¶

delete(where: str) -> DeleteResult

    

      
Delete rows from the table.

This can be used to delete a single row, many rows, all rows, or
sometimes no rows (if your predicate matches nothing).

Parameters:

    
        
- 
          `where`
              (`str`)
          –
          
            
The SQL where clause to use when deleting rows.

- For example, 'x = 2' or 'x IN (1, 2, 3)'.

The filter must not be empty, or it will error.

          
        
    

Examples:

    
>>> import lancedb
>>> data = [
...    {"x": 1, "vector": [1.0, 2]},
...    {"x": 2, "vector": [3.0, 4]},
...    {"x": 3, "vector": [5.0, 6]}
... ]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.delete("x = 2")
DeleteResult(version=2)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  3  [5.0, 6.0]

    
If you have a list of values to delete, you can combine them into a
stringified list and use the `IN` operator:

    
>>> to_remove = [1, 5]
>>> to_remove = ", ".join([str(v) for v in to_remove])
>>> to_remove
'1, 5'
>>> table.delete(f"x IN ({to_remove})")
DeleteResult(version=3)
>>> table.to_pandas()
   x      vector
0  3  [5.0, 6.0]

            
              Source code in `lancedb/table.py`
              
4172
4173
4174
4175
4176
4177
4178
4179
4180
4181
4182
4183
4184
4185
4186
4187
4188
4189
4190
4191
4192
4193
4194
4195
4196
4197
4198
4199
4200
4201
4202
4203
4204
4205
4206
4207
4208
4209
4210
4211
4212
4213
4214
4215
4216
4217
4218
4219
4220
4221
4222
async def delete(self, where: str) -> DeleteResult:
    """Delete rows from the table.

    This can be used to delete a single row, many rows, all rows, or
    sometimes no rows (if your predicate matches nothing).

    Parameters
    ----------
    where: str
        The SQL where clause to use when deleting rows.

        - For example, 'x = 2' or 'x IN (1, 2, 3)'.

        The filter must not be empty, or it will error.

    Examples
    --------
    >>> import lancedb
    >>> data = [
    ...    {"x": 1, "vector": [1.0, 2]},
    ...    {"x": 2, "vector": [3.0, 4]},
    ...    {"x": 3, "vector": [5.0, 6]}
    ... ]
    >>> db = lancedb.connect("./.lancedb")
    >>> table = db.create_table("my_table", data)
    >>> table.to_pandas()
       x      vector
    0  1  [1.0, 2.0]
    1  2  [3.0, 4.0]
    2  3  [5.0, 6.0]
    >>> table.delete("x = 2")
    DeleteResult(version=2)
    >>> table.to_pandas()
       x      vector
    0  1  [1.0, 2.0]
    1  3  [5.0, 6.0]

    If you have a list of values to delete, you can combine them into a
    stringified list and use the `IN` operator:

    >>> to_remove = [1, 5]
    >>> to_remove = ", ".join([str(v) for v in to_remove])
    >>> to_remove
    '1, 5'
    >>> table.delete(f"x IN ({to_remove})")
    DeleteResult(version=3)
    >>> table.to_pandas()
       x      vector
    0  3  [5.0, 6.0]
    """
    return await self._inner.delete(where)

            
    

            update

  
      `async`
  

¶

update(updates: Optional[Dict[str, Any]] = None, *, where: Optional[str] = None, updates_sql: Optional[Dict[str, str]] = None) -> UpdateResult

    

      
This can be used to update zero to all rows in the table.

If a filter is provided with `where` then only rows matching the
filter will be updated.  Otherwise all rows will be updated.

Parameters:

    
        
- 
          `updates`
              (`Optional[Dict[str, Any]]`, default:
                  `None`
)
          –
          
            
The updates to apply.  The keys should be the name of the column to
update.  The values should be the new values to assign.  This is
required unless updates_sql is supplied.

          
        
        
- 
          `where`
              (`Optional[str]`, default:
                  `None`
)
          –
          
            
An SQL filter that controls which rows are updated. For example, 'x = 2'
or 'x IN (1, 2, 3)'.  Only rows that satisfy this filter will be udpated.

          
        
        
- 
          `updates_sql`
              (`Optional[Dict[str, str]]`, default:
                  `None`
)
          –
          
            
The updates to apply, expressed as SQL expression strings.  The keys should
be column names. The values should be SQL expressions.  These can be SQL
literals (e.g. "7" or "'foo'") or they can be expressions based on the
previous value of the row (e.g. "x + 1" to increment the x column by 1)

          
        
    

Returns:

    
        
- 
              `UpdateResult`
          –
          
            
An object containing:
- rows_updated: The number of rows that were updated
- version: The new version number of the table after the update

          
        
    

Examples:

    
>>> import asyncio
>>> import lancedb
>>> import pandas as pd
>>> async def demo_update():
...     data = pd.DataFrame({"x": [1, 2], "vector": [[1, 2], [3, 4]]})
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.create_table("my_table", data)
...     # x is [1, 2], vector is [[1, 2], [3, 4]]
...     await table.update({"vector": [10, 10]}, where="x = 2")
...     # x is [1, 2], vector is [[1, 2], [10, 10]]
...     await table.update(updates_sql={"x": "x + 1"})
...     # x is [2, 3], vector is [[1, 2], [10, 10]]
>>> asyncio.run(demo_update())

            
              Source code in `lancedb/table.py`
              
4224
4225
4226
4227
4228
4229
4230
4231
4232
4233
4234
4235
4236
4237
4238
4239
4240
4241
4242
4243
4244
4245
4246
4247
4248
4249
4250
4251
4252
4253
4254
4255
4256
4257
4258
4259
4260
4261
4262
4263
4264
4265
4266
4267
4268
4269
4270
4271
4272
4273
4274
4275
4276
4277
4278
4279
4280
4281
4282
4283
async def update(
    self,
    updates: Optional[Dict[str, Any]] = None,
    *,
    where: Optional[str] = None,
    updates_sql: Optional[Dict[str, str]] = None,
) -> UpdateResult:
    """
    This can be used to update zero to all rows in the table.

    If a filter is provided with `where` then only rows matching the
    filter will be updated.  Otherwise all rows will be updated.

    Parameters
    ----------
    updates: dict, optional
        The updates to apply.  The keys should be the name of the column to
        update.  The values should be the new values to assign.  This is
        required unless updates_sql is supplied.
    where: str, optional
        An SQL filter that controls which rows are updated. For example, 'x = 2'
        or 'x IN (1, 2, 3)'.  Only rows that satisfy this filter will be udpated.
    updates_sql: dict, optional
        The updates to apply, expressed as SQL expression strings.  The keys should
        be column names. The values should be SQL expressions.  These can be SQL
        literals (e.g. "7" or "'foo'") or they can be expressions based on the
        previous value of the row (e.g. "x + 1" to increment the x column by 1)

    Returns
    -------
    UpdateResult
        An object containing:
        - rows_updated: The number of rows that were updated
        - version: The new version number of the table after the update

    Examples
    --------
    >>> import asyncio
    >>> import lancedb
    >>> import pandas as pd
    >>> async def demo_update():
    ...     data = pd.DataFrame({"x": [1, 2], "vector": [[1, 2], [3, 4]]})
    ...     db = await lancedb.connect_async("./.lancedb")
    ...     table = await db.create_table("my_table", data)
    ...     # x is [1, 2], vector is [[1, 2], [3, 4]]
    ...     await table.update({"vector": [10, 10]}, where="x = 2")
    ...     # x is [1, 2], vector is [[1, 2], [10, 10]]
    ...     await table.update(updates_sql={"x": "x + 1"})
    ...     # x is [2, 3], vector is [[1, 2], [10, 10]]
    >>> asyncio.run(demo_update())
    """
    if updates is not None and updates_sql is not None:
        raise ValueError("Only one of updates or updates_sql can be provided")
    if updates is None and updates_sql is None:
        raise ValueError("Either updates or updates_sql must be provided")

    if updates is not None:
        updates_sql = {k: value_to_sql(v) for k, v in updates.items()}

    return await self._inner.update(updates_sql, where)

            
    

            add_columns

  
      `async`
  

¶

add_columns(transforms: dict[str, str] | field | List[field] | Schema) -> AddColumnsResult

    

      
Add new columns with defined values.

Parameters:

    
        
- 
          `transforms`
              (`dict[str, str] | field | List[field] | Schema`)
          –
          
            
A map of column name to a SQL expression to use to calculate the
value of the new column. These expressions will be evaluated for
each row in the table, and can reference existing columns.
Alternatively, you can pass a pyarrow field or schema to add
new columns with NULLs.

          
        
    

Returns:

    
        
- 
              `AddColumnsResult`
          –
          
            
version: the new version number of the table after adding columns.

          
        
    

            
              Source code in `lancedb/table.py`
              
4285
4286
4287
4288
4289
4290
4291
4292
4293
4294
4295
4296
4297
4298
4299
4300
4301
4302
4303
4304
4305
4306
4307
4308
4309
4310
4311
4312
4313
4314
4315
async def add_columns(
    self, transforms: dict[str, str] | pa.field | List[pa.field] | pa.Schema
) -> AddColumnsResult:
    """
    Add new columns with defined values.

    Parameters
    ----------
    transforms: Dict[str, str]
        A map of column name to a SQL expression to use to calculate the
        value of the new column. These expressions will be evaluated for
        each row in the table, and can reference existing columns.
        Alternatively, you can pass a pyarrow field or schema to add
        new columns with NULLs.

    Returns
    -------
    AddColumnsResult
        version: the new version number of the table after adding columns.

    """
    if isinstance(transforms, pa.Field):
        transforms = [transforms]
    if isinstance(transforms, list) and all(
        {isinstance(f, pa.Field) for f in transforms}
    ):
        transforms = pa.schema(transforms)
    if isinstance(transforms, pa.Schema):
        return await self._inner.add_columns_with_schema(transforms)
    else:
        return await self._inner.add_columns(list(transforms.items()))

            
    

            alter_columns

  
      `async`
  

¶

alter_columns(*alterations: Iterable[dict[str, Any]]) -> AlterColumnsResult

    

      
Alter column names and nullability.

alterations : Iterable[Dict[str, Any]]
    A sequence of dictionaries, each with the following keys:
    - "path": str
        The column path to alter. For a top-level column, this is the name.
        For a nested column, this is the dot-separated path, e.g. "a.b.c".
    - "rename": str, optional
        The new name of the column. If not specified, the column name is
        not changed.
    - "data_type": pyarrow.DataType, optional
       The new data type of the column. Existing values will be casted
       to this type. If not specified, the column data type is not changed.
    - "nullable": bool, optional
        Whether the column should be nullable. If not specified, the column
        nullability is not changed. Only non-nullable columns can be changed
        to nullable. Currently, you cannot change a nullable column to
        non-nullable.

Returns:

    
        
- 
              `AlterColumnsResult`
          –
          
            
version: the new version number of the table after the alteration.

          
        
    

            
              Source code in `lancedb/table.py`
              
4317
4318
4319
4320
4321
4322
4323
4324
4325
4326
4327
4328
4329
4330
4331
4332
4333
4334
4335
4336
4337
4338
4339
4340
4341
4342
4343
4344
4345
async def alter_columns(
    self, *alterations: Iterable[dict[str, Any]]
) -> AlterColumnsResult:
    """
    Alter column names and nullability.

    alterations : Iterable[Dict[str, Any]]
        A sequence of dictionaries, each with the following keys:
        - "path": str
            The column path to alter. For a top-level column, this is the name.
            For a nested column, this is the dot-separated path, e.g. "a.b.c".
        - "rename": str, optional
            The new name of the column. If not specified, the column name is
            not changed.
        - "data_type": pyarrow.DataType, optional
           The new data type of the column. Existing values will be casted
           to this type. If not specified, the column data type is not changed.
        - "nullable": bool, optional
            Whether the column should be nullable. If not specified, the column
            nullability is not changed. Only non-nullable columns can be changed
            to nullable. Currently, you cannot change a nullable column to
            non-nullable.

    Returns
    -------
    AlterColumnsResult
        version: the new version number of the table after the alteration.
    """
    return await self._inner.alter_columns(alterations)

            
    

            drop_columns

  
      `async`
  

¶

drop_columns(columns: Iterable[str])

    

      
Drop columns from the table.

Parameters:

    
        
- 
          `columns`
              (`Iterable[str]`)
          –
          
            
The names of the columns to drop.

          
        
    

            
              Source code in `lancedb/table.py`
              
4347
4348
4349
4350
4351
4352
4353
4354
4355
4356
async def drop_columns(self, columns: Iterable[str]):
    """
    Drop columns from the table.

    Parameters
    ----------
    columns : Iterable[str]
        The names of the columns to drop.
    """
    return await self._inner.drop_columns(columns)

            
    

            version

  
      `async`
  

¶

version() -> int

    

      
Retrieve the version of the table

LanceDb supports versioning.  Every operation that modifies the table increases
version.  As long as a version hasn't been deleted you can `[Self::checkout]`
that version to view the data at that point.  In addition, you can
`[Self::restore]` the version to replace the current table with a previous
version.

            
              Source code in `lancedb/table.py`
              
4358
4359
4360
4361
4362
4363
4364
4365
4366
4367
4368
async def version(self) -> int:
    """
    Retrieve the version of the table

    LanceDb supports versioning.  Every operation that modifies the table increases
    version.  As long as a version hasn't been deleted you can `[Self::checkout]`
    that version to view the data at that point.  In addition, you can
    `[Self::restore]` the version to replace the current table with a previous
    version.
    """
    return await self._inner.version()

            
    

            list_versions

  
      `async`
  

¶

list_versions()

    

      
List all versions of the table

            
              Source code in `lancedb/table.py`
              
4370
4371
4372
4373
4374
4375
4376
4377
4378
4379
4380
4381
async def list_versions(self):
    """
    List all versions of the table
    """
    versions = await self._inner.list_versions()
    for v in versions:
        ts_nanos = v["timestamp"]
        v["timestamp"] = datetime.fromtimestamp(ts_nanos // 1e9) + timedelta(
            microseconds=(ts_nanos % 1e9) // 1e3
        )

    return versions

            
    

            checkout

  
      `async`
  

¶

checkout(version: int | str)

    

      
Checks out a specific version of the Table

Any read operation on the table will now access the data at the checked out
version. As a consequence, calling this method will disable any read consistency
interval that was previously set.

This is a read-only operation that turns the table into a sort of "view"
or "detached head".  Other table instances will not be affected.  To make the
change permanent you can use the `[Self::restore]` method.

Any operation that modifies the table will fail while the table is in a checked
out state.

Parameters:

    
        
- 
          `version`
              (`int | str`)
          –
          
            
The version to check out. A version number (`int`) or a tag
(`str`) can be provided.

          
        
        
- 
          `To`
          –
          
            
          
        
    

            
              Source code in `lancedb/table.py`
              
4383
4384
4385
4386
4387
4388
4389
4390
4391
4392
4393
4394
4395
4396
4397
4398
4399
4400
4401
4402
4403
4404
4405
4406
4407
4408
4409
4410
4411
4412
4413
4414
async def checkout(self, version: int | str):
    """
    Checks out a specific version of the Table

    Any read operation on the table will now access the data at the checked out
    version. As a consequence, calling this method will disable any read consistency
    interval that was previously set.

    This is a read-only operation that turns the table into a sort of "view"
    or "detached head".  Other table instances will not be affected.  To make the
    change permanent you can use the `[Self::restore]` method.

    Any operation that modifies the table will fail while the table is in a checked
    out state.

    Parameters
    ----------
    version: int | str,
        The version to check out. A version number (`int`) or a tag
        (`str`) can be provided.

    To return the table to a normal state use `[Self::checkout_latest]`
    """
    try:
        await self._inner.checkout(version)
    except RuntimeError as e:
        if "not found" in str(e):
            raise ValueError(
                f"Version {version} no longer exists. Was it cleaned up?"
            )
        else:
            raise

            
    

            checkout_latest

  
      `async`
  

¶

checkout_latest()

    

      
Ensures the table is pointing at the latest version

This can be used to manually update a table when the read_consistency_interval
is None
It can also be used to undo a `[Self::checkout]` operation

            
              Source code in `lancedb/table.py`
              
4416
4417
4418
4419
4420
4421
4422
4423
4424
async def checkout_latest(self):
    """
    Ensures the table is pointing at the latest version

    This can be used to manually update a table when the read_consistency_interval
    is None
    It can also be used to undo a `[Self::checkout]` operation
    """
    await self._inner.checkout_latest()

            
    

            restore

  
      `async`
  

¶

restore(version: Optional[int | str] = None)

    

      
Restore the table to the currently checked out version

This operation will fail if checkout has not been called previously

This operation will overwrite the latest version of the table with a
previous version.  Any changes made since the checked out version will
no longer be visible.

Once the operation concludes the table will no longer be in a checked
out state and the read_consistency_interval, if any, will apply.

            
              Source code in `lancedb/table.py`
              
4426
4427
4428
4429
4430
4431
4432
4433
4434
4435
4436
4437
4438
4439
async def restore(self, version: Optional[int | str] = None):
    """
    Restore the table to the currently checked out version

    This operation will fail if checkout has not been called previously

    This operation will overwrite the latest version of the table with a
    previous version.  Any changes made since the checked out version will
    no longer be visible.

    Once the operation concludes the table will no longer be in a checked
    out state and the read_consistency_interval, if any, will apply.
    """
    await self._inner.restore(version)

            
    

            take_offsets

¶

take_offsets(offsets: list[int]) -> AsyncTakeQuery

    

      
Take a list of offsets from the table.

Offsets are 0-indexed and relative to the current version of the table.  Offsets
are not stable.  A row with an offset of N may have a different offset in a
different version of the table (e.g. if an earlier row is deleted).

Offsets are mostly useful for sampling as the set of all valid offsets is easily
known in advance to be [0, len(table)).

Parameters:

    
        
- 
          `offsets`
              (`list[int]`)
          –
          
            
The offsets to take.

          
        
    

Returns:

    
        
- 
              `RecordBatch`
          –
          
            
A record batch containing the rows at the given offsets.

          
        
    

            
              Source code in `lancedb/table.py`
              
4441
4442
4443
4444
4445
4446
4447
4448
4449
4450
4451
4452
4453
4454
4455
4456
4457
4458
4459
4460
4461
4462
def take_offsets(self, offsets: list[int]) -> AsyncTakeQuery:
    """
    Take a list of offsets from the table.

    Offsets are 0-indexed and relative to the current version of the table.  Offsets
    are not stable.  A row with an offset of N may have a different offset in a
    different version of the table (e.g. if an earlier row is deleted).

    Offsets are mostly useful for sampling as the set of all valid offsets is easily
    known in advance to be [0, len(table)).

    Parameters
    ----------
    offsets: list[int]
        The offsets to take.

    Returns
    -------
    pa.RecordBatch
        A record batch containing the rows at the given offsets.
    """
    return AsyncTakeQuery(self._inner.take_offsets(offsets))

            
    

            take_row_ids

¶

take_row_ids(row_ids: list[int]) -> AsyncTakeQuery

    

      
Take a list of row ids from the table.

Row ids are not stable and are relative to the current version of the table.
They can change due to compaction and updates.

Unlike offsets, row ids are not 0-indexed and no assumptions should be made
about the possible range of row ids.  In order to use this method you must
first obtain the row ids by scanning or searching the table.

Even so, row ids are more stable than offsets and can be useful in some
situations.

There is an ongoing effort to make row ids stable which is tracked at
https://github.com/lancedb/lancedb/issues/1120

Parameters:

    
        
- 
          `row_ids`
              (`list[int]`)
          –
          
            
The row ids to take.

          
        
    

Returns:

    
        
- 
              `AsyncTakeQuery`
          –
          
            
A query object that can be executed to get the rows.

          
        
    

            
              Source code in `lancedb/table.py`
              
4464
4465
4466
4467
4468
4469
4470
4471
4472
4473
4474
4475
4476
4477
4478
4479
4480
4481
4482
4483
4484
4485
4486
4487
4488
4489
4490
4491
def take_row_ids(self, row_ids: list[int]) -> AsyncTakeQuery:
    """
    Take a list of row ids from the table.

    Row ids are not stable and are relative to the current version of the table.
    They can change due to compaction and updates.

    Unlike offsets, row ids are not 0-indexed and no assumptions should be made
    about the possible range of row ids.  In order to use this method you must
    first obtain the row ids by scanning or searching the table.

    Even so, row ids are more stable than offsets and can be useful in some
    situations.

    There is an ongoing effort to make row ids stable which is tracked at
    https://github.com/lancedb/lancedb/issues/1120

    Parameters
    ----------
    row_ids: list[int]
        The row ids to take.

    Returns
    -------
    AsyncTakeQuery
        A query object that can be executed to get the rows.
    """
    return AsyncTakeQuery(self._inner.take_row_ids(row_ids))

            
    

            optimize

  
      `async`
  

¶

optimize(*, cleanup_older_than: Optional[timedelta] = None, delete_unverified: bool = False, retrain=False) -> OptimizeStats

    

      
Optimize the on-disk data and indices for better performance.

Modeled after `VACUUM` in PostgreSQL.

Optimization covers three operations:

- Compaction: Merges small files into larger ones

- Prune: Removes old versions of the dataset

- Index: Optimizes the indices, adding new data to existing indices

Parameters:

    
        
- 
          `cleanup_older_than`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
All files belonging to versions older than this will be removed.  Set
to 0 days to remove all versions except the latest.  The latest version
is never removed.

          
        
        
- 
          `delete_unverified`
              (`bool`, default:
                  `False`
)
          –
          
            
Files leftover from a failed transaction may appear to be part of an
in-progress operation (e.g. appending new data) and these files will not
be deleted unless they are at least 7 days old. If delete_unverified is True
then these files will be deleted regardless of their age.

          
        
        
- 
          `retrain`
          –
          
            
This parameter is no longer used and is deprecated.

          
        
    

  Experimental API
  
The optimization process is undergoing active development and may change.
Our goal with these changes is to improve the performance of optimization and
reduce the complexity.

That being said, it is essential today to run optimize if you want the best
performance.  It should be stable and safe to use in production, but it our
hope that the API may be simplified (or not even need to be called) in the
future.

The frequency an application shoudl call optimize is based on the frequency of
data modifications.  If data is frequently added, deleted, or updated then
optimize should be run frequently.  A good rule of thumb is to run optimize if
you have added or modified 100,000 or more records or run more than 20 data
modification operations.

            
              Source code in `lancedb/table.py`
              
4511
4512
4513
4514
4515
4516
4517
4518
4519
4520
4521
4522
4523
4524
4525
4526
4527
4528
4529
4530
4531
4532
4533
4534
4535
4536
4537
4538
4539
4540
4541
4542
4543
4544
4545
4546
4547
4548
4549
4550
4551
4552
4553
4554
4555
4556
4557
4558
4559
4560
4561
4562
4563
4564
4565
4566
4567
4568
4569
4570
4571
4572
4573
4574
4575
4576
4577
async def optimize(
    self,
    *,
    cleanup_older_than: Optional[timedelta] = None,
    delete_unverified: bool = False,
    retrain=False,
) -> OptimizeStats:
    """
    Optimize the on-disk data and indices for better performance.

    Modeled after ``VACUUM`` in PostgreSQL.

    Optimization covers three operations:

     * Compaction: Merges small files into larger ones
     * Prune: Removes old versions of the dataset
     * Index: Optimizes the indices, adding new data to existing indices

    Parameters
    ----------
    cleanup_older_than: timedelta, optional default 7 days
        All files belonging to versions older than this will be removed.  Set
        to 0 days to remove all versions except the latest.  The latest version
        is never removed.
    delete_unverified: bool, default False
        Files leftover from a failed transaction may appear to be part of an
        in-progress operation (e.g. appending new data) and these files will not
        be deleted unless they are at least 7 days old. If delete_unverified is True
        then these files will be deleted regardless of their age.
    retrain: bool, default False
        This parameter is no longer used and is deprecated.

    Experimental API
    ----------------

    The optimization process is undergoing active development and may change.
    Our goal with these changes is to improve the performance of optimization and
    reduce the complexity.

    That being said, it is essential today to run optimize if you want the best
    performance.  It should be stable and safe to use in production, but it our
    hope that the API may be simplified (or not even need to be called) in the
    future.

    The frequency an application shoudl call optimize is based on the frequency of
    data modifications.  If data is frequently added, deleted, or updated then
    optimize should be run frequently.  A good rule of thumb is to run optimize if
    you have added or modified 100,000 or more records or run more than 20 data
    modification operations.
    """
    cleanup_since_ms: Optional[int] = None
    if cleanup_older_than is not None:
        cleanup_since_ms = round(cleanup_older_than.total_seconds() * 1000)

    if retrain:
        import warnings

        warnings.warn(
            "The 'retrain' parameter is deprecated and will be removed in a "
            "future version.",
            DeprecationWarning,
        )

    return await self._inner.optimize(
        cleanup_since_ms=cleanup_since_ms,
        delete_unverified=delete_unverified,
    )

            
    

            list_indices

  
      `async`
  

¶

list_indices() -> Iterable[IndexConfig]

    

      
List all indices that have been created with Self::create_index

            
              Source code in `lancedb/table.py`
              
4579
4580
4581
4582
4583
async def list_indices(self) -> Iterable[IndexConfig]:
    """
    List all indices that have been created with Self::create_index
    """
    return await self._inner.list_indices()

            
    

            index_stats

  
      `async`
  

¶

index_stats(index_name: str) -> Optional[IndexStatistics]

    

      
Retrieve statistics about an index

Parameters:

    
        
- 
          `index_name`
              (`str`)
          –
          
            
The name of the index to retrieve statistics for

          
        
    

Returns:

    
        
- 
              `IndexStatistics or None`
          –
          
            
The statistics about the index. Returns None if the index does not exist.

          
        
    

            
              Source code in `lancedb/table.py`
              
4585
4586
4587
4588
4589
4590
4591
4592
4593
4594
4595
4596
4597
4598
4599
4600
4601
4602
4603
async def index_stats(self, index_name: str) -> Optional[IndexStatistics]:
    """
    Retrieve statistics about an index

    Parameters
    ----------
    index_name: str
        The name of the index to retrieve statistics for

    Returns
    -------
    IndexStatistics or None
        The statistics about the index. Returns None if the index does not exist.
    """
    stats = await self._inner.index_stats(index_name)
    if stats is None:
        return None
    else:
        return IndexStatistics(**stats)

            
    

            uses_v2_manifest_paths

  
      `async`
  

¶

uses_v2_manifest_paths() -> bool

    

      
Check if the table is using the new v2 manifest paths.

Returns:

    
        
- 
              `bool`
          –
          
            
True if the table is using the new v2 manifest paths, False otherwise.

          
        
    

            
              Source code in `lancedb/table.py`
              
4605
4606
4607
4608
4609
4610
4611
4612
4613
4614
async def uses_v2_manifest_paths(self) -> bool:
    """
    Check if the table is using the new v2 manifest paths.

    Returns
    -------
    bool
        True if the table is using the new v2 manifest paths, False otherwise.
    """
    return await self._inner.uses_v2_manifest_paths()

            
    

            migrate_manifest_paths_v2

  
      `async`
  

¶

migrate_manifest_paths_v2()

    

      
Migrate the manifest paths to the new format.

This will update the manifest to use the new v2 format for paths.

This function is idempotent, and can be run multiple times without
changing the state of the object store.

Danger

This should not be run while other concurrent operations are happening.
And it should also run until completion before resuming other operations.

You can use
AsyncTable.uses_v2_manifest_paths
to check if the table is already using the new path style.

            
              Source code in `lancedb/table.py`
              
4616
4617
4618
4619
4620
4621
4622
4623
4624
4625
4626
4627
4628
4629
4630
4631
4632
4633
4634
async def migrate_manifest_paths_v2(self):
    """
    Migrate the manifest paths to the new format.

    This will update the manifest to use the new v2 format for paths.

    This function is idempotent, and can be run multiple times without
    changing the state of the object store.

    !!! danger

        This should not be run while other concurrent operations are happening.
        And it should also run until completion before resuming other operations.

    You can use
    [AsyncTable.uses_v2_manifest_paths][lancedb.table.AsyncTable.uses_v2_manifest_paths]
    to check if the table is already using the new path style.
    """
    await self._inner.migrate_manifest_paths_v2()

            
    

            replace_field_metadata

  
      `async`
  

¶

replace_field_metadata(field_name: str, new_metadata: dict[str, str])

    

      
Replace the metadata of a field in the schema

Parameters:

    
        
- 
          `field_name`
              (`str`)
          –
          
            
The name of the field to replace the metadata for

          
        
        
- 
          `new_metadata`
              (`dict[str, str]`)
          –
          
            
The new metadata to set

          
        
    

            
              Source code in `lancedb/table.py`
              
4636
4637
4638
4639
4640
4641
4642
4643
4644
4645
4646
4647
4648
4649
async def replace_field_metadata(
    self, field_name: str, new_metadata: dict[str, str]
):
    """
    Replace the metadata of a field in the schema

    Parameters
    ----------
    field_name: str
        The name of the field to replace the metadata for
    new_metadata: dict
        The new metadata to set
    """
    await self._inner.replace_field_metadata(field_name, new_metadata)

            
    

  

    

            lancedb.table.AsyncTags

¶

    

      
Async table tag manager.

              
                Source code in `lancedb/table.py`
                
4833
4834
4835
4836
4837
4838
4839
4840
4841
4842
4843
4844
4845
4846
4847
4848
4849
4850
4851
4852
4853
4854
4855
4856
4857
4858
4859
4860
4861
4862
4863
4864
4865
4866
4867
4868
4869
4870
4871
4872
4873
4874
4875
4876
4877
4878
4879
4880
4881
4882
4883
4884
4885
4886
4887
4888
4889
4890
4891
4892
4893
4894
4895
4896
4897
4898
4899
class AsyncTags:
    """
    Async table tag manager.
    """

    def __init__(self, table):
        self._table = table

    async def list(self) -> Dict[str, Tag]:
        """
        List all table tags.

        Returns
        -------
        dict[str, Tag]
            A dictionary mapping tag names to version numbers.
        """
        return await self._table.tags.list()

    async def get_version(self, tag: str) -> int:
        """
        Get the version of a tag.

        Parameters
        ----------
        tag: str,
            The name of the tag to get the version for.
        """
        return await self._table.tags.get_version(tag)

    async def create(self, tag: str, version: int) -> None:
        """
        Create a tag for a given table version.

        Parameters
        ----------
        tag: str,
            The name of the tag to create. This name must be unique among all tag
            names for the table.
        version: int,
            The table version to tag.
        """
        await self._table.tags.create(tag, version)

    async def delete(self, tag: str) -> None:
        """
        Delete tag from the table.

        Parameters
        ----------
        tag: str,
            The name of the tag to delete.
        """
        await self._table.tags.delete(tag)

    async def update(self, tag: str, version: int) -> None:
        """
        Update tag to a new version.

        Parameters
        ----------
        tag: str,
            The name of the tag to update.
        version: int,
            The new table version to tag.
        """
        await self._table.tags.update(tag, version)

              

  

            list

  
      `async`
  

¶

list() -> Dict[str, Tag]

    

      
List all table tags.

Returns:

    
        
- 
              `dict[str, Tag]`
          –
          
            
A dictionary mapping tag names to version numbers.

          
        
    

            
              Source code in `lancedb/table.py`
              
4841
4842
4843
4844
4845
4846
4847
4848
4849
4850
async def list(self) -> Dict[str, Tag]:
    """
    List all table tags.

    Returns
    -------
    dict[str, Tag]
        A dictionary mapping tag names to version numbers.
    """
    return await self._table.tags.list()

            
    

            get_version

  
      `async`
  

¶

get_version(tag: str) -> int

    

      
Get the version of a tag.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to get the version for.

          
        
    

            
              Source code in `lancedb/table.py`
              
4852
4853
4854
4855
4856
4857
4858
4859
4860
4861
async def get_version(self, tag: str) -> int:
    """
    Get the version of a tag.

    Parameters
    ----------
    tag: str,
        The name of the tag to get the version for.
    """
    return await self._table.tags.get_version(tag)

            
    

            create

  
      `async`
  

¶

create(tag: str, version: int) -> None

    

      
Create a tag for a given table version.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to create. This name must be unique among all tag
names for the table.

          
        
        
- 
          `version`
              (`int`)
          –
          
            
The table version to tag.

          
        
    

            
              Source code in `lancedb/table.py`
              
4863
4864
4865
4866
4867
4868
4869
4870
4871
4872
4873
4874
4875
async def create(self, tag: str, version: int) -> None:
    """
    Create a tag for a given table version.

    Parameters
    ----------
    tag: str,
        The name of the tag to create. This name must be unique among all tag
        names for the table.
    version: int,
        The table version to tag.
    """
    await self._table.tags.create(tag, version)

            
    

            delete

  
      `async`
  

¶

delete(tag: str) -> None

    

      
Delete tag from the table.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to delete.

          
        
    

            
              Source code in `lancedb/table.py`
              
4877
4878
4879
4880
4881
4882
4883
4884
4885
4886
async def delete(self, tag: str) -> None:
    """
    Delete tag from the table.

    Parameters
    ----------
    tag: str,
        The name of the tag to delete.
    """
    await self._table.tags.delete(tag)

            
    

            update

  
      `async`
  

¶

update(tag: str, version: int) -> None

    

      
Update tag to a new version.

Parameters:

    
        
- 
          `tag`
              (`str`)
          –
          
            
The name of the tag to update.

          
        
        
- 
          `version`
              (`int`)
          –
          
            
The new table version to tag.

          
        
    

            
              Source code in `lancedb/table.py`
              
4888
4889
4890
4891
4892
4893
4894
4895
4896
4897
4898
4899
async def update(self, tag: str, version: int) -> None:
    """
    Update tag to a new version.

    Parameters
    ----------
    tag: str,
        The name of the tag to update.
    version: int,
        The new table version to tag.
    """
    await self._table.tags.update(tag, version)

            
    

  

    

## Indices (Asynchronous)¶

Indices can be created on a table to speed up queries. This section
lists the indices that LanceDb supports.

            lancedb.index.BTree

  
      `dataclass`
  

¶

    

      
Describes a btree index configuration

A btree index is an index on scalar columns.  The index stores a copy of the
column in sorted order.  A header entry is created for each block of rows
(currently the block size is fixed at 4096).  These header entries are stored
in a separate cacheable structure (a btree).  To search for data the header is
used to determine which blocks need to be read from disk.

For example, a btree index in a table with 1Bi rows requires
sizeof(Scalar) * 256Ki bytes of memory and will generally need to read
sizeof(Scalar) * 4096 bytes to find the correct row ids.

This index is good for scalar columns with mostly distinct values and does best
when the query is highly selective. It works with numeric, temporal, and string
columns.

The btree index does not currently have any parameters though parameters such as
the block size may be added in the future.

              
                Source code in `lancedb/index.py`
                
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
@dataclass
class BTree:
    """Describes a btree index configuration

    A btree index is an index on scalar columns.  The index stores a copy of the
    column in sorted order.  A header entry is created for each block of rows
    (currently the block size is fixed at 4096).  These header entries are stored
    in a separate cacheable structure (a btree).  To search for data the header is
    used to determine which blocks need to be read from disk.

    For example, a btree index in a table with 1Bi rows requires
    sizeof(Scalar) * 256Ki bytes of memory and will generally need to read
    sizeof(Scalar) * 4096 bytes to find the correct row ids.

    This index is good for scalar columns with mostly distinct values and does best
    when the query is highly selective. It works with numeric, temporal, and string
    columns.

    The btree index does not currently have any parameters though parameters such as
    the block size may be added in the future.
    """

    pass

              

  

  

    

            lancedb.index.Bitmap

  
      `dataclass`
  

¶

    

      
Describe a Bitmap index configuration.

A `Bitmap` index stores a bitmap for each distinct value in the column for
every row.

This index works best for low-cardinality numeric or string columns,
where the number of unique values is small (i.e., less than a few thousands).
`Bitmap` index can accelerate the following filters:

- `<`, `<=`, `=`, `>`, `>=`

- `IN (value1, value2, ...)`

- `between (value1, value2)`

- `is null`

For example, a bitmap index with a table with 1Bi rows, and 128 distinct values,
requires 128 / 8 * 1Bi bytes on disk.

              
                Source code in `lancedb/index.py`
                
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
@dataclass
class Bitmap:
    """Describe a Bitmap index configuration.

    A `Bitmap` index stores a bitmap for each distinct value in the column for
    every row.

    This index works best for low-cardinality numeric or string columns,
    where the number of unique values is small (i.e., less than a few thousands).
    `Bitmap` index can accelerate the following filters:

    - `<`, `<=`, `=`, `>`, `>=`
    - `IN (value1, value2, ...)`
    - `between (value1, value2)`
    - `is null`

    For example, a bitmap index with a table with 1Bi rows, and 128 distinct values,
    requires 128 / 8 * 1Bi bytes on disk.
    """

    pass

              

  

  

    

            lancedb.index.LabelList

  
      `dataclass`
  

¶

    

      
Describe a LabelList index configuration.

`LabelList` is a scalar index that can be used on `List<T>` columns to
support queries with `array_contains_all` and `array_contains_any`
using an underlying bitmap index.

For example, it works with `tags`, `categories`, `keywords`, etc.

              
                Source code in `lancedb/index.py`
                
81
82
83
84
85
86
87
88
89
90
91
92
@dataclass
class LabelList:
    """Describe a LabelList index configuration.

    `LabelList` is a scalar index that can be used on `List<T>` columns to
    support queries with `array_contains_all` and `array_contains_any`
    using an underlying bitmap index.

    For example, it works with `tags`, `categories`, `keywords`, etc.
    """

    pass

              

  

  

    

            lancedb.index.FTS

  
      `dataclass`
  

¶

    

      
Describe a FTS index configuration.

`FTS` is a full-text search index that can be used on `String` columns

For example, it works with `title`, `description`, `content`, etc.

Attributes:

    
        
- 
          `with_position`
              (`bool, default False`)
          –
          
            
Whether to store the position of the token in the document. Setting this
to False can reduce the size of the index and improve indexing speed,
but it will disable support for phrase queries.

          
        
        
- 
          `base_tokenizer`
              (`str, default "simple"`)
          –
          
            
The base tokenizer to use for tokenization. Options are:
- "simple": Splits text by whitespace and punctuation.
- "whitespace": Split text by whitespace, but not punctuation.
- "raw": No tokenization. The entire text is treated as a single token.

          
        
        
- 
          `language`
              (`str, default "English"`)
          –
          
            
The language to use for tokenization.

          
        
        
- 
          `max_token_length`
              (`int, default 40`)
          –
          
            
The maximum token length to index. Tokens longer than this length will be
ignored.

          
        
        
- 
          `lower_case`
              (`bool, default True`)
          –
          
            
Whether to convert the token to lower case. This makes queries case-insensitive.

          
        
        
- 
          `stem`
              (`bool, default True`)
          –
          
            
Whether to stem the token. Stemming reduces words to their root form.
For example, in English "running" and "runs" would both be reduced to "run".

          
        
        
- 
          `remove_stop_words`
              (`bool, default True`)
          –
          
            
Whether to remove stop words. Stop words are common words that are often
removed from text before indexing. For example, in English "the" and "and".

          
        
        
- 
          `ascii_folding`
              (`bool, default True`)
          –
          
            
Whether to fold ASCII characters. This converts accented characters to
their ASCII equivalent. For example, "café" would be converted to "cafe".

          
        
    

              
                Source code in `lancedb/index.py`
                
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
@dataclass
class FTS:
    """Describe a FTS index configuration.

    `FTS` is a full-text search index that can be used on `String` columns

    For example, it works with `title`, `description`, `content`, etc.

    Attributes
    ----------
    with_position : bool, default False
        Whether to store the position of the token in the document. Setting this
        to False can reduce the size of the index and improve indexing speed,
        but it will disable support for phrase queries.
    base_tokenizer : str, default "simple"
        The base tokenizer to use for tokenization. Options are:
        - "simple": Splits text by whitespace and punctuation.
        - "whitespace": Split text by whitespace, but not punctuation.
        - "raw": No tokenization. The entire text is treated as a single token.
    language : str, default "English"
        The language to use for tokenization.
    max_token_length : int, default 40
        The maximum token length to index. Tokens longer than this length will be
        ignored.
    lower_case : bool, default True
        Whether to convert the token to lower case. This makes queries case-insensitive.
    stem : bool, default True
        Whether to stem the token. Stemming reduces words to their root form.
        For example, in English "running" and "runs" would both be reduced to "run".
    remove_stop_words : bool, default True
        Whether to remove stop words. Stop words are common words that are often
        removed from text before indexing. For example, in English "the" and "and".
    ascii_folding : bool, default True
        Whether to fold ASCII characters. This converts accented characters to
        their ASCII equivalent. For example, "café" would be converted to "cafe".
    """

    with_position: bool = False
    base_tokenizer: Literal["simple", "raw", "whitespace"] = "simple"
    language: str = "English"
    max_token_length: Optional[int] = 40
    lower_case: bool = True
    stem: bool = True
    remove_stop_words: bool = True
    ascii_folding: bool = True
    ngram_min_length: int = 3
    ngram_max_length: int = 3
    prefix_only: bool = False

              

  

  

    

            lancedb.index.IvfPq

  
      `dataclass`
  

¶

    

      
Describes an IVF PQ Index

This index stores a compressed (quantized) copy of every vector.  These vectors
are grouped into partitions of similar vectors.  Each partition keeps track of
a centroid which is the average value of all vectors in the group.

During a query the centroids are compared with the query vector to find the
closest partitions.  The compressed vectors in these partitions are then
searched to find the closest vectors.

The compression scheme is called product quantization.  Each vector is divide
into subvectors and then each subvector is quantized into a small number of
bits.  the parameters `num_bits` and `num_subvectors` control this process,
providing a tradeoff between index size (and thus search speed) and index
accuracy.

The partitioning process is called IVF and the `num_partitions` parameter
controls how many groups to create.

Note that training an IVF PQ index on a large dataset is a slow operation and
currently is also a memory intensive operation.

Attributes:

    
        
- 
          `distance_type`
              (`str, default "l2"`)
          –
          
            
The distance metric used to train the index

This is used when training the index to calculate the IVF partitions
(vectors are grouped in partitions with similar vectors according to this
distance type) and to calculate a subvector's code during quantization.

The distance type used to train an index MUST match the distance type used
to search the index.  Failure to do so will yield inaccurate results.

The following distance types are available:

"l2" - Euclidean distance. This is a very common distance metric that
accounts for both magnitude and direction when determining the distance
between vectors. l2 distance has a range of [0, ∞).

"cosine" - Cosine distance.  Cosine distance is a distance metric
calculated from the cosine similarity between two vectors. Cosine
similarity is a measure of similarity between two non-zero vectors of an
inner product space. It is defined to equal the cosine of the angle
between them.  Unlike l2, the cosine distance is not affected by the
magnitude of the vectors.  Cosine distance has a range of [0, 2].

Note: the cosine distance is undefined when one (or both) of the vectors
are all zeros (there is no direction).  These vectors are invalid and may
never be returned from a vector search.

"dot" - Dot product. Dot distance is the dot product of two vectors. Dot
distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
l2 norm is 1), then dot distance is equivalent to the cosine distance.

          
        
        
- 
          `num_partitions`
              (`int, default sqrt(num_rows)`)
          –
          
            
The number of IVF partitions to create.

This value should generally scale with the number of rows in the dataset.
By default the number of partitions is the square root of the number of
rows.

If this value is too large then the first part of the search (picking the
right partition) will be slow.  If this value is too small then the second
part of the search (searching within a partition) will be slow.

          
        
        
- 
          `num_sub_vectors`
              (`int, default is vector dimension / 16`)
          –
          
            
Number of sub-vectors of PQ.

This value controls how much the vector is compressed during the
quantization step.  The more sub vectors there are the less the vector is
compressed.  The default is the dimension of the vector divided by 16.  If
the dimension is not evenly divisible by 16 we use the dimension divded by
8.

The above two cases are highly preferred.  Having 8 or 16 values per
subvector allows us to use efficient SIMD instructions.

If the dimension is not visible by 8 then we use 1 subvector.  This is not
ideal and will likely result in poor performance.

          
        
        
- 
          `num_bits`
              (`int, default 8`)
          –
          
            
Number of bits to encode each sub-vector.

This value controls how much the sub-vectors are compressed.  The more bits
the more accurate the index but the slower search.  The default is 8
bits.  Only 4 and 8 are supported.

          
        
        
- 
          `max_iterations`
              (`int, default 50`)
          –
          
            
Max iteration to train kmeans.

When training an IVF PQ index we use kmeans to calculate the partitions.
This parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases
these extra iterations have diminishing returns.

The default value is 50.

          
        
        
- 
          `sample_rate`
              (`int, default 256`)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF PQ index is trained, we need to calculate partitions.  These
are groups of vectors that are similar to each other.  To do this we use an
algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we run
kmeans on a random sample of the data.  This parameter controls the size of
the sample.  The total number of vectors used to train the index is
`sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in most
cases the default should be sufficient.

The default value is 256.

          
        
        
- 
          `target_partition_size, default is 8192`
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
    

              
                Source code in `lancedb/index.py`
                
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
@dataclass
class IvfPq:
    """Describes an IVF PQ Index

    This index stores a compressed (quantized) copy of every vector.  These vectors
    are grouped into partitions of similar vectors.  Each partition keeps track of
    a centroid which is the average value of all vectors in the group.

    During a query the centroids are compared with the query vector to find the
    closest partitions.  The compressed vectors in these partitions are then
    searched to find the closest vectors.

    The compression scheme is called product quantization.  Each vector is divide
    into subvectors and then each subvector is quantized into a small number of
    bits.  the parameters `num_bits` and `num_subvectors` control this process,
    providing a tradeoff between index size (and thus search speed) and index
    accuracy.

    The partitioning process is called IVF and the `num_partitions` parameter
    controls how many groups to create.

    Note that training an IVF PQ index on a large dataset is a slow operation and
    currently is also a memory intensive operation.

    Attributes
    ----------
    distance_type: str, default "l2"
        The distance metric used to train the index

        This is used when training the index to calculate the IVF partitions
        (vectors are grouped in partitions with similar vectors according to this
        distance type) and to calculate a subvector's code during quantization.

        The distance type used to train an index MUST match the distance type used
        to search the index.  Failure to do so will yield inaccurate results.

        The following distance types are available:

        "l2" - Euclidean distance. This is a very common distance metric that
        accounts for both magnitude and direction when determining the distance
        between vectors. l2 distance has a range of [0, ∞).

        "cosine" - Cosine distance.  Cosine distance is a distance metric
        calculated from the cosine similarity between two vectors. Cosine
        similarity is a measure of similarity between two non-zero vectors of an
        inner product space. It is defined to equal the cosine of the angle
        between them.  Unlike l2, the cosine distance is not affected by the
        magnitude of the vectors.  Cosine distance has a range of [0, 2].

        Note: the cosine distance is undefined when one (or both) of the vectors
        are all zeros (there is no direction).  These vectors are invalid and may
        never be returned from a vector search.

        "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
        distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
        l2 norm is 1), then dot distance is equivalent to the cosine distance.
    num_partitions: int, default sqrt(num_rows)
        The number of IVF partitions to create.

        This value should generally scale with the number of rows in the dataset.
        By default the number of partitions is the square root of the number of
        rows.

        If this value is too large then the first part of the search (picking the
        right partition) will be slow.  If this value is too small then the second
        part of the search (searching within a partition) will be slow.
    num_sub_vectors: int, default is vector dimension / 16
        Number of sub-vectors of PQ.

        This value controls how much the vector is compressed during the
        quantization step.  The more sub vectors there are the less the vector is
        compressed.  The default is the dimension of the vector divided by 16.  If
        the dimension is not evenly divisible by 16 we use the dimension divded by
        8.

        The above two cases are highly preferred.  Having 8 or 16 values per
        subvector allows us to use efficient SIMD instructions.

        If the dimension is not visible by 8 then we use 1 subvector.  This is not
        ideal and will likely result in poor performance.
    num_bits: int, default 8
        Number of bits to encode each sub-vector.

        This value controls how much the sub-vectors are compressed.  The more bits
        the more accurate the index but the slower search.  The default is 8
        bits.  Only 4 and 8 are supported.
    max_iterations: int, default 50
        Max iteration to train kmeans.

        When training an IVF PQ index we use kmeans to calculate the partitions.
        This parameter controls how many iterations of kmeans to run.

        Increasing this might improve the quality of the index but in most cases
        these extra iterations have diminishing returns.

        The default value is 50.
    sample_rate: int, default 256
        The rate used to calculate the number of training vectors for kmeans.

        When an IVF PQ index is trained, we need to calculate partitions.  These
        are groups of vectors that are similar to each other.  To do this we use an
        algorithm called kmeans.

        Running kmeans on a large dataset can be slow.  To speed this up we run
        kmeans on a random sample of the data.  This parameter controls the size of
        the sample.  The total number of vectors used to train the index is
        `sample_rate * num_partitions`.

        Increasing this value might improve the quality of the index but in most
        cases the default should be sufficient.

        The default value is 256.

    target_partition_size, default is 8192

        The target size of each partition.

        This value controls the tradeoff between search performance and accuracy.
        faster search but less accurate results as higher value.
    """

    distance_type: Literal["l2", "cosine", "dot"] = "l2"
    num_partitions: Optional[int] = None
    num_sub_vectors: Optional[int] = None
    num_bits: int = 8
    max_iterations: int = 50
    sample_rate: int = 256
    target_partition_size: Optional[int] = None

              

  

  

    

            lancedb.index.HnswPq

  
      `dataclass`
  

¶

    

      
Describe a HNSW-PQ index configuration.

HNSW-PQ stands for Hierarchical Navigable Small World - Product Quantization.
It is a variant of the HNSW algorithm that uses product quantization to compress
the vectors. To create an HNSW-PQ index, you can specify the following parameters:

Parameters:

    
        
- 
          `distance_type`
              (`Literal['l2', 'cosine', 'dot']`, default:
                  `'l2'`
)
          –
          
            
The distance metric used to train the index.

The following distance types are available:

"l2" - Euclidean distance. This is a very common distance metric that
accounts for both magnitude and direction when determining the distance
between vectors. l2 distance has a range of [0, ∞).

"cosine" - Cosine distance.  Cosine distance is a distance metric
calculated from the cosine similarity between two vectors. Cosine
similarity is a measure of similarity between two non-zero vectors of an
inner product space. It is defined to equal the cosine of the angle
between them.  Unlike l2, the cosine distance is not affected by the
magnitude of the vectors.  Cosine distance has a range of [0, 2].

"dot" - Dot product. Dot distance is the dot product of two vectors. Dot
distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
l2 norm is 1), then dot distance is equivalent to the cosine distance.

          
        
        
- 
          `num_partitions`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The number of IVF partitions to create.

For HNSW, we recommend a small number of partitions. Setting this to 1 works
well for most tables. For very large tables, training just one HNSW graph
will require too much memory. Each partition becomes its own HNSW graph, so
setting this value higher reduces the peak memory use of training.

          
        
        
- 
          `default`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The number of IVF partitions to create.

For HNSW, we recommend a small number of partitions. Setting this to 1 works
well for most tables. For very large tables, training just one HNSW graph
will require too much memory. Each partition becomes its own HNSW graph, so
setting this value higher reduces the peak memory use of training.

          
        
        
- 
          `num_sub_vectors`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
Number of sub-vectors of PQ.

This value controls how much the vector is compressed during the
quantization step. The more sub vectors there are the less the vector is
compressed.  The default is the dimension of the vector divided by 16.
If the dimension is not evenly divisible by 16 we use the dimension
divided by 8.

The above two cases are highly preferred.  Having 8 or 16 values per
subvector allows us to use efficient SIMD instructions.

If the dimension is not visible by 8 then we use 1 subvector.  This is not
ideal and will likely result in poor performance.

num_bits: int, default 8
Number of bits to encode each sub-vector.

This value controls how much the sub-vectors are compressed.  The more bits
the more accurate the index but the slower search. Only 4 and 8 are supported.

          
        
        
- 
          `default`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
Number of sub-vectors of PQ.

This value controls how much the vector is compressed during the
quantization step. The more sub vectors there are the less the vector is
compressed.  The default is the dimension of the vector divided by 16.
If the dimension is not evenly divisible by 16 we use the dimension
divided by 8.

The above two cases are highly preferred.  Having 8 or 16 values per
subvector allows us to use efficient SIMD instructions.

If the dimension is not visible by 8 then we use 1 subvector.  This is not
ideal and will likely result in poor performance.

num_bits: int, default 8
Number of bits to encode each sub-vector.

This value controls how much the sub-vectors are compressed.  The more bits
the more accurate the index but the slower search. Only 4 and 8 are supported.

          
        
        
- 
          `max_iterations`
              (`int`, default:
                  `50`
)
          –
          
            
Max iterations to train kmeans.

When training an IVF index we use kmeans to calculate the partitions.  This
parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases the
parameter is unused because kmeans will converge with fewer iterations.  The
parameter is only used in cases where kmeans does not appear to converge.  In
those cases it is unlikely that setting this larger will lead to the index
converging anyways.

          
        
        
- 
          `default`
              (`int`, default:
                  `50`
)
          –
          
            
Max iterations to train kmeans.

When training an IVF index we use kmeans to calculate the partitions.  This
parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases the
parameter is unused because kmeans will converge with fewer iterations.  The
parameter is only used in cases where kmeans does not appear to converge.  In
those cases it is unlikely that setting this larger will lead to the index
converging anyways.

          
        
        
- 
          `sample_rate`
              (`int`, default:
                  `256`
)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF index is trained, we need to calculate partitions.  These are
groups of vectors that are similar to each other.  To do this we use an
algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we
run kmeans on a random sample of the data.  This parameter controls the
size of the sample.  The total number of vectors used to train the index
is `sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in
most cases the default should be sufficient.

          
        
        
- 
          `default`
              (`int`, default:
                  `256`
)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF index is trained, we need to calculate partitions.  These are
groups of vectors that are similar to each other.  To do this we use an
algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we
run kmeans on a random sample of the data.  This parameter controls the
size of the sample.  The total number of vectors used to train the index
is `sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in
most cases the default should be sufficient.

          
        
        
- 
          `m`
              (`int`, default:
                  `20`
)
          –
          
            
The number of neighbors to select for each vector in the HNSW graph.

This value controls the tradeoff between search speed and accuracy.
The higher the value the more accurate the search but the slower it will be.

          
        
        
- 
          `default`
              (`int`, default:
                  `20`
)
          –
          
            
The number of neighbors to select for each vector in the HNSW graph.

This value controls the tradeoff between search speed and accuracy.
The higher the value the more accurate the search but the slower it will be.

          
        
        
- 
          `ef_construction`
              (`int`, default:
                  `300`
)
          –
          
            
The number of candidates to evaluate during the construction of the HNSW graph.

This value controls the tradeoff between build speed and accuracy.
The higher the value the more accurate the build but the slower it will be.
150 to 300 is the typical range. 100 is a minimum for good quality search
results. In most cases, there is no benefit to setting this higher than 500.
This value should be set to a value that is not less than `ef` in the
search phase.

          
        
        
- 
          `default`
              (`int`, default:
                  `300`
)
          –
          
            
The number of candidates to evaluate during the construction of the HNSW graph.

This value controls the tradeoff between build speed and accuracy.
The higher the value the more accurate the build but the slower it will be.
150 to 300 is the typical range. 100 is a minimum for good quality search
results. In most cases, there is no benefit to setting this higher than 500.
This value should be set to a value that is not less than `ef` in the
search phase.

          
        
        
- 
          `target_partition_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
        
- 
          `default`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
    

              
                Source code in `lancedb/index.py`
                
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
@dataclass
class HnswPq:
    """Describe a HNSW-PQ index configuration.

    HNSW-PQ stands for Hierarchical Navigable Small World - Product Quantization.
    It is a variant of the HNSW algorithm that uses product quantization to compress
    the vectors. To create an HNSW-PQ index, you can specify the following parameters:

    Parameters
    ----------

    distance_type: str, default "l2"

        The distance metric used to train the index.

        The following distance types are available:

        "l2" - Euclidean distance. This is a very common distance metric that
        accounts for both magnitude and direction when determining the distance
        between vectors. l2 distance has a range of [0, ∞).

        "cosine" - Cosine distance.  Cosine distance is a distance metric
        calculated from the cosine similarity between two vectors. Cosine
        similarity is a measure of similarity between two non-zero vectors of an
        inner product space. It is defined to equal the cosine of the angle
        between them.  Unlike l2, the cosine distance is not affected by the
        magnitude of the vectors.  Cosine distance has a range of [0, 2].

        "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
        distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
        l2 norm is 1), then dot distance is equivalent to the cosine distance.

    num_partitions, default sqrt(num_rows)

        The number of IVF partitions to create.

        For HNSW, we recommend a small number of partitions. Setting this to 1 works
        well for most tables. For very large tables, training just one HNSW graph
        will require too much memory. Each partition becomes its own HNSW graph, so
        setting this value higher reduces the peak memory use of training.

    num_sub_vectors, default is vector dimension / 16

        Number of sub-vectors of PQ.

        This value controls how much the vector is compressed during the
        quantization step. The more sub vectors there are the less the vector is
        compressed.  The default is the dimension of the vector divided by 16.
        If the dimension is not evenly divisible by 16 we use the dimension
        divided by 8.

        The above two cases are highly preferred.  Having 8 or 16 values per
        subvector allows us to use efficient SIMD instructions.

        If the dimension is not visible by 8 then we use 1 subvector.  This is not
        ideal and will likely result in poor performance.

     num_bits: int, default 8
        Number of bits to encode each sub-vector.

        This value controls how much the sub-vectors are compressed.  The more bits
        the more accurate the index but the slower search. Only 4 and 8 are supported.

    max_iterations, default 50

        Max iterations to train kmeans.

        When training an IVF index we use kmeans to calculate the partitions.  This
        parameter controls how many iterations of kmeans to run.

        Increasing this might improve the quality of the index but in most cases the
        parameter is unused because kmeans will converge with fewer iterations.  The
        parameter is only used in cases where kmeans does not appear to converge.  In
        those cases it is unlikely that setting this larger will lead to the index
        converging anyways.

    sample_rate, default 256

        The rate used to calculate the number of training vectors for kmeans.

        When an IVF index is trained, we need to calculate partitions.  These are
        groups of vectors that are similar to each other.  To do this we use an
        algorithm called kmeans.

        Running kmeans on a large dataset can be slow.  To speed this up we
        run kmeans on a random sample of the data.  This parameter controls the
        size of the sample.  The total number of vectors used to train the index
        is `sample_rate * num_partitions`.

        Increasing this value might improve the quality of the index but in
        most cases the default should be sufficient.

    m, default 20

        The number of neighbors to select for each vector in the HNSW graph.

        This value controls the tradeoff between search speed and accuracy.
        The higher the value the more accurate the search but the slower it will be.

    ef_construction, default 300

        The number of candidates to evaluate during the construction of the HNSW graph.

        This value controls the tradeoff between build speed and accuracy.
        The higher the value the more accurate the build but the slower it will be.
        150 to 300 is the typical range. 100 is a minimum for good quality search
        results. In most cases, there is no benefit to setting this higher than 500.
        This value should be set to a value that is not less than `ef` in the
        search phase.

    target_partition_size, default is 1,048,576

        The target size of each partition.

        This value controls the tradeoff between search performance and accuracy.
        faster search but less accurate results as higher value.
    """

    distance_type: Literal["l2", "cosine", "dot"] = "l2"
    num_partitions: Optional[int] = None
    num_sub_vectors: Optional[int] = None
    num_bits: int = 8
    max_iterations: int = 50
    sample_rate: int = 256
    m: int = 20
    ef_construction: int = 300
    target_partition_size: Optional[int] = None

              

  

  

    

            lancedb.index.HnswSq

  
      `dataclass`
  

¶

    

      
Describe a HNSW-SQ index configuration.

HNSW-SQ stands for Hierarchical Navigable Small World - Scalar Quantization.
It is a variant of the HNSW algorithm that uses scalar quantization to compress
the vectors.

Parameters:

    
        
- 
          `distance_type`
              (`Literal['l2', 'cosine', 'dot']`, default:
                  `'l2'`
)
          –
          
            
The distance metric used to train the index.

The following distance types are available:

"l2" - Euclidean distance. This is a very common distance metric that
accounts for both magnitude and direction when determining the distance
between vectors. l2 distance has a range of [0, ∞).

"cosine" - Cosine distance.  Cosine distance is a distance metric
calculated from the cosine similarity between two vectors. Cosine
similarity is a measure of similarity between two non-zero vectors of an
inner product space. It is defined to equal the cosine of the angle
between them.  Unlike l2, the cosine distance is not affected by the
magnitude of the vectors.  Cosine distance has a range of [0, 2].

"dot" - Dot product. Dot distance is the dot product of two vectors. Dot
distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
l2 norm is 1), then dot distance is equivalent to the cosine distance.

          
        
        
- 
          `num_partitions`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The number of IVF partitions to create.

For HNSW, we recommend a small number of partitions. Setting this to 1 works
well for most tables. For very large tables, training just one HNSW graph
will require too much memory. Each partition becomes its own HNSW graph, so
setting this value higher reduces the peak memory use of training.

          
        
        
- 
          `default`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The number of IVF partitions to create.

For HNSW, we recommend a small number of partitions. Setting this to 1 works
well for most tables. For very large tables, training just one HNSW graph
will require too much memory. Each partition becomes its own HNSW graph, so
setting this value higher reduces the peak memory use of training.

          
        
        
- 
          `max_iterations`
              (`int`, default:
                  `50`
)
          –
          
            
Max iterations to train kmeans.

When training an IVF index we use kmeans to calculate the partitions.
This parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases
the parameter is unused because kmeans will converge with fewer iterations.
The parameter is only used in cases where kmeans does not appear to converge.
In those cases it is unlikely that setting this larger will lead to
the index converging anyways.

          
        
        
- 
          `default`
              (`int`, default:
                  `50`
)
          –
          
            
Max iterations to train kmeans.

When training an IVF index we use kmeans to calculate the partitions.
This parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases
the parameter is unused because kmeans will converge with fewer iterations.
The parameter is only used in cases where kmeans does not appear to converge.
In those cases it is unlikely that setting this larger will lead to
the index converging anyways.

          
        
        
- 
          `sample_rate`
              (`int`, default:
                  `256`
)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF index is trained, we need to calculate partitions.  These
are groups of vectors that are similar to each other.  To do this
we use an algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we
run kmeans on a random sample of the data.  This parameter controls the
size of the sample.  The total number of vectors used to train the index
is `sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in
most cases the default should be sufficient.

          
        
        
- 
          `default`
              (`int`, default:
                  `256`
)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF index is trained, we need to calculate partitions.  These
are groups of vectors that are similar to each other.  To do this
we use an algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we
run kmeans on a random sample of the data.  This parameter controls the
size of the sample.  The total number of vectors used to train the index
is `sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in
most cases the default should be sufficient.

          
        
        
- 
          `m`
              (`int`, default:
                  `20`
)
          –
          
            
The number of neighbors to select for each vector in the HNSW graph.

This value controls the tradeoff between search speed and accuracy.
The higher the value the more accurate the search but the slower it will be.

          
        
        
- 
          `default`
              (`int`, default:
                  `20`
)
          –
          
            
The number of neighbors to select for each vector in the HNSW graph.

This value controls the tradeoff between search speed and accuracy.
The higher the value the more accurate the search but the slower it will be.

          
        
        
- 
          `ef_construction`
              (`int`, default:
                  `300`
)
          –
          
            
The number of candidates to evaluate during the construction of the HNSW graph.

This value controls the tradeoff between build speed and accuracy.
The higher the value the more accurate the build but the slower it will be.
150 to 300 is the typical range. 100 is a minimum for good quality search
results. In most cases, there is no benefit to setting this higher than 500.
This value should be set to a value that is not less than `ef` in the search
phase.

          
        
        
- 
          `default`
              (`int`, default:
                  `300`
)
          –
          
            
The number of candidates to evaluate during the construction of the HNSW graph.

This value controls the tradeoff between build speed and accuracy.
The higher the value the more accurate the build but the slower it will be.
150 to 300 is the typical range. 100 is a minimum for good quality search
results. In most cases, there is no benefit to setting this higher than 500.
This value should be set to a value that is not less than `ef` in the search
phase.

          
        
        
- 
          `target_partition_size`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
        
- 
          `default`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
    

              
                Source code in `lancedb/index.py`
                
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
@dataclass
class HnswSq:
    """Describe a HNSW-SQ index configuration.

    HNSW-SQ stands for Hierarchical Navigable Small World - Scalar Quantization.
    It is a variant of the HNSW algorithm that uses scalar quantization to compress
    the vectors.

    Parameters
    ----------

    distance_type: str, default "l2"

        The distance metric used to train the index.

        The following distance types are available:

        "l2" - Euclidean distance. This is a very common distance metric that
        accounts for both magnitude and direction when determining the distance
        between vectors. l2 distance has a range of [0, ∞).

        "cosine" - Cosine distance.  Cosine distance is a distance metric
        calculated from the cosine similarity between two vectors. Cosine
        similarity is a measure of similarity between two non-zero vectors of an
        inner product space. It is defined to equal the cosine of the angle
        between them.  Unlike l2, the cosine distance is not affected by the
        magnitude of the vectors.  Cosine distance has a range of [0, 2].

        "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
        distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
        l2 norm is 1), then dot distance is equivalent to the cosine distance.

    num_partitions, default sqrt(num_rows)

        The number of IVF partitions to create.

        For HNSW, we recommend a small number of partitions. Setting this to 1 works
        well for most tables. For very large tables, training just one HNSW graph
        will require too much memory. Each partition becomes its own HNSW graph, so
        setting this value higher reduces the peak memory use of training.

    max_iterations, default 50

        Max iterations to train kmeans.

        When training an IVF index we use kmeans to calculate the partitions.
        This parameter controls how many iterations of kmeans to run.

        Increasing this might improve the quality of the index but in most cases
        the parameter is unused because kmeans will converge with fewer iterations.
        The parameter is only used in cases where kmeans does not appear to converge.
        In those cases it is unlikely that setting this larger will lead to
        the index converging anyways.

    sample_rate, default 256

        The rate used to calculate the number of training vectors for kmeans.

        When an IVF index is trained, we need to calculate partitions.  These
        are groups of vectors that are similar to each other.  To do this
        we use an algorithm called kmeans.

        Running kmeans on a large dataset can be slow.  To speed this up we
        run kmeans on a random sample of the data.  This parameter controls the
        size of the sample.  The total number of vectors used to train the index
        is `sample_rate * num_partitions`.

        Increasing this value might improve the quality of the index but in
        most cases the default should be sufficient.

    m, default 20

        The number of neighbors to select for each vector in the HNSW graph.

        This value controls the tradeoff between search speed and accuracy.
        The higher the value the more accurate the search but the slower it will be.

    ef_construction, default 300

        The number of candidates to evaluate during the construction of the HNSW graph.

        This value controls the tradeoff between build speed and accuracy.
        The higher the value the more accurate the build but the slower it will be.
        150 to 300 is the typical range. 100 is a minimum for good quality search
        results. In most cases, there is no benefit to setting this higher than 500.
        This value should be set to a value that is not less than `ef` in the search
        phase.

    target_partition_size, default is 1,048,576

        The target size of each partition.

        This value controls the tradeoff between search performance and accuracy.
        faster search but less accurate results as higher value.
    """

    distance_type: Literal["l2", "cosine", "dot"] = "l2"
    num_partitions: Optional[int] = None
    max_iterations: int = 50
    sample_rate: int = 256
    m: int = 20
    ef_construction: int = 300
    target_partition_size: Optional[int] = None

              

  

  

    

            lancedb.index.IvfFlat

  
      `dataclass`
  

¶

    

      
Describes an IVF Flat Index

This index stores raw vectors.
These vectors are grouped into partitions of similar vectors.
Each partition keeps track of a centroid which is
the average value of all vectors in the group.

Attributes:

    
        
- 
          `distance_type`
              (`str, default "l2"`)
          –
          
            
The distance metric used to train the index

This is used when training the index to calculate the IVF partitions
(vectors are grouped in partitions with similar vectors according to this
distance type) and to calculate a subvector's code during quantization.

The distance type used to train an index MUST match the distance type used
to search the index.  Failure to do so will yield inaccurate results.

The following distance types are available:

"l2" - Euclidean distance. This is a very common distance metric that
accounts for both magnitude and direction when determining the distance
between vectors. l2 distance has a range of [0, ∞).

"cosine" - Cosine distance.  Cosine distance is a distance metric
calculated from the cosine similarity between two vectors. Cosine
similarity is a measure of similarity between two non-zero vectors of an
inner product space. It is defined to equal the cosine of the angle
between them.  Unlike l2, the cosine distance is not affected by the
magnitude of the vectors.  Cosine distance has a range of [0, 2].

Note: the cosine distance is undefined when one (or both) of the vectors
are all zeros (there is no direction).  These vectors are invalid and may
never be returned from a vector search.

"dot" - Dot product. Dot distance is the dot product of two vectors. Dot
distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
l2 norm is 1), then dot distance is equivalent to the cosine distance.

"hamming" - Hamming distance. Hamming distance is a distance metric
calculated as the number of positions at which the corresponding bits are
different. Hamming distance has a range of [0, vector dimension].

          
        
        
- 
          `num_partitions`
              (`int, default sqrt(num_rows)`)
          –
          
            
The number of IVF partitions to create.

This value should generally scale with the number of rows in the dataset.
By default the number of partitions is the square root of the number of
rows.

If this value is too large then the first part of the search (picking the
right partition) will be slow.  If this value is too small then the second
part of the search (searching within a partition) will be slow.

          
        
        
- 
          `max_iterations`
              (`int, default 50`)
          –
          
            
Max iteration to train kmeans.

When training an IVF PQ index we use kmeans to calculate the partitions.
This parameter controls how many iterations of kmeans to run.

Increasing this might improve the quality of the index but in most cases
these extra iterations have diminishing returns.

The default value is 50.

          
        
        
- 
          `sample_rate`
              (`int, default 256`)
          –
          
            
The rate used to calculate the number of training vectors for kmeans.

When an IVF PQ index is trained, we need to calculate partitions.  These
are groups of vectors that are similar to each other.  To do this we use an
algorithm called kmeans.

Running kmeans on a large dataset can be slow.  To speed this up we run
kmeans on a random sample of the data.  This parameter controls the size of
the sample.  The total number of vectors used to train the index is
`sample_rate * num_partitions`.

Increasing this value might improve the quality of the index but in most
cases the default should be sufficient.

The default value is 256.

          
        
        
- 
          `target_partition_size, default is 8192`
          –
          
            
The target size of each partition.

This value controls the tradeoff between search performance and accuracy.
faster search but less accurate results as higher value.

          
        
    

              
                Source code in `lancedb/index.py`
                
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
@dataclass
class IvfFlat:
    """Describes an IVF Flat Index

    This index stores raw vectors.
    These vectors are grouped into partitions of similar vectors.
    Each partition keeps track of a centroid which is
    the average value of all vectors in the group.

    Attributes
    ----------
    distance_type: str, default "l2"
        The distance metric used to train the index

        This is used when training the index to calculate the IVF partitions
        (vectors are grouped in partitions with similar vectors according to this
        distance type) and to calculate a subvector's code during quantization.

        The distance type used to train an index MUST match the distance type used
        to search the index.  Failure to do so will yield inaccurate results.

        The following distance types are available:

        "l2" - Euclidean distance. This is a very common distance metric that
        accounts for both magnitude and direction when determining the distance
        between vectors. l2 distance has a range of [0, ∞).

        "cosine" - Cosine distance.  Cosine distance is a distance metric
        calculated from the cosine similarity between two vectors. Cosine
        similarity is a measure of similarity between two non-zero vectors of an
        inner product space. It is defined to equal the cosine of the angle
        between them.  Unlike l2, the cosine distance is not affected by the
        magnitude of the vectors.  Cosine distance has a range of [0, 2].

        Note: the cosine distance is undefined when one (or both) of the vectors
        are all zeros (there is no direction).  These vectors are invalid and may
        never be returned from a vector search.

        "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
        distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
        l2 norm is 1), then dot distance is equivalent to the cosine distance.

        "hamming" - Hamming distance. Hamming distance is a distance metric
        calculated as the number of positions at which the corresponding bits are
        different. Hamming distance has a range of [0, vector dimension].

    num_partitions: int, default sqrt(num_rows)
        The number of IVF partitions to create.

        This value should generally scale with the number of rows in the dataset.
        By default the number of partitions is the square root of the number of
        rows.

        If this value is too large then the first part of the search (picking the
        right partition) will be slow.  If this value is too small then the second
        part of the search (searching within a partition) will be slow.

    max_iterations: int, default 50
        Max iteration to train kmeans.

        When training an IVF PQ index we use kmeans to calculate the partitions.
        This parameter controls how many iterations of kmeans to run.

        Increasing this might improve the quality of the index but in most cases
        these extra iterations have diminishing returns.

        The default value is 50.
    sample_rate: int, default 256
        The rate used to calculate the number of training vectors for kmeans.

        When an IVF PQ index is trained, we need to calculate partitions.  These
        are groups of vectors that are similar to each other.  To do this we use an
        algorithm called kmeans.

        Running kmeans on a large dataset can be slow.  To speed this up we run
        kmeans on a random sample of the data.  This parameter controls the size of
        the sample.  The total number of vectors used to train the index is
        `sample_rate * num_partitions`.

        Increasing this value might improve the quality of the index but in most
        cases the default should be sufficient.

        The default value is 256.

    target_partition_size, default is 8192

        The target size of each partition.

        This value controls the tradeoff between search performance and accuracy.
        faster search but less accurate results as higher value.
    """

    distance_type: Literal["l2", "cosine", "dot", "hamming"] = "l2"
    num_partitions: Optional[int] = None
    max_iterations: int = 50
    sample_rate: int = 256
    target_partition_size: Optional[int] = None

              

  

  

    

            lancedb.table.IndexStatistics

  
      `dataclass`
  

¶

    

      
Statistics about an index.

Attributes:

    
        
- 
          `num_indexed_rows`
              (`int`)
          –
          
            
The number of rows that are covered by this index.

          
        
        
- 
          `num_unindexed_rows`
              (`int`)
          –
          
            
The number of rows that are not covered by this index.

          
        
        
- 
          `index_type`
              (`str`)
          –
          
            
The type of index that was created.

          
        
        
- 
          `distance_type`
              (`Optional[str]`)
          –
          
            
The distance type used by the index.

          
        
        
- 
          `num_indices`
              (`Optional[int]`)
          –
          
            
The number of parts the index is split into.

          
        
        
- 
          `loss`
              (`Optional[float]`)
          –
          
            
The KMeans loss for the index, for only vector indices.

          
        
    

              
                Source code in `lancedb/table.py`
                
4652
4653
4654
4655
4656
4657
4658
4659
4660
4661
4662
4663
4664
4665
4666
4667
4668
4669
4670
4671
4672
4673
4674
4675
4676
4677
4678
4679
4680
4681
4682
4683
4684
4685
@dataclass
class IndexStatistics:
    """
    Statistics about an index.

    Attributes
    ----------
    num_indexed_rows: int
        The number of rows that are covered by this index.
    num_unindexed_rows: int
        The number of rows that are not covered by this index.
    index_type: str
        The type of index that was created.
    distance_type: Optional[str]
        The distance type used by the index.
    num_indices: Optional[int]
        The number of parts the index is split into.
    loss: Optional[float]
        The KMeans loss for the index, for only vector indices.
    """

    num_indexed_rows: int
    num_unindexed_rows: int
    index_type: Literal[
        "IVF_PQ", "IVF_HNSW_PQ", "IVF_HNSW_SQ", "FTS", "BTREE", "BITMAP", "LABEL_LIST"
    ]
    distance_type: Optional[Literal["l2", "cosine", "dot"]] = None
    num_indices: Optional[int] = None
    loss: Optional[float] = None

    # This exists for backwards compatibility with an older API, which returned
    # a dictionary instead of a class.
    def __getitem__(self, key):
        return getattr(self, key)

              

  

  

    

## Querying (Asynchronous)¶

Queries allow you to return data from your database. Basic queries can be
created with the AsyncTable.query method
to return the entire (typically filtered) table. Vector searches return the
rows nearest to a query vector and can be created with the
AsyncTable.vector_search method.

            lancedb.query.AsyncQuery

¶

    
            

              Bases: `AsyncStandardQuery`

              
                Source code in `lancedb/query.py`
                
2572
2573
2574
2575
2576
2577
2578
2579
2580
2581
2582
2583
2584
2585
2586
2587
2588
2589
2590
2591
2592
2593
2594
2595
2596
2597
2598
2599
2600
2601
2602
2603
2604
2605
2606
2607
2608
2609
2610
2611
2612
2613
2614
2615
2616
2617
2618
2619
2620
2621
2622
2623
2624
2625
2626
2627
2628
2629
2630
2631
2632
2633
2634
2635
2636
2637
2638
2639
2640
2641
2642
2643
2644
2645
2646
2647
2648
2649
2650
2651
2652
2653
2654
2655
2656
2657
2658
2659
2660
2661
2662
2663
2664
2665
2666
2667
2668
2669
2670
2671
2672
2673
2674
2675
2676
2677
2678
2679
2680
2681
2682
2683
2684
2685
2686
2687
2688
2689
2690
2691
2692
2693
2694
2695
2696
2697
2698
2699
2700
2701
2702
2703
class AsyncQuery(AsyncStandardQuery):
    def __init__(self, inner: LanceQuery):
        """
        Construct an AsyncQuery

        This method is not intended to be called directly.  Instead, use the
        [AsyncTable.query][lancedb.table.AsyncTable.query] method to create a query.
        """
        super().__init__(inner)
        self._inner = inner

    @classmethod
    def _query_vec_to_array(self, vec: Union[VEC, Tuple]):
        if isinstance(vec, list):
            return pa.array(vec)
        if isinstance(vec, np.ndarray):
            return pa.array(vec)
        if isinstance(vec, pa.Array):
            return vec
        if isinstance(vec, pa.ChunkedArray):
            return vec.combine_chunks()
        if isinstance(vec, tuple):
            return pa.array(vec)
        # We've checked everything we formally support in our typings
        # but, as a fallback, let pyarrow try and convert it anyway.
        # This can allow for some more exotic things like iterables
        return pa.array(vec)

    def nearest_to(
        self,
        query_vector: Union[VEC, Tuple, List[VEC]],
    ) -> AsyncVectorQuery:
        """
        Find the nearest vectors to the given query vector.

        This converts the query from a plain query to a vector query.

        This method will attempt to convert the input to the query vector
        expected by the embedding model.  If the input cannot be converted
        then an error will be thrown.

        By default, there is no embedding model, and the input should be
        something that can be converted to a pyarrow array of floats.  This
        includes lists, numpy arrays, and tuples.

        If there is only one vector column (a column whose data type is a
        fixed size list of floats) then the column does not need to be specified.
        If there is more than one vector column you must use
        [AsyncVectorQuery.column][lancedb.query.AsyncVectorQuery.column] to specify
        which column you would like to compare with.

        If no index has been created on the vector column then a vector query
        will perform a distance comparison between the query vector and every
        vector in the database and then sort the results.  This is sometimes
        called a "flat search"

        For small databases, with tens of thousands of vectors or less, this can
        be reasonably fast.  In larger databases you should create a vector index
        on the column.  If there is a vector index then an "approximate" nearest
        neighbor search (frequently called an ANN search) will be performed.  This
        search is much faster, but the results will be approximate.

        The query can be further parameterized using the returned builder.  There
        are various ANN search parameters that will let you fine tune your recall
        accuracy vs search latency.

        Vector searches always have a [limit][].  If `limit` has not been called then
        a default `limit` of 10 will be used.

        Typically, a single vector is passed in as the query. However, you can also
        pass in multiple vectors. When multiple vectors are passed in, if the vector
        column is with multivector type, then the vectors will be treated as a single
        query. Or the vectors will be treated as multiple queries, this can be useful
        if you want to find the nearest vectors to multiple query vectors.
        This is not expected to be faster than making multiple queries concurrently;
        it is just a convenience method. If multiple vectors are passed in then
        an additional column `query_index` will be added to the results. This column
        will contain the index of the query vector that the result is nearest to.
        """
        if query_vector is None:
            raise ValueError("query_vector can not be None")

        if (
            isinstance(query_vector, (list, np.ndarray, pa.Array))
            and len(query_vector) > 0
            and isinstance(query_vector[0], (list, np.ndarray, pa.Array))
        ):
            # multiple have been passed
            query_vectors = [AsyncQuery._query_vec_to_array(v) for v in query_vector]
            new_self = self._inner.nearest_to(query_vectors[0])
            for v in query_vectors[1:]:
                new_self.add_query_vector(v)
            return AsyncVectorQuery(new_self)
        else:
            return AsyncVectorQuery(
                self._inner.nearest_to(AsyncQuery._query_vec_to_array(query_vector))
            )

    def nearest_to_text(
        self, query: str | FullTextQuery, columns: Union[str, List[str], None] = None
    ) -> AsyncFTSQuery:
        """
        Find the documents that are most relevant to the given text query.

        This method will perform a full text search on the table and return
        the most relevant documents.  The relevance is determined by BM25.

        The columns to search must be with native FTS index
        (Tantivy-based can't work with this method).

        By default, all indexed columns are searched,
        now only one column can be searched at a time.

        Parameters
        ----------
        query: str
            The text query to search for.
        columns: str or list of str, default None
            The columns to search in. If None, all indexed columns are searched.
            For now only one column can be searched at a time.
        """
        if isinstance(columns, str):
            columns = [columns]
        if columns is None:
            columns = []

        if isinstance(query, str):
            return AsyncFTSQuery(
                self._inner.nearest_to_text({"query": query, "columns": columns})
            )
        # FullTextQuery object
        return AsyncFTSQuery(self._inner.nearest_to_text({"query": query}))

              

  

            to_query_object

¶

to_query_object() -> Query

    

      
Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

            
              Source code in `lancedb/query.py`
              
2213
2214
2215
2216
2217
2218
2219
2220
def to_query_object(self) -> Query:
    """
    Convert the query into a query object

    This is currently experimental but can be useful as the query object is pure
    python and more easily serializable.
    """
    return Query.from_inner(self._inner.to_query_request())

            
    

            select

¶

select(columns: Union[List[str], dict[str, str]]) -> Self

    

      
Return only the specified columns.

By default a query will return all columns from the table.  However, this can
have a very significant impact on latency.  LanceDb stores data in a columnar
fashion.  This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b".  This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str].  A column will be
returned for each entry in the map.  The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`.  The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

            
              Source code in `lancedb/query.py`
              
2222
2223
2224
2225
2226
2227
2228
2229
2230
2231
2232
2233
2234
2235
2236
2237
2238
2239
2240
2241
2242
2243
2244
2245
2246
2247
2248
2249
2250
2251
2252
2253
2254
2255
2256
2257
2258
def select(self, columns: Union[List[str], dict[str, str]]) -> Self:
    """
    Return only the specified columns.

    By default a query will return all columns from the table.  However, this can
    have a very significant impact on latency.  LanceDb stores data in a columnar
    fashion.  This
    means we can finely tune our I/O to select exactly the columns we need.

    As a best practice you should always limit queries to the columns that you need.
    If you pass in a list of column names then only those columns will be
    returned.

    You can also use this method to create new "dynamic" columns based on your
    existing columns. For example, you may not care about "a" or "b" but instead
    simply want "a + b".  This is often seen in the SELECT clause of an SQL query
    (e.g. `SELECT a+b FROM my_table`).

    To create dynamic columns you can pass in a dict[str, str].  A column will be
    returned for each entry in the map.  The key provides the name of the column.
    The value is an SQL string used to specify how the column is calculated.

    For example, an SQL query might state `SELECT a + b AS combined, c`.  The
    equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

    Columns will always be returned in the order given, even if that order is
    different than the order used when adding the data.
    """
    if isinstance(columns, list) and all(isinstance(c, str) for c in columns):
        self._inner.select_columns(columns)
    elif isinstance(columns, dict) and all(
        isinstance(k, str) and isinstance(v, str) for k, v in columns.items()
    ):
        self._inner.select(list(columns.items()))
    else:
        raise TypeError("columns must be a list of column names or a dict")
    return self

            
    

            with_row_id

¶

with_row_id() -> Self

    

      
Include the _rowid column in the results.

            
              Source code in `lancedb/query.py`
              
2260
2261
2262
2263
2264
2265
def with_row_id(self) -> Self:
    """
    Include the _rowid column in the results.
    """
    self._inner.with_row_id()
    return self

            
    

            to_batches

  
      `async`
  

¶

to_batches(*, max_batch_length: Optional[int] = None, timeout: Optional[timedelta] = None) -> AsyncRecordBatchReader

    

      
Execute the query and return the results as an Apache Arrow RecordBatchReader.

Parameters:

    
        
- 
          `max_batch_length`
              (`Optional[int]`, default:
                  `None`
)
          –
          
            
The maximum number of selected records in a single RecordBatch object.
If not specified, a default batch length is used.
It is possible for batches to be smaller than the provided length if the
underlying data is stored in smaller chunks.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2267
2268
2269
2270
2271
2272
2273
2274
2275
2276
2277
2278
2279
2280
2281
2282
2283
2284
2285
2286
2287
2288
2289
2290
2291
2292
2293
async def to_batches(
    self,
    *,
    max_batch_length: Optional[int] = None,
    timeout: Optional[timedelta] = None,
) -> AsyncRecordBatchReader:
    """
    Execute the query and return the results as an Apache Arrow RecordBatchReader.

    Parameters
    ----------

    max_batch_length: Optional[int]
        The maximum number of selected records in a single RecordBatch object.
        If not specified, a default batch length is used.
        It is possible for batches to be smaller than the provided length if the
        underlying data is stored in smaller chunks.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return AsyncRecordBatchReader(
        await self._inner.execute(
            max_batch_length=max_batch_length, timeout=timeout
        )
    )

            
    

            output_schema

  
      `async`
  

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
2295
2296
2297
2298
2299
2300
2301
async def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return await self._inner.output_schema()

            
    

            to_arrow

  
      `async`
  

¶

to_arrow(timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning.  If
you expect a large number of results, you may want to use
to_batches

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2303
2304
2305
2306
2307
2308
2309
2310
2311
2312
2313
2314
2315
2316
2317
2318
2319
2320
2321
async def to_arrow(self, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and collect the results into an Apache Arrow Table.

    This method will collect all results into memory before returning.  If
    you expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches]

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    batch_iter = await self.to_batches(timeout=timeout)
    return pa.Table.from_batches(
        await batch_iter.read_all(), schema=batch_iter.schema
    )

            
    

            to_list

  
      `async`
  

¶

to_list(timeout: Optional[timedelta] = None) -> List[dict]

    

      
Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2323
2324
2325
2326
2327
2328
2329
2330
2331
2332
2333
2334
2335
2336
2337
2338
async def to_list(self, timeout: Optional[timedelta] = None) -> List[dict]:
    """
    Execute the query and return the results as a list of dictionaries.

    Each list entry is a dictionary with the selected column names as keys,
    or all table columns if `select` is not called. The vector and the "_distance"
    fields are returned whether or not they're explicitly selected.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (await self.to_arrow(timeout=timeout)).to_pylist()

            
    

            to_pandas

  
      `async`
  

¶

to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'

    

      
Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
pandas separately.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())

Parameters:

    
        
- 
          `flatten`
              (`Optional[Union[int, bool]]`, default:
                  `None`
)
          –
          
            
If flatten is True, flatten all nested columns.
If flatten is an integer, flatten the nested columns up to the
specified depth.
If unspecified, do not flatten the nested columns.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2340
2341
2342
2343
2344
2345
2346
2347
2348
2349
2350
2351
2352
2353
2354
2355
2356
2357
2358
2359
2360
2361
2362
2363
2364
2365
2366
2367
2368
2369
2370
2371
2372
2373
2374
2375
2376
2377
2378
2379
async def to_pandas(
    self,
    flatten: Optional[Union[int, bool]] = None,
    timeout: Optional[timedelta] = None,
) -> "pd.DataFrame":
    """
    Execute the query and collect the results into a pandas DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    pandas separately.

    Examples
    --------

    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = batch.to_pandas()
    >>> asyncio.run(doctest_example())

    Parameters
    ----------
    flatten: Optional[Union[int, bool]]
        If flatten is True, flatten all nested columns.
        If flatten is an integer, flatten the nested columns up to the
        specified depth.
        If unspecified, do not flatten the nested columns.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (
        flatten_columns(await self.to_arrow(timeout=timeout), flatten)
    ).to_pandas()

            
    

            to_polars

  
      `async`
  

¶

to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'

    

      
Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
polars separately.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

Examples:

    
>>> import asyncio
>>> import polars as pl
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())

            
              Source code in `lancedb/query.py`
              
2381
2382
2383
2384
2385
2386
2387
2388
2389
2390
2391
2392
2393
2394
2395
2396
2397
2398
2399
2400
2401
2402
2403
2404
2405
2406
2407
2408
2409
2410
2411
2412
2413
2414
2415
async def to_polars(
    self,
    timeout: Optional[timedelta] = None,
) -> "pl.DataFrame":
    """
    Execute the query and collect the results into a Polars DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    polars separately.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.

    Examples
    --------

    >>> import asyncio
    >>> import polars as pl
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = pl.from_arrow(batch)
    >>> asyncio.run(doctest_example())
    """
    import polars as pl

    return pl.from_arrow(await self.to_arrow(timeout=timeout))

            
    

            to_pydantic

  
      `async`
  

¶

to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]

    

      
Convert results to a list of pydantic models.

Parameters:

    
        
- 
          `model`
              (`Type[LanceModel]`)
          –
          
            
The pydantic model to use.

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `list[LanceModel]`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2417
2418
2419
2420
2421
2422
2423
2424
2425
2426
2427
2428
2429
2430
2431
2432
2433
2434
2435
2436
2437
async def to_pydantic(
    self, model: Type[LanceModel], *, timeout: Optional[timedelta] = None
) -> List[LanceModel]:
    """
    Convert results to a list of pydantic models.

    Parameters
    ----------
    model : Type[LanceModel]
        The pydantic model to use.
    timeout : timedelta, optional
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    list[LanceModel]
    """
    return [
        model(**row) for row in (await self.to_arrow(timeout=timeout)).to_pylist()
    ]

            
    

            explain_plan

  
      `async`
  

¶

explain_plan(verbose: Optional[bool] = False)

    

      
Return the execution plan for this query.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2439
2440
2441
2442
2443
2444
2445
2446
2447
2448
2449
2450
2451
2452
2453
2454
2455
2456
2457
2458
2459
2460
2461
2462
2463
2464
2465
2466
2467
2468
2469
async def explain_plan(self, verbose: Optional[bool] = False):
    """Return the execution plan for this query.

    Examples
    --------
    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
    ...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
    ...     print(plan)
    >>> asyncio.run(doctest_example()) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
      GlobalLimitExec: skip=0, fetch=10
        FilterExec: _distance@2 IS NOT NULL
          SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
            KNNVectorDistance: metric=l2
              LanceRead: uri=..., projection=[vector], ...
    <BLANKLINE>

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501
    return await self._inner.explain_plan(verbose)

            
    

            analyze_plan

  
      `async`
  

¶

analyze_plan()

    

      
Execute the query and display with runtime metrics.

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2471
2472
2473
2474
2475
2476
2477
2478
async def analyze_plan(self):
    """Execute the query and display with runtime metrics.

    Returns
    -------
    plan : str
    """
    return await self._inner.analyze_plan()

            
    

            where

¶

where(predicate: str) -> Self

    

      
Only return rows matching the given predicate

The predicate should be supplied as an SQL query string.

Examples:

    
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"

    
Filtering performance can often be improved by creating a scalar index
on the filter column(s).

            
              Source code in `lancedb/query.py`
              
2495
2496
2497
2498
2499
2500
2501
2502
2503
2504
2505
2506
2507
2508
2509
2510
2511
2512
def where(self, predicate: str) -> Self:
    """
    Only return rows matching the given predicate

    The predicate should be supplied as an SQL query string.

    Examples
    --------

    >>> predicate = "x > 10"
    >>> predicate = "y > 0 AND y < 100"
    >>> predicate = "x > 5 OR y = 'test'"

    Filtering performance can often be improved by creating a scalar index
    on the filter column(s).
    """
    self._inner.where(predicate)
    return self

            
    

            limit

¶

limit(limit: int) -> Self

    

      
Set the maximum number of results to return.

By default, a plain search has no limit.  If this method is not
called then every valid row from the table will be returned.

            
              Source code in `lancedb/query.py`
              
2514
2515
2516
2517
2518
2519
2520
2521
2522
def limit(self, limit: int) -> Self:
    """
    Set the maximum number of results to return.

    By default, a plain search has no limit.  If this method is not
    called then every valid row from the table will be returned.
    """
    self._inner.limit(limit)
    return self

            
    

            offset

¶

offset(offset: int) -> Self

    

      
Set the offset for the results.

Parameters:

    
        
- 
          `offset`
              (`int`)
          –
          
            
The offset to start fetching results from.

          
        
    

            
              Source code in `lancedb/query.py`
              
2524
2525
2526
2527
2528
2529
2530
2531
2532
2533
2534
def offset(self, offset: int) -> Self:
    """
    Set the offset for the results.

    Parameters
    ----------
    offset: int
        The offset to start fetching results from.
    """
    self._inner.offset(offset)
    return self

            
    

            fast_search

¶

fast_search() -> Self

    

      
Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
AsyncTable.optimize.

            
              Source code in `lancedb/query.py`
              
2536
2537
2538
2539
2540
2541
2542
2543
2544
2545
2546
2547
2548
def fast_search(self) -> Self:
    """
    Skip searching un-indexed data.

    This can make queries faster, but will miss any data that has not been
    indexed.

    !!! tip
        You can add new data into an existing index by calling
        [AsyncTable.optimize][lancedb.table.AsyncTable.optimize].
    """
    self._inner.fast_search()
    return self

            
    

            postfilter

¶

postfilter() -> Self

    

      
If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search.  This is how
filtering is typically understood to work.  This prefilter step does add some
additional latency.  Creating a scalar index on the filter column(s) can
often improve this latency.  However, sometimes a filter is too complex or
scalar indices cannot be applied to the column.  In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search.  This
means we only run the filter on a much smaller set of data.  However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

            
              Source code in `lancedb/query.py`
              
2550
2551
2552
2553
2554
2555
2556
2557
2558
2559
2560
2561
2562
2563
2564
2565
2566
2567
2568
2569
def postfilter(self) -> Self:
    """
    If this is called then filtering will happen after the search instead of
    before.
    By default filtering will be performed before the search.  This is how
    filtering is typically understood to work.  This prefilter step does add some
    additional latency.  Creating a scalar index on the filter column(s) can
    often improve this latency.  However, sometimes a filter is too complex or
    scalar indices cannot be applied to the column.  In these cases postfiltering
    can be used instead of prefiltering to improve latency.
    Post filtering applies the filter to the results of the search.  This
    means we only run the filter on a much smaller set of data.  However, it can
    cause the query to return fewer than `limit` results (or even no results) if
    none of the nearest results match the filter.
    Post filtering happens during the "refine stage" (described in more detail in
    @see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
    factor can often help restore some of the results lost by post filtering.
    """
    self._inner.postfilter()
    return self

            
    

            __init__

¶

__init__(inner: Query)

    

      
Construct an AsyncQuery

This method is not intended to be called directly.  Instead, use the
AsyncTable.query method to create a query.

            
              Source code in `lancedb/query.py`
              
2573
2574
2575
2576
2577
2578
2579
2580
2581
def __init__(self, inner: LanceQuery):
    """
    Construct an AsyncQuery

    This method is not intended to be called directly.  Instead, use the
    [AsyncTable.query][lancedb.table.AsyncTable.query] method to create a query.
    """
    super().__init__(inner)
    self._inner = inner

            
    

            nearest_to

¶

nearest_to(query_vector: Union[VEC, Tuple, List[VEC]]) -> AsyncVectorQuery

    

      
Find the nearest vectors to the given query vector.

This converts the query from a plain query to a vector query.

This method will attempt to convert the input to the query vector
expected by the embedding model.  If the input cannot be converted
then an error will be thrown.

By default, there is no embedding model, and the input should be
something that can be converted to a pyarrow array of floats.  This
includes lists, numpy arrays, and tuples.

If there is only one vector column (a column whose data type is a
fixed size list of floats) then the column does not need to be specified.
If there is more than one vector column you must use
AsyncVectorQuery.column to specify
which column you would like to compare with.

If no index has been created on the vector column then a vector query
will perform a distance comparison between the query vector and every
vector in the database and then sort the results.  This is sometimes
called a "flat search"

For small databases, with tens of thousands of vectors or less, this can
be reasonably fast.  In larger databases you should create a vector index
on the column.  If there is a vector index then an "approximate" nearest
neighbor search (frequently called an ANN search) will be performed.  This
search is much faster, but the results will be approximate.

The query can be further parameterized using the returned builder.  There
are various ANN search parameters that will let you fine tune your recall
accuracy vs search latency.

Vector searches always have a limit.  If `limit` has not been called then
a default `limit` of 10 will be used.

Typically, a single vector is passed in as the query. However, you can also
pass in multiple vectors. When multiple vectors are passed in, if the vector
column is with multivector type, then the vectors will be treated as a single
query. Or the vectors will be treated as multiple queries, this can be useful
if you want to find the nearest vectors to multiple query vectors.
This is not expected to be faster than making multiple queries concurrently;
it is just a convenience method. If multiple vectors are passed in then
an additional column `query_index` will be added to the results. This column
will contain the index of the query vector that the result is nearest to.

            
              Source code in `lancedb/query.py`
              
2600
2601
2602
2603
2604
2605
2606
2607
2608
2609
2610
2611
2612
2613
2614
2615
2616
2617
2618
2619
2620
2621
2622
2623
2624
2625
2626
2627
2628
2629
2630
2631
2632
2633
2634
2635
2636
2637
2638
2639
2640
2641
2642
2643
2644
2645
2646
2647
2648
2649
2650
2651
2652
2653
2654
2655
2656
2657
2658
2659
2660
2661
2662
2663
2664
2665
2666
2667
2668
def nearest_to(
    self,
    query_vector: Union[VEC, Tuple, List[VEC]],
) -> AsyncVectorQuery:
    """
    Find the nearest vectors to the given query vector.

    This converts the query from a plain query to a vector query.

    This method will attempt to convert the input to the query vector
    expected by the embedding model.  If the input cannot be converted
    then an error will be thrown.

    By default, there is no embedding model, and the input should be
    something that can be converted to a pyarrow array of floats.  This
    includes lists, numpy arrays, and tuples.

    If there is only one vector column (a column whose data type is a
    fixed size list of floats) then the column does not need to be specified.
    If there is more than one vector column you must use
    [AsyncVectorQuery.column][lancedb.query.AsyncVectorQuery.column] to specify
    which column you would like to compare with.

    If no index has been created on the vector column then a vector query
    will perform a distance comparison between the query vector and every
    vector in the database and then sort the results.  This is sometimes
    called a "flat search"

    For small databases, with tens of thousands of vectors or less, this can
    be reasonably fast.  In larger databases you should create a vector index
    on the column.  If there is a vector index then an "approximate" nearest
    neighbor search (frequently called an ANN search) will be performed.  This
    search is much faster, but the results will be approximate.

    The query can be further parameterized using the returned builder.  There
    are various ANN search parameters that will let you fine tune your recall
    accuracy vs search latency.

    Vector searches always have a [limit][].  If `limit` has not been called then
    a default `limit` of 10 will be used.

    Typically, a single vector is passed in as the query. However, you can also
    pass in multiple vectors. When multiple vectors are passed in, if the vector
    column is with multivector type, then the vectors will be treated as a single
    query. Or the vectors will be treated as multiple queries, this can be useful
    if you want to find the nearest vectors to multiple query vectors.
    This is not expected to be faster than making multiple queries concurrently;
    it is just a convenience method. If multiple vectors are passed in then
    an additional column `query_index` will be added to the results. This column
    will contain the index of the query vector that the result is nearest to.
    """
    if query_vector is None:
        raise ValueError("query_vector can not be None")

    if (
        isinstance(query_vector, (list, np.ndarray, pa.Array))
        and len(query_vector) > 0
        and isinstance(query_vector[0], (list, np.ndarray, pa.Array))
    ):
        # multiple have been passed
        query_vectors = [AsyncQuery._query_vec_to_array(v) for v in query_vector]
        new_self = self._inner.nearest_to(query_vectors[0])
        for v in query_vectors[1:]:
            new_self.add_query_vector(v)
        return AsyncVectorQuery(new_self)
    else:
        return AsyncVectorQuery(
            self._inner.nearest_to(AsyncQuery._query_vec_to_array(query_vector))
        )

            
    

            nearest_to_text

¶

nearest_to_text(query: str | FullTextQuery, columns: Union[str, List[str], None] = None) -> AsyncFTSQuery

    

      
Find the documents that are most relevant to the given text query.

This method will perform a full text search on the table and return
the most relevant documents.  The relevance is determined by BM25.

The columns to search must be with native FTS index
(Tantivy-based can't work with this method).

By default, all indexed columns are searched,
now only one column can be searched at a time.

Parameters:

    
        
- 
          `query`
              (`str | FullTextQuery`)
          –
          
            
The text query to search for.

          
        
        
- 
          `columns`
              (`Union[str, List[str], None]`, default:
                  `None`
)
          –
          
            
The columns to search in. If None, all indexed columns are searched.
For now only one column can be searched at a time.

          
        
    

            
              Source code in `lancedb/query.py`
              
2670
2671
2672
2673
2674
2675
2676
2677
2678
2679
2680
2681
2682
2683
2684
2685
2686
2687
2688
2689
2690
2691
2692
2693
2694
2695
2696
2697
2698
2699
2700
2701
2702
2703
def nearest_to_text(
    self, query: str | FullTextQuery, columns: Union[str, List[str], None] = None
) -> AsyncFTSQuery:
    """
    Find the documents that are most relevant to the given text query.

    This method will perform a full text search on the table and return
    the most relevant documents.  The relevance is determined by BM25.

    The columns to search must be with native FTS index
    (Tantivy-based can't work with this method).

    By default, all indexed columns are searched,
    now only one column can be searched at a time.

    Parameters
    ----------
    query: str
        The text query to search for.
    columns: str or list of str, default None
        The columns to search in. If None, all indexed columns are searched.
        For now only one column can be searched at a time.
    """
    if isinstance(columns, str):
        columns = [columns]
    if columns is None:
        columns = []

    if isinstance(query, str):
        return AsyncFTSQuery(
            self._inner.nearest_to_text({"query": query, "columns": columns})
        )
    # FullTextQuery object
    return AsyncFTSQuery(self._inner.nearest_to_text({"query": query}))

            
    

  

    

            lancedb.query.AsyncVectorQuery

¶

    
            

              Bases: `AsyncStandardQuery`, `AsyncVectorQueryBase`

              
                Source code in `lancedb/query.py`
                
2985
2986
2987
2988
2989
2990
2991
2992
2993
2994
2995
2996
2997
2998
2999
3000
3001
3002
3003
3004
3005
3006
3007
3008
3009
3010
3011
3012
3013
3014
3015
3016
3017
3018
3019
3020
3021
3022
3023
3024
3025
3026
3027
3028
3029
3030
3031
3032
3033
3034
3035
3036
3037
3038
3039
3040
3041
3042
3043
3044
3045
3046
3047
3048
3049
3050
3051
3052
3053
3054
3055
3056
3057
3058
3059
3060
3061
3062
3063
3064
3065
class AsyncVectorQuery(AsyncStandardQuery, AsyncVectorQueryBase):
    def __init__(self, inner: LanceVectorQuery):
        """
        Construct an AsyncVectorQuery

        This method is not intended to be called directly.  Instead, create
        a query first with [AsyncTable.query][lancedb.table.AsyncTable.query] and then
        use [AsyncQuery.nearest_to][lancedb.query.AsyncQuery.nearest_to]] to convert to
        a vector query.  Or you can use
        [AsyncTable.vector_search][lancedb.table.AsyncTable.vector_search]
        """
        super().__init__(inner)
        self._inner = inner
        self._reranker = None
        self._query_string = None

    def rerank(
        self, reranker: Reranker = RRFReranker(), query_string: Optional[str] = None
    ) -> AsyncHybridQuery:
        if reranker and not isinstance(reranker, Reranker):
            raise ValueError("reranker must be an instance of Reranker class.")

        self._reranker = reranker

        if not self._query_string and not query_string:
            raise ValueError("query_string must be provided to rerank the results.")

        self._query_string = query_string

        return self

    def nearest_to_text(
        self, query: str | FullTextQuery, columns: Union[str, List[str], None] = None
    ) -> AsyncHybridQuery:
        """
        Find the documents that are most relevant to the given text query,
        in addition to vector search.

        This converts the vector query into a hybrid query.

        This search will perform a full text search on the table and return
        the most relevant documents, combined with the vector query results.
        The text relevance is determined by BM25.

        The columns to search must be with native FTS index
        (Tantivy-based can't work with this method).

        By default, all indexed columns are searched,
        now only one column can be searched at a time.

        Parameters
        ----------
        query: str
            The text query to search for.
        columns: str or list of str, default None
            The columns to search in. If None, all indexed columns are searched.
            For now only one column can be searched at a time.
        """
        if isinstance(columns, str):
            columns = [columns]
        if columns is None:
            columns = []

        if isinstance(query, str):
            return AsyncHybridQuery(
                self._inner.nearest_to_text({"query": query, "columns": columns})
            )
        # FullTextQuery object
        return AsyncHybridQuery(self._inner.nearest_to_text({"query": query}))

    async def to_batches(
        self,
        *,
        max_batch_length: Optional[int] = None,
        timeout: Optional[timedelta] = None,
    ) -> AsyncRecordBatchReader:
        reader = await super().to_batches(timeout=timeout)
        results = pa.Table.from_batches(await reader.read_all(), reader.schema)
        if self._reranker:
            results = self._reranker.rerank_vector(self._query_string, results)
        return AsyncRecordBatchReader(results, max_batch_length=max_batch_length)

              

  

            column

¶

column(column: str) -> Self

    

      
Set the vector column to query

This controls which column is compared to the query vector supplied in
the call to AsyncQuery.nearest_to.

This parameter must be specified if the table has more than one column
whose data type is a fixed-size-list of floats.

            
              Source code in `lancedb/query.py`
              
2812
2813
2814
2815
2816
2817
2818
2819
2820
2821
2822
2823
def column(self, column: str) -> Self:
    """
    Set the vector column to query

    This controls which column is compared to the query vector supplied in
    the call to [AsyncQuery.nearest_to][lancedb.query.AsyncQuery.nearest_to].

    This parameter must be specified if the table has more than one column
    whose data type is a fixed-size-list of floats.
    """
    self._inner.column(column)
    return self

            
    

            nprobes

¶

nprobes(nprobes: int) -> Self

    

      
Set the number of partitions to search (probe)

This argument is only used when the vector column has an IVF-based index.
If there is no index then this value is ignored.

The IVF stage of IVF PQ divides the input into partitions (clusters) of
related values.

The partition whose centroids are closest to the query vector will be
exhaustiely searched to find matches.  This parameter controls how many
partitions should be searched.

Increasing this value will increase the recall of your query but will
also increase the latency of your query.  The default value is 20.  This
default is good for many cases but the best value to use will depend on
your data and the recall that you need to achieve.

For best results we recommend tuning this parameter with a benchmark against
your actual data to find the smallest possible value that will still give
you the desired recall.

            
              Source code in `lancedb/query.py`
              
2825
2826
2827
2828
2829
2830
2831
2832
2833
2834
2835
2836
2837
2838
2839
2840
2841
2842
2843
2844
2845
2846
2847
2848
2849
def nprobes(self, nprobes: int) -> Self:
    """
    Set the number of partitions to search (probe)

    This argument is only used when the vector column has an IVF-based index.
    If there is no index then this value is ignored.

    The IVF stage of IVF PQ divides the input into partitions (clusters) of
    related values.

    The partition whose centroids are closest to the query vector will be
    exhaustiely searched to find matches.  This parameter controls how many
    partitions should be searched.

    Increasing this value will increase the recall of your query but will
    also increase the latency of your query.  The default value is 20.  This
    default is good for many cases but the best value to use will depend on
    your data and the recall that you need to achieve.

    For best results we recommend tuning this parameter with a benchmark against
    your actual data to find the smallest possible value that will still give
    you the desired recall.
    """
    self._inner.nprobes(nprobes)
    return self

            
    

            minimum_nprobes

¶

minimum_nprobes(minimum_nprobes: int) -> Self

    

      
Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every indexed vector query and will
increase recall at the expense of latency.

            
              Source code in `lancedb/query.py`
              
2851
2852
2853
2854
2855
2856
2857
2858
2859
2860
def minimum_nprobes(self, minimum_nprobes: int) -> Self:
    """Set the minimum number of probes to use.

    See `nprobes` for more details.

    These partitions will be searched on every indexed vector query and will
    increase recall at the expense of latency.
    """
    self._inner.minimum_nprobes(minimum_nprobes)
    return self

            
    

            maximum_nprobes

¶

maximum_nprobes(maximum_nprobes: int) -> Self

    

      
Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

            
              Source code in `lancedb/query.py`
              
2862
2863
2864
2865
2866
2867
2868
2869
2870
2871
2872
2873
2874
2875
2876
2877
def maximum_nprobes(self, maximum_nprobes: int) -> Self:
    """Set the maximum number of probes to use.

    See `nprobes` for more details.

    If this value is greater than `minimum_nprobes` then the excess partitions
    will be searched only if we have not found enough results.

    This can be useful when there is a narrow filter to allow these queries to
    spend more time searching and avoid potential false negatives.

    If this value is 0 then no limit will be applied and all partitions could be
    searched if needed to satisfy the limit.
    """
    self._inner.maximum_nprobes(maximum_nprobes)
    return self

            
    

            distance_range

¶

distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> Self

    

      
Set the distance range to use.

Only rows with distances within range [lower_bound, upper_bound)
will be returned.

Parameters:

    
        
- 
          `lower_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The lower bound of the distance range.

          
        
        
- 
          `upper_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The upper bound of the distance range.

          
        
    

Returns:

    
        
- 
              `AsyncVectorQuery`
          –
          
            
The AsyncVectorQuery object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2879
2880
2881
2882
2883
2884
2885
2886
2887
2888
2889
2890
2891
2892
2893
2894
2895
2896
2897
2898
2899
2900
def distance_range(
    self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
) -> Self:
    """Set the distance range to use.

    Only rows with distances within range [lower_bound, upper_bound)
    will be returned.

    Parameters
    ----------
    lower_bound: Optional[float]
        The lower bound of the distance range.
    upper_bound: Optional[float]
        The upper bound of the distance range.

    Returns
    -------
    AsyncVectorQuery
        The AsyncVectorQuery object.
    """
    self._inner.distance_range(lower_bound, upper_bound)
    return self

            
    

            ef

¶

ef(ef: int) -> Self

    

      
Set the number of candidates to consider during search

This argument is only used when the vector column has an HNSW index.
If there is no index then this value is ignored.

Increasing this value will increase the recall of your query but will also
increase the latency of your query.  The default value is 1.5 * limit.  This
default is good for many cases but the best value to use will depend on your
data and the recall that you need to achieve.

            
              Source code in `lancedb/query.py`
              
2902
2903
2904
2905
2906
2907
2908
2909
2910
2911
2912
2913
2914
2915
def ef(self, ef: int) -> Self:
    """
    Set the number of candidates to consider during search

    This argument is only used when the vector column has an HNSW index.
    If there is no index then this value is ignored.

    Increasing this value will increase the recall of your query but will also
    increase the latency of your query.  The default value is 1.5 * limit.  This
    default is good for many cases but the best value to use will depend on your
    data and the recall that you need to achieve.
    """
    self._inner.ef(ef)
    return self

            
    

            refine_factor

¶

refine_factor(refine_factor: int) -> Self

    

      
A multiplier to control how many additional rows are taken during the refine
step

This argument is only used when the vector column has an IVF PQ index.
If there is no index then this value is ignored.

An IVF PQ index stores compressed (quantized) values.  They query vector is
compared against these values and, since they are compressed, the comparison is
inaccurate.

This parameter can be used to refine the results.  It can improve both improve
recall and correct the ordering of the nearest results.

To refine results LanceDb will first perform an ANN search to find the nearest
`limit` * `refine_factor` results.  In other words, if `refine_factor` is 3 and
`limit` is the default (10) then the first 30 results will be selected.  LanceDb
then fetches the full, uncompressed, values for these 30 results.  The results
are then reordered by the true distance and only the nearest 10 are kept.

Note: there is a difference between calling this method with a value of 1 and
never calling this method at all.  Calling this method with any value will have
an impact on your search latency.  When you call this method with a
`refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
values so that it can potentially reorder the results.

Note: if this method is NOT called then the distances returned in the _distance
column will be approximate distances based on the comparison of the quantized
query vector and the quantized result vectors.  This can be considerably
different than the true distance between the query vector and the actual
uncompressed vector.

            
              Source code in `lancedb/query.py`
              
2917
2918
2919
2920
2921
2922
2923
2924
2925
2926
2927
2928
2929
2930
2931
2932
2933
2934
2935
2936
2937
2938
2939
2940
2941
2942
2943
2944
2945
2946
2947
2948
2949
2950
2951
def refine_factor(self, refine_factor: int) -> Self:
    """
    A multiplier to control how many additional rows are taken during the refine
    step

    This argument is only used when the vector column has an IVF PQ index.
    If there is no index then this value is ignored.

    An IVF PQ index stores compressed (quantized) values.  They query vector is
    compared against these values and, since they are compressed, the comparison is
    inaccurate.

    This parameter can be used to refine the results.  It can improve both improve
    recall and correct the ordering of the nearest results.

    To refine results LanceDb will first perform an ANN search to find the nearest
    `limit` * `refine_factor` results.  In other words, if `refine_factor` is 3 and
    `limit` is the default (10) then the first 30 results will be selected.  LanceDb
    then fetches the full, uncompressed, values for these 30 results.  The results
    are then reordered by the true distance and only the nearest 10 are kept.

    Note: there is a difference between calling this method with a value of 1 and
    never calling this method at all.  Calling this method with any value will have
    an impact on your search latency.  When you call this method with a
    `refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
    values so that it can potentially reorder the results.

    Note: if this method is NOT called then the distances returned in the _distance
    column will be approximate distances based on the comparison of the quantized
    query vector and the quantized result vectors.  This can be considerably
    different than the true distance between the query vector and the actual
    uncompressed vector.
    """
    self._inner.refine_factor(refine_factor)
    return self

            
    

            distance_type

¶

distance_type(distance_type: str) -> Self

    

      
Set the distance metric to use

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric.  This parameter controls which distance metric
to use.  See @see {@link IvfPqOptions.distanceType} for more details on the
different distance metrics available.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index.  If this is not done then the
results will be invalid.

By default "l2" is used.

            
              Source code in `lancedb/query.py`
              
2953
2954
2955
2956
2957
2958
2959
2960
2961
2962
2963
2964
2965
2966
2967
2968
2969
def distance_type(self, distance_type: str) -> Self:
    """
    Set the distance metric to use

    When performing a vector search we try and find the "nearest" vectors according
    to some kind of distance metric.  This parameter controls which distance metric
    to use.  See @see {@link IvfPqOptions.distanceType} for more details on the
    different distance metrics available.

    Note: if there is a vector index then the distance type used MUST match the
    distance type used to train the vector index.  If this is not done then the
    results will be invalid.

    By default "l2" is used.
    """
    self._inner.distance_type(distance_type)
    return self

            
    

            bypass_vector_index

¶

bypass_vector_index() -> Self

    

      
If this is called then any vector index is skipped

An exhaustive (flat) search will be performed.  The query vector will
be compared to every vector in the table.  At high scales this can be
expensive.  However, this is often still useful.  For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

            
              Source code in `lancedb/query.py`
              
2971
2972
2973
2974
2975
2976
2977
2978
2979
2980
2981
2982
def bypass_vector_index(self) -> Self:
    """
    If this is called then any vector index is skipped

    An exhaustive (flat) search will be performed.  The query vector will
    be compared to every vector in the table.  At high scales this can be
    expensive.  However, this is often still useful.  For example, skipping
    the vector index can give you ground truth results which you can use to
    calculate your recall to select an appropriate value for nprobes.
    """
    self._inner.bypass_vector_index()
    return self

            
    

            to_query_object

¶

to_query_object() -> Query

    

      
Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

            
              Source code in `lancedb/query.py`
              
2213
2214
2215
2216
2217
2218
2219
2220
def to_query_object(self) -> Query:
    """
    Convert the query into a query object

    This is currently experimental but can be useful as the query object is pure
    python and more easily serializable.
    """
    return Query.from_inner(self._inner.to_query_request())

            
    

            select

¶

select(columns: Union[List[str], dict[str, str]]) -> Self

    

      
Return only the specified columns.

By default a query will return all columns from the table.  However, this can
have a very significant impact on latency.  LanceDb stores data in a columnar
fashion.  This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b".  This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str].  A column will be
returned for each entry in the map.  The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`.  The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

            
              Source code in `lancedb/query.py`
              
2222
2223
2224
2225
2226
2227
2228
2229
2230
2231
2232
2233
2234
2235
2236
2237
2238
2239
2240
2241
2242
2243
2244
2245
2246
2247
2248
2249
2250
2251
2252
2253
2254
2255
2256
2257
2258
def select(self, columns: Union[List[str], dict[str, str]]) -> Self:
    """
    Return only the specified columns.

    By default a query will return all columns from the table.  However, this can
    have a very significant impact on latency.  LanceDb stores data in a columnar
    fashion.  This
    means we can finely tune our I/O to select exactly the columns we need.

    As a best practice you should always limit queries to the columns that you need.
    If you pass in a list of column names then only those columns will be
    returned.

    You can also use this method to create new "dynamic" columns based on your
    existing columns. For example, you may not care about "a" or "b" but instead
    simply want "a + b".  This is often seen in the SELECT clause of an SQL query
    (e.g. `SELECT a+b FROM my_table`).

    To create dynamic columns you can pass in a dict[str, str].  A column will be
    returned for each entry in the map.  The key provides the name of the column.
    The value is an SQL string used to specify how the column is calculated.

    For example, an SQL query might state `SELECT a + b AS combined, c`.  The
    equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

    Columns will always be returned in the order given, even if that order is
    different than the order used when adding the data.
    """
    if isinstance(columns, list) and all(isinstance(c, str) for c in columns):
        self._inner.select_columns(columns)
    elif isinstance(columns, dict) and all(
        isinstance(k, str) and isinstance(v, str) for k, v in columns.items()
    ):
        self._inner.select(list(columns.items()))
    else:
        raise TypeError("columns must be a list of column names or a dict")
    return self

            
    

            with_row_id

¶

with_row_id() -> Self

    

      
Include the _rowid column in the results.

            
              Source code in `lancedb/query.py`
              
2260
2261
2262
2263
2264
2265
def with_row_id(self) -> Self:
    """
    Include the _rowid column in the results.
    """
    self._inner.with_row_id()
    return self

            
    

            output_schema

  
      `async`
  

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
2295
2296
2297
2298
2299
2300
2301
async def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return await self._inner.output_schema()

            
    

            to_arrow

  
      `async`
  

¶

to_arrow(timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning.  If
you expect a large number of results, you may want to use
to_batches

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2303
2304
2305
2306
2307
2308
2309
2310
2311
2312
2313
2314
2315
2316
2317
2318
2319
2320
2321
async def to_arrow(self, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and collect the results into an Apache Arrow Table.

    This method will collect all results into memory before returning.  If
    you expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches]

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    batch_iter = await self.to_batches(timeout=timeout)
    return pa.Table.from_batches(
        await batch_iter.read_all(), schema=batch_iter.schema
    )

            
    

            to_list

  
      `async`
  

¶

to_list(timeout: Optional[timedelta] = None) -> List[dict]

    

      
Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2323
2324
2325
2326
2327
2328
2329
2330
2331
2332
2333
2334
2335
2336
2337
2338
async def to_list(self, timeout: Optional[timedelta] = None) -> List[dict]:
    """
    Execute the query and return the results as a list of dictionaries.

    Each list entry is a dictionary with the selected column names as keys,
    or all table columns if `select` is not called. The vector and the "_distance"
    fields are returned whether or not they're explicitly selected.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (await self.to_arrow(timeout=timeout)).to_pylist()

            
    

            to_pandas

  
      `async`
  

¶

to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'

    

      
Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
pandas separately.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())

Parameters:

    
        
- 
          `flatten`
              (`Optional[Union[int, bool]]`, default:
                  `None`
)
          –
          
            
If flatten is True, flatten all nested columns.
If flatten is an integer, flatten the nested columns up to the
specified depth.
If unspecified, do not flatten the nested columns.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2340
2341
2342
2343
2344
2345
2346
2347
2348
2349
2350
2351
2352
2353
2354
2355
2356
2357
2358
2359
2360
2361
2362
2363
2364
2365
2366
2367
2368
2369
2370
2371
2372
2373
2374
2375
2376
2377
2378
2379
async def to_pandas(
    self,
    flatten: Optional[Union[int, bool]] = None,
    timeout: Optional[timedelta] = None,
) -> "pd.DataFrame":
    """
    Execute the query and collect the results into a pandas DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    pandas separately.

    Examples
    --------

    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = batch.to_pandas()
    >>> asyncio.run(doctest_example())

    Parameters
    ----------
    flatten: Optional[Union[int, bool]]
        If flatten is True, flatten all nested columns.
        If flatten is an integer, flatten the nested columns up to the
        specified depth.
        If unspecified, do not flatten the nested columns.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (
        flatten_columns(await self.to_arrow(timeout=timeout), flatten)
    ).to_pandas()

            
    

            to_polars

  
      `async`
  

¶

to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'

    

      
Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
polars separately.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

Examples:

    
>>> import asyncio
>>> import polars as pl
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())

            
              Source code in `lancedb/query.py`
              
2381
2382
2383
2384
2385
2386
2387
2388
2389
2390
2391
2392
2393
2394
2395
2396
2397
2398
2399
2400
2401
2402
2403
2404
2405
2406
2407
2408
2409
2410
2411
2412
2413
2414
2415
async def to_polars(
    self,
    timeout: Optional[timedelta] = None,
) -> "pl.DataFrame":
    """
    Execute the query and collect the results into a Polars DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    polars separately.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.

    Examples
    --------

    >>> import asyncio
    >>> import polars as pl
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = pl.from_arrow(batch)
    >>> asyncio.run(doctest_example())
    """
    import polars as pl

    return pl.from_arrow(await self.to_arrow(timeout=timeout))

            
    

            to_pydantic

  
      `async`
  

¶

to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]

    

      
Convert results to a list of pydantic models.

Parameters:

    
        
- 
          `model`
              (`Type[LanceModel]`)
          –
          
            
The pydantic model to use.

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `list[LanceModel]`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2417
2418
2419
2420
2421
2422
2423
2424
2425
2426
2427
2428
2429
2430
2431
2432
2433
2434
2435
2436
2437
async def to_pydantic(
    self, model: Type[LanceModel], *, timeout: Optional[timedelta] = None
) -> List[LanceModel]:
    """
    Convert results to a list of pydantic models.

    Parameters
    ----------
    model : Type[LanceModel]
        The pydantic model to use.
    timeout : timedelta, optional
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    list[LanceModel]
    """
    return [
        model(**row) for row in (await self.to_arrow(timeout=timeout)).to_pylist()
    ]

            
    

            explain_plan

  
      `async`
  

¶

explain_plan(verbose: Optional[bool] = False)

    

      
Return the execution plan for this query.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2439
2440
2441
2442
2443
2444
2445
2446
2447
2448
2449
2450
2451
2452
2453
2454
2455
2456
2457
2458
2459
2460
2461
2462
2463
2464
2465
2466
2467
2468
2469
async def explain_plan(self, verbose: Optional[bool] = False):
    """Return the execution plan for this query.

    Examples
    --------
    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
    ...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
    ...     print(plan)
    >>> asyncio.run(doctest_example()) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
      GlobalLimitExec: skip=0, fetch=10
        FilterExec: _distance@2 IS NOT NULL
          SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
            KNNVectorDistance: metric=l2
              LanceRead: uri=..., projection=[vector], ...
    <BLANKLINE>

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501
    return await self._inner.explain_plan(verbose)

            
    

            analyze_plan

  
      `async`
  

¶

analyze_plan()

    

      
Execute the query and display with runtime metrics.

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2471
2472
2473
2474
2475
2476
2477
2478
async def analyze_plan(self):
    """Execute the query and display with runtime metrics.

    Returns
    -------
    plan : str
    """
    return await self._inner.analyze_plan()

            
    

            where

¶

where(predicate: str) -> Self

    

      
Only return rows matching the given predicate

The predicate should be supplied as an SQL query string.

Examples:

    
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"

    
Filtering performance can often be improved by creating a scalar index
on the filter column(s).

            
              Source code in `lancedb/query.py`
              
2495
2496
2497
2498
2499
2500
2501
2502
2503
2504
2505
2506
2507
2508
2509
2510
2511
2512
def where(self, predicate: str) -> Self:
    """
    Only return rows matching the given predicate

    The predicate should be supplied as an SQL query string.

    Examples
    --------

    >>> predicate = "x > 10"
    >>> predicate = "y > 0 AND y < 100"
    >>> predicate = "x > 5 OR y = 'test'"

    Filtering performance can often be improved by creating a scalar index
    on the filter column(s).
    """
    self._inner.where(predicate)
    return self

            
    

            limit

¶

limit(limit: int) -> Self

    

      
Set the maximum number of results to return.

By default, a plain search has no limit.  If this method is not
called then every valid row from the table will be returned.

            
              Source code in `lancedb/query.py`
              
2514
2515
2516
2517
2518
2519
2520
2521
2522
def limit(self, limit: int) -> Self:
    """
    Set the maximum number of results to return.

    By default, a plain search has no limit.  If this method is not
    called then every valid row from the table will be returned.
    """
    self._inner.limit(limit)
    return self

            
    

            offset

¶

offset(offset: int) -> Self

    

      
Set the offset for the results.

Parameters:

    
        
- 
          `offset`
              (`int`)
          –
          
            
The offset to start fetching results from.

          
        
    

            
              Source code in `lancedb/query.py`
              
2524
2525
2526
2527
2528
2529
2530
2531
2532
2533
2534
def offset(self, offset: int) -> Self:
    """
    Set the offset for the results.

    Parameters
    ----------
    offset: int
        The offset to start fetching results from.
    """
    self._inner.offset(offset)
    return self

            
    

            fast_search

¶

fast_search() -> Self

    

      
Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
AsyncTable.optimize.

            
              Source code in `lancedb/query.py`
              
2536
2537
2538
2539
2540
2541
2542
2543
2544
2545
2546
2547
2548
def fast_search(self) -> Self:
    """
    Skip searching un-indexed data.

    This can make queries faster, but will miss any data that has not been
    indexed.

    !!! tip
        You can add new data into an existing index by calling
        [AsyncTable.optimize][lancedb.table.AsyncTable.optimize].
    """
    self._inner.fast_search()
    return self

            
    

            postfilter

¶

postfilter() -> Self

    

      
If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search.  This is how
filtering is typically understood to work.  This prefilter step does add some
additional latency.  Creating a scalar index on the filter column(s) can
often improve this latency.  However, sometimes a filter is too complex or
scalar indices cannot be applied to the column.  In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search.  This
means we only run the filter on a much smaller set of data.  However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

            
              Source code in `lancedb/query.py`
              
2550
2551
2552
2553
2554
2555
2556
2557
2558
2559
2560
2561
2562
2563
2564
2565
2566
2567
2568
2569
def postfilter(self) -> Self:
    """
    If this is called then filtering will happen after the search instead of
    before.
    By default filtering will be performed before the search.  This is how
    filtering is typically understood to work.  This prefilter step does add some
    additional latency.  Creating a scalar index on the filter column(s) can
    often improve this latency.  However, sometimes a filter is too complex or
    scalar indices cannot be applied to the column.  In these cases postfiltering
    can be used instead of prefiltering to improve latency.
    Post filtering applies the filter to the results of the search.  This
    means we only run the filter on a much smaller set of data.  However, it can
    cause the query to return fewer than `limit` results (or even no results) if
    none of the nearest results match the filter.
    Post filtering happens during the "refine stage" (described in more detail in
    @see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
    factor can often help restore some of the results lost by post filtering.
    """
    self._inner.postfilter()
    return self

            
    

            __init__

¶

__init__(inner: VectorQuery)

    

      
Construct an AsyncVectorQuery

This method is not intended to be called directly.  Instead, create
a query first with AsyncTable.query and then
use AsyncQuery.nearest_to] to convert to
a vector query.  Or you can use
AsyncTable.vector_search

            
              Source code in `lancedb/query.py`
              
2986
2987
2988
2989
2990
2991
2992
2993
2994
2995
2996
2997
2998
2999
def __init__(self, inner: LanceVectorQuery):
    """
    Construct an AsyncVectorQuery

    This method is not intended to be called directly.  Instead, create
    a query first with [AsyncTable.query][lancedb.table.AsyncTable.query] and then
    use [AsyncQuery.nearest_to][lancedb.query.AsyncQuery.nearest_to]] to convert to
    a vector query.  Or you can use
    [AsyncTable.vector_search][lancedb.table.AsyncTable.vector_search]
    """
    super().__init__(inner)
    self._inner = inner
    self._reranker = None
    self._query_string = None

            
    

            nearest_to_text

¶

nearest_to_text(query: str | FullTextQuery, columns: Union[str, List[str], None] = None) -> AsyncHybridQuery

    

      
Find the documents that are most relevant to the given text query,
in addition to vector search.

This converts the vector query into a hybrid query.

This search will perform a full text search on the table and return
the most relevant documents, combined with the vector query results.
The text relevance is determined by BM25.

The columns to search must be with native FTS index
(Tantivy-based can't work with this method).

By default, all indexed columns are searched,
now only one column can be searched at a time.

Parameters:

    
        
- 
          `query`
              (`str | FullTextQuery`)
          –
          
            
The text query to search for.

          
        
        
- 
          `columns`
              (`Union[str, List[str], None]`, default:
                  `None`
)
          –
          
            
The columns to search in. If None, all indexed columns are searched.
For now only one column can be searched at a time.

          
        
    

            
              Source code in `lancedb/query.py`
              
3016
3017
3018
3019
3020
3021
3022
3023
3024
3025
3026
3027
3028
3029
3030
3031
3032
3033
3034
3035
3036
3037
3038
3039
3040
3041
3042
3043
3044
3045
3046
3047
3048
3049
3050
3051
3052
3053
def nearest_to_text(
    self, query: str | FullTextQuery, columns: Union[str, List[str], None] = None
) -> AsyncHybridQuery:
    """
    Find the documents that are most relevant to the given text query,
    in addition to vector search.

    This converts the vector query into a hybrid query.

    This search will perform a full text search on the table and return
    the most relevant documents, combined with the vector query results.
    The text relevance is determined by BM25.

    The columns to search must be with native FTS index
    (Tantivy-based can't work with this method).

    By default, all indexed columns are searched,
    now only one column can be searched at a time.

    Parameters
    ----------
    query: str
        The text query to search for.
    columns: str or list of str, default None
        The columns to search in. If None, all indexed columns are searched.
        For now only one column can be searched at a time.
    """
    if isinstance(columns, str):
        columns = [columns]
    if columns is None:
        columns = []

    if isinstance(query, str):
        return AsyncHybridQuery(
            self._inner.nearest_to_text({"query": query, "columns": columns})
        )
    # FullTextQuery object
    return AsyncHybridQuery(self._inner.nearest_to_text({"query": query}))

            
    

  

    

            lancedb.query.AsyncFTSQuery

¶

    
            

              Bases: `AsyncStandardQuery`

      
A query for full text search for LanceDB.

              
                Source code in `lancedb/query.py`
                
2706
2707
2708
2709
2710
2711
2712
2713
2714
2715
2716
2717
2718
2719
2720
2721
2722
2723
2724
2725
2726
2727
2728
2729
2730
2731
2732
2733
2734
2735
2736
2737
2738
2739
2740
2741
2742
2743
2744
2745
2746
2747
2748
2749
2750
2751
2752
2753
2754
2755
2756
2757
2758
2759
2760
2761
2762
2763
2764
2765
2766
2767
2768
2769
2770
2771
2772
2773
2774
2775
2776
2777
2778
2779
2780
2781
2782
2783
2784
2785
2786
2787
2788
2789
2790
2791
2792
2793
2794
2795
2796
2797
2798
2799
2800
2801
2802
2803
2804
2805
2806
2807
2808
class AsyncFTSQuery(AsyncStandardQuery):
    """A query for full text search for LanceDB."""

    def __init__(self, inner: LanceFTSQuery):
        super().__init__(inner)
        self._inner = inner
        self._reranker = None

    def get_query(self) -> str:
        return self._inner.get_query()

    def rerank(
        self,
        reranker: Reranker = RRFReranker(),
    ) -> AsyncFTSQuery:
        if reranker and not isinstance(reranker, Reranker):
            raise ValueError("reranker must be an instance of Reranker class.")

        self._reranker = reranker

        return self

    def nearest_to(
        self,
        query_vector: Union[VEC, Tuple, List[VEC]],
    ) -> AsyncHybridQuery:
        """
        In addition doing text search on the LanceDB Table, also
        find the nearest vectors to the given query vector.

        This converts the query from a FTS Query to a Hybrid query. Results
        from the vector search will be combined with results from the FTS query.

        This method will attempt to convert the input to the query vector
        expected by the embedding model.  If the input cannot be converted
        then an error will be thrown.

        By default, there is no embedding model, and the input should be
        something that can be converted to a pyarrow array of floats.  This
        includes lists, numpy arrays, and tuples.

        If there is only one vector column (a column whose data type is a
        fixed size list of floats) then the column does not need to be specified.
        If there is more than one vector column you must use
        [AsyncVectorQuery.column][lancedb.query.AsyncVectorQuery.column] to specify
        which column you would like to compare with.

        If no index has been created on the vector column then a vector query
        will perform a distance comparison between the query vector and every
        vector in the database and then sort the results.  This is sometimes
        called a "flat search"

        For small databases, with tens of thousands of vectors or less, this can
        be reasonably fast.  In larger databases you should create a vector index
        on the column.  If there is a vector index then an "approximate" nearest
        neighbor search (frequently called an ANN search) will be performed.  This
        search is much faster, but the results will be approximate.

        The query can be further parameterized using the returned builder.  There
        are various ANN search parameters that will let you fine tune your recall
        accuracy vs search latency.

        Hybrid searches always have a [limit][].  If `limit` has not been called then
        a default `limit` of 10 will be used.

        Typically, a single vector is passed in as the query. However, you can also
        pass in multiple vectors.  This can be useful if you want to find the nearest
        vectors to multiple query vectors. This is not expected to be faster than
        making multiple queries concurrently; it is just a convenience method.
        If multiple vectors are passed in then an additional column `query_index`
        will be added to the results.  This column will contain the index of the
        query vector that the result is nearest to.
        """
        if query_vector is None:
            raise ValueError("query_vector can not be None")

        if (
            isinstance(query_vector, list)
            and len(query_vector) > 0
            and not isinstance(query_vector[0], (float, int))
        ):
            # multiple have been passed
            query_vectors = [AsyncQuery._query_vec_to_array(v) for v in query_vector]
            new_self = self._inner.nearest_to(query_vectors[0])
            for v in query_vectors[1:]:
                new_self.add_query_vector(v)
            return AsyncHybridQuery(new_self)
        else:
            return AsyncHybridQuery(
                self._inner.nearest_to(AsyncQuery._query_vec_to_array(query_vector))
            )

    async def to_batches(
        self,
        *,
        max_batch_length: Optional[int] = None,
        timeout: Optional[timedelta] = None,
    ) -> AsyncRecordBatchReader:
        reader = await super().to_batches(timeout=timeout)
        results = pa.Table.from_batches(await reader.read_all(), reader.schema)
        if self._reranker:
            results = self._reranker.rerank_fts(self.get_query(), results)
        return AsyncRecordBatchReader(results, max_batch_length=max_batch_length)

              

  

            to_query_object

¶

to_query_object() -> Query

    

      
Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

            
              Source code in `lancedb/query.py`
              
2213
2214
2215
2216
2217
2218
2219
2220
def to_query_object(self) -> Query:
    """
    Convert the query into a query object

    This is currently experimental but can be useful as the query object is pure
    python and more easily serializable.
    """
    return Query.from_inner(self._inner.to_query_request())

            
    

            select

¶

select(columns: Union[List[str], dict[str, str]]) -> Self

    

      
Return only the specified columns.

By default a query will return all columns from the table.  However, this can
have a very significant impact on latency.  LanceDb stores data in a columnar
fashion.  This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b".  This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str].  A column will be
returned for each entry in the map.  The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`.  The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

            
              Source code in `lancedb/query.py`
              
2222
2223
2224
2225
2226
2227
2228
2229
2230
2231
2232
2233
2234
2235
2236
2237
2238
2239
2240
2241
2242
2243
2244
2245
2246
2247
2248
2249
2250
2251
2252
2253
2254
2255
2256
2257
2258
def select(self, columns: Union[List[str], dict[str, str]]) -> Self:
    """
    Return only the specified columns.

    By default a query will return all columns from the table.  However, this can
    have a very significant impact on latency.  LanceDb stores data in a columnar
    fashion.  This
    means we can finely tune our I/O to select exactly the columns we need.

    As a best practice you should always limit queries to the columns that you need.
    If you pass in a list of column names then only those columns will be
    returned.

    You can also use this method to create new "dynamic" columns based on your
    existing columns. For example, you may not care about "a" or "b" but instead
    simply want "a + b".  This is often seen in the SELECT clause of an SQL query
    (e.g. `SELECT a+b FROM my_table`).

    To create dynamic columns you can pass in a dict[str, str].  A column will be
    returned for each entry in the map.  The key provides the name of the column.
    The value is an SQL string used to specify how the column is calculated.

    For example, an SQL query might state `SELECT a + b AS combined, c`.  The
    equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

    Columns will always be returned in the order given, even if that order is
    different than the order used when adding the data.
    """
    if isinstance(columns, list) and all(isinstance(c, str) for c in columns):
        self._inner.select_columns(columns)
    elif isinstance(columns, dict) and all(
        isinstance(k, str) and isinstance(v, str) for k, v in columns.items()
    ):
        self._inner.select(list(columns.items()))
    else:
        raise TypeError("columns must be a list of column names or a dict")
    return self

            
    

            with_row_id

¶

with_row_id() -> Self

    

      
Include the _rowid column in the results.

            
              Source code in `lancedb/query.py`
              
2260
2261
2262
2263
2264
2265
def with_row_id(self) -> Self:
    """
    Include the _rowid column in the results.
    """
    self._inner.with_row_id()
    return self

            
    

            output_schema

  
      `async`
  

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
2295
2296
2297
2298
2299
2300
2301
async def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return await self._inner.output_schema()

            
    

            to_arrow

  
      `async`
  

¶

to_arrow(timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning.  If
you expect a large number of results, you may want to use
to_batches

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2303
2304
2305
2306
2307
2308
2309
2310
2311
2312
2313
2314
2315
2316
2317
2318
2319
2320
2321
async def to_arrow(self, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and collect the results into an Apache Arrow Table.

    This method will collect all results into memory before returning.  If
    you expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches]

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    batch_iter = await self.to_batches(timeout=timeout)
    return pa.Table.from_batches(
        await batch_iter.read_all(), schema=batch_iter.schema
    )

            
    

            to_list

  
      `async`
  

¶

to_list(timeout: Optional[timedelta] = None) -> List[dict]

    

      
Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2323
2324
2325
2326
2327
2328
2329
2330
2331
2332
2333
2334
2335
2336
2337
2338
async def to_list(self, timeout: Optional[timedelta] = None) -> List[dict]:
    """
    Execute the query and return the results as a list of dictionaries.

    Each list entry is a dictionary with the selected column names as keys,
    or all table columns if `select` is not called. The vector and the "_distance"
    fields are returned whether or not they're explicitly selected.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (await self.to_arrow(timeout=timeout)).to_pylist()

            
    

            to_pandas

  
      `async`
  

¶

to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'

    

      
Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
pandas separately.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())

Parameters:

    
        
- 
          `flatten`
              (`Optional[Union[int, bool]]`, default:
                  `None`
)
          –
          
            
If flatten is True, flatten all nested columns.
If flatten is an integer, flatten the nested columns up to the
specified depth.
If unspecified, do not flatten the nested columns.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2340
2341
2342
2343
2344
2345
2346
2347
2348
2349
2350
2351
2352
2353
2354
2355
2356
2357
2358
2359
2360
2361
2362
2363
2364
2365
2366
2367
2368
2369
2370
2371
2372
2373
2374
2375
2376
2377
2378
2379
async def to_pandas(
    self,
    flatten: Optional[Union[int, bool]] = None,
    timeout: Optional[timedelta] = None,
) -> "pd.DataFrame":
    """
    Execute the query and collect the results into a pandas DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    pandas separately.

    Examples
    --------

    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = batch.to_pandas()
    >>> asyncio.run(doctest_example())

    Parameters
    ----------
    flatten: Optional[Union[int, bool]]
        If flatten is True, flatten all nested columns.
        If flatten is an integer, flatten the nested columns up to the
        specified depth.
        If unspecified, do not flatten the nested columns.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (
        flatten_columns(await self.to_arrow(timeout=timeout), flatten)
    ).to_pandas()

            
    

            to_polars

  
      `async`
  

¶

to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'

    

      
Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
polars separately.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

Examples:

    
>>> import asyncio
>>> import polars as pl
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())

            
              Source code in `lancedb/query.py`
              
2381
2382
2383
2384
2385
2386
2387
2388
2389
2390
2391
2392
2393
2394
2395
2396
2397
2398
2399
2400
2401
2402
2403
2404
2405
2406
2407
2408
2409
2410
2411
2412
2413
2414
2415
async def to_polars(
    self,
    timeout: Optional[timedelta] = None,
) -> "pl.DataFrame":
    """
    Execute the query and collect the results into a Polars DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    polars separately.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.

    Examples
    --------

    >>> import asyncio
    >>> import polars as pl
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = pl.from_arrow(batch)
    >>> asyncio.run(doctest_example())
    """
    import polars as pl

    return pl.from_arrow(await self.to_arrow(timeout=timeout))

            
    

            to_pydantic

  
      `async`
  

¶

to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]

    

      
Convert results to a list of pydantic models.

Parameters:

    
        
- 
          `model`
              (`Type[LanceModel]`)
          –
          
            
The pydantic model to use.

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `list[LanceModel]`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2417
2418
2419
2420
2421
2422
2423
2424
2425
2426
2427
2428
2429
2430
2431
2432
2433
2434
2435
2436
2437
async def to_pydantic(
    self, model: Type[LanceModel], *, timeout: Optional[timedelta] = None
) -> List[LanceModel]:
    """
    Convert results to a list of pydantic models.

    Parameters
    ----------
    model : Type[LanceModel]
        The pydantic model to use.
    timeout : timedelta, optional
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    list[LanceModel]
    """
    return [
        model(**row) for row in (await self.to_arrow(timeout=timeout)).to_pylist()
    ]

            
    

            explain_plan

  
      `async`
  

¶

explain_plan(verbose: Optional[bool] = False)

    

      
Return the execution plan for this query.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2439
2440
2441
2442
2443
2444
2445
2446
2447
2448
2449
2450
2451
2452
2453
2454
2455
2456
2457
2458
2459
2460
2461
2462
2463
2464
2465
2466
2467
2468
2469
async def explain_plan(self, verbose: Optional[bool] = False):
    """Return the execution plan for this query.

    Examples
    --------
    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
    ...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
    ...     print(plan)
    >>> asyncio.run(doctest_example()) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
      GlobalLimitExec: skip=0, fetch=10
        FilterExec: _distance@2 IS NOT NULL
          SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
            KNNVectorDistance: metric=l2
              LanceRead: uri=..., projection=[vector], ...
    <BLANKLINE>

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501
    return await self._inner.explain_plan(verbose)

            
    

            analyze_plan

  
      `async`
  

¶

analyze_plan()

    

      
Execute the query and display with runtime metrics.

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2471
2472
2473
2474
2475
2476
2477
2478
async def analyze_plan(self):
    """Execute the query and display with runtime metrics.

    Returns
    -------
    plan : str
    """
    return await self._inner.analyze_plan()

            
    

            where

¶

where(predicate: str) -> Self

    

      
Only return rows matching the given predicate

The predicate should be supplied as an SQL query string.

Examples:

    
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"

    
Filtering performance can often be improved by creating a scalar index
on the filter column(s).

            
              Source code in `lancedb/query.py`
              
2495
2496
2497
2498
2499
2500
2501
2502
2503
2504
2505
2506
2507
2508
2509
2510
2511
2512
def where(self, predicate: str) -> Self:
    """
    Only return rows matching the given predicate

    The predicate should be supplied as an SQL query string.

    Examples
    --------

    >>> predicate = "x > 10"
    >>> predicate = "y > 0 AND y < 100"
    >>> predicate = "x > 5 OR y = 'test'"

    Filtering performance can often be improved by creating a scalar index
    on the filter column(s).
    """
    self._inner.where(predicate)
    return self

            
    

            limit

¶

limit(limit: int) -> Self

    

      
Set the maximum number of results to return.

By default, a plain search has no limit.  If this method is not
called then every valid row from the table will be returned.

            
              Source code in `lancedb/query.py`
              
2514
2515
2516
2517
2518
2519
2520
2521
2522
def limit(self, limit: int) -> Self:
    """
    Set the maximum number of results to return.

    By default, a plain search has no limit.  If this method is not
    called then every valid row from the table will be returned.
    """
    self._inner.limit(limit)
    return self

            
    

            offset

¶

offset(offset: int) -> Self

    

      
Set the offset for the results.

Parameters:

    
        
- 
          `offset`
              (`int`)
          –
          
            
The offset to start fetching results from.

          
        
    

            
              Source code in `lancedb/query.py`
              
2524
2525
2526
2527
2528
2529
2530
2531
2532
2533
2534
def offset(self, offset: int) -> Self:
    """
    Set the offset for the results.

    Parameters
    ----------
    offset: int
        The offset to start fetching results from.
    """
    self._inner.offset(offset)
    return self

            
    

            fast_search

¶

fast_search() -> Self

    

      
Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
AsyncTable.optimize.

            
              Source code in `lancedb/query.py`
              
2536
2537
2538
2539
2540
2541
2542
2543
2544
2545
2546
2547
2548
def fast_search(self) -> Self:
    """
    Skip searching un-indexed data.

    This can make queries faster, but will miss any data that has not been
    indexed.

    !!! tip
        You can add new data into an existing index by calling
        [AsyncTable.optimize][lancedb.table.AsyncTable.optimize].
    """
    self._inner.fast_search()
    return self

            
    

            postfilter

¶

postfilter() -> Self

    

      
If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search.  This is how
filtering is typically understood to work.  This prefilter step does add some
additional latency.  Creating a scalar index on the filter column(s) can
often improve this latency.  However, sometimes a filter is too complex or
scalar indices cannot be applied to the column.  In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search.  This
means we only run the filter on a much smaller set of data.  However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

            
              Source code in `lancedb/query.py`
              
2550
2551
2552
2553
2554
2555
2556
2557
2558
2559
2560
2561
2562
2563
2564
2565
2566
2567
2568
2569
def postfilter(self) -> Self:
    """
    If this is called then filtering will happen after the search instead of
    before.
    By default filtering will be performed before the search.  This is how
    filtering is typically understood to work.  This prefilter step does add some
    additional latency.  Creating a scalar index on the filter column(s) can
    often improve this latency.  However, sometimes a filter is too complex or
    scalar indices cannot be applied to the column.  In these cases postfiltering
    can be used instead of prefiltering to improve latency.
    Post filtering applies the filter to the results of the search.  This
    means we only run the filter on a much smaller set of data.  However, it can
    cause the query to return fewer than `limit` results (or even no results) if
    none of the nearest results match the filter.
    Post filtering happens during the "refine stage" (described in more detail in
    @see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
    factor can often help restore some of the results lost by post filtering.
    """
    self._inner.postfilter()
    return self

            
    

            nearest_to

¶

nearest_to(query_vector: Union[VEC, Tuple, List[VEC]]) -> AsyncHybridQuery

    

      
In addition doing text search on the LanceDB Table, also
find the nearest vectors to the given query vector.

This converts the query from a FTS Query to a Hybrid query. Results
from the vector search will be combined with results from the FTS query.

This method will attempt to convert the input to the query vector
expected by the embedding model.  If the input cannot be converted
then an error will be thrown.

By default, there is no embedding model, and the input should be
something that can be converted to a pyarrow array of floats.  This
includes lists, numpy arrays, and tuples.

If there is only one vector column (a column whose data type is a
fixed size list of floats) then the column does not need to be specified.
If there is more than one vector column you must use
AsyncVectorQuery.column to specify
which column you would like to compare with.

If no index has been created on the vector column then a vector query
will perform a distance comparison between the query vector and every
vector in the database and then sort the results.  This is sometimes
called a "flat search"

For small databases, with tens of thousands of vectors or less, this can
be reasonably fast.  In larger databases you should create a vector index
on the column.  If there is a vector index then an "approximate" nearest
neighbor search (frequently called an ANN search) will be performed.  This
search is much faster, but the results will be approximate.

The query can be further parameterized using the returned builder.  There
are various ANN search parameters that will let you fine tune your recall
accuracy vs search latency.

Hybrid searches always have a limit.  If `limit` has not been called then
a default `limit` of 10 will be used.

Typically, a single vector is passed in as the query. However, you can also
pass in multiple vectors.  This can be useful if you want to find the nearest
vectors to multiple query vectors. This is not expected to be faster than
making multiple queries concurrently; it is just a convenience method.
If multiple vectors are passed in then an additional column `query_index`
will be added to the results.  This column will contain the index of the
query vector that the result is nearest to.

            
              Source code in `lancedb/query.py`
              
2728
2729
2730
2731
2732
2733
2734
2735
2736
2737
2738
2739
2740
2741
2742
2743
2744
2745
2746
2747
2748
2749
2750
2751
2752
2753
2754
2755
2756
2757
2758
2759
2760
2761
2762
2763
2764
2765
2766
2767
2768
2769
2770
2771
2772
2773
2774
2775
2776
2777
2778
2779
2780
2781
2782
2783
2784
2785
2786
2787
2788
2789
2790
2791
2792
2793
2794
2795
2796
def nearest_to(
    self,
    query_vector: Union[VEC, Tuple, List[VEC]],
) -> AsyncHybridQuery:
    """
    In addition doing text search on the LanceDB Table, also
    find the nearest vectors to the given query vector.

    This converts the query from a FTS Query to a Hybrid query. Results
    from the vector search will be combined with results from the FTS query.

    This method will attempt to convert the input to the query vector
    expected by the embedding model.  If the input cannot be converted
    then an error will be thrown.

    By default, there is no embedding model, and the input should be
    something that can be converted to a pyarrow array of floats.  This
    includes lists, numpy arrays, and tuples.

    If there is only one vector column (a column whose data type is a
    fixed size list of floats) then the column does not need to be specified.
    If there is more than one vector column you must use
    [AsyncVectorQuery.column][lancedb.query.AsyncVectorQuery.column] to specify
    which column you would like to compare with.

    If no index has been created on the vector column then a vector query
    will perform a distance comparison between the query vector and every
    vector in the database and then sort the results.  This is sometimes
    called a "flat search"

    For small databases, with tens of thousands of vectors or less, this can
    be reasonably fast.  In larger databases you should create a vector index
    on the column.  If there is a vector index then an "approximate" nearest
    neighbor search (frequently called an ANN search) will be performed.  This
    search is much faster, but the results will be approximate.

    The query can be further parameterized using the returned builder.  There
    are various ANN search parameters that will let you fine tune your recall
    accuracy vs search latency.

    Hybrid searches always have a [limit][].  If `limit` has not been called then
    a default `limit` of 10 will be used.

    Typically, a single vector is passed in as the query. However, you can also
    pass in multiple vectors.  This can be useful if you want to find the nearest
    vectors to multiple query vectors. This is not expected to be faster than
    making multiple queries concurrently; it is just a convenience method.
    If multiple vectors are passed in then an additional column `query_index`
    will be added to the results.  This column will contain the index of the
    query vector that the result is nearest to.
    """
    if query_vector is None:
        raise ValueError("query_vector can not be None")

    if (
        isinstance(query_vector, list)
        and len(query_vector) > 0
        and not isinstance(query_vector[0], (float, int))
    ):
        # multiple have been passed
        query_vectors = [AsyncQuery._query_vec_to_array(v) for v in query_vector]
        new_self = self._inner.nearest_to(query_vectors[0])
        for v in query_vectors[1:]:
            new_self.add_query_vector(v)
        return AsyncHybridQuery(new_self)
    else:
        return AsyncHybridQuery(
            self._inner.nearest_to(AsyncQuery._query_vec_to_array(query_vector))
        )

            
    

  

    

            lancedb.query.AsyncHybridQuery

¶

    
            

              Bases: `AsyncStandardQuery`, `AsyncVectorQueryBase`

      
A query builder that performs hybrid vector and full text search.
Results are combined and reranked based on the specified reranker.
By default, the results are reranked using the RRFReranker, which
uses reciprocal rank fusion score for reranking.

To make the vector and fts results comparable, the scores are normalized.
Instead of normalizing scores, the `normalize` parameter can be set to "rank"
in the `rerank` method to convert the scores to ranks and then normalize them.

              
                Source code in `lancedb/query.py`
                
3068
3069
3070
3071
3072
3073
3074
3075
3076
3077
3078
3079
3080
3081
3082
3083
3084
3085
3086
3087
3088
3089
3090
3091
3092
3093
3094
3095
3096
3097
3098
3099
3100
3101
3102
3103
3104
3105
3106
3107
3108
3109
3110
3111
3112
3113
3114
3115
3116
3117
3118
3119
3120
3121
3122
3123
3124
3125
3126
3127
3128
3129
3130
3131
3132
3133
3134
3135
3136
3137
3138
3139
3140
3141
3142
3143
3144
3145
3146
3147
3148
3149
3150
3151
3152
3153
3154
3155
3156
3157
3158
3159
3160
3161
3162
3163
3164
3165
3166
3167
3168
3169
3170
3171
3172
3173
3174
3175
3176
3177
3178
3179
3180
3181
3182
3183
3184
3185
3186
3187
3188
3189
3190
3191
3192
3193
3194
3195
3196
3197
3198
3199
3200
3201
3202
3203
3204
3205
3206
3207
3208
3209
3210
3211
3212
3213
3214
3215
class AsyncHybridQuery(AsyncStandardQuery, AsyncVectorQueryBase):
    """
    A query builder that performs hybrid vector and full text search.
    Results are combined and reranked based on the specified reranker.
    By default, the results are reranked using the RRFReranker, which
    uses reciprocal rank fusion score for reranking.

    To make the vector and fts results comparable, the scores are normalized.
    Instead of normalizing scores, the `normalize` parameter can be set to "rank"
    in the `rerank` method to convert the scores to ranks and then normalize them.
    """

    def __init__(self, inner: LanceHybridQuery):
        super().__init__(inner)
        self._inner = inner
        self._norm = "score"
        self._reranker = RRFReranker()

    def rerank(
        self, reranker: Reranker = RRFReranker(), normalize: str = "score"
    ) -> AsyncHybridQuery:
        """
        Rerank the hybrid search results using the specified reranker. The reranker
        must be an instance of Reranker class.

        Parameters
        ----------
        reranker: Reranker, default RRFReranker()
            The reranker to use. Must be an instance of Reranker class.
        normalize: str, default "score"
            The method to normalize the scores. Can be "rank" or "score". If "rank",
            the scores are converted to ranks and then normalized. If "score", the
            scores are normalized directly.
        Returns
        -------
        AsyncHybridQuery
            The AsyncHybridQuery object.
        """
        if normalize not in ["rank", "score"]:
            raise ValueError("normalize must be 'rank' or 'score'.")
        if reranker and not isinstance(reranker, Reranker):
            raise ValueError("reranker must be an instance of Reranker class.")

        self._norm = normalize
        self._reranker = reranker

        return self

    async def to_batches(
        self,
        *,
        max_batch_length: Optional[int] = None,
        timeout: Optional[timedelta] = None,
    ) -> AsyncRecordBatchReader:
        fts_query = AsyncFTSQuery(self._inner.to_fts_query())
        vec_query = AsyncVectorQuery(self._inner.to_vector_query())

        # save the row ID choice that was made on the query builder and force it
        # to actually fetch the row ids because we need this for reranking
        with_row_ids = self._inner.get_with_row_id()
        fts_query.with_row_id()
        vec_query.with_row_id()

        fts_results, vector_results = await asyncio.gather(
            fts_query.to_arrow(timeout=timeout),
            vec_query.to_arrow(timeout=timeout),
        )

        result = LanceHybridQueryBuilder._combine_hybrid_results(
            fts_results=fts_results,
            vector_results=vector_results,
            norm=self._norm,
            fts_query=fts_query.get_query(),
            reranker=self._reranker,
            limit=self._inner.get_limit(),
            with_row_ids=with_row_ids,
        )

        return AsyncRecordBatchReader(result, max_batch_length=max_batch_length)

    async def explain_plan(self, verbose: Optional[bool] = False):
        """Return the execution plan for this query.

        The output includes both the vector and FTS search plans.

        Examples
        --------
        >>> import asyncio
        >>> from lancedb import connect_async
        >>> from lancedb.index import FTS
        >>> async def doctest_example():
        ...     conn = await connect_async("./.lancedb")
        ...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0], "text": "hello world"}])
        ...     await table.create_index("text", config=FTS(with_position=False))
        ...     plan = await table.query().nearest_to([1.0, 2.0]).nearest_to_text("hello").explain_plan(True)
        ...     print(plan)
        >>> asyncio.run(doctest_example()) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        RRFReranker(K=60)
            ProjectionExec: expr=[vector@0 as vector, text@3 as text, _distance@2 as _distance]
              Take: columns="vector, _rowid, _distance, (text)"
                CoalesceBatchesExec: target_batch_size=1024
                  GlobalLimitExec: skip=0, fetch=10
                    FilterExec: _distance@2 IS NOT NULL
                      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                        KNNVectorDistance: metric=l2
                          LanceRead: uri=..., projection=[vector], ...
            ProjectionExec: expr=[vector@2 as vector, text@3 as text, _score@1 as _score]
              Take: columns="_rowid, _score, (vector), (text)"
                CoalesceBatchesExec: target_batch_size=1024
                  GlobalLimitExec: skip=0, fetch=10
                    MatchQuery: column=text, query=hello

        Parameters
        ----------
        verbose : bool, default False
            Use a verbose output format.

        Returns
        -------
        plan : str
        """  # noqa: E501

        vector_plan = await self._inner.to_vector_query().explain_plan(verbose)
        fts_plan = await self._inner.to_fts_query().explain_plan(verbose)
        # Indent sub-plans under the reranker
        indented_vector = "\n".join("  " + line for line in vector_plan.splitlines())
        indented_fts = "\n".join("  " + line for line in fts_plan.splitlines())
        return f"{self._reranker}\n  {indented_vector}\n  {indented_fts}"

    async def analyze_plan(self):
        """
        Execute the query and return the physical execution plan with runtime metrics.

        This runs both the vector and FTS (full-text search) queries and returns
        detailed metrics for each step of execution—such as rows processed,
        elapsed time, I/O stats, and more. It’s useful for debugging and
        performance analysis.

        Returns
        -------
        plan : str
        """
        results = ["Vector Search Query:"]
        results.append(await self._inner.to_vector_query().analyze_plan())
        results.append("FTS Search Query:")
        results.append(await self._inner.to_fts_query().analyze_plan())

        return "\n".join(results)

              

  

            column

¶

column(column: str) -> Self

    

      
Set the vector column to query

This controls which column is compared to the query vector supplied in
the call to AsyncQuery.nearest_to.

This parameter must be specified if the table has more than one column
whose data type is a fixed-size-list of floats.

            
              Source code in `lancedb/query.py`
              
2812
2813
2814
2815
2816
2817
2818
2819
2820
2821
2822
2823
def column(self, column: str) -> Self:
    """
    Set the vector column to query

    This controls which column is compared to the query vector supplied in
    the call to [AsyncQuery.nearest_to][lancedb.query.AsyncQuery.nearest_to].

    This parameter must be specified if the table has more than one column
    whose data type is a fixed-size-list of floats.
    """
    self._inner.column(column)
    return self

            
    

            nprobes

¶

nprobes(nprobes: int) -> Self

    

      
Set the number of partitions to search (probe)

This argument is only used when the vector column has an IVF-based index.
If there is no index then this value is ignored.

The IVF stage of IVF PQ divides the input into partitions (clusters) of
related values.

The partition whose centroids are closest to the query vector will be
exhaustiely searched to find matches.  This parameter controls how many
partitions should be searched.

Increasing this value will increase the recall of your query but will
also increase the latency of your query.  The default value is 20.  This
default is good for many cases but the best value to use will depend on
your data and the recall that you need to achieve.

For best results we recommend tuning this parameter with a benchmark against
your actual data to find the smallest possible value that will still give
you the desired recall.

            
              Source code in `lancedb/query.py`
              
2825
2826
2827
2828
2829
2830
2831
2832
2833
2834
2835
2836
2837
2838
2839
2840
2841
2842
2843
2844
2845
2846
2847
2848
2849
def nprobes(self, nprobes: int) -> Self:
    """
    Set the number of partitions to search (probe)

    This argument is only used when the vector column has an IVF-based index.
    If there is no index then this value is ignored.

    The IVF stage of IVF PQ divides the input into partitions (clusters) of
    related values.

    The partition whose centroids are closest to the query vector will be
    exhaustiely searched to find matches.  This parameter controls how many
    partitions should be searched.

    Increasing this value will increase the recall of your query but will
    also increase the latency of your query.  The default value is 20.  This
    default is good for many cases but the best value to use will depend on
    your data and the recall that you need to achieve.

    For best results we recommend tuning this parameter with a benchmark against
    your actual data to find the smallest possible value that will still give
    you the desired recall.
    """
    self._inner.nprobes(nprobes)
    return self

            
    

            minimum_nprobes

¶

minimum_nprobes(minimum_nprobes: int) -> Self

    

      
Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every indexed vector query and will
increase recall at the expense of latency.

            
              Source code in `lancedb/query.py`
              
2851
2852
2853
2854
2855
2856
2857
2858
2859
2860
def minimum_nprobes(self, minimum_nprobes: int) -> Self:
    """Set the minimum number of probes to use.

    See `nprobes` for more details.

    These partitions will be searched on every indexed vector query and will
    increase recall at the expense of latency.
    """
    self._inner.minimum_nprobes(minimum_nprobes)
    return self

            
    

            maximum_nprobes

¶

maximum_nprobes(maximum_nprobes: int) -> Self

    

      
Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

            
              Source code in `lancedb/query.py`
              
2862
2863
2864
2865
2866
2867
2868
2869
2870
2871
2872
2873
2874
2875
2876
2877
def maximum_nprobes(self, maximum_nprobes: int) -> Self:
    """Set the maximum number of probes to use.

    See `nprobes` for more details.

    If this value is greater than `minimum_nprobes` then the excess partitions
    will be searched only if we have not found enough results.

    This can be useful when there is a narrow filter to allow these queries to
    spend more time searching and avoid potential false negatives.

    If this value is 0 then no limit will be applied and all partitions could be
    searched if needed to satisfy the limit.
    """
    self._inner.maximum_nprobes(maximum_nprobes)
    return self

            
    

            distance_range

¶

distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> Self

    

      
Set the distance range to use.

Only rows with distances within range [lower_bound, upper_bound)
will be returned.

Parameters:

    
        
- 
          `lower_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The lower bound of the distance range.

          
        
        
- 
          `upper_bound`
              (`Optional[float]`, default:
                  `None`
)
          –
          
            
The upper bound of the distance range.

          
        
    

Returns:

    
        
- 
              `AsyncVectorQuery`
          –
          
            
The AsyncVectorQuery object.

          
        
    

            
              Source code in `lancedb/query.py`
              
2879
2880
2881
2882
2883
2884
2885
2886
2887
2888
2889
2890
2891
2892
2893
2894
2895
2896
2897
2898
2899
2900
def distance_range(
    self, lower_bound: Optional[float] = None, upper_bound: Optional[float] = None
) -> Self:
    """Set the distance range to use.

    Only rows with distances within range [lower_bound, upper_bound)
    will be returned.

    Parameters
    ----------
    lower_bound: Optional[float]
        The lower bound of the distance range.
    upper_bound: Optional[float]
        The upper bound of the distance range.

    Returns
    -------
    AsyncVectorQuery
        The AsyncVectorQuery object.
    """
    self._inner.distance_range(lower_bound, upper_bound)
    return self

            
    

            ef

¶

ef(ef: int) -> Self

    

      
Set the number of candidates to consider during search

This argument is only used when the vector column has an HNSW index.
If there is no index then this value is ignored.

Increasing this value will increase the recall of your query but will also
increase the latency of your query.  The default value is 1.5 * limit.  This
default is good for many cases but the best value to use will depend on your
data and the recall that you need to achieve.

            
              Source code in `lancedb/query.py`
              
2902
2903
2904
2905
2906
2907
2908
2909
2910
2911
2912
2913
2914
2915
def ef(self, ef: int) -> Self:
    """
    Set the number of candidates to consider during search

    This argument is only used when the vector column has an HNSW index.
    If there is no index then this value is ignored.

    Increasing this value will increase the recall of your query but will also
    increase the latency of your query.  The default value is 1.5 * limit.  This
    default is good for many cases but the best value to use will depend on your
    data and the recall that you need to achieve.
    """
    self._inner.ef(ef)
    return self

            
    

            refine_factor

¶

refine_factor(refine_factor: int) -> Self

    

      
A multiplier to control how many additional rows are taken during the refine
step

This argument is only used when the vector column has an IVF PQ index.
If there is no index then this value is ignored.

An IVF PQ index stores compressed (quantized) values.  They query vector is
compared against these values and, since they are compressed, the comparison is
inaccurate.

This parameter can be used to refine the results.  It can improve both improve
recall and correct the ordering of the nearest results.

To refine results LanceDb will first perform an ANN search to find the nearest
`limit` * `refine_factor` results.  In other words, if `refine_factor` is 3 and
`limit` is the default (10) then the first 30 results will be selected.  LanceDb
then fetches the full, uncompressed, values for these 30 results.  The results
are then reordered by the true distance and only the nearest 10 are kept.

Note: there is a difference between calling this method with a value of 1 and
never calling this method at all.  Calling this method with any value will have
an impact on your search latency.  When you call this method with a
`refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
values so that it can potentially reorder the results.

Note: if this method is NOT called then the distances returned in the _distance
column will be approximate distances based on the comparison of the quantized
query vector and the quantized result vectors.  This can be considerably
different than the true distance between the query vector and the actual
uncompressed vector.

            
              Source code in `lancedb/query.py`
              
2917
2918
2919
2920
2921
2922
2923
2924
2925
2926
2927
2928
2929
2930
2931
2932
2933
2934
2935
2936
2937
2938
2939
2940
2941
2942
2943
2944
2945
2946
2947
2948
2949
2950
2951
def refine_factor(self, refine_factor: int) -> Self:
    """
    A multiplier to control how many additional rows are taken during the refine
    step

    This argument is only used when the vector column has an IVF PQ index.
    If there is no index then this value is ignored.

    An IVF PQ index stores compressed (quantized) values.  They query vector is
    compared against these values and, since they are compressed, the comparison is
    inaccurate.

    This parameter can be used to refine the results.  It can improve both improve
    recall and correct the ordering of the nearest results.

    To refine results LanceDb will first perform an ANN search to find the nearest
    `limit` * `refine_factor` results.  In other words, if `refine_factor` is 3 and
    `limit` is the default (10) then the first 30 results will be selected.  LanceDb
    then fetches the full, uncompressed, values for these 30 results.  The results
    are then reordered by the true distance and only the nearest 10 are kept.

    Note: there is a difference between calling this method with a value of 1 and
    never calling this method at all.  Calling this method with any value will have
    an impact on your search latency.  When you call this method with a
    `refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
    values so that it can potentially reorder the results.

    Note: if this method is NOT called then the distances returned in the _distance
    column will be approximate distances based on the comparison of the quantized
    query vector and the quantized result vectors.  This can be considerably
    different than the true distance between the query vector and the actual
    uncompressed vector.
    """
    self._inner.refine_factor(refine_factor)
    return self

            
    

            distance_type

¶

distance_type(distance_type: str) -> Self

    

      
Set the distance metric to use

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric.  This parameter controls which distance metric
to use.  See @see {@link IvfPqOptions.distanceType} for more details on the
different distance metrics available.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index.  If this is not done then the
results will be invalid.

By default "l2" is used.

            
              Source code in `lancedb/query.py`
              
2953
2954
2955
2956
2957
2958
2959
2960
2961
2962
2963
2964
2965
2966
2967
2968
2969
def distance_type(self, distance_type: str) -> Self:
    """
    Set the distance metric to use

    When performing a vector search we try and find the "nearest" vectors according
    to some kind of distance metric.  This parameter controls which distance metric
    to use.  See @see {@link IvfPqOptions.distanceType} for more details on the
    different distance metrics available.

    Note: if there is a vector index then the distance type used MUST match the
    distance type used to train the vector index.  If this is not done then the
    results will be invalid.

    By default "l2" is used.
    """
    self._inner.distance_type(distance_type)
    return self

            
    

            bypass_vector_index

¶

bypass_vector_index() -> Self

    

      
If this is called then any vector index is skipped

An exhaustive (flat) search will be performed.  The query vector will
be compared to every vector in the table.  At high scales this can be
expensive.  However, this is often still useful.  For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

            
              Source code in `lancedb/query.py`
              
2971
2972
2973
2974
2975
2976
2977
2978
2979
2980
2981
2982
def bypass_vector_index(self) -> Self:
    """
    If this is called then any vector index is skipped

    An exhaustive (flat) search will be performed.  The query vector will
    be compared to every vector in the table.  At high scales this can be
    expensive.  However, this is often still useful.  For example, skipping
    the vector index can give you ground truth results which you can use to
    calculate your recall to select an appropriate value for nprobes.
    """
    self._inner.bypass_vector_index()
    return self

            
    

            to_query_object

¶

to_query_object() -> Query

    

      
Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

            
              Source code in `lancedb/query.py`
              
2213
2214
2215
2216
2217
2218
2219
2220
def to_query_object(self) -> Query:
    """
    Convert the query into a query object

    This is currently experimental but can be useful as the query object is pure
    python and more easily serializable.
    """
    return Query.from_inner(self._inner.to_query_request())

            
    

            select

¶

select(columns: Union[List[str], dict[str, str]]) -> Self

    

      
Return only the specified columns.

By default a query will return all columns from the table.  However, this can
have a very significant impact on latency.  LanceDb stores data in a columnar
fashion.  This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b".  This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str].  A column will be
returned for each entry in the map.  The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`.  The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

            
              Source code in `lancedb/query.py`
              
2222
2223
2224
2225
2226
2227
2228
2229
2230
2231
2232
2233
2234
2235
2236
2237
2238
2239
2240
2241
2242
2243
2244
2245
2246
2247
2248
2249
2250
2251
2252
2253
2254
2255
2256
2257
2258
def select(self, columns: Union[List[str], dict[str, str]]) -> Self:
    """
    Return only the specified columns.

    By default a query will return all columns from the table.  However, this can
    have a very significant impact on latency.  LanceDb stores data in a columnar
    fashion.  This
    means we can finely tune our I/O to select exactly the columns we need.

    As a best practice you should always limit queries to the columns that you need.
    If you pass in a list of column names then only those columns will be
    returned.

    You can also use this method to create new "dynamic" columns based on your
    existing columns. For example, you may not care about "a" or "b" but instead
    simply want "a + b".  This is often seen in the SELECT clause of an SQL query
    (e.g. `SELECT a+b FROM my_table`).

    To create dynamic columns you can pass in a dict[str, str].  A column will be
    returned for each entry in the map.  The key provides the name of the column.
    The value is an SQL string used to specify how the column is calculated.

    For example, an SQL query might state `SELECT a + b AS combined, c`.  The
    equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

    Columns will always be returned in the order given, even if that order is
    different than the order used when adding the data.
    """
    if isinstance(columns, list) and all(isinstance(c, str) for c in columns):
        self._inner.select_columns(columns)
    elif isinstance(columns, dict) and all(
        isinstance(k, str) and isinstance(v, str) for k, v in columns.items()
    ):
        self._inner.select(list(columns.items()))
    else:
        raise TypeError("columns must be a list of column names or a dict")
    return self

            
    

            with_row_id

¶

with_row_id() -> Self

    

      
Include the _rowid column in the results.

            
              Source code in `lancedb/query.py`
              
2260
2261
2262
2263
2264
2265
def with_row_id(self) -> Self:
    """
    Include the _rowid column in the results.
    """
    self._inner.with_row_id()
    return self

            
    

            output_schema

  
      `async`
  

¶

output_schema() -> Schema

    

      
Return the output schema for the query

This does not execute the query.

            
              Source code in `lancedb/query.py`
              
2295
2296
2297
2298
2299
2300
2301
async def output_schema(self) -> pa.Schema:
    """
    Return the output schema for the query

    This does not execute the query.
    """
    return await self._inner.output_schema()

            
    

            to_arrow

  
      `async`
  

¶

to_arrow(timeout: Optional[timedelta] = None) -> Table

    

      
Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning.  If
you expect a large number of results, you may want to use
to_batches

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2303
2304
2305
2306
2307
2308
2309
2310
2311
2312
2313
2314
2315
2316
2317
2318
2319
2320
2321
async def to_arrow(self, timeout: Optional[timedelta] = None) -> pa.Table:
    """
    Execute the query and collect the results into an Apache Arrow Table.

    This method will collect all results into memory before returning.  If
    you expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches]

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    batch_iter = await self.to_batches(timeout=timeout)
    return pa.Table.from_batches(
        await batch_iter.read_all(), schema=batch_iter.schema
    )

            
    

            to_list

  
      `async`
  

¶

to_list(timeout: Optional[timedelta] = None) -> List[dict]

    

      
Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2323
2324
2325
2326
2327
2328
2329
2330
2331
2332
2333
2334
2335
2336
2337
2338
async def to_list(self, timeout: Optional[timedelta] = None) -> List[dict]:
    """
    Execute the query and return the results as a list of dictionaries.

    Each list entry is a dictionary with the selected column names as keys,
    or all table columns if `select` is not called. The vector and the "_distance"
    fields are returned whether or not they're explicitly selected.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (await self.to_arrow(timeout=timeout)).to_pylist()

            
    

            to_pandas

  
      `async`
  

¶

to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'

    

      
Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
pandas separately.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())

Parameters:

    
        
- 
          `flatten`
              (`Optional[Union[int, bool]]`, default:
                  `None`
)
          –
          
            
If flatten is True, flatten all nested columns.
If flatten is an integer, flatten the nested columns up to the
specified depth.
If unspecified, do not flatten the nested columns.

          
        
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

            
              Source code in `lancedb/query.py`
              
2340
2341
2342
2343
2344
2345
2346
2347
2348
2349
2350
2351
2352
2353
2354
2355
2356
2357
2358
2359
2360
2361
2362
2363
2364
2365
2366
2367
2368
2369
2370
2371
2372
2373
2374
2375
2376
2377
2378
2379
async def to_pandas(
    self,
    flatten: Optional[Union[int, bool]] = None,
    timeout: Optional[timedelta] = None,
) -> "pd.DataFrame":
    """
    Execute the query and collect the results into a pandas DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    pandas separately.

    Examples
    --------

    >>> import asyncio
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = batch.to_pandas()
    >>> asyncio.run(doctest_example())

    Parameters
    ----------
    flatten: Optional[Union[int, bool]]
        If flatten is True, flatten all nested columns.
        If flatten is an integer, flatten the nested columns up to the
        specified depth.
        If unspecified, do not flatten the nested columns.
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.
    """
    return (
        flatten_columns(await self.to_arrow(timeout=timeout), flatten)
    ).to_pandas()

            
    

            to_polars

  
      `async`
  

¶

to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'

    

      
Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning.  If you
expect a large number of results, you may want to use
to_batches and convert each batch to
polars separately.

Parameters:

    
        
- 
          `timeout`
              (`Optional[timedelta]`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If not specified, no timeout is applied. If the query does not
complete within the specified time, an error will be raised.

          
        
    

Examples:

    
>>> import asyncio
>>> import polars as pl
>>> from lancedb import connect_async
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())

            
              Source code in `lancedb/query.py`
              
2381
2382
2383
2384
2385
2386
2387
2388
2389
2390
2391
2392
2393
2394
2395
2396
2397
2398
2399
2400
2401
2402
2403
2404
2405
2406
2407
2408
2409
2410
2411
2412
2413
2414
2415
async def to_polars(
    self,
    timeout: Optional[timedelta] = None,
) -> "pl.DataFrame":
    """
    Execute the query and collect the results into a Polars DataFrame.

    This method will collect all results into memory before returning.  If you
    expect a large number of results, you may want to use
    [to_batches][lancedb.query.AsyncQueryBase.to_batches] and convert each batch to
    polars separately.

    Parameters
    ----------
    timeout: Optional[timedelta]
        The maximum time to wait for the query to complete.
        If not specified, no timeout is applied. If the query does not
        complete within the specified time, an error will be raised.

    Examples
    --------

    >>> import asyncio
    >>> import polars as pl
    >>> from lancedb import connect_async
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
    ...     async for batch in await table.query().to_batches():
    ...         batch_df = pl.from_arrow(batch)
    >>> asyncio.run(doctest_example())
    """
    import polars as pl

    return pl.from_arrow(await self.to_arrow(timeout=timeout))

            
    

            to_pydantic

  
      `async`
  

¶

to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]

    

      
Convert results to a list of pydantic models.

Parameters:

    
        
- 
          `model`
              (`Type[LanceModel]`)
          –
          
            
The pydantic model to use.

          
        
        
- 
          `timeout`
              (`timedelta`, default:
                  `None`
)
          –
          
            
The maximum time to wait for the query to complete.
If None, wait indefinitely.

          
        
    

Returns:

    
        
- 
              `list[LanceModel]`
          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
2417
2418
2419
2420
2421
2422
2423
2424
2425
2426
2427
2428
2429
2430
2431
2432
2433
2434
2435
2436
2437
async def to_pydantic(
    self, model: Type[LanceModel], *, timeout: Optional[timedelta] = None
) -> List[LanceModel]:
    """
    Convert results to a list of pydantic models.

    Parameters
    ----------
    model : Type[LanceModel]
        The pydantic model to use.
    timeout : timedelta, optional
        The maximum time to wait for the query to complete.
        If None, wait indefinitely.

    Returns
    -------
    list[LanceModel]
    """
    return [
        model(**row) for row in (await self.to_arrow(timeout=timeout)).to_pylist()
    ]

            
    

            where

¶

where(predicate: str) -> Self

    

      
Only return rows matching the given predicate

The predicate should be supplied as an SQL query string.

Examples:

    
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"

    
Filtering performance can often be improved by creating a scalar index
on the filter column(s).

            
              Source code in `lancedb/query.py`
              
2495
2496
2497
2498
2499
2500
2501
2502
2503
2504
2505
2506
2507
2508
2509
2510
2511
2512
def where(self, predicate: str) -> Self:
    """
    Only return rows matching the given predicate

    The predicate should be supplied as an SQL query string.

    Examples
    --------

    >>> predicate = "x > 10"
    >>> predicate = "y > 0 AND y < 100"
    >>> predicate = "x > 5 OR y = 'test'"

    Filtering performance can often be improved by creating a scalar index
    on the filter column(s).
    """
    self._inner.where(predicate)
    return self

            
    

            limit

¶

limit(limit: int) -> Self

    

      
Set the maximum number of results to return.

By default, a plain search has no limit.  If this method is not
called then every valid row from the table will be returned.

            
              Source code in `lancedb/query.py`
              
2514
2515
2516
2517
2518
2519
2520
2521
2522
def limit(self, limit: int) -> Self:
    """
    Set the maximum number of results to return.

    By default, a plain search has no limit.  If this method is not
    called then every valid row from the table will be returned.
    """
    self._inner.limit(limit)
    return self

            
    

            offset

¶

offset(offset: int) -> Self

    

      
Set the offset for the results.

Parameters:

    
        
- 
          `offset`
              (`int`)
          –
          
            
The offset to start fetching results from.

          
        
    

            
              Source code in `lancedb/query.py`
              
2524
2525
2526
2527
2528
2529
2530
2531
2532
2533
2534
def offset(self, offset: int) -> Self:
    """
    Set the offset for the results.

    Parameters
    ----------
    offset: int
        The offset to start fetching results from.
    """
    self._inner.offset(offset)
    return self

            
    

            fast_search

¶

fast_search() -> Self

    

      
Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
AsyncTable.optimize.

            
              Source code in `lancedb/query.py`
              
2536
2537
2538
2539
2540
2541
2542
2543
2544
2545
2546
2547
2548
def fast_search(self) -> Self:
    """
    Skip searching un-indexed data.

    This can make queries faster, but will miss any data that has not been
    indexed.

    !!! tip
        You can add new data into an existing index by calling
        [AsyncTable.optimize][lancedb.table.AsyncTable.optimize].
    """
    self._inner.fast_search()
    return self

            
    

            postfilter

¶

postfilter() -> Self

    

      
If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search.  This is how
filtering is typically understood to work.  This prefilter step does add some
additional latency.  Creating a scalar index on the filter column(s) can
often improve this latency.  However, sometimes a filter is too complex or
scalar indices cannot be applied to the column.  In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search.  This
means we only run the filter on a much smaller set of data.  However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

            
              Source code in `lancedb/query.py`
              
2550
2551
2552
2553
2554
2555
2556
2557
2558
2559
2560
2561
2562
2563
2564
2565
2566
2567
2568
2569
def postfilter(self) -> Self:
    """
    If this is called then filtering will happen after the search instead of
    before.
    By default filtering will be performed before the search.  This is how
    filtering is typically understood to work.  This prefilter step does add some
    additional latency.  Creating a scalar index on the filter column(s) can
    often improve this latency.  However, sometimes a filter is too complex or
    scalar indices cannot be applied to the column.  In these cases postfiltering
    can be used instead of prefiltering to improve latency.
    Post filtering applies the filter to the results of the search.  This
    means we only run the filter on a much smaller set of data.  However, it can
    cause the query to return fewer than `limit` results (or even no results) if
    none of the nearest results match the filter.
    Post filtering happens during the "refine stage" (described in more detail in
    @see {@link VectorQuery#refineFactor}).  This means that setting a higher refine
    factor can often help restore some of the results lost by post filtering.
    """
    self._inner.postfilter()
    return self

            
    

            rerank

¶

rerank(reranker: Reranker = RRFReranker(), normalize: str = 'score') -> AsyncHybridQuery

    

      
Rerank the hybrid search results using the specified reranker. The reranker
must be an instance of Reranker class.

Parameters:

    
        
- 
          `reranker`
              (`Reranker`, default:
                  `RRFReranker()`
)
          –
          
            
The reranker to use. Must be an instance of Reranker class.

          
        
        
- 
          `normalize`
              (`str`, default:
                  `'score'`
)
          –
          
            
The method to normalize the scores. Can be "rank" or "score". If "rank",
the scores are converted to ranks and then normalized. If "score", the
scores are normalized directly.

          
        
    

Returns:

    
        
- 
              `AsyncHybridQuery`
          –
          
            
The AsyncHybridQuery object.

          
        
    

            
              Source code in `lancedb/query.py`
              
3086
3087
3088
3089
3090
3091
3092
3093
3094
3095
3096
3097
3098
3099
3100
3101
3102
3103
3104
3105
3106
3107
3108
3109
3110
3111
3112
3113
3114
def rerank(
    self, reranker: Reranker = RRFReranker(), normalize: str = "score"
) -> AsyncHybridQuery:
    """
    Rerank the hybrid search results using the specified reranker. The reranker
    must be an instance of Reranker class.

    Parameters
    ----------
    reranker: Reranker, default RRFReranker()
        The reranker to use. Must be an instance of Reranker class.
    normalize: str, default "score"
        The method to normalize the scores. Can be "rank" or "score". If "rank",
        the scores are converted to ranks and then normalized. If "score", the
        scores are normalized directly.
    Returns
    -------
    AsyncHybridQuery
        The AsyncHybridQuery object.
    """
    if normalize not in ["rank", "score"]:
        raise ValueError("normalize must be 'rank' or 'score'.")
    if reranker and not isinstance(reranker, Reranker):
        raise ValueError("reranker must be an instance of Reranker class.")

    self._norm = normalize
    self._reranker = reranker

    return self

            
    

            explain_plan

  
      `async`
  

¶

explain_plan(verbose: Optional[bool] = False)

    

      
Return the execution plan for this query.

The output includes both the vector and FTS search plans.

Examples:

    
>>> import asyncio
>>> from lancedb import connect_async
>>> from lancedb.index import FTS
>>> async def doctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0], "text": "hello world"}])
...     await table.create_index("text", config=FTS(with_position=False))
...     plan = await table.query().nearest_to([1.0, 2.0]).nearest_to_text("hello").explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
RRFReranker(K=60)
    ProjectionExec: expr=[vector@0 as vector, text@3 as text, _distance@2 as _distance]
      Take: columns="vector, _rowid, _distance, (text)"
        CoalesceBatchesExec: target_batch_size=1024
          GlobalLimitExec: skip=0, fetch=10
            FilterExec: _distance@2 IS NOT NULL
              SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                KNNVectorDistance: metric=l2
                  LanceRead: uri=..., projection=[vector], ...
    ProjectionExec: expr=[vector@2 as vector, text@3 as text, _score@1 as _score]
      Take: columns="_rowid, _score, (vector), (text)"
        CoalesceBatchesExec: target_batch_size=1024
          GlobalLimitExec: skip=0, fetch=10
            MatchQuery: column=text, query=hello

Parameters:

    
        
- 
          `verbose`
              (`bool`, default:
                  `False`
)
          –
          
            
Use a verbose output format.

          
        
    

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
3148
3149
3150
3151
3152
3153
3154
3155
3156
3157
3158
3159
3160
3161
3162
3163
3164
3165
3166
3167
3168
3169
3170
3171
3172
3173
3174
3175
3176
3177
3178
3179
3180
3181
3182
3183
3184
3185
3186
3187
3188
3189
3190
3191
3192
3193
3194
3195
async def explain_plan(self, verbose: Optional[bool] = False):
    """Return the execution plan for this query.

    The output includes both the vector and FTS search plans.

    Examples
    --------
    >>> import asyncio
    >>> from lancedb import connect_async
    >>> from lancedb.index import FTS
    >>> async def doctest_example():
    ...     conn = await connect_async("./.lancedb")
    ...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0], "text": "hello world"}])
    ...     await table.create_index("text", config=FTS(with_position=False))
    ...     plan = await table.query().nearest_to([1.0, 2.0]).nearest_to_text("hello").explain_plan(True)
    ...     print(plan)
    >>> asyncio.run(doctest_example()) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    RRFReranker(K=60)
        ProjectionExec: expr=[vector@0 as vector, text@3 as text, _distance@2 as _distance]
          Take: columns="vector, _rowid, _distance, (text)"
            CoalesceBatchesExec: target_batch_size=1024
              GlobalLimitExec: skip=0, fetch=10
                FilterExec: _distance@2 IS NOT NULL
                  SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                    KNNVectorDistance: metric=l2
                      LanceRead: uri=..., projection=[vector], ...
        ProjectionExec: expr=[vector@2 as vector, text@3 as text, _score@1 as _score]
          Take: columns="_rowid, _score, (vector), (text)"
            CoalesceBatchesExec: target_batch_size=1024
              GlobalLimitExec: skip=0, fetch=10
                MatchQuery: column=text, query=hello

    Parameters
    ----------
    verbose : bool, default False
        Use a verbose output format.

    Returns
    -------
    plan : str
    """  # noqa: E501

    vector_plan = await self._inner.to_vector_query().explain_plan(verbose)
    fts_plan = await self._inner.to_fts_query().explain_plan(verbose)
    # Indent sub-plans under the reranker
    indented_vector = "\n".join("  " + line for line in vector_plan.splitlines())
    indented_fts = "\n".join("  " + line for line in fts_plan.splitlines())
    return f"{self._reranker}\n  {indented_vector}\n  {indented_fts}"

            
    

            analyze_plan

  
      `async`
  

¶

analyze_plan()

    

      
Execute the query and return the physical execution plan with runtime metrics.

This runs both the vector and FTS (full-text search) queries and returns
detailed metrics for each step of execution—such as rows processed,
elapsed time, I/O stats, and more. It’s useful for debugging and
performance analysis.

Returns:

    
        
- 
`plan` (              `str`
)          –
          
            
          
        
    

            
              Source code in `lancedb/query.py`
              
3197
3198
3199
3200
3201
3202
3203
3204
3205
3206
3207
3208
3209
3210
3211
3212
3213
3214
3215
async def analyze_plan(self):
    """
    Execute the query and return the physical execution plan with runtime metrics.

    This runs both the vector and FTS (full-text search) queries and returns
    detailed metrics for each step of execution—such as rows processed,
    elapsed time, I/O stats, and more. It’s useful for debugging and
    performance analysis.

    Returns
    -------
    plan : str
    """
    results = ["Vector Search Query:"]
    results.append(await self._inner.to_vector_query().analyze_plan())
    results.append("FTS Search Query:")
    results.append(await self._inner.to_fts_query().analyze_plan())

    return "\n".join(results)

            
    

  

    

  

                
              
            
          
          
  

        
        
          
  
  

  Back to top

        
      
      
        
  
    
      
      
    
  
  
    
      
  
  
    Made with
    
      Material for MkDocs
