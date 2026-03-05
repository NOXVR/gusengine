# Source: https://docs.python.org/3/library/glob.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

glob â Unix style pathname pattern expansion — Python 3.14.3 documentation
    
    
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
          [next](fnmatch.html) |
        
- 
          [previous](tempfile.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
          
- [File and Directory Access](filesys.html) »
        
- [`glob` â Unix style pathname pattern expansion]()
                
- 
                    

    
        
          
          
        
    
                     |
                
            
- 

    Theme
    
        Auto
        Light
        Dark
    
 |
            
      
        

    
      
        
          
            
  

# `glob` â Unix style pathname pattern expansion[Â¶](#module-glob)

**Source code:** [Lib/glob.py](https://github.com/python/cpython/tree/3.14/Lib/glob.py)

The `glob` module finds pathnames
using pattern matching rules similar to the Unix shell.
No tilde expansion is done, but `*`, `?`, and character
ranges expressed with `[]` will be correctly matched.  This is done by using
the [`os.scandir()`](os.html#os.scandir) and [`fnmatch.fnmatch()`](fnmatch.html#fnmatch.fnmatch) functions in concert, and
not by actually invoking a subshell.

Note

The pathnames are returned in no particular order.  If you need a specific
order, sort the results.

Files beginning with a dot (`.`) can only be matched by
patterns that also start with a dot,
unlike [`fnmatch.fnmatch()`](fnmatch.html#fnmatch.fnmatch) or [`pathlib.Path.glob()`](pathlib.html#pathlib.Path.glob).
For tilde and shell variable expansion, use [`os.path.expanduser()`](os.path.html#os.path.expanduser) and
[`os.path.expandvars()`](os.path.html#os.path.expandvars).

For a literal match, wrap the meta-characters in brackets.
For example, `'[?]'` matches the character `'?'`.

The `glob` module defines the following functions:

glob.glob(pathname, *, root_dir=None, dir_fd=None, recursive=False, include_hidden=False)[Â¶](#glob.glob)

Return a possibly empty list of path names that match *pathname*, which must be
a string containing a path specification. *pathname* can be either absolute
(like `/usr/src/Python-1.5/Makefile`) or relative (like
`../../Tools/*/*.gif`), and can contain shell-style wildcards. Broken
symlinks are included in the results (as in the shell). Whether or not the
results are sorted depends on the file system.  If a file that satisfies
conditions is removed or added during the call of this function, whether
a path name for that file will be included is unspecified.

If *root_dir* is not `None`, it should be a [path-like object](../glossary.html#term-path-like-object)
specifying the root directory for searching.  It has the same effect on
`glob()` as changing the current directory before calling it.  If
*pathname* is relative, the result will contain paths relative to
*root_dir*.

This function can support [paths relative to directory descriptors](os.html#dir-fd) with the *dir_fd* parameter.

If *recursive* is true, the pattern â`**`â will match any files and zero or
more directories, subdirectories and symbolic links to directories. If the
pattern is followed by an [`os.sep`](os.html#os.sep) or [`os.altsep`](os.html#os.altsep) then files will not
match.

If *include_hidden* is true, â`**`â pattern will match hidden directories.

Raises an [auditing event](sys.html#auditing) `glob.glob` with arguments `pathname`, `recursive`.

Raises an [auditing event](sys.html#auditing) `glob.glob/2` with arguments `pathname`, `recursive`, `root_dir`, `dir_fd`.

Note

Using the â`**`â pattern in large directory trees may consume
an inordinate amount of time.

Note

This function may return duplicate path names if *pathname*
contains multiple â`**`â patterns and *recursive* is true.

Changed in version 3.5: Support for recursive globs using â`**`â.

Changed in version 3.10: Added the *root_dir* and *dir_fd* parameters.

Changed in version 3.11: Added the *include_hidden* parameter.

glob.iglob(pathname, *, root_dir=None, dir_fd=None, recursive=False, include_hidden=False)[Â¶](#glob.iglob)

Return an [iterator](../glossary.html#term-iterator) which yields the same values as [`glob()`](#module-glob)
without actually storing them all simultaneously.

Raises an [auditing event](sys.html#auditing) `glob.glob` with arguments `pathname`, `recursive`.

Raises an [auditing event](sys.html#auditing) `glob.glob/2` with arguments `pathname`, `recursive`, `root_dir`, `dir_fd`.

Note

This function may return duplicate path names if *pathname*
contains multiple â`**`â patterns and *recursive* is true.

Changed in version 3.5: Support for recursive globs using â`**`â.

Changed in version 3.10: Added the *root_dir* and *dir_fd* parameters.

Changed in version 3.11: Added the *include_hidden* parameter.

glob.escape(pathname)[Â¶](#glob.escape)

Escape all special characters (`'?'`, `'*'` and `'['`).
This is useful if you want to match an arbitrary literal string that may
have special characters in it.  Special characters in drive/UNC
sharepoints are not escaped, e.g. on Windows
`escape('//?/c:/Quo vadis?.txt')` returns `'//?/c:/Quo vadis[?].txt'`.

Added in version 3.4.

glob.translate(pathname, *, recursive=False, include_hidden=False, seps=None)[Â¶](#glob.translate)

Convert the given path specification to a regular expression for use with
[`re.match()`](re.html#re.match). The path specification can contain shell-style wildcards.

For example:

>>> import glob, re
>>>
>>> regex = glob.translate('**/*.txt', recursive=True, include_hidden=True)
>>> regex
'(?s:(?:.+/)?[^/]*\\.txt)\\z'
>>> reobj = re.compile(regex)
>>> reobj.match('foo/bar/baz.txt')
<re.Match object; span=(0, 15), match='foo/bar/baz.txt'>

Path separators and segments are meaningful to this function, unlike
[`fnmatch.translate()`](fnmatch.html#fnmatch.translate). By default wildcards do not match path
separators, and `*` pattern segments match precisely one path segment.

If *recursive* is true, the pattern segment â`**`â will match any number
of path segments.

If *include_hidden* is true, wildcards can match path segments that start
with a dot (`.`).

A sequence of path separators may be supplied to the *seps* argument. If
not given, [`os.sep`](os.html#os.sep) and [`altsep`](os.html#os.altsep) (if available) are used.

See also

[`pathlib.PurePath.full_match()`](pathlib.html#pathlib.PurePath.full_match) and [`pathlib.Path.glob()`](pathlib.html#pathlib.Path.glob)
methods, which call this function to implement pattern matching and
globbing.

Added in version 3.13.

## Examples[Â¶](#examples)

Consider a directory containing the following files:
`1.gif`, `2.txt`, `card.gif` and a subdirectory `sub`
which contains only the file `3.txt`.  [`glob()`](#module-glob) will produce
the following results.  Notice how any leading components of the path are
preserved.

>>> import glob
>>> glob.glob('./[0-9].*')
['./1.gif', './2.txt']
>>> glob.glob('*.gif')
['1.gif', 'card.gif']
>>> glob.glob('?.gif')
['1.gif']
>>> glob.glob('**/*.txt', recursive=True)
['2.txt', 'sub/3.txt']
>>> glob.glob('./**/', recursive=True)
['./', './sub/']

If the directory contains files starting with `.` they wonât be matched by
default. For example, consider a directory containing `card.gif` and
`.card.gif`:

>>> import glob
>>> glob.glob('*.gif')
['card.gif']
>>> glob.glob('.c*')
['.card.gif']

See also

The [`fnmatch`](fnmatch.html#module-fnmatch) module offers shell-style filename (not path) expansion.

See also

The [`pathlib`](pathlib.html#module-pathlib) module offers high-level path objects.

            
          
        
      
      
        
  
    
### [Table of Contents](../contents.html)

    

- [`glob` â Unix style pathname pattern expansion](#)

- [Examples](#examples)

  
  
    
#### Previous topic

    
[`tempfile` â Generate temporary files and directories](tempfile.html)

  
  
    
#### Next topic

    
[`fnmatch` â Unix filename pattern matching](fnmatch.html)

  
  
    
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
          [next](fnmatch.html) |
        
- 
          [previous](tempfile.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
          
- [File and Directory Access](filesys.html) »
        
- [`glob` â Unix style pathname pattern expansion]()
                
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
