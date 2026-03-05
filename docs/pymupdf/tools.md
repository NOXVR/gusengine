# Source: https://pymupdf.readthedocs.io/en/latest/tools.html
# Downloaded: 2026-02-16
# This is the OFFICIAL documentation, not a summary.

---

- 
- 
- 
- 
- 
        
- 
        
- 

    
- 
        Tools - PyMuPDF documentation
      
- 
    
- 
    
- 
    
- 
    
- 
    
    

  
    
    
    

  
    Contents
    
      

    
  
  
    Menu
    
      
- 
      
- 
      
- 
    
  
  
    Expand
    
      

    
  
  
    Light mode
    
      
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
    
  
  
    Dark mode
    
      

      

    
  
  
    Auto light/dark, in light mode
    
      

      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
    
  
  
    Auto light/dark, in dark mode
    
      

      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
- 
      
    
  
  
    
      

      

      

      

    
  
  
    
      

      

      

      

      

    
  

[Skip to content](#furo-main-content)

  
    
      
        
      
    
    
      [PyMuPDF  documentation](index.html)
    
    
      
        
          
          
          
          
        
      
      
        
      
    
  
  
    
      
      
  
    
    
  
  
  PyMuPDF  documentation
  

  
  
  

  
About

- [Features Comparison](about.html)

- [PyMuPDF Product Suite](about.html#pymupdf-product-suite)

- [Performance](about.html#performance)

- [License and Copyright](about.html#license-and-copyright)

- [PyMuPDF Layout](pymupdf-layout/index.html)

- [PyMuPDF4LLM](pymupdf4llm/index.html)

- [PyMuPDF Pro](pymupdf-pro/index.html)

User Guide

- [Installation](installation.html)

- [The Basics](the-basics.html)

- [Tutorial](tutorial.html)

- [PyMuPDF, LLM & RAG](rag.html)

- [Resources](resources.html)

How to Guide

- [Opening Files](how-to-open-a-file.html)

- [Converting Files](converting-files.html)

- [OCR - Optical Character Recognition](recipes-ocr.html)

- [Text](recipes-text.html)

- [Images](recipes-images.html)

- [Annotations](recipes-annotations.html)

- [Drawing and Graphics](recipes-drawing-and-graphics.html)

- [Stories](recipes-stories.html)

- [Journalling](recipes-journalling.html)

- [Multiprocessing](recipes-multiprocessing.html)

- [Optional Content Support](recipes-optional-content.html)

- [Low-Level Interfaces](recipes-low-level-interfaces.html)

- [Common Issues and their Solutions](recipes-common-issues-and-their-solutions.html)

API Reference

- [Command line interface](module.html)

- [Classes](classes.html)

- [Annot](annot.html)

- [Archive](archive-class.html)

- [Colorspace](colorspace.html)

- [DisplayList](displaylist.html)

- [Document](document.html)

- [DocumentWriter](document-writer-class.html)

- [Font](font.html)

- [Identity](identity.html)

- [IRect](irect.html)

- [Link](link.html)

- [linkDest](linkdest.html)

- [Matrix](matrix.html)

- [Outline](outline.html)

- [Page](page.html)

- [Pixmap](pixmap.html)

- [Point](point.html)

- [Quad](quad.html)

- [Rect](rect.html)

- [Shape](shape.html)

- [Story](story-class.html)

- [TextPage](textpage.html)

- [TextWriter](textwriter.html)

- [Tools](#)

- [Widget](widget.html)

- [Xml](xml-class.html)

- [Operator Algebra for Geometry Objects](algebra.html)

- [Low Level Functions and Classes](lowlevel.html)

- [Functions](functions.html)

- [Device](device.html)

- [Working together: DisplayList and TextPage](coop_low.html)

- [Glossary](glossary.html)

- [Constants and Enumerations](vars.html)

- [Color Database](colors.html)

Other

- [Appendix 1: Details on Text Extraction](app1.html)

- [Appendix 2: Considerations on Embedded Files](app2.html)

- [Appendix 3: Assorted Technical Information](app3.html)

- [Appendix 4: Performance Comparison Methodology](app4.html)

- [Change Log](changes.html)

- [Deprecated Names](znames.html)

      
      
    
  
  
    
      
        
          
            

          
          Back to top
        
        
          
  
    
    View this page
  

            
              
              
              
              
            
          
          
            
          
        
        
          

    pymupdf.io
    
      
      
      
    
    
        [English](javaScript:changeLanguage('en'))
        [日本語](javaScript:changeLanguage('ja'))
        [한국어](javaScript:changeLanguage('ko'))
    

    
        [Find #pymupdf on Discord](https://discord.gg/TSpYGBW4eq)
        
            
                
                    
                        
                    
                    
                        

                    
                
            
        
    
    
        [Try our forum! ](https://forum.mupdf.com)
    

# Tools[¶](#tools)

This class is a collection of utility methods and attributes, mainly around memory management. To simplify and speed up its use, it is automatically instantiated under the name *TOOLS* when PyMuPDF is imported.

**Method / Attribute**

**Description**

[`Tools.gen_id()`](#Tools.gen_id)

generate a unique identifier

[`Tools.store_shrink()`](#Tools.store_shrink)

shrink the storables cache [[1]](#f1)

[`Tools.mupdf_warnings()`](#Tools.mupdf_warnings)

return the accumulated MuPDF warnings

[`Tools.mupdf_display_errors()`](#Tools.mupdf_display_errors)

control whether MuPDF errors are displayed as messages.

[`Tools.mupdf_display_warnings()`](#Tools.mupdf_display_warnings)

control whether MuPDF warnings are displayed as messages.

[`Tools.reset_mupdf_warnings()`](#Tools.reset_mupdf_warnings)

empty MuPDF warnings/errors message buffer.

[`Tools.set_aa_level()`](#Tools.set_aa_level)

set the anti-aliasing values

[`Tools.set_annot_stem()`](#Tools.set_annot_stem)

set the prefix of new annotation / link ids

[`Tools.set_small_glyph_heights()`](#Tools.set_small_glyph_heights)

search and extract using small bbox heights

[`Tools.set_subset_fontnames()`](#Tools.set_subset_fontnames)

control suppression of subset fontname tags

[`Tools.show_aa_level()`](#Tools.show_aa_level)

return the anti-aliasing values

[`Tools.unset_quad_corrections()`](#Tools.unset_quad_corrections)

disable PyMuPDF-specific code

[`Tools.fitz_config`](#Tools.fitz_config)

configuration settings of PyMuPDF

[`Tools.store_maxsize`](#Tools.store_maxsize)

maximum storables cache size

[`Tools.store_size`](#Tools.store_size)

current storables cache size

**Class API**

class Tools[¶](#Tools)

gen_id()[¶](#Tools.gen_id)

A convenience method returning a unique positive integer which will increase by 1 on every invocation. Example usages include creating unique keys in databases - its creation should be faster than using timestamps by an order of magnitude.

Note

MuPDF has dropped support for this in v1.14.0, so we have re-implemented a similar function with the following differences:

- 
It is not part of MuPDF’s global context and not threadsafe (not an issue because we do not support threads in PyMuPDF anyway).

- 
It is implemented as *int*. This means that the maximum number is *sys.maxsize*. Should this number ever be exceeded, the counter starts over again at 1.

Return type:

int

Returns:

a unique positive integer.

set_annot_stem(stem=None)[¶](#Tools.set_annot_stem)

- 
New in v1.18.6

Set or inquire the prefix for the id of new annotations, fields or links.

Parameters:

**stem** (*str*) – if omitted, the current value is returned, default is “fitz”. Annotations, fields / widgets and links technically are subtypes of the same type of object (`/Annot`) in PDF documents. An `/Annot` object may be given a unique identifier within a page. For each of the applicable subtypes, PyMuPDF generates identifiers “stem-Annn”, “stem-Wnnn” or “stem-Lnnn” respectively. The number “nnn” is used to enforce the required uniqueness.

Return type:

str

Returns:

the current value.

set_small_glyph_heights(on=None)[¶](#Tools.set_small_glyph_heights)

- 
New in v1.18.5

Set or inquire reduced bbox heights in text extract and text search methods.

Parameters:

**on** (*bool*) – if omitted or `None`, the current setting is returned. For other values the *bool()* function is applied to set a global variable. If `True`, [`Page.search_for()`](page.html#Page.search_for) and [`Page.get_text()`](page.html#Page.get_text) methods return character, span, line or block bboxes that have a height of *font size*. If `False` (standard setting when PyMuPDF is imported), bbox height will be based on font properties and normally equal *line height*.

Return type:

bool

Returns:

`True` or `False`.

Note

Text extraction options “xml”, “xhtml” and “html”, which directly wrap MuPDF code, are not influenced by this.

set_subset_fontnames(on=None)[¶](#Tools.set_subset_fontnames)

- 
New in v1.18.9

Control suppression of subset fontname tags in text extractions.

Parameters:

**on** (*bool*) – if omitted / `None`, the current setting is returned. Arguments evaluating to `True` or `False` set a global variable. If `True`, options “dict”, “json”, “rawdict” and “rawjson” will return e.g. `"NOHSJV+Calibri-Light"`, otherwise only `"Calibri-Light"` (the default). The setting remains in effect until changed again.

Return type:

bool

Returns:

`True` or `False`.

Note

Except mentioned above, no other text extraction variants are influenced by this. This is especially true for the options “xml”, “xhtml” and “html”, which are based on MuPDF code. They extract the font name `"Calibri-Light"`, or even just the **family** name – `Calibri` in this example.

unset_quad_corrections(on=None)[¶](#Tools.unset_quad_corrections)

- 
New in v1.18.10

Enable / disable PyMuPDF-specific code, that tries to rebuild valid character quads when encountering nonsense in [`Page.get_text()`](page.html#Page.get_text) text extractions. This code depends on certain font properties (ascender and descender), which do not exist in rare situations and cause segmentation faults when trying to access them. This method sets a global parameter in PyMuPDF, which suppresses execution of this code.

Parameters:

**on** (*bool*) – if omitted or `None`, the current setting is returned. For other values the *bool()* function is applied to set a global variable. If `True`, PyMuPDF will not try to access the resp. font properties and use values `ascender=0.8` and `descender=-0.2` instead.

Return type:

bool

Returns:

`True` or `False`.

store_shrink(percent)[¶](#Tools.store_shrink)

Reduce the storables cache by a percentage of its current size.

Parameters:

**percent** (*int*) – the percentage of current size to free. If 100+ the store will be emptied, if zero, nothing will happen. MuPDF’s caching strategy is “least recently used”, so low-usage elements get deleted first.

Return type:

int

Returns:

the new current store size. Depending on the situation, the size reduction may be larger than the requested percentage.

show_aa_level()[¶](#Tools.show_aa_level)

- 
New in version 1.16.14

Return the current anti-aliasing values. These values control the rendering quality of graphics and text elements.

Return type:

dict

Returns:

A dictionary with the following initial content: `{'graphics': 8, 'text': 8, 'graphics_min_line_width': 0.0}`.

set_aa_level(level)[¶](#Tools.set_aa_level)

- 
New in version 1.16.14

Set the new number of bits to use for anti-aliasing. The same value is taken currently for graphics and text rendering. This might change in a future MuPDF release.

Parameters:

**level** (*int*) – an integer ranging between 0 and 8. Value outside this range will be silently changed to valid values. The value will remain in effect throughout the current session or until changed again.

reset_mupdf_warnings()[¶](#Tools.reset_mupdf_warnings)

- 
New in version 1.16.0

Empty MuPDF warnings message buffer.

mupdf_display_errors(value=None)[¶](#Tools.mupdf_display_errors)

Control whether MuPDF errors should be displayed as PyMuPDF messages.

Parameters:

**value**

- 
If `None`, the current setting is left unchanged.

- 
Otherwise changes the current setting to `bool(value)`;
if `True`, future MuPDF errors will be shown as [ messages](app3.html#messages).

- 
Regardless of this setting, MuPDF errors will always be stored in the warnings store.

- 
Upon import of PyMuPDF this value is `True`.

Returns:

The current setting as `True` or `False`.

- 
New in version 1.16.8

mupdf_display_warnings(value=None)[¶](#Tools.mupdf_display_warnings)

Control whether MuPDF warnings should be displayed as PyMuPDF messages.

Parameters:

**value**

- 
If `None`, the current setting is left unchanged.

- 
Otherwise changes the current setting to `bool(value)`;
if `True`, future MuPDF warnings will be shown as [ messages](app3.html#messages).

- 
Regardless of this setting, MuPDF warnings will always be stored in the warnings store.

- 
Upon import of PyMuPDF this value is `True`.

Returns:

The current setting as `True` or `False`.

- 
New in version 1.16.8

mupdf_warnings(reset=True)[¶](#Tools.mupdf_warnings)

- 
New in version 1.16.0

Return all stored MuPDF messages as a string with interspersed line-breaks.

Parameters:

**reset** (*bool*) – *(new in version 1.16.7)* whether to automatically empty the store.

fitz_config[¶](#Tools.fitz_config)

A dictionary containing the actual values used for configuring PyMuPDF and MuPDF. Also refer to the installation chapter. This is an overview of the keys, each of which describes the status of a support aspect.

**Key**

**Support included for …**

plotter-g

Gray colorspace rendering

plotter-rgb

RGB colorspace rendering

plotter-cmyk

CMYK colorspcae rendering

plotter-n

overprint rendering

pdf

PDF documents

xps

XPS documents

svg

SVG documents

cbz

CBZ documents

img

IMG documents

html

HTML documents

epub

EPUB documents

jpx

JPEG2000 images

js

JavaScript

tofu

all TOFU fonts

tofu-cjk

CJK font subset (China, Japan, Korea)

tofu-cjk-ext

CJK font extensions

tofu-cjk-lang

CJK font language extensions

tofu-emoji

TOFU emoji fonts

tofu-historic

TOFU historic fonts

tofu-symbol

TOFU symbol fonts

tofu-sil

TOFU SIL fonts

icc

ICC profiles

py-memory

using Python memory management [[2]](#f2)

base14

Base-14 fonts (should always be true)

For an explanation of the term “TOFU” see [this Wikipedia article](https://en.wikipedia.org/wiki/Noto_fonts):

In [1]: import pymupdf
In [2]: TOOLS.fitz_config
Out[2]:
{'plotter-g': True,
 'plotter-rgb': True,
 'plotter-cmyk': True,
 'plotter-n': True,
 'pdf': True,
 'xps': True,
 'svg': True,
 'cbz': True,
 'img': True,
 'html': True,
 'epub': True,
 'jpx': True,
 'js': True,
 'tofu': False,
 'tofu-cjk': True,
 'tofu-cjk-ext': False,
 'tofu-cjk-lang': False,
 'tofu-emoji': False,
 'tofu-historic': False,
 'tofu-symbol': False,
 'tofu-sil': False,
 'icc': True,
 'py-memory': False,
 'base14': True}

Return type:

dict

store_maxsize[¶](#Tools.store_maxsize)

Maximum storables cache size in bytes. PyMuPDF is generated with a value of 268’435’456 (256 MB, the default value), which you should therefore always see here. If this value is zero, then an “unlimited” growth is permitted.

Return type:

int

store_size[¶](#Tools.store_size)

Current storables cache size in bytes. This value may change (and will usually increase) with every use of a PyMuPDF function. It will (automatically) decrease only when [`Tools.store_maxsize`](#Tools.store_maxsize) is going to be exceeded: in this case, MuPDF will evict low-usage objects until the value is again in range.

Return type:

int

## Example Session[¶](#example-session)

>>> import pymupdf
# print the maximum and current cache sizes
>>> pymupdf.TOOLS.store_maxsize
268435456
>>> pymupdf.TOOLS.store_size
0
>>> doc = pymupdf.open("demo1.pdf")
# pixmap creation puts lots of object in cache (text, images, fonts),
# apart from the pixmap itself
>>> pix = doc[0].get_pixmap(alpha=False)
>>> pymupdf.TOOLS.store_size
454519
# release (at least) 50% of the storage
>>> pymupdf.TOOLS.store_shrink(50)
13471
>>> pymupdf.TOOLS.store_size
13471
# get a few unique numbers
>>> pymupdf.TOOLS.gen_id()
1
>>> pymupdf.TOOLS.gen_id()
2
>>> pymupdf.TOOLS.gen_id()
3
# close document and see how much cache is still in use
>>> doc.close()
>>> pymupdf.TOOLS.store_size
0
>>>

Footnotes

[[1](#id2)]

This memory area is internally used by MuPDF, and it serves as a cache for objects that have already been read and interpreted, thus improving performance. The most bulky object types are images and also fonts. When an application starts up the MuPDF library (in our case this happens as part of *import pymupdf*), it must specify a maximum size for this area. PyMuPDF’s uses the default value (256 MB) to limit memory consumption. Use the methods here to control or investigate store usage. For example: even after a document has been closed and all related objects have been deleted, the store usage may still not drop down to zero. So you might want to enforce that before opening another document.

[[2](#id3)]

By default PyMuPDF and MuPDF use `malloc()`/`free()` for dynamic memory management. One can instead force them to use the Python allocation functions `PyMem_New()`/`PyMem_Del()`, by modifying *fitz/fitz.i* to do `#define JM_MEMORY 1` and rebuilding PyMuPDF.

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

This documentation covers all versions up to 1.27.1.

        
      
      
        
        
          
              
                
                  Next
                
                Widget
              
              
            
          
              
              
                
                  Previous
                
                
                TextWriter
                
              
            
        
        
          
            
                Copyright © 2015-2026, Artifex
            
            Made with 
            [Furo](https://github.com/pradyunsg/furo)
            
              Last updated on 16. Feb 2026
          
          
            
          
        
        
      
    
    
      
      
      
        
          
            On this page
          
        
        
          
            

- [Tools](#)

- [`Tools`](#Tools)

- [`Tools.gen_id()`](#Tools.gen_id)

- [`Tools.set_annot_stem()`](#Tools.set_annot_stem)

- [`Tools.set_small_glyph_heights()`](#Tools.set_small_glyph_heights)

- [`Tools.set_subset_fontnames()`](#Tools.set_subset_fontnames)

- [`Tools.unset_quad_corrections()`](#Tools.unset_quad_corrections)

- [`Tools.store_shrink()`](#Tools.store_shrink)

- [`Tools.show_aa_level()`](#Tools.show_aa_level)

- [`Tools.set_aa_level()`](#Tools.set_aa_level)

- [`Tools.reset_mupdf_warnings()`](#Tools.reset_mupdf_warnings)

- [`Tools.mupdf_display_errors()`](#Tools.mupdf_display_errors)

- [`Tools.mupdf_display_warnings()`](#Tools.mupdf_display_warnings)

- [`Tools.mupdf_warnings()`](#Tools.mupdf_warnings)

- [`Tools.fitz_config`](#Tools.fitz_config)

- [`Tools.store_maxsize`](#Tools.store_maxsize)

- [`Tools.store_size`](#Tools.store_size)

- [Example Session](#example-session)
