# Source: https://docs.python.org/3/library/json.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

json â JSON encoder and decoder — Python 3.14.3 documentation
    
    
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
            
            
            
             
            
            

  

    
    
    
        
    

  
    
      
### Navigation

      
        
- 
          [index](../genindex.html)
        
- 
          [modules](../py-modindex.html) |
        
- 
          [next](mailbox.html) |
        
- 
          [previous](email.iterators.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
          
- [Internet Data Handling](netdata.html) »
        
- [`json` â JSON encoder and decoder]()
                
- 
                    

    
        
          
          
        
    
                     |
                
            
- 

    Theme
    
        Auto
        Light
        Dark
    
 |
            
      
        

    
      
        
          
            
  

# `json` â JSON encoder and decoder[Â¶](#module-json)

**Source code:** [Lib/json/__init__.py](https://github.com/python/cpython/tree/3.14/Lib/json/__init__.py)

[JSON (JavaScript Object Notation)](https://json.org), specified by
[**RFC 7159**](https://datatracker.ietf.org/doc/html/rfc7159.html) (which obsoletes [**RFC 4627**](https://datatracker.ietf.org/doc/html/rfc4627.html)) and by
[ECMA-404](https://ecma-international.org/publications-and-standards/standards/ecma-404/),
is a lightweight data interchange format inspired by
[JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax
(although it is not a strict subset of JavaScript [[1]](#rfc-errata) ).

Note

The term âobjectâ in the context of JSON processing in Python can be
ambiguous. All values in Python are objects. In JSON, an object refers to
any data wrapped in curly braces, similar to a Python dictionary.

Warning

Be cautious when parsing JSON data from untrusted sources. A malicious
JSON string may cause the decoder to consume considerable CPU and memory
resources. Limiting the size of data to be parsed is recommended.

This module exposes an API familiar to users of the standard library
[`marshal`](marshal.html#module-marshal) and [`pickle`](pickle.html#module-pickle) modules.

Encoding basic Python object hierarchies:

>>> import json
>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'
>>> print(json.dumps("\"foo\bar"))
"\"foo\bar"
>>> print(json.dumps('\u1234'))
"\u1234"
>>> print(json.dumps('\\'))
"\\"
>>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
{"a": 0, "b": 0, "c": 0}
>>> from io import StringIO
>>> io = StringIO()
>>> json.dump(['streaming API'], io)
>>> io.getvalue()
'["streaming API"]'

Compact encoding:

>>> import json
>>> json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
'[1,2,3,{"4":5,"6":7}]'

Pretty printing:

>>> import json
>>> print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
{
    "4": 5,
    "6": 7
}

Customizing JSON object encoding:

>>> import json
>>> def custom_json(obj):
...     if isinstance(obj, complex):
...         return {'__complex__': True, 'real': obj.real, 'imag': obj.imag}
...     raise TypeError(f'Cannot serialize object of {type(obj)}')
...
>>> json.dumps(1 + 2j, default=custom_json)
'{"__complex__": true, "real": 1.0, "imag": 2.0}'

Decoding JSON:

>>> import json
>>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
['foo', {'bar': ['baz', None, 1.0, 2]}]
>>> json.loads('"\\"foo\\bar"')
'"foo\x08ar'
>>> from io import StringIO
>>> io = StringIO('["streaming API"]')
>>> json.load(io)
['streaming API']

Customizing JSON object decoding:

>>> import json
>>> def as_complex(dct):
...     if '__complex__' in dct:
...         return complex(dct['real'], dct['imag'])
...     return dct
...
>>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
...     object_hook=as_complex)
(1+2j)
>>> import decimal
>>> json.loads('1.1', parse_float=decimal.Decimal)
Decimal('1.1')

Extending [`JSONEncoder`](#json.JSONEncoder):

>>> import json
>>> class ComplexEncoder(json.JSONEncoder):
...     def default(self, obj):
...         if isinstance(obj, complex):
...             return [obj.real, obj.imag]
...         # Let the base class default method raise the TypeError
...         return super().default(obj)
...
>>> json.dumps(2 + 1j, cls=ComplexEncoder)
'[2.0, 1.0]'
>>> ComplexEncoder().encode(2 + 1j)
'[2.0, 1.0]'
>>> list(ComplexEncoder().iterencode(2 + 1j))
['[2.0', ', 1.0', ']']

Using `json` from the shell to validate and pretty-print:

$ echo '{"json":"obj"}' | python -m json
{
    "json": "obj"
}
$ echo '{1.2:3.4}' | python -m json
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

See [Command-line interface](#json-commandline) for detailed documentation.

Note

JSON is a subset of [YAML](https://yaml.org/) 1.2.  The JSON produced by
this moduleâs default settings (in particular, the default *separators*
value) is also a subset of YAML 1.0 and 1.1.  This module can thus also be
used as a YAML serializer.

Note

This moduleâs encoders and decoders preserve input and output order by
default.  Order is only lost if the underlying containers are unordered.

## Basic Usage[Â¶](#basic-usage)

json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)[Â¶](#json.dump)

Serialize *obj* as a JSON formatted stream to *fp* (a `.write()`-supporting
[file-like object](../glossary.html#term-file-like-object)) using this [Python-to-JSON conversion table](#py-to-json-table).

Note

Unlike [`pickle`](pickle.html#module-pickle) and [`marshal`](marshal.html#module-marshal), JSON is not a framed protocol,
so trying to serialize multiple objects with repeated calls to
[`dump()`](#json.dump) using the same *fp* will result in an invalid JSON file.

Parameters:

- 
**obj** ([*object*](functions.html#object)) â The Python object to be serialized.

- 
**fp** ([file-like object](../glossary.html#term-file-like-object)) â The file-like object *obj* will be serialized to.
The `json` module always produces [`str`](stdtypes.html#str) objects,
not [`bytes`](stdtypes.html#bytes) objects,
therefore `fp.write()` must support [`str`](stdtypes.html#str) input.

- 
**skipkeys** ([*bool*](functions.html#bool)) â If `True`, keys that are not of a basic type
([`str`](stdtypes.html#str), [`int`](functions.html#int), [`float`](functions.html#float), [`bool`](functions.html#bool), `None`)
will be skipped instead of raising a [`TypeError`](exceptions.html#TypeError).
Default `False`.

- 
**ensure_ascii** ([*bool*](functions.html#bool)) â If `True` (the default), the output is guaranteed to
have all incoming non-ASCII and non-printable characters escaped.
If `False`, all characters will be outputted as-is, except for
the characters that must be escaped: quotation mark, reverse solidus,
and the control characters U+0000 through U+001F.

- 
**check_circular** ([*bool*](functions.html#bool)) â If `False`, the circular reference check for container types is skipped
and a circular reference will result in a [`RecursionError`](exceptions.html#RecursionError) (or worse).
Default `True`.

- 
**allow_nan** ([*bool*](functions.html#bool)) â If `False`, serialization of out-of-range [`float`](functions.html#float) values
(`nan`, `inf`, `-inf`) will result in a [`ValueError`](exceptions.html#ValueError),
in strict compliance with the JSON specification.
If `True` (the default), their JavaScript equivalents
(`NaN`, `Infinity`, `-Infinity`) are used.

- 
**cls** (a [`JSONEncoder`](#json.JSONEncoder) subclass) â If set, a custom JSON encoder with the
[`default()`](#json.JSONEncoder.default) method overridden,
for serializing into custom datatypes.
If `None` (the default), `JSONEncoder` is used.

- 
**indent** ([*int*](functions.html#int)* | *[*str*](stdtypes.html#str)* | **None*) â If a positive integer or string, JSON array elements and
object members will be pretty-printed with that indent level.
A positive integer indents that many spaces per level;
a string (such as `"\t"`) is used to indent each level.
If zero, negative, or `""` (the empty string),
only newlines are inserted.
If `None` (the default), the most compact representation is used.

- 
**separators** ([*tuple*](stdtypes.html#tuple)* | **None*) â A two-tuple: `(item_separator, key_separator)`.
If `None` (the default), *separators* defaults to
`(', ', ': ')` if *indent* is `None`,
and `(',', ': ')` otherwise.
For the most compact JSON,
specify `(',', ':')` to eliminate whitespace.

- 
**default** ([callable](../glossary.html#term-callable) | None) â A function that is called for objects that canât otherwise be serialized.
It should return a JSON encodable version of the object
or raise a [`TypeError`](exceptions.html#TypeError).
If `None` (the default), `TypeError` is raised.

- 
**sort_keys** ([*bool*](functions.html#bool)) â If `True`, dictionaries will be outputted sorted by key.
Default `False`.

Changed in version 3.2: Allow strings for *indent* in addition to integers.

Changed in version 3.4: Use `(',', ': ')` as default if *indent* is not `None`.

Changed in version 3.6: All optional parameters are now [keyword-only](../glossary.html#keyword-only-parameter).

json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)[Â¶](#json.dumps)

Serialize *obj* to a JSON formatted [`str`](stdtypes.html#str) using this conversion
table.  The arguments have the same meaning as in
[`dump()`](#json.dump).

Note

Keys in key/value pairs of JSON are always of the type [`str`](stdtypes.html#str). When
a dictionary is converted into JSON, all the keys of the dictionary are
coerced to strings. As a result of this, if a dictionary is converted
into JSON and then back into a dictionary, the dictionary may not equal
the original one. That is, `loads(dumps(x)) != x` if x has non-string
keys.

json.load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)[Â¶](#json.load)

Deserialize *fp* to a Python object
using the [JSON-to-Python conversion table](#json-to-py-table).

Parameters:

- 
**fp** ([file-like object](../glossary.html#term-file-like-object)) â A `.read()`-supporting [text file](../glossary.html#term-text-file) or [binary file](../glossary.html#term-binary-file)
containing the JSON document to be deserialized.

- 
**cls** (a [`JSONDecoder`](#json.JSONDecoder) subclass) â If set, a custom JSON decoder.
Additional keyword arguments to `load()`
will be passed to the constructor of *cls*.
If `None` (the default), `JSONDecoder` is used.

- 
**object_hook** ([callable](../glossary.html#term-callable) | None) â If set, a function that is called with the result of
any JSON object literal decoded (a [`dict`](stdtypes.html#dict)).
The return value of this function will be used
instead of the [`dict`](stdtypes.html#dict).
This feature can be used to implement custom decoders,
for example [JSON-RPC](https://www.jsonrpc.org) class hinting.
Default `None`.

- 
**object_pairs_hook** ([callable](../glossary.html#term-callable) | None) â If set, a function that is called with the result of
any JSON object literal decoded with an ordered list of pairs.
The return value of this function will be used
instead of the [`dict`](stdtypes.html#dict).
This feature can be used to implement custom decoders.
If *object_hook* is also set, *object_pairs_hook* takes priority.
Default `None`.

- 
**parse_float** ([callable](../glossary.html#term-callable) | None) â If set, a function that is called with
the string of every JSON float to be decoded.
If `None` (the default), it is equivalent to `float(num_str)`.
This can be used to parse JSON floats into custom datatypes,
for example [`decimal.Decimal`](decimal.html#decimal.Decimal).

- 
**parse_int** ([callable](../glossary.html#term-callable) | None) â If set, a function that is called with
the string of every JSON int to be decoded.
If `None` (the default), it is equivalent to `int(num_str)`.
This can be used to parse JSON integers into custom datatypes,
for example [`float`](functions.html#float).

- 
**parse_constant** ([callable](../glossary.html#term-callable) | None) â If set, a function that is called with one of the following strings:
`'-Infinity'`, `'Infinity'`, or `'NaN'`.
This can be used to raise an exception
if invalid JSON numbers are encountered.
Default `None`.

Raises:

- 
[**JSONDecodeError**](#json.JSONDecodeError) â When the data being deserialized is not a valid JSON document.

- 
[**UnicodeDecodeError**](exceptions.html#UnicodeDecodeError) â When the data being deserialized does not contain
UTF-8, UTF-16 or UTF-32 encoded data.

Changed in version 3.1: 

- 
Added the optional *object_pairs_hook* parameter.

- 
*parse_constant* doesnât get called on ânullâ, âtrueâ, âfalseâ anymore.

Changed in version 3.6: 

- 
All optional parameters are now [keyword-only](../glossary.html#keyword-only-parameter).

- 
*fp* can now be a [binary file](../glossary.html#term-binary-file).
The input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.11: The default *parse_int* of [`int()`](functions.html#int) now limits the maximum length of
the integer string via the interpreterâs integer string
conversion length limitation to help avoid denial
of service attacks.

json.loads(s, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)[Â¶](#json.loads)

Identical to [`load()`](#json.load), but instead of a file-like object,
deserialize *s* (a [`str`](stdtypes.html#str), [`bytes`](stdtypes.html#bytes) or [`bytearray`](stdtypes.html#bytearray)
instance containing a JSON document) to a Python object using this
[conversion table](#json-to-py-table).

Changed in version 3.6: *s* can now be of type [`bytes`](stdtypes.html#bytes) or [`bytearray`](stdtypes.html#bytearray). The
input encoding should be UTF-8, UTF-16 or UTF-32.

Changed in version 3.9: The keyword argument *encoding* has been removed.

## Encoders and Decoders[Â¶](#encoders-and-decoders)

class json.JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None)[Â¶](#json.JSONDecoder)

Simple JSON decoder.

Performs the following translations in decoding by default:

JSON

Python

object

dict

array

list

string

str

number (int)

int

number (real)

float

true

True

false

False

null

None

It also understands `NaN`, `Infinity`, and `-Infinity` as their
corresponding `float` values, which is outside the JSON spec.

*object_hook* is an optional function that will be called with the result of
every JSON object decoded and its return value will be used in place of the
given [`dict`](stdtypes.html#dict).  This can be used to provide custom deserializations
(e.g. to support [JSON-RPC](https://www.jsonrpc.org) class hinting).

*object_pairs_hook* is an optional function that will be called with the
result of every JSON object decoded with an ordered list of pairs.  The
return value of *object_pairs_hook* will be used instead of the
[`dict`](stdtypes.html#dict).  This feature can be used to implement custom decoders.  If
*object_hook* is also defined, the *object_pairs_hook* takes priority.

Changed in version 3.1: Added support for *object_pairs_hook*.

*parse_float* is an optional function that will be called with the string of
every JSON float to be decoded.  By default, this is equivalent to
`float(num_str)`.  This can be used to use another datatype or parser for
JSON floats (e.g. [`decimal.Decimal`](decimal.html#decimal.Decimal)).

*parse_int* is an optional function that will be called with the string of
every JSON int to be decoded.  By default, this is equivalent to
`int(num_str)`.  This can be used to use another datatype or parser for
JSON integers (e.g. [`float`](functions.html#float)).

*parse_constant* is an optional function that will be called with one of the
following strings: `'-Infinity'`, `'Infinity'`, `'NaN'`.  This can be
used to raise an exception if invalid JSON numbers are encountered.

If *strict* is false (`True` is the default), then control characters
will be allowed inside strings.  Control characters in this context are
those with character codes in the 0â31 range, including `'\t'` (tab),
`'\n'`, `'\r'` and `'\0'`.

If the data being deserialized is not a valid JSON document, a
[`JSONDecodeError`](#json.JSONDecodeError) will be raised.

Changed in version 3.6: All parameters are now [keyword-only](../glossary.html#keyword-only-parameter).

decode(s)[Â¶](#json.JSONDecoder.decode)

Return the Python representation of *s* (a [`str`](stdtypes.html#str) instance
containing a JSON document).

[`JSONDecodeError`](#json.JSONDecodeError) will be raised if the given JSON document is not
valid.

raw_decode(s)[Â¶](#json.JSONDecoder.raw_decode)

Decode a JSON document from *s* (a [`str`](stdtypes.html#str) beginning with a
JSON document) and return a 2-tuple of the Python representation
and the index in *s* where the document ended.

This can be used to decode a JSON document from a string that may have
extraneous data at the end.

class json.JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)[Â¶](#json.JSONEncoder)

Extensible JSON encoder for Python data structures.

Supports the following objects and types by default:

Python

JSON

dict

object

list, tuple

array

str

string

int, float, int- & float-derived Enums

number

True

true

False

false

None

null

Changed in version 3.4: Added support for int- and float-derived Enum classes.

To extend this to recognize other objects, subclass and implement a
[`default()`](#json.JSONEncoder.default) method with another method that returns a serializable object
for `o` if possible, otherwise it should call the superclass implementation
(to raise [`TypeError`](exceptions.html#TypeError)).

If *skipkeys* is false (the default), a [`TypeError`](exceptions.html#TypeError) will be raised when
trying to encode keys that are not [`str`](stdtypes.html#str), [`int`](functions.html#int), [`float`](functions.html#float),
[`bool`](functions.html#bool) or `None`.  If *skipkeys* is true, such items are simply skipped.

If *ensure_ascii* is true (the default), the output is guaranteed to
have all incoming non-ASCII and non-printable characters escaped.
If *ensure_ascii* is false, all characters will be output as-is, except for
the characters that must be escaped: quotation mark, reverse solidus,
and the control characters U+0000 through U+001F.

If *check_circular* is true (the default), then lists, dicts, and custom
encoded objects will be checked for circular references during encoding to
prevent an infinite recursion (which would cause a [`RecursionError`](exceptions.html#RecursionError)).
Otherwise, no such check takes place.

If *allow_nan* is true (the default), then `NaN`, `Infinity`, and
`-Infinity` will be encoded as such.  This behavior is not JSON
specification compliant, but is consistent with most JavaScript based
encoders and decoders.  Otherwise, it will be a [`ValueError`](exceptions.html#ValueError) to encode
such floats.

If *sort_keys* is true (default: `False`), then the output of dictionaries
will be sorted by key; this is useful for regression tests to ensure that
JSON serializations can be compared on a day-to-day basis.

If *indent* is a non-negative integer or string, then JSON array elements and
object members will be pretty-printed with that indent level.  An indent level
of 0, negative, or `""` will only insert newlines.  `None` (the default)
selects the most compact representation. Using a positive integer indent
indents that many spaces per level.  If *indent* is a string (such as `"\t"`),
that string is used to indent each level.

Changed in version 3.2: Allow strings for *indent* in addition to integers.

If specified, *separators* should be an `(item_separator, key_separator)`
tuple.  The default is `(', ', ': ')` if *indent* is `None` and
`(',', ': ')` otherwise.  To get the most compact JSON representation,
you should specify `(',', ':')` to eliminate whitespace.

Changed in version 3.4: Use `(',', ': ')` as default if *indent* is not `None`.

If specified, *default* should be a function that gets called for objects that
canât otherwise be serialized.  It should return a JSON encodable version of
the object or raise a [`TypeError`](exceptions.html#TypeError).  If not specified, [`TypeError`](exceptions.html#TypeError)
is raised.

Changed in version 3.6: All parameters are now [keyword-only](../glossary.html#keyword-only-parameter).

default(o)[Â¶](#json.JSONEncoder.default)

Implement this method in a subclass such that it returns a serializable
object for *o*, or calls the base implementation (to raise a
[`TypeError`](exceptions.html#TypeError)).

For example, to support arbitrary iterators, you could implement
[`default()`](#json.JSONEncoder.default) like this:

def default(self, o):
   try:
       iterable = iter(o)
   except TypeError:
       pass
   else:
       return list(iterable)
   # Let the base class default method raise the TypeError
   return super().default(o)

encode(o)[Â¶](#json.JSONEncoder.encode)

Return a JSON string representation of a Python data structure, *o*.  For
example:

>>> json.JSONEncoder().encode({"foo": ["bar", "baz"]})
'{"foo": ["bar", "baz"]}'

iterencode(o)[Â¶](#json.JSONEncoder.iterencode)

Encode the given object, *o*, and yield each string representation as
available.  For example:

for chunk in json.JSONEncoder().iterencode(bigobject):
    mysocket.write(chunk)

## Exceptions[Â¶](#exceptions)

exception json.JSONDecodeError(msg, doc, pos)[Â¶](#json.JSONDecodeError)

Subclass of [`ValueError`](exceptions.html#ValueError) with the following additional attributes:

msg[Â¶](#json.JSONDecodeError.msg)

The unformatted error message.

doc[Â¶](#json.JSONDecodeError.doc)

The JSON document being parsed.

pos[Â¶](#json.JSONDecodeError.pos)

The start index of *doc* where parsing failed.

lineno[Â¶](#json.JSONDecodeError.lineno)

The line corresponding to *pos*.

colno[Â¶](#json.JSONDecodeError.colno)

The column corresponding to *pos*.

Added in version 3.5.

## Standard Compliance and Interoperability[Â¶](#standard-compliance-and-interoperability)

The JSON format is specified by [**RFC 7159**](https://datatracker.ietf.org/doc/html/rfc7159.html) and by
[ECMA-404](https://ecma-international.org/publications-and-standards/standards/ecma-404/).
This section details this moduleâs level of compliance with the RFC.
For simplicity, [`JSONEncoder`](#json.JSONEncoder) and [`JSONDecoder`](#json.JSONDecoder) subclasses, and
parameters other than those explicitly mentioned, are not considered.

This module does not comply with the RFC in a strict fashion, implementing some
extensions that are valid JavaScript but not valid JSON.  In particular:

- 
Infinite and NaN number values are accepted and output;

- 
Repeated names within an object are accepted, and only the value of the last
name-value pair is used.

Since the RFC permits RFC-compliant parsers to accept input texts that are not
RFC-compliant, this moduleâs deserializer is technically RFC-compliant under
default settings.

### Character Encodings[Â¶](#character-encodings)

The RFC requires that JSON be represented using either UTF-8, UTF-16, or
UTF-32, with UTF-8 being the recommended default for maximum interoperability.

As permitted, though not required, by the RFC, this moduleâs serializer sets
*ensure_ascii=True* by default, thus escaping the output so that the resulting
strings only contain printable ASCII characters.

Other than the *ensure_ascii* parameter, this module is defined strictly in
terms of conversion between Python objects and
[`Unicode strings`](stdtypes.html#str), and thus does not otherwise directly address
the issue of character encodings.

The RFC prohibits adding a byte order mark (BOM) to the start of a JSON text,
and this moduleâs serializer does not add a BOM to its output.
The RFC permits, but does not require, JSON deserializers to ignore an initial
BOM in their input.  This moduleâs deserializer raises a [`ValueError`](exceptions.html#ValueError)
when an initial BOM is present.

The RFC does not explicitly forbid JSON strings which contain byte sequences
that donât correspond to valid Unicode characters (e.g. unpaired UTF-16
surrogates), but it does note that they may cause interoperability problems.
By default, this module accepts and outputs (when present in the original
[`str`](stdtypes.html#str)) code points for such sequences.

### Infinite and NaN Number Values[Â¶](#infinite-and-nan-number-values)

The RFC does not permit the representation of infinite or NaN number values.
Despite that, by default, this module accepts and outputs `Infinity`,
`-Infinity`, and `NaN` as if they were valid JSON number literal values:

>>> # Neither of these calls raises an exception, but the results are not valid JSON
>>> json.dumps(float('-inf'))
'-Infinity'
>>> json.dumps(float('nan'))
'NaN'
>>> # Same when deserializing
>>> json.loads('-Infinity')
-inf
>>> json.loads('NaN')
nan

In the serializer, the *allow_nan* parameter can be used to alter this
behavior.  In the deserializer, the *parse_constant* parameter can be used to
alter this behavior.

### Repeated Names Within an Object[Â¶](#repeated-names-within-an-object)

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name:

>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}

The *object_pairs_hook* parameter can be used to alter this behavior.

### Top-level Non-Object, Non-Array Values[Â¶](#top-level-non-object-non-array-values)

The old version of JSON specified by the obsolete [**RFC 4627**](https://datatracker.ietf.org/doc/html/rfc4627.html) required that
the top-level value of a JSON text must be either a JSON object or array
(Python [`dict`](stdtypes.html#dict) or [`list`](stdtypes.html#list)), and could not be a JSON null,
boolean, number, or string value.  [**RFC 7159**](https://datatracker.ietf.org/doc/html/rfc7159.html) removed that restriction, and
this module does not and has never implemented that restriction in either its
serializer or its deserializer.

Regardless, for maximum interoperability, you may wish to voluntarily adhere
to the restriction yourself.

### Implementation Limitations[Â¶](#implementation-limitations)

Some JSON deserializer implementations may set limits on:

- 
the size of accepted JSON texts

- 
the maximum level of nesting of JSON objects and arrays

- 
the range and precision of JSON numbers

- 
the content and maximum length of JSON strings

This module does not impose any such limits beyond those of the relevant
Python datatypes themselves or the Python interpreter itself.

When serializing to JSON, beware any such limitations in applications that may
consume your JSON.  In particular, it is common for JSON numbers to be
deserialized into IEEE 754 double precision numbers and thus subject to that
representationâs range and precision limitations.  This is especially relevant
when serializing Python [`int`](functions.html#int) values of extremely large magnitude, or
when serializing instances of âexoticâ numerical types such as
[`decimal.Decimal`](decimal.html#decimal.Decimal).

## Command-line interface[Â¶](#module-json.tool)

**Source code:** [Lib/json/tool.py](https://github.com/python/cpython/tree/3.14/Lib/json/tool.py)

The `json` module can be invoked as a script via `python -m json`
to validate and pretty-print JSON objects. The `json.tool` submodule
implements this interface.

If the optional `infile` and `outfile` arguments are not
specified, [`sys.stdin`](sys.html#sys.stdin) and [`sys.stdout`](sys.html#sys.stdout) will be used respectively:

$ echo '{"json": "obj"}' | python -m json
{
    "json": "obj"
}
$ echo '{1.2:3.4}' | python -m json
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

Changed in version 3.5: The output is now in the same order as the input. Use the
[`--sort-keys`](#cmdoption-json-sort-keys) option to sort the output of dictionaries
alphabetically by key.

Changed in version 3.14: The `json` module may now be directly executed as
`python -m json`. For backwards compatibility, invoking
the CLI as `python -m json.tool` remains supported.

### Command-line options[Â¶](#command-line-options)

infile[Â¶](#cmdoption-json-arg-infile)

The JSON file to be validated or pretty-printed:

$ python -m json mp_films.json
[
    {
        "title": "And Now for Something Completely Different",
        "year": 1971
    },
    {
        "title": "Monty Python and the Holy Grail",
        "year": 1975
    }
]

If *infile* is not specified, read from [`sys.stdin`](sys.html#sys.stdin).

outfile[Â¶](#cmdoption-json-arg-outfile)

Write the output of the *infile* to the given *outfile*. Otherwise, write it
to [`sys.stdout`](sys.html#sys.stdout).

--sort-keys[Â¶](#cmdoption-json-sort-keys)

Sort the output of dictionaries alphabetically by key.

Added in version 3.5.

--no-ensure-ascii[Â¶](#cmdoption-json-no-ensure-ascii)

Disable escaping of non-ascii characters, see [`json.dumps()`](#json.dumps) for more information.

Added in version 3.9.

--json-lines[Â¶](#cmdoption-json-json-lines)

Parse every input line as separate JSON object.

Added in version 3.8.

--indent, --tab, --no-indent, --compact[Â¶](#cmdoption-json-indent)

Mutually exclusive options for whitespace control.

Added in version 3.9.

-h, --help[Â¶](#cmdoption-json-h)

Show the help message.

Footnotes

[[1](#id1)]

As noted in [the errata for RFC 7159](https://www.rfc-editor.org/errata_search.php?rfc=7159),
JSON permits literal U+2028 (LINE SEPARATOR) and
U+2029 (PARAGRAPH SEPARATOR) characters in strings, whereas JavaScript
(as of ECMAScript Edition 5.1) does not.

            
          
        
      
      
        
  
    
### [Table of Contents](../contents.html)

    

- [`json` â JSON encoder and decoder](#)

- [Basic Usage](#basic-usage)

- [Encoders and Decoders](#encoders-and-decoders)

- [Exceptions](#exceptions)

- [Standard Compliance and Interoperability](#standard-compliance-and-interoperability)

- [Character Encodings](#character-encodings)

- [Infinite and NaN Number Values](#infinite-and-nan-number-values)

- [Repeated Names Within an Object](#repeated-names-within-an-object)

- [Top-level Non-Object, Non-Array Values](#top-level-non-object-non-array-values)

- [Implementation Limitations](#implementation-limitations)

- [Command-line interface](#module-json.tool)

- [Command-line options](#command-line-options)

  
  
    
#### Previous topic

    
[`email.iterators`: Iterators](email.iterators.html)

  
  
    
#### Next topic

    
[`mailbox` â Manipulate mailboxes in various formats](mailbox.html)

  
  
    
### This page

    
      
- [Report a bug](../bugs.html)
      
- 
        Show source
        
      
      
    
  
        

Â«

      
      
      
    
      
### Navigation

      
        
- 
          [index](../genindex.html)
        
- 
          [modules](../py-modindex.html) |
        
- 
          [next](mailbox.html) |
        
- 
          [previous](email.iterators.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
          
- [Internet Data Handling](netdata.html) »
        
- [`json` â JSON encoder and decoder]()
                
- 
                    

    
        
          
          
        
    
                     |
                
            
- 

    Theme
    
        Auto
        Light
        Dark
    
 |
            
      
      
    
    © [Copyright](../copyright.html) 2001 Python Software Foundation.
    

    This page is licensed under the Python Software Foundation License Version 2.
    

    Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License.
    

    
      See [History and License](/license.html) for more information.

    
    
    

    The Python Software Foundation is a non-profit corporation.
[Please donate.](https://www.python.org/psf/donations/)

    

      Last updated on Feb 16, 2026 (15:42 UTC).
    
      [Found a bug](/bugs.html)?
    
    

    Created using [Sphinx](https://www.sphinx-doc.org/) 8.2.3.
