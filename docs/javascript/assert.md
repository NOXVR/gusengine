# Source: https://nodejs.org/api/assert.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

Assert | Node.js v25.6.1 Documentation
  
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
      

      

- [Assert](#assert)

- [Strict assertion mode](#strict-assertion-mode)

- [Legacy assertion mode](#legacy-assertion-mode)

- [Class: `assert.AssertionError`](#class-assertassertionerror)

- [`new assert.AssertionError(options)`](#new-assertassertionerroroptions)

- [Class: `assert.Assert`](#class-assertassert)

- [`new assert.Assert([options])`](#new-assertassertoptions)

- [`assert(value[, message])`](#assertvalue-message)

- [`assert.deepEqual(actual, expected[, message])`](#assertdeepequalactual-expected-message)

- [Comparison details](#comparison-details)

- [`assert.deepStrictEqual(actual, expected[, message])`](#assertdeepstrictequalactual-expected-message)

- [Comparison details](#comparison-details_1)

- [`assert.doesNotMatch(string, regexp[, message])`](#assertdoesnotmatchstring-regexp-message)

- [`assert.doesNotReject(asyncFn[, error][, message])`](#assertdoesnotrejectasyncfn-error-message)

- [`assert.doesNotThrow(fn[, error][, message])`](#assertdoesnotthrowfn-error-message)

- [`assert.equal(actual, expected[, message])`](#assertequalactual-expected-message)

- [`assert.fail([message])`](#assertfailmessage)

- [`assert.ifError(value)`](#assertiferrorvalue)

- [`assert.match(string, regexp[, message])`](#assertmatchstring-regexp-message)

- [`assert.notDeepEqual(actual, expected[, message])`](#assertnotdeepequalactual-expected-message)

- [`assert.notDeepStrictEqual(actual, expected[, message])`](#assertnotdeepstrictequalactual-expected-message)

- [`assert.notEqual(actual, expected[, message])`](#assertnotequalactual-expected-message)

- [`assert.notStrictEqual(actual, expected[, message])`](#assertnotstrictequalactual-expected-message)

- [`assert.ok(value[, message])`](#assertokvalue-message)

- [`assert.rejects(asyncFn[, error][, message])`](#assertrejectsasyncfn-error-message)

- [`assert.strictEqual(actual, expected[, message])`](#assertstrictequalactual-expected-message)

- [`assert.throws(fn[, error][, message])`](#assertthrowsfn-error-message)

- [`assert.partialDeepStrictEqual(actual, expected[, message])`](#assertpartialdeepstrictequalactual-expected-message)

- [Comparison details](#comparison-details_2)

    
  
            
    
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
      
      
- [25.x](https://nodejs.org/docs/latest-v25.x/api/assert.html)

- [24.x LTS](https://nodejs.org/docs/latest-v24.x/api/assert.html)

- [23.x](https://nodejs.org/docs/latest-v23.x/api/assert.html)

- [22.x LTS](https://nodejs.org/docs/latest-v22.x/api/assert.html)

- [21.x](https://nodejs.org/docs/latest-v21.x/api/assert.html)

- [20.x LTS](https://nodejs.org/docs/latest-v20.x/api/assert.html)

- [19.x](https://nodejs.org/docs/latest-v19.x/api/assert.html)

- [18.x](https://nodejs.org/docs/latest-v18.x/api/assert.html)

- [17.x](https://nodejs.org/docs/latest-v17.x/api/assert.html)

- [16.x](https://nodejs.org/docs/latest-v16.x/api/assert.html)

- [15.x](https://nodejs.org/docs/latest-v15.x/api/assert.html)

- [14.x](https://nodejs.org/docs/latest-v14.x/api/assert.html)

- [13.x](https://nodejs.org/docs/latest-v13.x/api/assert.html)

- [12.x](https://nodejs.org/docs/latest-v12.x/api/assert.html)

- [11.x](https://nodejs.org/docs/latest-v11.x/api/assert.html)

- [10.x](https://nodejs.org/docs/latest-v10.x/api/assert.html)

- [9.x](https://nodejs.org/docs/latest-v9.x/api/assert.html)

- [8.x](https://nodejs.org/docs/latest-v8.x/api/assert.html)

- [7.x](https://nodejs.org/docs/latest-v7.x/api/assert.html)

- [6.x](https://nodejs.org/docs/latest-v6.x/api/assert.html)

- [5.x](https://nodejs.org/docs/latest-v5.x/api/assert.html)

- [4.x](https://nodejs.org/docs/latest-v4.x/api/assert.html)

- [0.12.x](https://nodejs.org/docs/latest-v0.12.x/api/assert.html)

- [0.10.x](https://nodejs.org/docs/latest-v0.10.x/api/assert.html)
    
  
            
- 
              
                
                Options
              
        
              
                
                  
- 
                    [View on single page](all.html)
                  
                  
- 
                    [View as JSON](assert.json)
                  
                  
- [Edit on GitHub](https://github.com/nodejs/node/edit/main/doc/api/assert.md)    
                
              
            
          
        
        
      

      Table of contents

- [Assert](#assert)

- [Strict assertion mode](#strict-assertion-mode)

- [Legacy assertion mode](#legacy-assertion-mode)

- [Class: `assert.AssertionError`](#class-assertassertionerror)

- [`new assert.AssertionError(options)`](#new-assertassertionerroroptions)

- [Class: `assert.Assert`](#class-assertassert)

- [`new assert.Assert([options])`](#new-assertassertoptions)

- [`assert(value[, message])`](#assertvalue-message)

- [`assert.deepEqual(actual, expected[, message])`](#assertdeepequalactual-expected-message)

- [Comparison details](#comparison-details)

- [`assert.deepStrictEqual(actual, expected[, message])`](#assertdeepstrictequalactual-expected-message)

- [Comparison details](#comparison-details_1)

- [`assert.doesNotMatch(string, regexp[, message])`](#assertdoesnotmatchstring-regexp-message)

- [`assert.doesNotReject(asyncFn[, error][, message])`](#assertdoesnotrejectasyncfn-error-message)

- [`assert.doesNotThrow(fn[, error][, message])`](#assertdoesnotthrowfn-error-message)

- [`assert.equal(actual, expected[, message])`](#assertequalactual-expected-message)

- [`assert.fail([message])`](#assertfailmessage)

- [`assert.ifError(value)`](#assertiferrorvalue)

- [`assert.match(string, regexp[, message])`](#assertmatchstring-regexp-message)

- [`assert.notDeepEqual(actual, expected[, message])`](#assertnotdeepequalactual-expected-message)

- [`assert.notDeepStrictEqual(actual, expected[, message])`](#assertnotdeepstrictequalactual-expected-message)

- [`assert.notEqual(actual, expected[, message])`](#assertnotequalactual-expected-message)

- [`assert.notStrictEqual(actual, expected[, message])`](#assertnotstrictequalactual-expected-message)

- [`assert.ok(value[, message])`](#assertokvalue-message)

- [`assert.rejects(asyncFn[, error][, message])`](#assertrejectsasyncfn-error-message)

- [`assert.strictEqual(actual, expected[, message])`](#assertstrictequalactual-expected-message)

- [`assert.throws(fn[, error][, message])`](#assertthrowsfn-error-message)

- [`assert.partialDeepStrictEqual(actual, expected[, message])`](#assertpartialdeepstrictequalactual-expected-message)

- [Comparison details](#comparison-details_2)

      
        
## Assert[#](#assert)

[Stability: 2](documentation.html#stability-index) - Stable

**Source Code:** [lib/assert.js](https://github.com/nodejs/node/blob/v25.6.1/lib/assert.js)

The `node:assert` module provides a set of assertion functions for verifying
invariants.

### Strict assertion mode[#](#strict-assertion-mode)

History

VersionChanges
v15.0.0

Exposed as `require('node:assert/strict')`.

v13.9.0, v12.16.2

Changed "strict mode" to "strict assertion mode" and "legacy mode" to "legacy assertion mode" to avoid confusion with the more usual meaning of "strict mode".

v9.9.0

Added error diffs to the strict assertion mode.

v9.9.0

Added strict assertion mode to the assert module.

v9.9.0

Added in: v9.9.0

In strict assertion mode, non-strict methods behave like their corresponding
strict methods. For example, [`assert.deepEqual()`](#assertdeepequalactual-expected-message) will behave like
[`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message).

In strict assertion mode, error messages for objects display a diff. In legacy
assertion mode, error messages for objects display the objects, often truncated.

To use strict assertion mode:

```
`import { strict as assert } from 'node:assert';``const assert = require('node:assert').strict;`copy
```

```
`import assert from 'node:assert/strict';``const assert = require('node:assert/strict');`copy
```

Example error diff:

import { strict as assert } from 'node:assert';

assert.deepEqual([[[1, 2, 3]], 4, 5], [[[1, 2, '3']], 4, 5]);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected ... Lines skipped
//
//   [
//     [
// ...
//       2,
// +     3
// -     '3'
//     ],
// ...
//     5
//   ]const assert = require('node:assert/strict');

assert.deepEqual([[[1, 2, 3]], 4, 5], [[[1, 2, '3']], 4, 5]);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected ... Lines skipped
//
//   [
//     [
// ...
//       2,
// +     3
// -     '3'
//     ],
// ...
//     5
//   ]copy

To deactivate the colors, use the `NO_COLOR` or `NODE_DISABLE_COLORS`
environment variables. This will also deactivate the colors in the REPL. For
more on color support in terminal environments, read the tty
[`getColorDepth()`](tty.html#writestreamgetcolordepthenv) documentation.

### Legacy assertion mode[#](#legacy-assertion-mode)

Legacy assertion mode uses the [`==` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality) in:

- [`assert.deepEqual()`](#assertdeepequalactual-expected-message)

- [`assert.equal()`](#assertequalactual-expected-message)

- [`assert.notDeepEqual()`](#assertnotdeepequalactual-expected-message)

- [`assert.notEqual()`](#assertnotequalactual-expected-message)

To use legacy assertion mode:

```
`import assert from 'node:assert';``const assert = require('node:assert');`copy
```

Legacy assertion mode may have surprising results, especially when using
[`assert.deepEqual()`](#assertdeepequalactual-expected-message):

// WARNING: This does not throw an AssertionError in legacy assertion mode!
assert.deepEqual(/a/gi, new Date()); copy

### Class: `assert.AssertionError`[#](#class-assertassertionerror)

- Extends: [<errors.Error>](errors.html#class-error)

Indicates the failure of an assertion. All errors thrown by the `node:assert`
module will be instances of the `AssertionError` class.

#### `new assert.AssertionError(options)`[#](#new-assertassertionerroroptions)

Added in: v0.1.21

- `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) If provided, the error message is set to this value.

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) The `actual` property on the error instance.

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) The `expected` property on the error instance.

- `operator` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) The `operator` property on the error instance.

- `stackStartFn` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) If provided, the generated stack trace omits
frames before this function.

- `diff` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) If set to `'full'`, shows the full diff in assertion errors. Defaults to `'simple'`.
Accepted values: `'simple'`, `'full'`.

A subclass of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) that indicates the failure of an assertion.

All instances contain the built-in `Error` properties (`message` and `name`)
and:

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) Set to the `actual` argument for methods such as
[`assert.strictEqual()`](#assertstrictequalactual-expected-message).

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) Set to the `expected` value for methods such as
[`assert.strictEqual()`](#assertstrictequalactual-expected-message).

- `generatedMessage` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type) Indicates if the message was auto-generated
(`true`) or not.

- `code` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) Value is always `ERR_ASSERTION` to show that the error is an
assertion error.

- `operator` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) Set to the passed in operator value.

import assert from 'node:assert';

// Generate an AssertionError to compare the error message later:
const { message } = new assert.AssertionError({
  actual: 1,
  expected: 2,
  operator: 'strictEqual',
});

// Verify error output:
try {
  assert.strictEqual(1, 2);
} catch (err) {
  assert(err instanceof assert.AssertionError);
  assert.strictEqual(err.message, message);
  assert.strictEqual(err.name, 'AssertionError');
  assert.strictEqual(err.actual, 1);
  assert.strictEqual(err.expected, 2);
  assert.strictEqual(err.code, 'ERR_ASSERTION');
  assert.strictEqual(err.operator, 'strictEqual');
  assert.strictEqual(err.generatedMessage, true);
}const assert = require('node:assert');

// Generate an AssertionError to compare the error message later:
const { message } = new assert.AssertionError({
  actual: 1,
  expected: 2,
  operator: 'strictEqual',
});

// Verify error output:
try {
  assert.strictEqual(1, 2);
} catch (err) {
  assert(err instanceof assert.AssertionError);
  assert.strictEqual(err.message, message);
  assert.strictEqual(err.name, 'AssertionError');
  assert.strictEqual(err.actual, 1);
  assert.strictEqual(err.expected, 2);
  assert.strictEqual(err.code, 'ERR_ASSERTION');
  assert.strictEqual(err.operator, 'strictEqual');
  assert.strictEqual(err.generatedMessage, true);
}copy

### Class: `assert.Assert`[#](#class-assertassert)

Added in: v24.6.0, v22.19.0

The `Assert` class allows creating independent assertion instances with custom options.

#### `new assert.Assert([options])`[#](#new-assertassertoptions)

History

VersionChanges
v24.9.0

Added `skipPrototype` option.

- `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)

- `diff` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) If set to `'full'`, shows the full diff in assertion errors. Defaults to `'simple'`.
Accepted values: `'simple'`, `'full'`.

- `strict` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type) If set to `true`, non-strict methods behave like their
corresponding strict methods. Defaults to `true`.

- `skipPrototype` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type) If set to `true`, skips prototype and constructor
comparison in deep equality checks. Defaults to `false`.

Creates a new assertion instance. The `diff` option controls the verbosity of diffs in assertion error messages.

const { Assert } = require('node:assert');
const assertInstance = new Assert({ diff: 'full' });
assertInstance.deepStrictEqual({ a: 1 }, { a: 2 });
// Shows a full diff in the error message. copy

**Important**: When destructuring assertion methods from an `Assert` instance,
the methods lose their connection to the instance's configuration options (such
as `diff`, `strict`, and `skipPrototype` settings).
The destructured methods will fall back to default behavior instead.

const myAssert = new Assert({ diff: 'full' });

// This works as expected - uses 'full' diff
myAssert.strictEqual({ a: 1 }, { b: { c: 1 } });

// This loses the 'full' diff setting - falls back to default 'simple' diff
const { strictEqual } = myAssert;
strictEqual({ a: 1 }, { b: { c: 1 } }); copy

The `skipPrototype` option affects all deep equality methods:

class Foo {
  constructor(a) {
    this.a = a;
  }
}

class Bar {
  constructor(a) {
    this.a = a;
  }
}

const foo = new Foo(1);
const bar = new Bar(1);

// Default behavior - fails due to different constructors
const assert1 = new Assert();
assert1.deepStrictEqual(foo, bar); // AssertionError

// Skip prototype comparison - passes if properties are equal
const assert2 = new Assert({ skipPrototype: true });
assert2.deepStrictEqual(foo, bar); // OK copy

When destructured, methods lose access to the instance's `this` context and revert to default assertion behavior
(diff: 'simple', non-strict mode).
To maintain custom options when using destructured methods, avoid
destructuring and call methods directly on the instance.

### `assert(value[, message])`[#](#assertvalue-message)

Added in: v0.5.9

- `value` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types) The input that is checked for being truthy.

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

An alias of [`assert.ok()`](#assertokvalue-message).

### `assert.deepEqual(actual, expected[, message])`[#](#assertdeepequalactual-expected-message)

History

VersionChanges
v25.0.0

Promises are not considered equal anymore if they are not of the same instance.

v25.0.0

Invalid dates are now considered equal.

v24.0.0

Recursion now stops when either side encounters a circular reference.

v22.2.0, v20.15.0

Error cause and errors properties are now compared as well.

v18.0.0

Regular expressions lastIndex property is now compared as well.

v16.0.0, v14.18.0

In Legacy assertion mode, changed status from Deprecated to Legacy.

v14.0.0

NaN is now treated as being identical if both sides are NaN.

v12.0.0

The type tags are now properly compared and there are a couple minor comparison adjustments to make the check less surprising.

v9.0.0

The `Error` names and messages are now properly compared.

v8.0.0

The `Set` and `Map` content is also compared.

v6.4.0, v4.7.1

Typed array slices are handled correctly now.

v6.1.0, v4.5.0

Objects with circular references can be used as inputs now.

v5.10.1, v4.4.3

Handle non-`Uint8Array` typed arrays correctly.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

**Strict assertion mode**

An alias of [`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message).

**Legacy assertion mode**

[Stability: 3](documentation.html#stability-index) - Legacy: Use [`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message) instead.

Tests for deep equality between the `actual` and `expected` parameters. Consider
using [`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message) instead. [`assert.deepEqual()`](#assertdeepequalactual-expected-message) can have
surprising results.

*Deep equality* means that the enumerable "own" properties of child objects
are also recursively evaluated by the following rules.

#### Comparison details[#](#comparison-details)

- Primitive values are compared with the [`==` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality),
with the exception of [<NaN>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN). It is treated as being identical in case
both sides are [<NaN>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN).

- [Type tags](https://tc39.github.io/ecma262/#sec-object.prototype.tostring) of objects should be the same.

- Only [enumerable "own" properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Enumerability_and_ownership_of_properties) are considered.

- Object constructors are compared when available.

- [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) names, messages, causes, and errors are always compared,
even if these are not enumerable properties.

- [Object wrappers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures#primitive_values) are compared both as objects and unwrapped values.

- `Object` properties are compared unordered.

- [<Map>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) keys and [<Set>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) items are compared unordered.

- Recursion stops when both sides differ or either side encounters a circular
reference.

- Implementation does not test the [`[[Prototype]]`](https://tc39.github.io/ecma262/#sec-ordinary-object-internal-methods-and-internal-slots) of
objects.

- [<Symbol>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) properties are not compared.

- [<WeakMap>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap), [<WeakSet>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet) and [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) instances are **not** compared
structurally. They are only equal if they reference the same object. Any
comparison between different `WeakMap`, `WeakSet`, or `Promise` instances
will result in inequality, even if they contain the same content.

- [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) lastIndex, flags, and source are always compared, even if these
are not enumerable properties.

The following example does not throw an [`AssertionError`](#class-assertassertionerror) because the
primitives are compared using the [`==` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality).

import assert from 'node:assert';
// WARNING: This does not throw an AssertionError!

assert.deepEqual('+00000000', false);const assert = require('node:assert');
// WARNING: This does not throw an AssertionError!

assert.deepEqual('+00000000', false);copy

"Deep" equality means that the enumerable "own" properties of child objects
are evaluated also:

import assert from 'node:assert';

const obj1 = {
  a: {
    b: 1,
  },
};
const obj2 = {
  a: {
    b: 2,
  },
};
const obj3 = {
  a: {
    b: 1,
  },
};
const obj4 = { __proto__: obj1 };

assert.deepEqual(obj1, obj1);
// OK

// Values of b are different:
assert.deepEqual(obj1, obj2);
// AssertionError: { a: { b: 1 } } deepEqual { a: { b: 2 } }

assert.deepEqual(obj1, obj3);
// OK

// Prototypes are ignored:
assert.deepEqual(obj1, obj4);
// AssertionError: { a: { b: 1 } } deepEqual {}const assert = require('node:assert');

const obj1 = {
  a: {
    b: 1,
  },
};
const obj2 = {
  a: {
    b: 2,
  },
};
const obj3 = {
  a: {
    b: 1,
  },
};
const obj4 = { __proto__: obj1 };

assert.deepEqual(obj1, obj1);
// OK

// Values of b are different:
assert.deepEqual(obj1, obj2);
// AssertionError: { a: { b: 1 } } deepEqual { a: { b: 2 } }

assert.deepEqual(obj1, obj3);
// OK

// Prototypes are ignored:
assert.deepEqual(obj1, obj4);
// AssertionError: { a: { b: 1 } } deepEqual {}copy

If the values are not equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message`
property set equal to the value of the `message` parameter. If the `message`
parameter is undefined, a default error message is assigned. If the `message`
parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
[`AssertionError`](#class-assertassertionerror).

### `assert.deepStrictEqual(actual, expected[, message])`[#](#assertdeepstrictequalactual-expected-message)

History

VersionChanges
v25.0.0

Promises are not considered equal anymore if they are not of the same instance.

v25.0.0

Invalid dates are now considered equal.

v24.0.0

Recursion now stops when either side encounters a circular reference.

v22.2.0, v20.15.0

Error cause and errors properties are now compared as well.

v18.0.0

Regular expressions lastIndex property is now compared as well.

v9.0.0

Enumerable symbol properties are now compared.

v9.0.0

The `NaN` is now compared using the [SameValueZero](https://tc39.github.io/ecma262/#sec-samevaluezero) comparison.

v8.5.0

The `Error` names and messages are now properly compared.

v8.0.0

The `Set` and `Map` content is also compared.

v6.1.0

Objects with circular references can be used as inputs now.

v6.4.0, v4.7.1

Typed array slices are handled correctly now.

v5.10.1, v4.4.3

Handle non-`Uint8Array` typed arrays correctly.

v1.2.0

Added in: v1.2.0

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests for deep equality between the `actual` and `expected` parameters.
"Deep" equality means that the enumerable "own" properties of child objects
are recursively evaluated also by the following rules.

#### Comparison details[#](#comparison-details_1)

- Primitive values are compared using [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).

- [Type tags](https://tc39.github.io/ecma262/#sec-object.prototype.tostring) of objects should be the same.

- [`[[Prototype]]`](https://tc39.github.io/ecma262/#sec-ordinary-object-internal-methods-and-internal-slots) of objects are compared using
the [`===` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Strict_equality).

- Only [enumerable "own" properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Enumerability_and_ownership_of_properties) are considered.

- [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) names, messages, causes, and errors are always compared,
even if these are not enumerable properties.
`errors` is also compared.

- Enumerable own [<Symbol>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) properties are compared as well.

- [Object wrappers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures#primitive_values) are compared both as objects and unwrapped values.

- `Object` properties are compared unordered.

- [<Map>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) keys and [<Set>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) items are compared unordered.

- Recursion stops when both sides differ or either side encounters a circular
reference.

- [<WeakMap>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap), [<WeakSet>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet) and [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) instances are **not** compared
structurally. They are only equal if they reference the same object. Any
comparison between different `WeakMap`, `WeakSet`, or `Promise` instances
will result in inequality, even if they contain the same content.

- [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) lastIndex, flags, and source are always compared, even if these
are not enumerable properties.

import assert from 'node:assert/strict';

// This fails because 1 !== '1'.
assert.deepStrictEqual({ a: 1 }, { a: '1' });
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
//   {
// +   a: 1
// -   a: '1'
//   }

// The following objects don't have own properties
const date = new Date();
const object = {};
const fakeDate = {};
Object.setPrototypeOf(fakeDate, Date.prototype);

// Different [[Prototype]]:
assert.deepStrictEqual(object, fakeDate);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + {}
// - Date {}

// Different type tags:
assert.deepStrictEqual(date, fakeDate);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + 2018-04-26T00:49:08.604Z
// - Date {}

assert.deepStrictEqual(NaN, NaN);
// OK because Object.is(NaN, NaN) is true.

// Different unwrapped numbers:
assert.deepStrictEqual(new Number(1), new Number(2));
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + [Number: 1]
// - [Number: 2]

assert.deepStrictEqual(new String('foo'), Object('foo'));
// OK because the object and the string are identical when unwrapped.

assert.deepStrictEqual(-0, -0);
// OK

// Different zeros:
assert.deepStrictEqual(0, -0);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + 0
// - -0

const symbol1 = Symbol();
const symbol2 = Symbol();
assert.deepStrictEqual({ [symbol1]: 1 }, { [symbol1]: 1 });
// OK, because it is the same symbol on both objects.

assert.deepStrictEqual({ [symbol1]: 1 }, { [symbol2]: 1 });
// AssertionError [ERR_ASSERTION]: Inputs identical but not reference equal:
//
// {
//   Symbol(): 1
// }

const weakMap1 = new WeakMap();
const weakMap2 = new WeakMap();
const obj = {};

weakMap1.set(obj, 'value');
weakMap2.set(obj, 'value');

// Comparing different instances fails, even with same contents
assert.deepStrictEqual(weakMap1, weakMap2);
// AssertionError: Values have same structure but are not reference-equal:
//
// WeakMap {
//   <items unknown>
// }

// Comparing the same instance to itself succeeds
assert.deepStrictEqual(weakMap1, weakMap1);
// OK

const weakSet1 = new WeakSet();
const weakSet2 = new WeakSet();
weakSet1.add(obj);
weakSet2.add(obj);

// Comparing different instances fails, even with same contents
assert.deepStrictEqual(weakSet1, weakSet2);
// AssertionError: Values have same structure but are not reference-equal:
// + actual - expected
//
// WeakSet {
//   <items unknown>
// }

// Comparing the same instance to itself succeeds
assert.deepStrictEqual(weakSet1, weakSet1);
// OKconst assert = require('node:assert/strict');

// This fails because 1 !== '1'.
assert.deepStrictEqual({ a: 1 }, { a: '1' });
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
//   {
// +   a: 1
// -   a: '1'
//   }

// The following objects don't have own properties
const date = new Date();
const object = {};
const fakeDate = {};
Object.setPrototypeOf(fakeDate, Date.prototype);

// Different [[Prototype]]:
assert.deepStrictEqual(object, fakeDate);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + {}
// - Date {}

// Different type tags:
assert.deepStrictEqual(date, fakeDate);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + 2018-04-26T00:49:08.604Z
// - Date {}

assert.deepStrictEqual(NaN, NaN);
// OK because Object.is(NaN, NaN) is true.

// Different unwrapped numbers:
assert.deepStrictEqual(new Number(1), new Number(2));
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + [Number: 1]
// - [Number: 2]

assert.deepStrictEqual(new String('foo'), Object('foo'));
// OK because the object and the string are identical when unwrapped.

assert.deepStrictEqual(-0, -0);
// OK

// Different zeros:
assert.deepStrictEqual(0, -0);
// AssertionError: Expected inputs to be strictly deep-equal:
// + actual - expected
//
// + 0
// - -0

const symbol1 = Symbol();
const symbol2 = Symbol();
assert.deepStrictEqual({ [symbol1]: 1 }, { [symbol1]: 1 });
// OK, because it is the same symbol on both objects.

assert.deepStrictEqual({ [symbol1]: 1 }, { [symbol2]: 1 });
// AssertionError [ERR_ASSERTION]: Inputs identical but not reference equal:
//
// {
//   Symbol(): 1
// }

const weakMap1 = new WeakMap();
const weakMap2 = new WeakMap();
const obj = {};

weakMap1.set(obj, 'value');
weakMap2.set(obj, 'value');

// Comparing different instances fails, even with same contents
assert.deepStrictEqual(weakMap1, weakMap2);
// AssertionError: Values have same structure but are not reference-equal:
//
// WeakMap {
//   <items unknown>
// }

// Comparing the same instance to itself succeeds
assert.deepStrictEqual(weakMap1, weakMap1);
// OK

const weakSet1 = new WeakSet();
const weakSet2 = new WeakSet();
weakSet1.add(obj);
weakSet2.add(obj);

// Comparing different instances fails, even with same contents
assert.deepStrictEqual(weakSet1, weakSet2);
// AssertionError: Values have same structure but are not reference-equal:
// + actual - expected
//
// WeakSet {
//   <items unknown>
// }

// Comparing the same instance to itself succeeds
assert.deepStrictEqual(weakSet1, weakSet1);
// OKcopy

If the values are not equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message`
property set equal to the value of the `message` parameter. If the `message`
parameter is undefined, a default error message is assigned. If the `message`
parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
`AssertionError`.

### `assert.doesNotMatch(string, regexp[, message])`[#](#assertdoesnotmatchstring-regexp-message)

History

VersionChanges
v16.0.0

This API is no longer experimental.

v13.6.0, v12.16.0

Added in: v13.6.0, v12.16.0

- `string` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

- `regexp` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Expects the `string` input not to match the regular expression.

import assert from 'node:assert/strict';

assert.doesNotMatch('I will fail', /fail/);
// AssertionError [ERR_ASSERTION]: The input was expected to not match the ...

assert.doesNotMatch(123, /pass/);
// AssertionError [ERR_ASSERTION]: The "string" argument must be of type string.

assert.doesNotMatch('I will pass', /different/);
// OKconst assert = require('node:assert/strict');

assert.doesNotMatch('I will fail', /fail/);
// AssertionError [ERR_ASSERTION]: The input was expected to not match the ...

assert.doesNotMatch(123, /pass/);
// AssertionError [ERR_ASSERTION]: The "string" argument must be of type string.

assert.doesNotMatch('I will pass', /different/);
// OKcopy

If the values do match, or if the `string` argument is of another type than
`string`, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message` property set equal
to the value of the `message` parameter. If the `message` parameter is
undefined, a default error message is assigned. If the `message` parameter is an
instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
[`AssertionError`](#class-assertassertionerror).

### `assert.doesNotReject(asyncFn[, error][, message])`[#](#assertdoesnotrejectasyncfn-error-message)

Added in: v10.0.0

- `asyncFn` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) | [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

- `error` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) | [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

- Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Awaits the `asyncFn` promise or, if `asyncFn` is a function, immediately
calls the function and awaits the returned promise to complete. It will then
check that the promise is not rejected.

If `asyncFn` is a function and it throws an error synchronously,
`assert.doesNotReject()` will return a rejected `Promise` with that error. If
the function does not return a promise, `assert.doesNotReject()` will return a
rejected `Promise` with an [`ERR_INVALID_RETURN_VALUE`](errors.html#err_invalid_return_value) error. In both cases
the error handler is skipped.

Using `assert.doesNotReject()` is actually not useful because there is little
benefit in catching a rejection and then rejecting it again. Instead, consider
adding a comment next to the specific code path that should not reject and keep
error messages as expressive as possible.

If specified, `error` can be a [`Class`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) or a validation
function. See [`assert.throws()`](#assertthrowsfn-error-message) for more details.

Besides the async nature to await the completion behaves identically to
[`assert.doesNotThrow()`](#assertdoesnotthrowfn-error-message).

import assert from 'node:assert/strict';

await assert.doesNotReject(
  async () => {
    throw new TypeError('Wrong value');
  },
  SyntaxError,
);const assert = require('node:assert/strict');

(async () => {
  await assert.doesNotReject(
    async () => {
      throw new TypeError('Wrong value');
    },
    SyntaxError,
  );
})();copy

import assert from 'node:assert/strict';

assert.doesNotReject(Promise.reject(new TypeError('Wrong value')))
  .then(() => {
    // ...
  });const assert = require('node:assert/strict');

assert.doesNotReject(Promise.reject(new TypeError('Wrong value')))
  .then(() => {
    // ...
  });copy

### `assert.doesNotThrow(fn[, error][, message])`[#](#assertdoesnotthrowfn-error-message)

History

VersionChanges
v5.11.0, v4.4.5

The `message` parameter is respected now.

v4.2.0

The `error` parameter can now be an arrow function.

v0.1.21

Added in: v0.1.21

- `fn` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

- `error` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) | [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

Asserts that the function `fn` does not throw an error.

Using `assert.doesNotThrow()` is actually not useful because there
is no benefit in catching an error and then rethrowing it. Instead, consider
adding a comment next to the specific code path that should not throw and keep
error messages as expressive as possible.

When `assert.doesNotThrow()` is called, it will immediately call the `fn`
function.

If an error is thrown and it is the same type as that specified by the `error`
parameter, then an [`AssertionError`](#class-assertassertionerror) is thrown. If the error is of a
different type, or if the `error` parameter is undefined, the error is
propagated back to the caller.

If specified, `error` can be a [`Class`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), or a validation
function. See [`assert.throws()`](#assertthrowsfn-error-message) for more details.

The following, for instance, will throw the [<TypeError>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypeError) because there is no
matching error type in the assertion:

import assert from 'node:assert/strict';

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  SyntaxError,
);const assert = require('node:assert/strict');

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  SyntaxError,
);copy

However, the following will result in an [`AssertionError`](#class-assertassertionerror) with the message
'Got unwanted exception...':

import assert from 'node:assert/strict';

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  TypeError,
);const assert = require('node:assert/strict');

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  TypeError,
);copy

If an [`AssertionError`](#class-assertassertionerror) is thrown and a value is provided for the `message`
parameter, the value of `message` will be appended to the [`AssertionError`](#class-assertassertionerror)
message:

import assert from 'node:assert/strict';

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  /Wrong value/,
  'Whoops',
);
// Throws: AssertionError: Got unwanted exception: Whoopsconst assert = require('node:assert/strict');

assert.doesNotThrow(
  () => {
    throw new TypeError('Wrong value');
  },
  /Wrong value/,
  'Whoops',
);
// Throws: AssertionError: Got unwanted exception: Whoopscopy

### `assert.equal(actual, expected[, message])`[#](#assertequalactual-expected-message)

History

VersionChanges
v16.0.0, v14.18.0

In Legacy assertion mode, changed status from Deprecated to Legacy.

v14.0.0

NaN is now treated as being identical if both sides are NaN.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

**Strict assertion mode**

An alias of [`assert.strictEqual()`](#assertstrictequalactual-expected-message).

**Legacy assertion mode**

[Stability: 3](documentation.html#stability-index) - Legacy: Use [`assert.strictEqual()`](#assertstrictequalactual-expected-message) instead.

Tests shallow, coercive equality between the `actual` and `expected` parameters
using the [`==` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality). `NaN` is specially handled
and treated as being identical if both sides are `NaN`.

import assert from 'node:assert';

assert.equal(1, 1);
// OK, 1 == 1
assert.equal(1, '1');
// OK, 1 == '1'
assert.equal(NaN, NaN);
// OK

assert.equal(1, 2);
// AssertionError: 1 == 2
assert.equal({ a: { b: 1 } }, { a: { b: 1 } });
// AssertionError: { a: { b: 1 } } == { a: { b: 1 } }const assert = require('node:assert');

assert.equal(1, 1);
// OK, 1 == 1
assert.equal(1, '1');
// OK, 1 == '1'
assert.equal(NaN, NaN);
// OK

assert.equal(1, 2);
// AssertionError: 1 == 2
assert.equal({ a: { b: 1 } }, { a: { b: 1 } });
// AssertionError: { a: { b: 1 } } == { a: { b: 1 } }copy

If the values are not equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message`
property set equal to the value of the `message` parameter. If the `message`
parameter is undefined, a default error message is assigned. If the `message`
parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
`AssertionError`.

### `assert.fail([message])`[#](#assertfailmessage)

Added in: v0.1.21

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) **Default:** `'Failed'`

Throws an [`AssertionError`](#class-assertassertionerror) with the provided error message or a default
error message. If the `message` parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then
it will be thrown instead of the [`AssertionError`](#class-assertassertionerror).

import assert from 'node:assert/strict';

assert.fail();
// AssertionError [ERR_ASSERTION]: Failed

assert.fail('boom');
// AssertionError [ERR_ASSERTION]: boom

assert.fail(new TypeError('need array'));
// TypeError: need arrayconst assert = require('node:assert/strict');

assert.fail();
// AssertionError [ERR_ASSERTION]: Failed

assert.fail('boom');
// AssertionError [ERR_ASSERTION]: boom

assert.fail(new TypeError('need array'));
// TypeError: need arraycopy

### `assert.ifError(value)`[#](#assertiferrorvalue)

History

VersionChanges
v10.0.0

Instead of throwing the original error it is now wrapped into an [`AssertionError`][] that contains the full stack trace.

v10.0.0

Value may now only be `undefined` or `null`. Before all falsy values were handled the same as `null` and did not throw.

v0.1.97

Added in: v0.1.97

- `value` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

Throws `value` if `value` is not `undefined` or `null`. This is useful when
testing the `error` argument in callbacks. The stack trace contains all frames
from the error passed to `ifError()` including the potential new frames for
`ifError()` itself.

import assert from 'node:assert/strict';

assert.ifError(null);
// OK
assert.ifError(0);
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: 0
assert.ifError('error');
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: 'error'
assert.ifError(new Error());
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: Error

// Create some random error frames.
let err;
(function errorFrame() {
  err = new Error('test error');
})();

(function ifErrorFrame() {
  assert.ifError(err);
})();
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: test error
//     at ifErrorFrame
//     at errorFrameconst assert = require('node:assert/strict');

assert.ifError(null);
// OK
assert.ifError(0);
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: 0
assert.ifError('error');
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: 'error'
assert.ifError(new Error());
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: Error

// Create some random error frames.
let err;
(function errorFrame() {
  err = new Error('test error');
})();

(function ifErrorFrame() {
  assert.ifError(err);
})();
// AssertionError [ERR_ASSERTION]: ifError got unwanted exception: test error
//     at ifErrorFrame
//     at errorFramecopy

### `assert.match(string, regexp[, message])`[#](#assertmatchstring-regexp-message)

History

VersionChanges
v16.0.0

This API is no longer experimental.

v13.6.0, v12.16.0

Added in: v13.6.0, v12.16.0

- `string` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

- `regexp` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Expects the `string` input to match the regular expression.

import assert from 'node:assert/strict';

assert.match('I will fail', /pass/);
// AssertionError [ERR_ASSERTION]: The input did not match the regular ...

assert.match(123, /pass/);
// AssertionError [ERR_ASSERTION]: The "string" argument must be of type string.

assert.match('I will pass', /pass/);
// OKconst assert = require('node:assert/strict');

assert.match('I will fail', /pass/);
// AssertionError [ERR_ASSERTION]: The input did not match the regular ...

assert.match(123, /pass/);
// AssertionError [ERR_ASSERTION]: The "string" argument must be of type string.

assert.match('I will pass', /pass/);
// OKcopy

If the values do not match, or if the `string` argument is of another type than
`string`, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message` property set equal
to the value of the `message` parameter. If the `message` parameter is
undefined, a default error message is assigned. If the `message` parameter is an
instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
[`AssertionError`](#class-assertassertionerror).

### `assert.notDeepEqual(actual, expected[, message])`[#](#assertnotdeepequalactual-expected-message)

History

VersionChanges
v16.0.0, v14.18.0

In Legacy assertion mode, changed status from Deprecated to Legacy.

v14.0.0

NaN is now treated as being identical if both sides are NaN.

v9.0.0

The `Error` names and messages are now properly compared.

v8.0.0

The `Set` and `Map` content is also compared.

v6.4.0, v4.7.1

Typed array slices are handled correctly now.

v6.1.0, v4.5.0

Objects with circular references can be used as inputs now.

v5.10.1, v4.4.3

Handle non-`Uint8Array` typed arrays correctly.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

**Strict assertion mode**

An alias of [`assert.notDeepStrictEqual()`](#assertnotdeepstrictequalactual-expected-message).

**Legacy assertion mode**

[Stability: 3](documentation.html#stability-index) - Legacy: Use [`assert.notDeepStrictEqual()`](#assertnotdeepstrictequalactual-expected-message) instead.

Tests for any deep inequality. Opposite of [`assert.deepEqual()`](#assertdeepequalactual-expected-message).

import assert from 'node:assert';

const obj1 = {
  a: {
    b: 1,
  },
};
const obj2 = {
  a: {
    b: 2,
  },
};
const obj3 = {
  a: {
    b: 1,
  },
};
const obj4 = { __proto__: obj1 };

assert.notDeepEqual(obj1, obj1);
// AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }

assert.notDeepEqual(obj1, obj2);
// OK

assert.notDeepEqual(obj1, obj3);
// AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }

assert.notDeepEqual(obj1, obj4);
// OKconst assert = require('node:assert');

const obj1 = {
  a: {
    b: 1,
  },
};
const obj2 = {
  a: {
    b: 2,
  },
};
const obj3 = {
  a: {
    b: 1,
  },
};
const obj4 = { __proto__: obj1 };

assert.notDeepEqual(obj1, obj1);
// AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }

assert.notDeepEqual(obj1, obj2);
// OK

assert.notDeepEqual(obj1, obj3);
// AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }

assert.notDeepEqual(obj1, obj4);
// OKcopy

If the values are deeply equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a
`message` property set equal to the value of the `message` parameter. If the
`message` parameter is undefined, a default error message is assigned. If the
`message` parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown
instead of the `AssertionError`.

### `assert.notDeepStrictEqual(actual, expected[, message])`[#](#assertnotdeepstrictequalactual-expected-message)

History

VersionChanges
v9.0.0

The `-0` and `+0` are not considered equal anymore.

v9.0.0

The `NaN` is now compared using the [SameValueZero](https://tc39.github.io/ecma262/#sec-samevaluezero) comparison.

v9.0.0

The `Error` names and messages are now properly compared.

v8.0.0

The `Set` and `Map` content is also compared.

v6.1.0

Objects with circular references can be used as inputs now.

v6.4.0, v4.7.1

Typed array slices are handled correctly now.

v5.10.1, v4.4.3

Handle non-`Uint8Array` typed arrays correctly.

v1.2.0

Added in: v1.2.0

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests for deep strict inequality. Opposite of [`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message).

import assert from 'node:assert/strict';

assert.notDeepStrictEqual({ a: 1 }, { a: '1' });
// OKconst assert = require('node:assert/strict');

assert.notDeepStrictEqual({ a: 1 }, { a: '1' });
// OKcopy

If the values are deeply and strictly equal, an [`AssertionError`](#class-assertassertionerror) is thrown
with a `message` property set equal to the value of the `message` parameter. If
the `message` parameter is undefined, a default error message is assigned. If
the `message` parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown
instead of the [`AssertionError`](#class-assertassertionerror).

### `assert.notEqual(actual, expected[, message])`[#](#assertnotequalactual-expected-message)

History

VersionChanges
v16.0.0, v14.18.0

In Legacy assertion mode, changed status from Deprecated to Legacy.

v14.0.0

NaN is now treated as being identical if both sides are NaN.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

**Strict assertion mode**

An alias of [`assert.notStrictEqual()`](#assertnotstrictequalactual-expected-message).

**Legacy assertion mode**

[Stability: 3](documentation.html#stability-index) - Legacy: Use [`assert.notStrictEqual()`](#assertnotstrictequalactual-expected-message) instead.

Tests shallow, coercive inequality with the [`!=` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Inequality). `NaN` is
specially handled and treated as being identical if both sides are `NaN`.

import assert from 'node:assert';

assert.notEqual(1, 2);
// OK

assert.notEqual(1, 1);
// AssertionError: 1 != 1

assert.notEqual(1, '1');
// AssertionError: 1 != '1'const assert = require('node:assert');

assert.notEqual(1, 2);
// OK

assert.notEqual(1, 1);
// AssertionError: 1 != 1

assert.notEqual(1, '1');
// AssertionError: 1 != '1'copy

If the values are equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message`
property set equal to the value of the `message` parameter. If the `message`
parameter is undefined, a default error message is assigned. If the `message`
parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
`AssertionError`.

### `assert.notStrictEqual(actual, expected[, message])`[#](#assertnotstrictequalactual-expected-message)

History

VersionChanges
v10.0.0

Used comparison changed from Strict Equality to `Object.is()`.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests strict inequality between the `actual` and `expected` parameters as
determined by [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).

import assert from 'node:assert/strict';

assert.notStrictEqual(1, 2);
// OK

assert.notStrictEqual(1, 1);
// AssertionError [ERR_ASSERTION]: Expected "actual" to be strictly unequal to:
//
// 1

assert.notStrictEqual(1, '1');
// OKconst assert = require('node:assert/strict');

assert.notStrictEqual(1, 2);
// OK

assert.notStrictEqual(1, 1);
// AssertionError [ERR_ASSERTION]: Expected "actual" to be strictly unequal to:
//
// 1

assert.notStrictEqual(1, '1');
// OKcopy

If the values are strictly equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a
`message` property set equal to the value of the `message` parameter. If the
`message` parameter is undefined, a default error message is assigned. If the
`message` parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown
instead of the `AssertionError`.

### `assert.ok(value[, message])`[#](#assertokvalue-message)

History

VersionChanges
v10.0.0

The `assert.ok()` (no arguments) will now use a predefined error message.

v0.1.21

Added in: v0.1.21

- `value` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests if `value` is truthy. It is equivalent to
`assert.equal(!!value, true, message)`.

If `value` is not truthy, an [`AssertionError`](#class-assertassertionerror) is thrown with a `message`
property set equal to the value of the `message` parameter. If the `message`
parameter is `undefined`, a default error message is assigned. If the `message`
parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown instead of the
`AssertionError`.
If no arguments are passed in at all `message` will be set to the string:
`'No value argument passed to `assert.ok()`'`.

Be aware that in the `repl` the error message will be different to the one
thrown in a file! See below for further details.

import assert from 'node:assert/strict';

assert.ok(true);
// OK
assert.ok(1);
// OK

assert.ok();
// AssertionError: No value argument passed to `assert.ok()`

assert.ok(false, 'it\'s false');
// AssertionError: it's false

// In the repl:
assert.ok(typeof 123 === 'string');
// AssertionError: false == true

// In a file (e.g. test.js):
assert.ok(typeof 123 === 'string');
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(typeof 123 === 'string')

assert.ok(false);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(false)

assert.ok(0);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(0) copy

const assert = require('node:assert/strict');

assert.ok(true);
// OK
assert.ok(1);
// OK

assert.ok();
// AssertionError: No value argument passed to `assert.ok()`

assert.ok(false, 'it\'s false');
// AssertionError: it's false

// In the repl:
assert.ok(typeof 123 === 'string');
// AssertionError: false == true

// In a file (e.g. test.js):
assert.ok(typeof 123 === 'string');
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(typeof 123 === 'string')

assert.ok(false);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(false)

assert.ok(0);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert.ok(0)import assert from 'node:assert/strict';

// Using `assert()` works the same:
assert(2 + 2 > 5);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert(2 + 2 > 5)copy

const assert = require('node:assert');

// Using `assert()` works the same:
assert(2 + 2 > 5);
// AssertionError: The expression evaluated to a falsy value:
//
//   assert(2 + 2 > 5) copy

### `assert.rejects(asyncFn[, error][, message])`[#](#assertrejectsasyncfn-error-message)

Added in: v10.0.0

- `asyncFn` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) | [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

- `error` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) | [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) | [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

- Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Awaits the `asyncFn` promise or, if `asyncFn` is a function, immediately
calls the function and awaits the returned promise to complete. It will then
check that the promise is rejected.

If `asyncFn` is a function and it throws an error synchronously,
`assert.rejects()` will return a rejected `Promise` with that error. If the
function does not return a promise, `assert.rejects()` will return a rejected
`Promise` with an [`ERR_INVALID_RETURN_VALUE`](errors.html#err_invalid_return_value) error. In both cases the error
handler is skipped.

Besides the async nature to await the completion behaves identically to
[`assert.throws()`](#assertthrowsfn-error-message).

If specified, `error` can be a [`Class`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), a validation function,
an object where each property will be tested for, or an instance of error where
each property will be tested for including the non-enumerable `message` and
`name` properties.

If specified, `message` will be the message provided by the [`AssertionError`](#class-assertassertionerror)
if the `asyncFn` fails to reject.

import assert from 'node:assert/strict';

await assert.rejects(
  async () => {
    throw new TypeError('Wrong value');
  },
  {
    name: 'TypeError',
    message: 'Wrong value',
  },
);const assert = require('node:assert/strict');

(async () => {
  await assert.rejects(
    async () => {
      throw new TypeError('Wrong value');
    },
    {
      name: 'TypeError',
      message: 'Wrong value',
    },
  );
})();copy

import assert from 'node:assert/strict';

await assert.rejects(
  async () => {
    throw new TypeError('Wrong value');
  },
  (err) => {
    assert.strictEqual(err.name, 'TypeError');
    assert.strictEqual(err.message, 'Wrong value');
    return true;
  },
);const assert = require('node:assert/strict');

(async () => {
  await assert.rejects(
    async () => {
      throw new TypeError('Wrong value');
    },
    (err) => {
      assert.strictEqual(err.name, 'TypeError');
      assert.strictEqual(err.message, 'Wrong value');
      return true;
    },
  );
})();copy

import assert from 'node:assert/strict';

assert.rejects(
  Promise.reject(new Error('Wrong value')),
  Error,
).then(() => {
  // ...
});const assert = require('node:assert/strict');

assert.rejects(
  Promise.reject(new Error('Wrong value')),
  Error,
).then(() => {
  // ...
});copy

`error` cannot be a string. If a string is provided as the second
argument, then `error` is assumed to be omitted and the string will be used for
`message` instead. This can lead to easy-to-miss mistakes. Please read the
example in [`assert.throws()`](#assertthrowsfn-error-message) carefully if using a string as the second
argument gets considered.

### `assert.strictEqual(actual, expected[, message])`[#](#assertstrictequalactual-expected-message)

History

VersionChanges
v10.0.0

Used comparison changed from Strict Equality to `Object.is()`.

v0.1.21

Added in: v0.1.21

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests strict equality between the `actual` and `expected` parameters as
determined by [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).

import assert from 'node:assert/strict';

assert.strictEqual(1, 2);
// AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
//
// 1 !== 2

assert.strictEqual(1, 1);
// OK

assert.strictEqual('Hello foobar', 'Hello World!');
// AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
// + actual - expected
//
// + 'Hello foobar'
// - 'Hello World!'
//          ^

const apples = 1;
const oranges = 2;
assert.strictEqual(apples, oranges, `apples ${apples} !== oranges ${oranges}`);
// AssertionError [ERR_ASSERTION]: apples 1 !== oranges 2

assert.strictEqual(1, '1', new TypeError('Inputs are not identical'));
// TypeError: Inputs are not identicalconst assert = require('node:assert/strict');

assert.strictEqual(1, 2);
// AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
//
// 1 !== 2

assert.strictEqual(1, 1);
// OK

assert.strictEqual('Hello foobar', 'Hello World!');
// AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
// + actual - expected
//
// + 'Hello foobar'
// - 'Hello World!'
//          ^

const apples = 1;
const oranges = 2;
assert.strictEqual(apples, oranges, `apples ${apples} !== oranges ${oranges}`);
// AssertionError [ERR_ASSERTION]: apples 1 !== oranges 2

assert.strictEqual(1, '1', new TypeError('Inputs are not identical'));
// TypeError: Inputs are not identicalcopy

If the values are not strictly equal, an [`AssertionError`](#class-assertassertionerror) is thrown with a
`message` property set equal to the value of the `message` parameter. If the
`message` parameter is undefined, a default error message is assigned. If the
`message` parameter is an instance of [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) then it will be thrown
instead of the [`AssertionError`](#class-assertassertionerror).

### `assert.throws(fn[, error][, message])`[#](#assertthrowsfn-error-message)

History

VersionChanges
v10.2.0

The `error` parameter can be an object containing regular expressions now.

v9.9.0

The `error` parameter can now be an object as well.

v4.2.0

The `error` parameter can now be an arrow function.

v0.1.21

Added in: v0.1.21

- `fn` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

- `error` [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) | [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) | [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)

Expects the function `fn` to throw an error.

If specified, `error` can be a [`Class`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp), a validation function,
a validation object where each property will be tested for strict deep equality,
or an instance of error where each property will be tested for strict deep
equality including the non-enumerable `message` and `name` properties. When
using an object, it is also possible to use a regular expression, when
validating against a string property. See below for examples.

If specified, `message` will be appended to the message provided by the
`AssertionError` if the `fn` call fails to throw or in case the error validation
fails.

Custom validation object/error instance:

import assert from 'node:assert/strict';

const err = new TypeError('Wrong value');
err.code = 404;
err.foo = 'bar';
err.info = {
  nested: true,
  baz: 'text',
};
err.reg = /abc/i;

assert.throws(
  () => {
    throw err;
  },
  {
    name: 'TypeError',
    message: 'Wrong value',
    info: {
      nested: true,
      baz: 'text',
    },
    // Only properties on the validation object will be tested for.
    // Using nested objects requires all properties to be present. Otherwise
    // the validation is going to fail.
  },
);

// Using regular expressions to validate error properties:
assert.throws(
  () => {
    throw err;
  },
  {
    // The `name` and `message` properties are strings and using regular
    // expressions on those will match against the string. If they fail, an
    // error is thrown.
    name: /^TypeError$/,
    message: /Wrong/,
    foo: 'bar',
    info: {
      nested: true,
      // It is not possible to use regular expressions for nested properties!
      baz: 'text',
    },
    // The `reg` property contains a regular expression and only if the
    // validation object contains an identical regular expression, it is going
    // to pass.
    reg: /abc/i,
  },
);

// Fails due to the different `message` and `name` properties:
assert.throws(
  () => {
    const otherErr = new Error('Not found');
    // Copy all enumerable properties from `err` to `otherErr`.
    for (const [key, value] of Object.entries(err)) {
      otherErr[key] = value;
    }
    throw otherErr;
  },
  // The error's `message` and `name` properties will also be checked when using
  // an error as validation object.
  err,
);const assert = require('node:assert/strict');

const err = new TypeError('Wrong value');
err.code = 404;
err.foo = 'bar';
err.info = {
  nested: true,
  baz: 'text',
};
err.reg = /abc/i;

assert.throws(
  () => {
    throw err;
  },
  {
    name: 'TypeError',
    message: 'Wrong value',
    info: {
      nested: true,
      baz: 'text',
    },
    // Only properties on the validation object will be tested for.
    // Using nested objects requires all properties to be present. Otherwise
    // the validation is going to fail.
  },
);

// Using regular expressions to validate error properties:
assert.throws(
  () => {
    throw err;
  },
  {
    // The `name` and `message` properties are strings and using regular
    // expressions on those will match against the string. If they fail, an
    // error is thrown.
    name: /^TypeError$/,
    message: /Wrong/,
    foo: 'bar',
    info: {
      nested: true,
      // It is not possible to use regular expressions for nested properties!
      baz: 'text',
    },
    // The `reg` property contains a regular expression and only if the
    // validation object contains an identical regular expression, it is going
    // to pass.
    reg: /abc/i,
  },
);

// Fails due to the different `message` and `name` properties:
assert.throws(
  () => {
    const otherErr = new Error('Not found');
    // Copy all enumerable properties from `err` to `otherErr`.
    for (const [key, value] of Object.entries(err)) {
      otherErr[key] = value;
    }
    throw otherErr;
  },
  // The error's `message` and `name` properties will also be checked when using
  // an error as validation object.
  err,
);copy

Validate instanceof using constructor:

import assert from 'node:assert/strict';

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  Error,
);const assert = require('node:assert/strict');

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  Error,
);copy

Validate error message using [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp):

Using a regular expression runs `.toString` on the error object, and will
therefore also include the error name.

import assert from 'node:assert/strict';

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  /^Error: Wrong value$/,
);const assert = require('node:assert/strict');

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  /^Error: Wrong value$/,
);copy

Custom error validation:

The function must return `true` to indicate all internal validations passed.
It will otherwise fail with an [`AssertionError`](#class-assertassertionerror).

import assert from 'node:assert/strict';

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  (err) => {
    assert(err instanceof Error);
    assert(/value/.test(err));
    // Avoid returning anything from validation functions besides `true`.
    // Otherwise, it's not clear what part of the validation failed. Instead,
    // throw an error about the specific validation that failed (as done in this
    // example) and add as much helpful debugging information to that error as
    // possible.
    return true;
  },
  'unexpected error',
);const assert = require('node:assert/strict');

assert.throws(
  () => {
    throw new Error('Wrong value');
  },
  (err) => {
    assert(err instanceof Error);
    assert(/value/.test(err));
    // Avoid returning anything from validation functions besides `true`.
    // Otherwise, it's not clear what part of the validation failed. Instead,
    // throw an error about the specific validation that failed (as done in this
    // example) and add as much helpful debugging information to that error as
    // possible.
    return true;
  },
  'unexpected error',
);copy

`error` cannot be a string. If a string is provided as the second
argument, then `error` is assumed to be omitted and the string will be used for
`message` instead. This can lead to easy-to-miss mistakes. Using the same
message as the thrown error message is going to result in an
`ERR_AMBIGUOUS_ARGUMENT` error. Please read the example below carefully if using
a string as the second argument gets considered:

import assert from 'node:assert/strict';

function throwingFirst() {
  throw new Error('First');
}

function throwingSecond() {
  throw new Error('Second');
}

function notThrowing() {}

// The second argument is a string and the input function threw an Error.
// The first case will not throw as it does not match for the error message
// thrown by the input function!
assert.throws(throwingFirst, 'Second');
// In the next example the message has no benefit over the message from the
// error and since it is not clear if the user intended to actually match
// against the error message, Node.js throws an `ERR_AMBIGUOUS_ARGUMENT` error.
assert.throws(throwingSecond, 'Second');
// TypeError [ERR_AMBIGUOUS_ARGUMENT]

// The string is only used (as message) in case the function does not throw:
assert.throws(notThrowing, 'Second');
// AssertionError [ERR_ASSERTION]: Missing expected exception: Second

// If it was intended to match for the error message do this instead:
// It does not throw because the error messages match.
assert.throws(throwingSecond, /Second$/);

// If the error message does not match, an AssertionError is thrown.
assert.throws(throwingFirst, /Second$/);
// AssertionError [ERR_ASSERTION]const assert = require('node:assert/strict');

function throwingFirst() {
  throw new Error('First');
}

function throwingSecond() {
  throw new Error('Second');
}

function notThrowing() {}

// The second argument is a string and the input function threw an Error.
// The first case will not throw as it does not match for the error message
// thrown by the input function!
assert.throws(throwingFirst, 'Second');
// In the next example the message has no benefit over the message from the
// error and since it is not clear if the user intended to actually match
// against the error message, Node.js throws an `ERR_AMBIGUOUS_ARGUMENT` error.
assert.throws(throwingSecond, 'Second');
// TypeError [ERR_AMBIGUOUS_ARGUMENT]

// The string is only used (as message) in case the function does not throw:
assert.throws(notThrowing, 'Second');
// AssertionError [ERR_ASSERTION]: Missing expected exception: Second

// If it was intended to match for the error message do this instead:
// It does not throw because the error messages match.
assert.throws(throwingSecond, /Second$/);

// If the error message does not match, an AssertionError is thrown.
assert.throws(throwingFirst, /Second$/);
// AssertionError [ERR_ASSERTION]copy

Due to the confusing error-prone notation, avoid a string as the second
argument.

### `assert.partialDeepStrictEqual(actual, expected[, message])`[#](#assertpartialdeepstrictequalactual-expected-message)

History

VersionChanges
v25.0.0

Promises are not considered equal anymore if they are not of the same instance.

v25.0.0

Invalid dates are now considered equal.

v24.0.0, v22.17.0

partialDeepStrictEqual is now Stable. Previously, it had been Experimental.

v23.4.0, v22.13.0

Added in: v23.4.0, v22.13.0

- `actual` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `expected` [<any>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Data_types)

- `message` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type) | [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)

Tests for partial deep equality between the `actual` and `expected` parameters.
"Deep" equality means that the enumerable "own" properties of child objects
are recursively evaluated also by the following rules. "Partial" equality means
that only properties that exist on the `expected` parameter are going to be
compared.

This method always passes the same test cases as [`assert.deepStrictEqual()`](#assertdeepstrictequalactual-expected-message),
behaving as a super set of it.

#### Comparison details[#](#comparison-details_2)

- Primitive values are compared using [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).

- [Type tags](https://tc39.github.io/ecma262/#sec-object.prototype.tostring) of objects should be the same.

- [`[[Prototype]]`](https://tc39.github.io/ecma262/#sec-ordinary-object-internal-methods-and-internal-slots) of objects are not compared.

- Only [enumerable "own" properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Enumerability_and_ownership_of_properties) are considered.

- [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) names, messages, causes, and errors are always compared,
even if these are not enumerable properties.
`errors` is also compared.

- Enumerable own [<Symbol>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) properties are compared as well.

- [Object wrappers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures#primitive_values) are compared both as objects and unwrapped values.

- `Object` properties are compared unordered.

- [<Map>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) keys and [<Set>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) items are compared unordered.

- Recursion stops when both sides differ or both sides encounter a circular
reference.

- [<WeakMap>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap), [<WeakSet>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet) and [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) instances are **not** compared
structurally. They are only equal if they reference the same object. Any
comparison between different `WeakMap`, `WeakSet`, or `Promise` instances
will result in inequality, even if they contain the same content.

- [<RegExp>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp) lastIndex, flags, and source are always compared, even if these
are not enumerable properties.

- Holes in sparse arrays are ignored.

import assert from 'node:assert';

assert.partialDeepStrictEqual(
  { a: { b: { c: 1 } } },
  { a: { b: { c: 1 } } },
);
// OK

assert.partialDeepStrictEqual(
  { a: 1, b: 2, c: 3 },
  { b: 2 },
);
// OK

assert.partialDeepStrictEqual(
  [1, 2, 3, 4, 5, 6, 7, 8, 9],
  [4, 5, 8],
);
// OK

assert.partialDeepStrictEqual(
  new Set([{ a: 1 }, { b: 1 }]),
  new Set([{ a: 1 }]),
);
// OK

assert.partialDeepStrictEqual(
  new Map([['key1', 'value1'], ['key2', 'value2']]),
  new Map([['key2', 'value2']]),
);
// OK

assert.partialDeepStrictEqual(123n, 123n);
// OK

assert.partialDeepStrictEqual(
  [1, 2, 3, 4, 5, 6, 7, 8, 9],
  [5, 4, 8],
);
// AssertionError

assert.partialDeepStrictEqual(
  { a: 1 },
  { a: 1, b: 2 },
);
// AssertionError

assert.partialDeepStrictEqual(
  { a: { b: 2 } },
  { a: { b: '2' } },
);
// AssertionErrorconst assert = require('node:assert');

assert.partialDeepStrictEqual(
  { a: { b: { c: 1 } } },
  { a: { b: { c: 1 } } },
);
// OK

assert.partialDeepStrictEqual(
  { a: 1, b: 2, c: 3 },
  { b: 2 },
);
// OK

assert.partialDeepStrictEqual(
  [1, 2, 3, 4, 5, 6, 7, 8, 9],
  [4, 5, 8],
);
// OK

assert.partialDeepStrictEqual(
  new Set([{ a: 1 }, { b: 1 }]),
  new Set([{ a: 1 }]),
);
// OK

assert.partialDeepStrictEqual(
  new Map([['key1', 'value1'], ['key2', 'value2']]),
  new Map([['key2', 'value2']]),
);
// OK

assert.partialDeepStrictEqual(123n, 123n);
// OK

assert.partialDeepStrictEqual(
  [1, 2, 3, 4, 5, 6, 7, 8, 9],
  [5, 4, 8],
);
// AssertionError

assert.partialDeepStrictEqual(
  { a: 1 },
  { a: 1, b: 2 },
);
// AssertionError

assert.partialDeepStrictEqual(
  { a: { b: 2 } },
  { a: { b: '2' } },
);
// AssertionErrorcopy
