# Source: https://nodejs.org/api/string_decoder.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

String decoder | Node.js v25.6.1 Documentation
  
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
      

      

- [String decoder](#string-decoder)

- [Class: `StringDecoder`](#class-stringdecoder)

- [`new StringDecoder([encoding])`](#new-stringdecoderencoding)

- [`stringDecoder.end([buffer])`](#stringdecoderendbuffer)

- [`stringDecoder.write(buffer)`](#stringdecoderwritebuffer)

    
  
            
    
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
      
      
- [25.x](https://nodejs.org/docs/latest-v25.x/api/string_decoder.html)

- [24.x LTS](https://nodejs.org/docs/latest-v24.x/api/string_decoder.html)

- [23.x](https://nodejs.org/docs/latest-v23.x/api/string_decoder.html)

- [22.x LTS](https://nodejs.org/docs/latest-v22.x/api/string_decoder.html)

- [21.x](https://nodejs.org/docs/latest-v21.x/api/string_decoder.html)

- [20.x LTS](https://nodejs.org/docs/latest-v20.x/api/string_decoder.html)

- [19.x](https://nodejs.org/docs/latest-v19.x/api/string_decoder.html)

- [18.x](https://nodejs.org/docs/latest-v18.x/api/string_decoder.html)

- [17.x](https://nodejs.org/docs/latest-v17.x/api/string_decoder.html)

- [16.x](https://nodejs.org/docs/latest-v16.x/api/string_decoder.html)

- [15.x](https://nodejs.org/docs/latest-v15.x/api/string_decoder.html)

- [14.x](https://nodejs.org/docs/latest-v14.x/api/string_decoder.html)

- [13.x](https://nodejs.org/docs/latest-v13.x/api/string_decoder.html)

- [12.x](https://nodejs.org/docs/latest-v12.x/api/string_decoder.html)

- [11.x](https://nodejs.org/docs/latest-v11.x/api/string_decoder.html)

- [10.x](https://nodejs.org/docs/latest-v10.x/api/string_decoder.html)

- [9.x](https://nodejs.org/docs/latest-v9.x/api/string_decoder.html)

- [8.x](https://nodejs.org/docs/latest-v8.x/api/string_decoder.html)

- [7.x](https://nodejs.org/docs/latest-v7.x/api/string_decoder.html)

- [6.x](https://nodejs.org/docs/latest-v6.x/api/string_decoder.html)

- [5.x](https://nodejs.org/docs/latest-v5.x/api/string_decoder.html)

- [4.x](https://nodejs.org/docs/latest-v4.x/api/string_decoder.html)

- [0.12.x](https://nodejs.org/docs/latest-v0.12.x/api/string_decoder.html)

- [0.10.x](https://nodejs.org/docs/latest-v0.10.x/api/string_decoder.html)
    
  
            
- 
              
                
                Options
              
        
              
                
                  
- 
                    [View on single page](all.html)
                  
                  
- 
                    [View as JSON](string_decoder.json)
                  
                  
- [Edit on GitHub](https://github.com/nodejs/node/edit/main/doc/api/string_decoder.md)    
                
              
            
          
        
        
      

      Table of contents

- [String decoder](#string-decoder)

- [Class: `StringDecoder`](#class-stringdecoder)

- [`new StringDecoder([encoding])`](#new-stringdecoderencoding)

- [`stringDecoder.end([buffer])`](#stringdecoderendbuffer)

- [`stringDecoder.write(buffer)`](#stringdecoderwritebuffer)

      
        
## String decoder[#](#string-decoder)

[Stability: 2](documentation.html#stability-index) - Stable

**Source Code:** [lib/string_decoder.js](https://github.com/nodejs/node/blob/v25.6.1/lib/string_decoder.js)

The `node:string_decoder` module provides an API for decoding `Buffer` objects
into strings in a manner that preserves encoded multi-byte UTF-8 and UTF-16
characters. It can be accessed using:

```
`import { StringDecoder } from 'node:string_decoder';``const { StringDecoder } = require('node:string_decoder');`copy
```

The following example shows the basic use of the `StringDecoder` class.

import { StringDecoder } from 'node:string_decoder';
import { Buffer } from 'node:buffer';
const decoder = new StringDecoder('utf8');

const cent = Buffer.from([0xC2, 0xA2]);
console.log(decoder.write(cent)); // Prints: ¢

const euro = Buffer.from([0xE2, 0x82, 0xAC]);
console.log(decoder.write(euro)); // Prints: €const { StringDecoder } = require('node:string_decoder');
const decoder = new StringDecoder('utf8');

const cent = Buffer.from([0xC2, 0xA2]);
console.log(decoder.write(cent)); // Prints: ¢

const euro = Buffer.from([0xE2, 0x82, 0xAC]);
console.log(decoder.write(euro)); // Prints: €copy

When a `Buffer` instance is written to the `StringDecoder` instance, an
internal buffer is used to ensure that the decoded string does not contain
any incomplete multibyte characters. These are held in the buffer until the
next call to `stringDecoder.write()` or until `stringDecoder.end()` is called.

In the following example, the three UTF-8 encoded bytes of the European Euro
symbol (`€`) are written over three separate operations:

import { StringDecoder } from 'node:string_decoder';
import { Buffer } from 'node:buffer';
const decoder = new StringDecoder('utf8');

decoder.write(Buffer.from([0xE2]));
decoder.write(Buffer.from([0x82]));
console.log(decoder.end(Buffer.from([0xAC]))); // Prints: €const { StringDecoder } = require('node:string_decoder');
const decoder = new StringDecoder('utf8');

decoder.write(Buffer.from([0xE2]));
decoder.write(Buffer.from([0x82]));
console.log(decoder.end(Buffer.from([0xAC]))); // Prints: €copy

### Class: `StringDecoder`[#](#class-stringdecoder)

#### `new StringDecoder([encoding])`[#](#new-stringdecoderencoding)

Added in: v0.1.99

- `encoding` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) The character [encoding](buffer.html#buffers-and-character-encodings) the `StringDecoder` will use.
**Default:** `'utf8'`.

Creates a new `StringDecoder` instance.

#### `stringDecoder.end([buffer])`[#](#stringdecoderendbuffer)

Added in: v0.9.3

- `buffer` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) The bytes to decode.

- Returns: [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

Returns any remaining input stored in the internal buffer as a string. Bytes
representing incomplete UTF-8 and UTF-16 characters will be replaced with
substitution characters appropriate for the character encoding.

If the `buffer` argument is provided, one final call to `stringDecoder.write()`
is performed before returning the remaining input.
After `end()` is called, the `stringDecoder` object can be reused for new input.

#### `stringDecoder.write(buffer)`[#](#stringdecoderwritebuffer)

History

VersionChanges
v8.0.0

Each invalid character is now replaced by a single replacement character instead of one for each individual byte.

v0.1.99

Added in: v0.1.99

- `buffer` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) The bytes to decode.

- Returns: [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

Returns a decoded string, ensuring that any incomplete multibyte characters at
the end of the `Buffer`, or `TypedArray`, or `DataView` are omitted from the
returned string and stored in an internal buffer for the next call to
`stringDecoder.write()` or `stringDecoder.end()`.
