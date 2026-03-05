# Source: https://nodejs.org/api/globals.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Global objects | Node.js v25.6.1 Documentation
  
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
      

      

- [Global objects](#global-objects)

- [Class: `AbortController`](#class-abortcontroller)

- [`abortController.abort([reason])`](#abortcontrollerabortreason)

- [`abortController.signal`](#abortcontrollersignal)

- [Class: `AbortSignal`](#class-abortsignal)

- [Static method: `AbortSignal.abort([reason])`](#static-method-abortsignalabortreason)

- [Static method: `AbortSignal.timeout(delay)`](#static-method-abortsignaltimeoutdelay)

- [Static method: `AbortSignal.any(signals)`](#static-method-abortsignalanysignals)

- [Event: `'abort'`](#event-abort)

- [`abortSignal.aborted`](#abortsignalaborted)

- [`abortSignal.onabort`](#abortsignalonabort)

- [`abortSignal.reason`](#abortsignalreason)

- [`abortSignal.throwIfAborted()`](#abortsignalthrowifaborted)

- [Class: `Blob`](#class-blob)

- [Class: `Buffer`](#class-buffer)

- [Class: `ByteLengthQueuingStrategy`](#class-bytelengthqueuingstrategy)

- [`__dirname`](#__dirname)

- [`__filename`](#__filename)

- [`atob(data)`](#atobdata)

- [Class: `BroadcastChannel`](#class-broadcastchannel)

- [`btoa(data)`](#btoadata)

- [`clearImmediate(immediateObject)`](#clearimmediateimmediateobject)

- [`clearInterval(intervalObject)`](#clearintervalintervalobject)

- [`clearTimeout(timeoutObject)`](#cleartimeouttimeoutobject)

- [Class: `CloseEvent`](#class-closeevent)

- [Class: `CompressionStream`](#class-compressionstream)

- [`console`](#console)

- [Class: `CountQueuingStrategy`](#class-countqueuingstrategy)

- [Class: `Crypto`](#class-crypto)

- [`crypto`](#crypto)

- [Class: `CryptoKey`](#class-cryptokey)

- [Class: `CustomEvent`](#class-customevent)

- [Class: `DecompressionStream`](#class-decompressionstream)

- [`ErrorEvent`](#errorevent)

- [Class: `Event`](#class-event)

- [Class: `EventSource`](#class-eventsource)

- [Class: `EventTarget`](#class-eventtarget)

- [`exports`](#exports)

- [`fetch`](#fetch)

- [Custom dispatcher](#custom-dispatcher)

- [Related classes](#related-classes)

- [Class: `File`](#class-file)

- [Class: `FormData`](#class-formdata)

- [`global`](#global)

- [Class: `Headers`](#class-headers)

- [`localStorage`](#localstorage)

- [Class: `MessageChannel`](#class-messagechannel)

- [Class: `MessageEvent`](#class-messageevent)

- [Class: `MessagePort`](#class-messageport)

- [`module`](#module)

- [Class: `Navigator`](#class-navigator)

- [`navigator`](#navigator)

- [`navigator.hardwareConcurrency`](#navigatorhardwareconcurrency)

- [`navigator.language`](#navigatorlanguage)

- [`navigator.languages`](#navigatorlanguages)

- [`navigator.platform`](#navigatorplatform)

- [`navigator.userAgent`](#navigatoruseragent)

- [`navigator.locks`](#navigatorlocks)

- [Class: `PerformanceEntry`](#class-performanceentry)

- [Class: `PerformanceMark`](#class-performancemark)

- [Class: `PerformanceMeasure`](#class-performancemeasure)

- [Class: `PerformanceObserver`](#class-performanceobserver)

- [Class: `PerformanceObserverEntryList`](#class-performanceobserverentrylist)

- [Class: `PerformanceResourceTiming`](#class-performanceresourcetiming)

- [`performance`](#performance)

- [`process`](#process)

- [`queueMicrotask(callback)`](#queuemicrotaskcallback)

- [Class: `ReadableByteStreamController`](#class-readablebytestreamcontroller)

- [Class: `ReadableStream`](#class-readablestream)

- [Class: `ReadableStreamBYOBReader`](#class-readablestreambyobreader)

- [Class: `ReadableStreamBYOBRequest`](#class-readablestreambyobrequest)

- [Class: `ReadableStreamDefaultController`](#class-readablestreamdefaultcontroller)

- [Class: `ReadableStreamDefaultReader`](#class-readablestreamdefaultreader)

- [`require()`](#require)

- [Class: `Response`](#class-response)

- [Class: `Request`](#class-request)

- [`sessionStorage`](#sessionstorage)

- [`setImmediate(callback[, ...args])`](#setimmediatecallback-args)

- [`setInterval(callback, delay[, ...args])`](#setintervalcallback-delay-args)

- [`setTimeout(callback, delay[, ...args])`](#settimeoutcallback-delay-args)

- [Class: `Storage`](#class-storage)

- [`structuredClone(value[, options])`](#structuredclonevalue-options)

- [Class: `SubtleCrypto`](#class-subtlecrypto)

- [Class: `DOMException`](#class-domexception)

- [Class: `TextDecoder`](#class-textdecoder)

- [Class: `TextDecoderStream`](#class-textdecoderstream)

- [Class: `TextEncoder`](#class-textencoder)

- [Class: `TextEncoderStream`](#class-textencoderstream)

- [Class: `TransformStream`](#class-transformstream)

- [Class: `TransformStreamDefaultController`](#class-transformstreamdefaultcontroller)

- [Class: `URL`](#class-url)

- [Class: `URLPattern`](#class-urlpattern)

- [Class: `URLSearchParams`](#class-urlsearchparams)

- [Class: `WebAssembly`](#class-webassembly)

- [Class: `WebSocket`](#class-websocket)

- [Class: `WritableStream`](#class-writablestream)

- [Class: `WritableStreamDefaultController`](#class-writablestreamdefaultcontroller)

- [Class: `WritableStreamDefaultWriter`](#class-writablestreamdefaultwriter)

    
  
            
    
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
      
      
- [25.x](https://nodejs.org/docs/latest-v25.x/api/globals.html)

- [24.x LTS](https://nodejs.org/docs/latest-v24.x/api/globals.html)

- [23.x](https://nodejs.org/docs/latest-v23.x/api/globals.html)

- [22.x LTS](https://nodejs.org/docs/latest-v22.x/api/globals.html)

- [21.x](https://nodejs.org/docs/latest-v21.x/api/globals.html)

- [20.x LTS](https://nodejs.org/docs/latest-v20.x/api/globals.html)

- [19.x](https://nodejs.org/docs/latest-v19.x/api/globals.html)

- [18.x](https://nodejs.org/docs/latest-v18.x/api/globals.html)

- [17.x](https://nodejs.org/docs/latest-v17.x/api/globals.html)

- [16.x](https://nodejs.org/docs/latest-v16.x/api/globals.html)

- [15.x](https://nodejs.org/docs/latest-v15.x/api/globals.html)

- [14.x](https://nodejs.org/docs/latest-v14.x/api/globals.html)

- [13.x](https://nodejs.org/docs/latest-v13.x/api/globals.html)

- [12.x](https://nodejs.org/docs/latest-v12.x/api/globals.html)

- [11.x](https://nodejs.org/docs/latest-v11.x/api/globals.html)

- [10.x](https://nodejs.org/docs/latest-v10.x/api/globals.html)

- [9.x](https://nodejs.org/docs/latest-v9.x/api/globals.html)

- [8.x](https://nodejs.org/docs/latest-v8.x/api/globals.html)

- [7.x](https://nodejs.org/docs/latest-v7.x/api/globals.html)

- [6.x](https://nodejs.org/docs/latest-v6.x/api/globals.html)

- [5.x](https://nodejs.org/docs/latest-v5.x/api/globals.html)

- [4.x](https://nodejs.org/docs/latest-v4.x/api/globals.html)

- [0.12.x](https://nodejs.org/docs/latest-v0.12.x/api/globals.html)

- [0.10.x](https://nodejs.org/docs/latest-v0.10.x/api/globals.html)
    
  
            
- 
              
                
                Options
              
        
              
                
                  
- 
                    [View on single page](all.html)
                  
                  
- 
                    [View as JSON](globals.json)
                  
                  
- [Edit on GitHub](https://github.com/nodejs/node/edit/main/doc/api/globals.md)    
                
              
            
          
        
        
      

      Table of contents

- [Global objects](#global-objects)

- [Class: `AbortController`](#class-abortcontroller)

- [`abortController.abort([reason])`](#abortcontrollerabortreason)

- [`abortController.signal`](#abortcontrollersignal)

- [Class: `AbortSignal`](#class-abortsignal)

- [Static method: `AbortSignal.abort([reason])`](#static-method-abortsignalabortreason)

- [Static method: `AbortSignal.timeout(delay)`](#static-method-abortsignaltimeoutdelay)

- [Static method: `AbortSignal.any(signals)`](#static-method-abortsignalanysignals)

- [Event: `'abort'`](#event-abort)

- [`abortSignal.aborted`](#abortsignalaborted)

- [`abortSignal.onabort`](#abortsignalonabort)

- [`abortSignal.reason`](#abortsignalreason)

- [`abortSignal.throwIfAborted()`](#abortsignalthrowifaborted)

- [Class: `Blob`](#class-blob)

- [Class: `Buffer`](#class-buffer)

- [Class: `ByteLengthQueuingStrategy`](#class-bytelengthqueuingstrategy)

- [`__dirname`](#__dirname)

- [`__filename`](#__filename)

- [`atob(data)`](#atobdata)

- [Class: `BroadcastChannel`](#class-broadcastchannel)

- [`btoa(data)`](#btoadata)

- [`clearImmediate(immediateObject)`](#clearimmediateimmediateobject)

- [`clearInterval(intervalObject)`](#clearintervalintervalobject)

- [`clearTimeout(timeoutObject)`](#cleartimeouttimeoutobject)

- [Class: `CloseEvent`](#class-closeevent)

- [Class: `CompressionStream`](#class-compressionstream)

- [`console`](#console)

- [Class: `CountQueuingStrategy`](#class-countqueuingstrategy)

- [Class: `Crypto`](#class-crypto)

- [`crypto`](#crypto)

- [Class: `CryptoKey`](#class-cryptokey)

- [Class: `CustomEvent`](#class-customevent)

- [Class: `DecompressionStream`](#class-decompressionstream)

- [`ErrorEvent`](#errorevent)

- [Class: `Event`](#class-event)

- [Class: `EventSource`](#class-eventsource)

- [Class: `EventTarget`](#class-eventtarget)

- [`exports`](#exports)

- [`fetch`](#fetch)

- [Custom dispatcher](#custom-dispatcher)

- [Related classes](#related-classes)

- [Class: `File`](#class-file)

- [Class: `FormData`](#class-formdata)

- [`global`](#global)

- [Class: `Headers`](#class-headers)

- [`localStorage`](#localstorage)

- [Class: `MessageChannel`](#class-messagechannel)

- [Class: `MessageEvent`](#class-messageevent)

- [Class: `MessagePort`](#class-messageport)

- [`module`](#module)

- [Class: `Navigator`](#class-navigator)

- [`navigator`](#navigator)

- [`navigator.hardwareConcurrency`](#navigatorhardwareconcurrency)

- [`navigator.language`](#navigatorlanguage)

- [`navigator.languages`](#navigatorlanguages)

- [`navigator.platform`](#navigatorplatform)

- [`navigator.userAgent`](#navigatoruseragent)

- [`navigator.locks`](#navigatorlocks)

- [Class: `PerformanceEntry`](#class-performanceentry)

- [Class: `PerformanceMark`](#class-performancemark)

- [Class: `PerformanceMeasure`](#class-performancemeasure)

- [Class: `PerformanceObserver`](#class-performanceobserver)

- [Class: `PerformanceObserverEntryList`](#class-performanceobserverentrylist)

- [Class: `PerformanceResourceTiming`](#class-performanceresourcetiming)

- [`performance`](#performance)

- [`process`](#process)

- [`queueMicrotask(callback)`](#queuemicrotaskcallback)

- [Class: `ReadableByteStreamController`](#class-readablebytestreamcontroller)

- [Class: `ReadableStream`](#class-readablestream)

- [Class: `ReadableStreamBYOBReader`](#class-readablestreambyobreader)

- [Class: `ReadableStreamBYOBRequest`](#class-readablestreambyobrequest)

- [Class: `ReadableStreamDefaultController`](#class-readablestreamdefaultcontroller)

- [Class: `ReadableStreamDefaultReader`](#class-readablestreamdefaultreader)

- [`require()`](#require)

- [Class: `Response`](#class-response)

- [Class: `Request`](#class-request)

- [`sessionStorage`](#sessionstorage)

- [`setImmediate(callback[, ...args])`](#setimmediatecallback-args)

- [`setInterval(callback, delay[, ...args])`](#setintervalcallback-delay-args)

- [`setTimeout(callback, delay[, ...args])`](#settimeoutcallback-delay-args)

- [Class: `Storage`](#class-storage)

- [`structuredClone(value[, options])`](#structuredclonevalue-options)

- [Class: `SubtleCrypto`](#class-subtlecrypto)

- [Class: `DOMException`](#class-domexception)

- [Class: `TextDecoder`](#class-textdecoder)

- [Class: `TextDecoderStream`](#class-textdecoderstream)

- [Class: `TextEncoder`](#class-textencoder)

- [Class: `TextEncoderStream`](#class-textencoderstream)

- [Class: `TransformStream`](#class-transformstream)

- [Class: `TransformStreamDefaultController`](#class-transformstreamdefaultcontroller)

- [Class: `URL`](#class-url)

- [Class: `URLPattern`](#class-urlpattern)

- [Class: `URLSearchParams`](#class-urlsearchparams)

- [Class: `WebAssembly`](#class-webassembly)

- [Class: `WebSocket`](#class-websocket)

- [Class: `WritableStream`](#class-writablestream)

- [Class: `WritableStreamDefaultController`](#class-writablestreamdefaultcontroller)

- [Class: `WritableStreamDefaultWriter`](#class-writablestreamdefaultwriter)

      
        
## Global objects[#](#global-objects)

[Stability: 2](documentation.html#stability-index) - Stable

These objects are available in all modules.

The following variables may appear to be global but are not. They exist only in
the scope of [CommonJS modules](modules.html):

- [`__dirname`](modules.html#__dirname)

- [`__filename`](modules.html#__filename)

- [`exports`](modules.html#exports)

- [`module`](modules.html#module)

- [`require()`](modules.html#requireid)

The objects listed here are specific to Node.js. There are [built-in objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)
that are part of the JavaScript language itself, which are also globally
accessible.

### Class: `AbortController`[#](#class-abortcontroller)

History

VersionChanges
v15.4.0

No longer experimental.

v15.0.0, v14.17.0

Added in: v15.0.0, v14.17.0

A utility class used to signal cancelation in selected `Promise`-based APIs.
The API is based on the Web API [<AbortController>](globals.html#class-abortcontroller).

const ac = new AbortController();

ac.signal.addEventListener('abort', () => console.log('Aborted!'),
                           { once: true });

ac.abort();

console.log(ac.signal.aborted);  // Prints true copy

#### `abortController.abort([reason])`[#](#abortcontrollerabortreason)

History

VersionChanges
v17.2.0, v16.14.0

Added the new optional reason argument.

v15.0.0, v14.17.0

Added in: v15.0.0, v14.17.0

- `reason` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) An optional reason, retrievable on the `AbortSignal`'s
`reason` property.

Triggers the abort signal, causing the `abortController.signal` to emit
the `'abort'` event.

#### `abortController.signal`[#](#abortcontrollersignal)

Added in: v15.0.0, v14.17.0

- Type: [<AbortSignal>](globals.html#class-abortsignal)

#### Class: `AbortSignal`[#](#class-abortsignal)

Added in: v15.0.0, v14.17.0

- Extends: [<EventTarget>](events.html#class-eventtarget)

The `AbortSignal` is used to notify observers when the
`abortController.abort()` method is called.

Static method: `AbortSignal.abort([reason])`[#](#static-method-abortsignalabortreason)

History

VersionChanges
v17.2.0, v16.14.0

Added the new optional reason argument.

v15.12.0, v14.17.0

Added in: v15.12.0, v14.17.0

- `reason` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- Returns: [<AbortSignal>](globals.html#class-abortsignal)

Returns a new already aborted `AbortSignal`.

Static method: `AbortSignal.timeout(delay)`[#](#static-method-abortsignaltimeoutdelay)

Added in: v17.3.0, v16.14.0

- `delay` [<number>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type) The number of milliseconds to wait before triggering
the AbortSignal.

Returns a new `AbortSignal` which will be aborted in `delay` milliseconds.

Static method: `AbortSignal.any(signals)`[#](#static-method-abortsignalanysignals)

Added in: v20.3.0, v18.17.0

- `signals` [<AbortSignal[]>](globals.html#class-abortsignal) The `AbortSignal`s of which to compose a new `AbortSignal`.

Returns a new `AbortSignal` which will be aborted if any of the provided
signals are aborted. Its [`abortSignal.reason`](#abortsignalreason) will be set to whichever
one of the `signals` caused it to be aborted.

Event: `'abort'`[#](#event-abort)

Added in: v15.0.0, v14.17.0

The `'abort'` event is emitted when the `abortController.abort()` method
is called. The callback is invoked with a single object argument with a
single `type` property set to `'abort'`:

const ac = new AbortController();

// Use either the onabort property...
ac.signal.onabort = () => console.log('aborted!');

// Or the EventTarget API...
ac.signal.addEventListener('abort', (event) => {
  console.log(event.type);  // Prints 'abort'
}, { once: true });

ac.abort(); copy

The `AbortController` with which the `AbortSignal` is associated will only
ever trigger the `'abort'` event once. We recommended that code check
that the `abortSignal.aborted` attribute is `false` before adding an `'abort'`
event listener.

Any event listeners attached to the `AbortSignal` should use the
`{ once: true }` option (or, if using the `EventEmitter` APIs to attach a
listener, use the `once()` method) to ensure that the event listener is
removed as soon as the `'abort'` event is handled. Failure to do so may
result in memory leaks.

`abortSignal.aborted`[#](#abortsignalaborted)

Added in: v15.0.0, v14.17.0

- Type: [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type) True after the `AbortController` has been aborted.

`abortSignal.onabort`[#](#abortsignalonabort)

Added in: v15.0.0, v14.17.0

- Type: [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

An optional callback function that may be set by user code to be notified
when the `abortController.abort()` function has been called.

`abortSignal.reason`[#](#abortsignalreason)

Added in: v17.2.0, v16.14.0

- Type: [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

An optional reason specified when the `AbortSignal` was triggered.

const ac = new AbortController();
ac.abort(new Error('boom!'));
console.log(ac.signal.reason);  // Error: boom! copy

`abortSignal.throwIfAborted()`[#](#abortsignalthrowifaborted)

Added in: v17.3.0, v16.17.0

If `abortSignal.aborted` is `true`, throws `abortSignal.reason`.

### Class: `Blob`[#](#class-blob)

Added in: v18.0.0

See [<Blob>](buffer.html#class-blob).

### Class: `Buffer`[#](#class-buffer)

Added in: v0.1.103

- Type: [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

Used to handle binary data. See the [buffer section](buffer.html).

### Class: `ByteLengthQueuingStrategy`[#](#class-bytelengthqueuingstrategy)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ByteLengthQueuingStrategy`](webstreams.html#class-bytelengthqueuingstrategy).

### `__dirname`[#](#__dirname)

This variable may appear to be global but is not. See [`__dirname`](modules.html#__dirname).

### `__filename`[#](#__filename)

This variable may appear to be global but is not. See [`__filename`](modules.html#__filename).

### `atob(data)`[#](#atobdata)

Added in: v16.0.0

[Stability: 3](documentation.html#stability-index) - Legacy. Use `Buffer.from(data, 'base64')` instead.

Global alias for [`buffer.atob()`](buffer.html#bufferatobdata).

An automated migration is available ([source](https://github.com/nodejs/userland-migrations/tree/main/recipes/buffer-atob-btoa)):

```
`npx codemod@latest @nodejs/buffer-atob-btoa` copy
```

### Class: `BroadcastChannel`[#](#class-broadcastchannel)

Added in: v18.0.0

See [<BroadcastChannel>](worker_threads.html#class-broadcastchannel-extends-eventtarget).

### `btoa(data)`[#](#btoadata)

Added in: v16.0.0

[Stability: 3](documentation.html#stability-index) - Legacy. Use `buf.toString('base64')` instead.

Global alias for [`buffer.btoa()`](buffer.html#bufferbtoadata).

An automated migration is available ([source](https://github.com/nodejs/userland-migrations/tree/main/recipes/buffer-atob-btoa)):

```
`npx codemod@latest @nodejs/buffer-atob-btoa` copy
```

### `clearImmediate(immediateObject)`[#](#clearimmediateimmediateobject)

Added in: v0.9.1

[`clearImmediate`](timers.html#clearimmediateimmediate) is described in the [timers](timers.html) section.

### `clearInterval(intervalObject)`[#](#clearintervalintervalobject)

Added in: v0.0.1

[`clearInterval`](timers.html#clearintervaltimeout) is described in the [timers](timers.html) section.

### `clearTimeout(timeoutObject)`[#](#cleartimeouttimeoutobject)

Added in: v0.0.1

[`clearTimeout`](timers.html#cleartimeouttimeout) is described in the [timers](timers.html) section.

### Class: `CloseEvent`[#](#class-closeevent)

Added in: v23.0.0

A browser-compatible implementation of [<CloseEvent>](https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent). Disable this API
with the [`--no-experimental-websocket`](cli.html#--no-experimental-websocket) CLI flag.

### Class: `CompressionStream`[#](#class-compressionstream)

History

VersionChanges
v24.7.0, v22.20.0

format now accepts `brotli` value.

v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`CompressionStream`](webstreams.html#class-compressionstream).

### `console`[#](#console)

Added in: v0.1.100

- Type: [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

Used to print to stdout and stderr. See the [`console`](console.html) section.

### Class: `CountQueuingStrategy`[#](#class-countqueuingstrategy)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`CountQueuingStrategy`](webstreams.html#class-countqueuingstrategy).

### Class: `Crypto`[#](#class-crypto)

History

VersionChanges
v23.0.0

No longer experimental.

v19.0.0

No longer behind `--experimental-global-webcrypto` CLI flag.

v17.6.0, v16.15.0

Added in: v17.6.0, v16.15.0

A browser-compatible implementation of [<Crypto>](webcrypto.html#class-crypto). This global is available
only if the Node.js binary was compiled with including support for the
`node:crypto` module.

### `crypto`[#](#crypto)

History

VersionChanges
v23.0.0

No longer experimental.

v19.0.0

No longer behind `--experimental-global-webcrypto` CLI flag.

v17.6.0, v16.15.0

Added in: v17.6.0, v16.15.0

A browser-compatible implementation of the [Web Crypto API](webcrypto.html).

### Class: `CryptoKey`[#](#class-cryptokey)

History

VersionChanges
v23.0.0

No longer experimental.

v19.0.0

No longer behind `--experimental-global-webcrypto` CLI flag.

v17.6.0, v16.15.0

Added in: v17.6.0, v16.15.0

A browser-compatible implementation of [<CryptoKey>](webcrypto.html#class-cryptokey). This global is available
only if the Node.js binary was compiled with including support for the
`node:crypto` module.

### Class: `CustomEvent`[#](#class-customevent)

History

VersionChanges
v23.0.0

No longer experimental.

v22.1.0, v20.13.0

CustomEvent is now stable.

v19.0.0

No longer behind `--experimental-global-customevent` CLI flag.

v18.7.0, v16.17.0

Added in: v18.7.0, v16.17.0

A browser-compatible implementation of [<CustomEvent>](events.html#class-customevent).

### Class: `DecompressionStream`[#](#class-decompressionstream)

History

VersionChanges
v24.7.0, v22.20.0

format now accepts `brotli` value.

v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`DecompressionStream`](webstreams.html#class-decompressionstream).

### `ErrorEvent`[#](#errorevent)

Added in: v25.0.0

A browser-compatible implementation of [<ErrorEvent>](https://developer.mozilla.org/en-US/docs/Web/API/ErrorEvent).

### Class: `Event`[#](#class-event)

History

VersionChanges
v15.4.0

No longer experimental.

v15.0.0

Added in: v15.0.0

A browser-compatible implementation of the `Event` class. See
[`EventTarget` and `Event` API](events.html#eventtarget-and-event-api) for more details.

### Class: `EventSource`[#](#class-eventsource)

Added in: v22.3.0, v20.18.0

[Stability: 1](documentation.html#stability-index) - Experimental. Enable this API with the [`--experimental-eventsource`](cli.html#--experimental-eventsource)
CLI flag.

A browser-compatible implementation of [<EventSource>](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

### Class: `EventTarget`[#](#class-eventtarget)

History

VersionChanges
v15.4.0

No longer experimental.

v15.0.0

Added in: v15.0.0

A browser-compatible implementation of the `EventTarget` class. See
[`EventTarget` and `Event` API](events.html#eventtarget-and-event-api) for more details.

### `exports`[#](#exports)

This variable may appear to be global but is not. See [`exports`](modules.html#exports).

### `fetch`[#](#fetch)

History

VersionChanges
v21.0.0

No longer experimental.

v18.0.0

No longer behind `--experimental-fetch` CLI flag.

v17.5.0, v16.15.0

Added in: v17.5.0, v16.15.0

A browser-compatible implementation of the [`fetch()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch) function.

const res = await fetch('https://nodejs.org/api/documentation.json');
if (res.ok) {
  const data = await res.json();
  console.log(data);
} copy

The implementation is based upon [undici](https://undici.nodejs.org), an HTTP/1.1 client
written from scratch for Node.js. You can figure out which version of `undici` is bundled
in your Node.js process reading the `process.versions.undici` property.

#### Custom dispatcher[#](#custom-dispatcher)

You can use a custom dispatcher to dispatch requests passing it in fetch's options object.
The dispatcher must be compatible with `undici`'s
[`Dispatcher` class](https://undici.nodejs.org/#/docs/api/Dispatcher.md).

```
`fetch(url, { dispatcher: new MyAgent() });` copy
```

It is possible to change the global dispatcher in Node.js by installing `undici` and using
the `setGlobalDispatcher()` method. Calling this method will affect both `undici` and
Node.js.

import { setGlobalDispatcher } from 'undici';
setGlobalDispatcher(new MyAgent()); copy

#### Related classes[#](#related-classes)

The following globals are available to use with `fetch`:

- [`FormData`](https://nodejs.org/api/globals.html#class-formdata)

- [`Headers`](https://nodejs.org/api/globals.html#class-headers)

- [`Request`](https://nodejs.org/api/globals.html#request)

- [`Response`](https://nodejs.org/api/globals.html#response).

### Class: `File`[#](#class-file)

Added in: v20.0.0

See [<File>](buffer.html#class-file).

### Class: `FormData`[#](#class-formdata)

History

VersionChanges
v21.0.0

No longer experimental.

v18.0.0

No longer behind `--experimental-fetch` CLI flag.

v17.6.0, v16.15.0

Added in: v17.6.0, v16.15.0

A browser-compatible implementation of [<FormData>](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

### `global`[#](#global)

Added in: v0.1.27

[Stability: 3](documentation.html#stability-index) - Legacy. Use [`globalThis`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis) instead.

- Type: [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) The global namespace object.

In browsers, the top-level scope has traditionally been the global scope. This
means that `var something` will define a new global variable, except within
ECMAScript modules. In Node.js, this is different. The top-level scope is not
the global scope; `var something` inside a Node.js module will be local to that
module, regardless of whether it is a [CommonJS module](modules.html) or an
[ECMAScript module](esm.html).

### Class: `Headers`[#](#class-headers)

History

VersionChanges
v21.0.0

No longer experimental.

v18.0.0

No longer behind `--experimental-fetch` CLI flag.

v17.5.0, v16.15.0

Added in: v17.5.0, v16.15.0

A browser-compatible implementation of [<Headers>](https://developer.mozilla.org/en-US/docs/Web/API/Headers).

### `localStorage`[#](#localstorage)

History

VersionChanges
v25.0.0

When webstorage is enabled and `--localstorage-file` is not provided, accessing the `localStorage` global now returns an empty object.

v25.0.0

This API is no longer behind `--experimental-webstorage` runtime flag.

v22.4.0

Added in: v22.4.0

[Stability: 1.2](documentation.html#stability-index) - Release candidate. Disable this API with [`--no-experimental-webstorage`](cli.html#--no-experimental-webstorage).

A browser-compatible implementation of [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage). Data is stored
unencrypted in the file specified by the [`--localstorage-file`](cli.html#--localstorage-filefile) CLI flag.
The maximum amount of data that can be stored is 10 MB.
Any modification of this data outside of the Web Storage API is not supported.
`localStorage` data is not stored per user or per request when used in the context
of a server, it is shared across all users and requests.

### Class: `MessageChannel`[#](#class-messagechannel)

Added in: v15.0.0

The `MessageChannel` class. See [`MessageChannel`](worker_threads.html#class-messagechannel) for more details.

### Class: `MessageEvent`[#](#class-messageevent)

Added in: v15.0.0

A browser-compatible implementation of [<MessageEvent>](https://developer.mozilla.org/en-US/docs/Web/API/MessageEvent).

### Class: `MessagePort`[#](#class-messageport)

Added in: v15.0.0

The `MessagePort` class. See [`MessagePort`](worker_threads.html#class-messageport) for more details.

### `module`[#](#module)

This variable may appear to be global but is not. See [`module`](modules.html#module).

### Class: `Navigator`[#](#class-navigator)

Added in: v21.0.0

[Stability: 1.1](documentation.html#stability-index) - Active development. Disable this API with the
[`--no-experimental-global-navigator`](cli.html#--no-experimental-global-navigator) CLI flag.

A partial implementation of the [Navigator API](https://html.spec.whatwg.org/multipage/system-state.html#the-navigator-object).

### `navigator`[#](#navigator)

Added in: v21.0.0

[Stability: 1.1](documentation.html#stability-index) - Active development. Disable this API with the
[`--no-experimental-global-navigator`](cli.html#--no-experimental-global-navigator) CLI flag.

A partial implementation of [`window.navigator`](https://developer.mozilla.org/en-US/docs/Web/API/Window/navigator).

#### `navigator.hardwareConcurrency`[#](#navigatorhardwareconcurrency)

Added in: v21.0.0

- Type: [<number>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type)

The `navigator.hardwareConcurrency` read-only property returns the number of
logical processors available to the current Node.js instance.

```
`console.log(`This process is running on ${navigator.hardwareConcurrency} logical processors`);` copy
```

#### `navigator.language`[#](#navigatorlanguage)

Added in: v21.2.0

- Type: [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

The `navigator.language` read-only property returns a string representing the
preferred language of the Node.js instance. The language will be determined by
the ICU library used by Node.js at runtime based on the
default language of the operating system.

The value is representing the language version as defined in [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646.txt).

The fallback value on builds without ICU is `'en-US'`.

```
`console.log(`The preferred language of the Node.js instance has the tag '${navigator.language}'`);` copy
```

#### `navigator.languages`[#](#navigatorlanguages)

Added in: v21.2.0

- Type: {Array}

The `navigator.languages` read-only property returns an array of strings
representing the preferred languages of the Node.js instance.
By default `navigator.languages` contains only the value of
`navigator.language`, which will be determined by the ICU library used by
Node.js at runtime based on the default language of the operating system.

The fallback value on builds without ICU is `['en-US']`.

```
`console.log(`The preferred languages are '${navigator.languages}'`);` copy
```

#### `navigator.platform`[#](#navigatorplatform)

Added in: v21.2.0

- Type: [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

The `navigator.platform` read-only property returns a string identifying the
platform on which the Node.js instance is running.

```
`console.log(`This process is running on ${navigator.platform}`);` copy
```

#### `navigator.userAgent`[#](#navigatoruseragent)

Added in: v21.1.0

- Type: [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

The `navigator.userAgent` read-only property returns user agent
consisting of the runtime name and major version number.

```
`console.log(`The user-agent is ${navigator.userAgent}`); // Prints "Node.js/21"` copy
```

#### `navigator.locks`[#](#navigatorlocks)

Added in: v24.5.0

[Stability: 1](documentation.html#stability-index) - Experimental

The `navigator.locks` read-only property returns a [`LockManager`](worker_threads.html#class-lockmanager) instance that
can be used to coordinate access to resources that may be shared across multiple
threads within the same process. This global implementation matches the semantics
of the [browser `LockManager`](https://developer.mozilla.org/en-US/docs/Web/API/LockManager) API.

// Request an exclusive lock
await navigator.locks.request('my_resource', async (lock) => {
  // The lock has been acquired.
  console.log(`Lock acquired: ${lock.name}`);
  // Lock is automatically released when the function returns
});

// Request a shared lock
await navigator.locks.request('shared_resource', { mode: 'shared' }, async (lock) => {
  // Multiple shared locks can be held simultaneously
  console.log(`Shared lock acquired: ${lock.name}`);
});// Request an exclusive lock
navigator.locks.request('my_resource', async (lock) => {
  // The lock has been acquired.
  console.log(`Lock acquired: ${lock.name}`);
  // Lock is automatically released when the function returns
}).then(() => {
  console.log('Lock released');
});

// Request a shared lock
navigator.locks.request('shared_resource', { mode: 'shared' }, async (lock) => {
  // Multiple shared locks can be held simultaneously
  console.log(`Shared lock acquired: ${lock.name}`);
}).then(() => {
  console.log('Shared lock released');
});copy

See [`worker_threads.locks`](worker_threads.html#worker_threadslocks) for detailed API documentation.

### Class: `PerformanceEntry`[#](#class-performanceentry)

Added in: v19.0.0

The `PerformanceEntry` class. See [`PerformanceEntry`](perf_hooks.html#class-performanceentry) for more details.

### Class: `PerformanceMark`[#](#class-performancemark)

Added in: v19.0.0

The `PerformanceMark` class. See [`PerformanceMark`](perf_hooks.html#class-performancemark) for more details.

### Class: `PerformanceMeasure`[#](#class-performancemeasure)

Added in: v19.0.0

The `PerformanceMeasure` class. See [`PerformanceMeasure`](perf_hooks.html#class-performancemeasure) for more details.

### Class: `PerformanceObserver`[#](#class-performanceobserver)

Added in: v19.0.0

The `PerformanceObserver` class. See [`PerformanceObserver`](perf_hooks.html#class-performanceobserver) for more details.

### Class: `PerformanceObserverEntryList`[#](#class-performanceobserverentrylist)

Added in: v19.0.0

The `PerformanceObserverEntryList` class. See
[`PerformanceObserverEntryList`](perf_hooks.html#class-performanceobserverentrylist) for more details.

### Class: `PerformanceResourceTiming`[#](#class-performanceresourcetiming)

Added in: v19.0.0

The `PerformanceResourceTiming` class. See [`PerformanceResourceTiming`](perf_hooks.html#class-performanceresourcetiming) for
more details.

### `performance`[#](#performance)

Added in: v16.0.0

The [`perf_hooks.performance`](perf_hooks.html#perf_hooksperformance) object.

### `process`[#](#process)

Added in: v0.1.7

- Type: [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

The process object. See the [`process` object](process.html#process) section.

### `queueMicrotask(callback)`[#](#queuemicrotaskcallback)

Added in: v11.0.0

- `callback` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) Function to be queued.

The `queueMicrotask()` method queues a microtask to invoke `callback`. If
`callback` throws an exception, the [`process` object](process.html#process) `'uncaughtException'`
event will be emitted.

The microtask queue is managed by V8 and may be used in a similar manner to
the [`process.nextTick()`](process.html#processnexttickcallback-args) queue, which is managed by Node.js. The
`process.nextTick()` queue is always processed before the microtask queue
within each turn of the Node.js event loop.

// Here, `queueMicrotask()` is used to ensure the 'load' event is always
// emitted asynchronously, and therefore consistently. Using
// `process.nextTick()` here would result in the 'load' event always emitting
// before any other promise jobs.

DataHandler.prototype.load = async function load(key) {
  const hit = this._cache.get(key);
  if (hit !== undefined) {
    queueMicrotask(() => {
      this.emit('load', hit);
    });
    return;
  }

  const data = await fetchData(key);
  this._cache.set(key, data);
  this.emit('load', data);
}; copy

### Class: `ReadableByteStreamController`[#](#class-readablebytestreamcontroller)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableByteStreamController`](webstreams.html#class-readablebytestreamcontroller).

### Class: `ReadableStream`[#](#class-readablestream)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableStream`](webstreams.html#class-readablestream).

### Class: `ReadableStreamBYOBReader`[#](#class-readablestreambyobreader)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableStreamBYOBReader`](webstreams.html#class-readablestreambyobreader).

### Class: `ReadableStreamBYOBRequest`[#](#class-readablestreambyobrequest)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableStreamBYOBRequest`](webstreams.html#class-readablestreambyobrequest).

### Class: `ReadableStreamDefaultController`[#](#class-readablestreamdefaultcontroller)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableStreamDefaultController`](webstreams.html#class-readablestreamdefaultcontroller).

### Class: `ReadableStreamDefaultReader`[#](#class-readablestreamdefaultreader)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`ReadableStreamDefaultReader`](webstreams.html#class-readablestreamdefaultreader).

### `require()`[#](#require)

This variable may appear to be global but is not. See [`require()`](modules.html#requireid).

### Class: `Response`[#](#class-response)

History

VersionChanges
v21.0.0

No longer experimental.

v18.0.0

No longer behind `--experimental-fetch` CLI flag.

v17.5.0, v16.15.0

Added in: v17.5.0, v16.15.0

A browser-compatible implementation of [<Response>](https://developer.mozilla.org/en-US/docs/Web/API/Response).

### Class: `Request`[#](#class-request)

History

VersionChanges
v21.0.0

No longer experimental.

v18.0.0

No longer behind `--experimental-fetch` CLI flag.

v17.5.0, v16.15.0

Added in: v17.5.0, v16.15.0

A browser-compatible implementation of [<Request>](https://developer.mozilla.org/en-US/docs/Web/API/Request).

### `sessionStorage`[#](#sessionstorage)

History

VersionChanges
v25.0.0

This API is no longer behind `--experimental-webstorage` runtime flag.

v22.4.0

Added in: v22.4.0

[Stability: 1.2](documentation.html#stability-index) - Release candidate. Disable this API with [`--no-experimental-webstorage`](cli.html#--no-experimental-webstorage).

A browser-compatible implementation of [`sessionStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage). Data is stored in
memory, with a storage quota of 10 MB. `sessionStorage` data persists only within
the currently running process, and is not shared between workers.

### `setImmediate(callback[, ...args])`[#](#setimmediatecallback-args)

Added in: v0.9.1

[`setImmediate`](timers.html#setimmediatecallback-args) is described in the [timers](timers.html) section.

### `setInterval(callback, delay[, ...args])`[#](#setintervalcallback-delay-args)

Added in: v0.0.1

[`setInterval`](timers.html#setintervalcallback-delay-args) is described in the [timers](timers.html) section.

### `setTimeout(callback, delay[, ...args])`[#](#settimeoutcallback-delay-args)

Added in: v0.0.1

[`setTimeout`](timers.html#settimeoutcallback-delay-args) is described in the [timers](timers.html) section.

### Class: `Storage`[#](#class-storage)

Added in: v22.4.0

[Stability: 1.2](documentation.html#stability-index) - Release candidate. Disable this API with [`--no-experimental-webstorage`](cli.html#--no-experimental-webstorage).

A browser-compatible implementation of [<Storage>](https://developer.mozilla.org/en-US/docs/Web/API/Storage).

### `structuredClone(value[, options])`[#](#structuredclonevalue-options)

Added in: v17.0.0

The WHATWG [`structuredClone`](https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone) method.

### Class: `SubtleCrypto`[#](#class-subtlecrypto)

History

VersionChanges
v19.0.0

No longer behind `--experimental-global-webcrypto` CLI flag.

v17.6.0, v16.15.0

Added in: v17.6.0, v16.15.0

A browser-compatible implementation of [<SubtleCrypto>](webcrypto.html#class-subtlecrypto). This global is available
only if the Node.js binary was compiled with including support for the
`node:crypto` module.

### Class: `DOMException`[#](#class-domexception)

Added in: v17.0.0

The WHATWG [<DOMException>](https://developer.mozilla.org/en-US/docs/Web/API/DOMException) class.

### Class: `TextDecoder`[#](#class-textdecoder)

Added in: v11.0.0

The WHATWG `TextDecoder` class. See the [`TextDecoder`](util.html#class-utiltextdecoder) section.

### Class: `TextDecoderStream`[#](#class-textdecoderstream)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`TextDecoderStream`](webstreams.html#class-textdecoderstream).

### Class: `TextEncoder`[#](#class-textencoder)

Added in: v11.0.0

The WHATWG `TextEncoder` class. See the [`TextEncoder`](util.html#class-utiltextencoder) section.

### Class: `TextEncoderStream`[#](#class-textencoderstream)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`TextEncoderStream`](webstreams.html#class-textencoderstream).

### Class: `TransformStream`[#](#class-transformstream)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`TransformStream`](webstreams.html#class-transformstream).

### Class: `TransformStreamDefaultController`[#](#class-transformstreamdefaultcontroller)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`TransformStreamDefaultController`](webstreams.html#class-transformstreamdefaultcontroller).

### Class: `URL`[#](#class-url)

Added in: v10.0.0

The WHATWG `URL` class. See the [`URL`](url.html#class-url) section.

### Class: `URLPattern`[#](#class-urlpattern)

Added in: v24.0.0

[Stability: 1](documentation.html#stability-index) - Experimental

The WHATWG `URLPattern` class. See the [`URLPattern`](url.html#class-urlpattern) section.

### Class: `URLSearchParams`[#](#class-urlsearchparams)

Added in: v10.0.0

The WHATWG `URLSearchParams` class. See the [`URLSearchParams`](url.html#class-urlsearchparams) section.

### Class: `WebAssembly`[#](#class-webassembly)

Added in: v8.0.0

- Type: [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

The object that acts as the namespace for all W3C
[WebAssembly](https://webassembly.org) related functionality. See the
[Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/WebAssembly) for usage and compatibility.

### Class: `WebSocket`[#](#class-websocket)

History

VersionChanges
v22.4.0

No longer experimental.

v22.0.0

No longer behind `--experimental-websocket` CLI flag.

v21.0.0, v20.10.0

Added in: v21.0.0, v20.10.0

A browser-compatible implementation of [<WebSocket>](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket). Disable this API
with the [`--no-experimental-websocket`](cli.html#--no-experimental-websocket) CLI flag.

### Class: `WritableStream`[#](#class-writablestream)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`WritableStream`](webstreams.html#class-writablestream).

### Class: `WritableStreamDefaultController`[#](#class-writablestreamdefaultcontroller)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`WritableStreamDefaultController`](webstreams.html#class-writablestreamdefaultcontroller).

### Class: `WritableStreamDefaultWriter`[#](#class-writablestreamdefaultwriter)

History

VersionChanges
v23.11.0, v22.15.0

Marking the API stable.

v18.0.0

Added in: v18.0.0

A browser-compatible implementation of [`WritableStreamDefaultWriter`](webstreams.html#class-writablestreamdefaultwriter).
