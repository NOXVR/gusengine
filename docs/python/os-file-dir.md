# Source: https://docs.python.org/3/library/filesys.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

File and Directory Access — Python 3.14.3 documentation
    
    
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
          [next](pathlib.html) |
        
- 
          [previous](operator.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
        
- [File and Directory Access]()
                
- 
                    

    
        
          
          
        
    
                     |
                
            
- 

    Theme
    
        Auto
        Light
        Dark
    
 |
            
      
        

    
      
        
          
            
  

# File and Directory Access[Â¶](#file-and-directory-access)

The modules described in this chapter deal with disk files and directories.  For
example, there are modules for reading the properties of files, manipulating
paths in a portable way, and creating temporary files.  The full list of modules
in this chapter is:

- [`pathlib` â Object-oriented filesystem paths](pathlib.html)

- [Basic use](pathlib.html#basic-use)

- [Exceptions](pathlib.html#exceptions)

- [Pure paths](pathlib.html#pure-paths)

- [General properties](pathlib.html#general-properties)

- [Operators](pathlib.html#operators)

- [Accessing individual parts](pathlib.html#accessing-individual-parts)

- [Methods and properties](pathlib.html#methods-and-properties)

- [Concrete paths](pathlib.html#concrete-paths)

- [Parsing and generating URIs](pathlib.html#parsing-and-generating-uris)

- [Expanding and resolving paths](pathlib.html#expanding-and-resolving-paths)

- [Querying file type and status](pathlib.html#querying-file-type-and-status)

- [Reading and writing files](pathlib.html#reading-and-writing-files)

- [Reading directories](pathlib.html#reading-directories)

- [Creating files and directories](pathlib.html#creating-files-and-directories)

- [Copying, moving and deleting](pathlib.html#copying-moving-and-deleting)

- [Permissions and ownership](pathlib.html#permissions-and-ownership)

- [Pattern language](pathlib.html#pattern-language)

- [Comparison to the `glob` module](pathlib.html#comparison-to-the-glob-module)

- [Comparison to the `os` and `os.path` modules](pathlib.html#comparison-to-the-os-and-os-path-modules)

- [Corresponding tools](pathlib.html#corresponding-tools)

- [Protocols](pathlib.html#module-pathlib.types)

- [`os.path` â Common pathname manipulations](os.path.html)

- [`stat` â Interpreting `stat()` results](stat.html)

- [`filecmp` â File and Directory Comparisons](filecmp.html)

- [The `dircmp` class](filecmp.html#the-dircmp-class)

- [`tempfile` â Generate temporary files and directories](tempfile.html)

- [Examples](tempfile.html#examples)

- [Deprecated functions and variables](tempfile.html#deprecated-functions-and-variables)

- [`glob` â Unix style pathname pattern expansion](glob.html)

- [Examples](glob.html#examples)

- [`fnmatch` â Unix filename pattern matching](fnmatch.html)

- [`linecache` â Random access to text lines](linecache.html)

- [`shutil` â High-level file operations](shutil.html)

- [Directory and files operations](shutil.html#directory-and-files-operations)

- [Platform-dependent efficient copy operations](shutil.html#platform-dependent-efficient-copy-operations)

- [copytree example](shutil.html#copytree-example)

- [rmtree example](shutil.html#rmtree-example)

- [Archiving operations](shutil.html#archiving-operations)

- [Archiving example](shutil.html#archiving-example)

- [Archiving example with *base_dir*](shutil.html#archiving-example-with-base-dir)

- [Querying the size of the output terminal](shutil.html#querying-the-size-of-the-output-terminal)

See also

Module [`os`](os.html#module-os)
Operating system interfaces, including functions to work with files at a
lower level than Python [file objects](../glossary.html#term-file-object).

Module [`io`](io.html#module-io)
Pythonâs built-in I/O library, including both abstract classes and
some concrete classes such as file I/O.

Built-in function [`open()`](functions.html#open)
The standard way to open files for reading and writing with Python.

            
          
        
      
      
        
  
    
#### Previous topic

    
[`operator` â Standard operators as functions](operator.html)

  
  
    
#### Next topic

    
[`pathlib` â Object-oriented filesystem paths](pathlib.html)

  
  
    
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
          [next](pathlib.html) |
        
- 
          [previous](operator.html) |

          
- 
          
- [Python](https://www.python.org/) »
          
- 
            
            
          
          
- 
              
          
    
- 
      [3.14.3 Documentation](../index.html) »
    

          
- [The Python Standard Library](index.html) »
        
- [File and Directory Access]()
                
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
