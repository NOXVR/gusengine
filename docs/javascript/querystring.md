# Source: https://nodejs.org/api/querystring.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Query string | Node.js v25.6.1 Documentation
  
- 
  
- 
  
- 
  
- 
  
  
  

  [Skip to content](#apicontent)
  
    
      
        
          Node.js
        
      
      

- [About this documentation](documentation.html)

- [Usage and example](synopsis.html)

- [Assertion testing](assert.html)

- [Asynchronous context tracking](async_context.html)

- [Async hooks](async_hooks.html)

- [Buffer](buffer.html)

- [C++ addons](addons.html)

- [C/C++ addons with Node-API](n-api.html)

- [C++ embedder API](embedding.html)

- [Child processes](child_process.html)

- [Cluster](cluster.html)

- [Command-line options](cli.html)

- [Console](console.html)

- [Crypto](crypto.html)

- [Debugger](debugger.html)

- [Deprecated APIs](deprecations.html)

- [Diagnostics Channel](diagnostics_channel.html)

- [DNS](dns.html)

- [Domain](domain.html)

- [Environment Variables](environment_variables.html)

- [Errors](errors.html)

- [Events](events.html)

- [File system](fs.html)

- [Globals](globals.html)

- [HTTP](http.html)

- [HTTP/2](http2.html)

- [HTTPS](https.html)

- [Inspector](inspector.html)

- [Internationalization](intl.html)

- [Modules: CommonJS modules](modules.html)

- [Modules: ECMAScript modules](esm.html)

- [Modules: `node:module` API](module.html)

- [Modules: Packages](packages.html)

- [Modules: TypeScript](typescript.html)

- [Net](net.html)

- [OS](os.html)

- [Path](path.html)

- [Performance hooks](perf_hooks.html)

- [Permissions](permissions.html)

- [Process](process.html)

- [Punycode](punycode.html)

- [Query strings](querystring.html)

- [Readline](readline.html)

- [REPL](repl.html)

- [Report](report.html)

- [Single executable applications](single-executable-applications.html)

- [SQLite](sqlite.html)

- [Stream](stream.html)

- [String decoder](string_decoder.html)

- [Test runner](test.html)

- [Timers](timers.html)

- [TLS/SSL](tls.html)

- [Trace events](tracing.html)

- [TTY](tty.html)

- [UDP/datagram](dgram.html)

- [URL](url.html)

- [Utilities](util.html)

- [V8](v8.html)

- [VM](vm.html)

- [WASI](wasi.html)

- [Web Crypto API](webcrypto.html)

- [Web Streams API](webstreams.html)

- [Worker threads](worker_threads.html)

- [Zlib](zlib.html)

- [Code repository and issue tracker](https://github.com/nodejs/node)

    

    
      
        
          
# Node.js v25.6.1 documentation

          
            
              

              

              

            
            
              

              

            
          
        
        
          
            
- Node.js v25.6.1
            
    
- 
      
        
        Table of contents
      

      

- [Query string](#query-string)

- [`querystring.decode()`](#querystringdecode)

- [`querystring.encode()`](#querystringencode)

- [`querystring.escape(str)`](#querystringescapestr)

- [`querystring.parse(str[, sep[, eq[, options]]])`](#querystringparsestr-sep-eq-options)

- [`querystring.stringify(obj[, sep[, eq[, options]]])`](#querystringstringifyobj-sep-eq-options)

- [`querystring.unescape(str)`](#querystringunescapestr)

    
  
            
    
- 
      
        
        Index
      

      

- [About this documentation](documentation.html)

- [Usage and example](synopsis.html)

      
- 
        [Index](index.html)
      
    
  

- [Assertion testing](assert.html)

- [Asynchronous context tracking](async_context.html)

- [Async hooks](async_hooks.html)

- [Buffer](buffer.html)

- [C++ addons](addons.html)

- [C/C++ addons with Node-API](n-api.html)

- [C++ embedder API](embedding.html)

- [Child processes](child_process.html)

- [Cluster](cluster.html)

- [Command-line options](cli.html)

- [Console](console.html)

- [Crypto](crypto.html)

- [Debugger](debugger.html)

- [Deprecated APIs](deprecations.html)

- [Diagnostics Channel](diagnostics_channel.html)

- [DNS](dns.html)

- [Domain](domain.html)

- [Environment Variables](environment_variables.html)

- [Errors](errors.html)

- [Events](events.html)

- [File system](fs.html)

- [Globals](globals.html)

- [HTTP](http.html)

- [HTTP/2](http2.html)

- [HTTPS](https.html)

- [Inspector](inspector.html)

- [Internationalization](intl.html)

- [Modules: CommonJS modules](modules.html)

- [Modules: ECMAScript modules](esm.html)

- [Modules: `node:module` API](module.html)

- [Modules: Packages](packages.html)

- [Modules: TypeScript](typescript.html)

- [Net](net.html)

- [OS](os.html)

- [Path](path.html)

- [Performance hooks](perf_hooks.html)

- [Permissions](permissions.html)

- [Process](process.html)

- [Punycode](punycode.html)

- [Query strings](querystring.html)

- [Readline](readline.html)

- [REPL](repl.html)

- [Report](report.html)

- [Single executable applications](single-executable-applications.html)

- [SQLite](sqlite.html)

- [Stream](stream.html)

- [String decoder](string_decoder.html)

- [Test runner](test.html)

- [Timers](timers.html)

- [TLS/SSL](tls.html)

- [Trace events](tracing.html)

- [TTY](tty.html)

- [UDP/datagram](dgram.html)

- [URL](url.html)

- [Utilities](util.html)

- [V8](v8.html)

- [VM](vm.html)

- [WASI](wasi.html)

- [Web Crypto API](webcrypto.html)

- [Web Streams API](webstreams.html)

- [Worker threads](worker_threads.html)

- [Zlib](zlib.html)

- [Code repository and issue tracker](https://github.com/nodejs/node)

    
  
            
    
- 
      
        
        Other versions
      
      
- [25.x](https://nodejs.org/docs/latest-v25.x/api/querystring.html)

- [24.x LTS](https://nodejs.org/docs/latest-v24.x/api/querystring.html)

- [23.x](https://nodejs.org/docs/latest-v23.x/api/querystring.html)

- [22.x LTS](https://nodejs.org/docs/latest-v22.x/api/querystring.html)

- [21.x](https://nodejs.org/docs/latest-v21.x/api/querystring.html)

- [20.x LTS](https://nodejs.org/docs/latest-v20.x/api/querystring.html)

- [19.x](https://nodejs.org/docs/latest-v19.x/api/querystring.html)

- [18.x](https://nodejs.org/docs/latest-v18.x/api/querystring.html)

- [17.x](https://nodejs.org/docs/latest-v17.x/api/querystring.html)

- [16.x](https://nodejs.org/docs/latest-v16.x/api/querystring.html)

- [15.x](https://nodejs.org/docs/latest-v15.x/api/querystring.html)

- [14.x](https://nodejs.org/docs/latest-v14.x/api/querystring.html)

- [13.x](https://nodejs.org/docs/latest-v13.x/api/querystring.html)

- [12.x](https://nodejs.org/docs/latest-v12.x/api/querystring.html)

- [11.x](https://nodejs.org/docs/latest-v11.x/api/querystring.html)

- [10.x](https://nodejs.org/docs/latest-v10.x/api/querystring.html)

- [9.x](https://nodejs.org/docs/latest-v9.x/api/querystring.html)

- [8.x](https://nodejs.org/docs/latest-v8.x/api/querystring.html)

- [7.x](https://nodejs.org/docs/latest-v7.x/api/querystring.html)

- [6.x](https://nodejs.org/docs/latest-v6.x/api/querystring.html)

- [5.x](https://nodejs.org/docs/latest-v5.x/api/querystring.html)

- [4.x](https://nodejs.org/docs/latest-v4.x/api/querystring.html)

- [0.12.x](https://nodejs.org/docs/latest-v0.12.x/api/querystring.html)

- [0.10.x](https://nodejs.org/docs/latest-v0.10.x/api/querystring.html)
    
  
            
- 
              
                
                Options
              
        
              
                
                  
- 
                    [View on single page](all.html)
                  
                  
- 
                    [View as JSON](querystring.json)
                  
                  
- [Edit on GitHub](https://github.com/nodejs/node/edit/main/doc/api/querystring.md)    
                
              
            
          
        
        
      

      Table of contents

- [Query string](#query-string)

- [`querystring.decode()`](#querystringdecode)

- [`querystring.encode()`](#querystringencode)

- [`querystring.escape(str)`](#querystringescapestr)

- [`querystring.parse(str[, sep[, eq[, options]]])`](#querystringparsestr-sep-eq-options)

- [`querystring.stringify(obj[, sep[, eq[, options]]])`](#querystringstringifyobj-sep-eq-options)

- [`querystring.unescape(str)`](#querystringunescapestr)

      
        
## Query string[#](#query-string)

[Stability: 2](documentation.html#stability-index) - Stable

**Source Code:** [lib/querystring.js](https://github.com/nodejs/node/blob/v25.6.1/lib/querystring.js)

The `node:querystring` module provides utilities for parsing and formatting URL
query strings. It can be accessed using:

```
`const querystring = require('node:querystring');` copy
```

`querystring` is more performant than [<URLSearchParams>](url.html#class-urlsearchparams) but is not a
standardized API. Use [<URLSearchParams>](url.html#class-urlsearchparams) when performance is not critical or
when compatibility with browser code is desirable.

### `querystring.decode()`[#](#querystringdecode)

Added in: v0.1.99

The `querystring.decode()` function is an alias for `querystring.parse()`.

### `querystring.encode()`[#](#querystringencode)

Added in: v0.1.99

The `querystring.encode()` function is an alias for `querystring.stringify()`.

### `querystring.escape(str)`[#](#querystringescapestr)

Added in: v0.1.25

- `str` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

The `querystring.escape()` method performs URL percent-encoding on the given
`str` in a manner that is optimized for the specific requirements of URL
query strings.

The `querystring.escape()` method is used by `querystring.stringify()` and is
generally not expected to be used directly. It is exported primarily to allow
application code to provide a replacement percent-encoding implementation if
necessary by assigning `querystring.escape` to an alternative function.

### `querystring.parse(str[, sep[, eq[, options]]])`[#](#querystringparsestr-sep-eq-options)

History

VersionChanges
v8.0.0

Multiple empty entries are now parsed correctly (e.g. `&=&=`).

v6.0.0

The returned object no longer inherits from `Object.prototype`.

v6.0.0, v4.2.4

The `eq` parameter may now have a length of more than `1`.

v0.1.25

Added in: v0.1.25

- `str` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) The URL query string to parse

- `sep` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) The substring used to delimit key and value pairs in the
query string. **Default:** `'&'`.

- `eq` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type). The substring used to delimit keys and values in the
query string. **Default:** `'='`.

- `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

- `decodeURIComponent` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) The function to use when decoding
percent-encoded characters in the query string. **Default:**
`querystring.unescape()`.

- `maxKeys` [<number>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type) Specifies the maximum number of keys to parse.
Specify `0` to remove key counting limitations. **Default:** `1000`.

The `querystring.parse()` method parses a URL query string (`str`) into a
collection of key and value pairs.

For example, the query string `'foo=bar&abc=xyz&abc=123'` is parsed into:

{
  "foo": "bar",
  "abc": ["xyz", "123"]
} copy

The object returned by the `querystring.parse()` method *does not*
prototypically inherit from the JavaScript `Object`. This means that typical
`Object` methods such as `obj.toString()`, `obj.hasOwnProperty()`, and others
are not defined and *will not work*.

By default, percent-encoded characters within the query string will be assumed
to use UTF-8 encoding. If an alternative character encoding is used, then an
alternative `decodeURIComponent` option will need to be specified:

// Assuming gbkDecodeURIComponent function already exists...

querystring.parse('w=%D6%D0%CE%C4&foo=bar', null, null,
                  { decodeURIComponent: gbkDecodeURIComponent }); copy

### `querystring.stringify(obj[, sep[, eq[, options]]])`[#](#querystringstringifyobj-sep-eq-options)

Added in: v0.1.25

- `obj` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) The object to serialize into a URL query string

- `sep` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) The substring used to delimit key and value pairs in the
query string. **Default:** `'&'`.

- `eq` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type). The substring used to delimit keys and values in the
query string. **Default:** `'='`.

- `options`

- `encodeURIComponent` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) The function to use when converting
URL-unsafe characters to percent-encoding in the query string. **Default:**
`querystring.escape()`.

The `querystring.stringify()` method produces a URL query string from a
given `obj` by iterating through the object's "own properties".

It serializes the following types of values passed in `obj`:
[<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<number>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type) | [<bigint>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#bigint_type) | [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type) | [<string[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<number[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type) | [<bigint[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#bigint_type) | [<boolean[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type)
The numeric values must be finite. Any other input values will be coerced to
empty strings.

querystring.stringify({ foo: 'bar', baz: ['qux', 'quux'], corge: '' });
// Returns 'foo=bar&baz=qux&baz=quux&corge='

querystring.stringify({ foo: 'bar', baz: 'qux' }, ';', ':');
// Returns 'foo:bar;baz:qux' copy

By default, characters requiring percent-encoding within the query string will
be encoded as UTF-8. If an alternative encoding is required, then an alternative
`encodeURIComponent` option will need to be specified:

// Assuming gbkEncodeURIComponent function already exists,

querystring.stringify({ w: '中文', foo: 'bar' }, null, null,
                      { encodeURIComponent: gbkEncodeURIComponent }); copy

### `querystring.unescape(str)`[#](#querystringunescapestr)

Added in: v0.1.25

- `str` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

The `querystring.unescape()` method performs decoding of URL percent-encoded
characters on the given `str`.

The `querystring.unescape()` method is used by `querystring.parse()` and is
generally not expected to be used directly. It is exported primarily to allow
application code to provide a replacement decoding implementation if
necessary by assigning `querystring.unescape` to an alternative function.

By default, the `querystring.unescape()` method will attempt to use the
JavaScript built-in `decodeURIComponent()` method to decode. If that fails,
a safer equivalent that does not throw on malformed URLs will be used.
