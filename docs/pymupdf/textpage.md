# Source: https://pymupdf.readthedocs.io/en/latest/textpage.html
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
        TextPage - PyMuPDF documentation
      
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

- [TextPage](#)

- [TextWriter](textwriter.html)

- [Tools](tools.html)

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
    

# TextPage[¶](#textpage)

This class represents text and images shown on a document page. All [MuPDF document types](how-to-open-a-file.html#supported-file-types) are supported.

The usual ways to create a textpage are [`DisplayList.get_textpage()`](displaylist.html#DisplayList.get_textpage) and [`Page.get_textpage()`](page.html#Page.get_textpage). Because there is a limited set of methods in this class, there exist wrappers in [Page](page.html#page) which are handier to use. The last column of this table shows these corresponding [Page](page.html#page) methods.

For a description of what this class is all about, see Appendix 2.

**Method**

**Description**

page get_text or search method

[`extractText()`](#TextPage.extractText)

extract plain text

“text”

[`extractTEXT()`](#TextPage.extractTEXT)

synonym of previous

“text”

[`extractBLOCKS()`](#TextPage.extractBLOCKS)

plain text grouped in blocks

“blocks”

[`extractWORDS()`](#TextPage.extractWORDS)

all words with their bbox

“words”

[`extractHTML()`](#TextPage.extractHTML)

page content in HTML format

“html”

[`extractXHTML()`](#TextPage.extractXHTML)

page content in XHTML format

“xhtml”

[`extractXML()`](#TextPage.extractXML)

page text in XML format

“xml”

[`extractDICT()`](#TextPage.extractDICT)

page content in *dict* format

“dict”

[`extractJSON()`](#TextPage.extractJSON)

page content in JSON format

“json”

[`extractRAWDICT()`](#TextPage.extractRAWDICT)

page content in *dict* format

“rawdict”

[`extractRAWJSON()`](#TextPage.extractRAWJSON)

page content in JSON format

“rawjson”

[`search()`](#TextPage.search)

Search for a string in the page

[`Page.search_for()`](page.html#Page.search_for)

**Class API**

class TextPage[¶](#TextPage)

extractText(sort=False)[¶](#TextPage.extractText)

extractTEXT(sort=False)[¶](#TextPage.extractTEXT)

Return a string of the page’s complete text. The text is UTF-8 unicode and in the same sequence as specified at the time of document creation.

Parameters:

**sort** (*bool*) – (new in v1.19.1) sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order.

Return type:

str

extractBLOCKS()[¶](#TextPage.extractBLOCKS)

Textpage content as a list of text lines grouped by block. Each list items looks like this:

``(x0, y0, x1, y1, "lines in the block", block_no, block_type)``

The first four entries are the block’s bbox coordinates, *block_type* is 1 for an image block, 3 for a vector block, and 0 for text. *block_no* is the block sequence number. Multiple text lines are joined via line breaks.

For an **image block**, its bbox and a text line with some image meta information is included – not the image **content**. Image blocks are included only if the extraction flag bit [`TEXT_PRESERVE_IMAGES`](vars.html#TEXT_PRESERVE_IMAGES) is set. An image block tuple will look like this:

``(x0, y0, x1, y1, "<image: colorspace-name, w: width, h: height, bpc: bits_per_component>\n", block_no, 1)``

For a **vector block**, the following item will be included. Vector blocks are included only if the extraction flag bit [`TEXT_COLLECT_VECTORS`](vars.html#TEXT_COLLECT_VECTORS) is set. A vector block tuple will look like this:

``(x0, y0, x1, y1, "<vector stroked, color: #rrggbb, alpha: 255, is-rect: true, continues: false>\n", block_no, 3)``

The keyword “vector” is followed by either “stroked” or “filled”. The color is given in HTML (hexadecimal RGB) format. Property `is-rect` is true, if the vector is not a curve and parallel to the x- or y-axis. So in essence is either a real rectangle or a line segment. Property `continues` indicates whether the vector is part of a path (and not the first item).

Note

When no further details are needed (as provided by [`Page.get_drawings()`](page.html#Page.get_drawings)), then this is an **inexpensive** way to extract basic vector graphics information. Another major advantage is that all block types (text, images and vectors) are included in the output in the same order as they are present in the page’s [`contents`](glossary.html#contents) stream.

This is a high-speed method with just enough information to output plain text in desired reading sequence.

Return type:

list

extractWORDS(delimiters=None)[¶](#TextPage.extractWORDS)

- 
Changed in v1.23.5: added `delimiters` parameter

Textpage content as a list of single words with bbox information. An item of this list looks like this:

(x0, y0, x1, y1, "word", block_no, line_no, word_no)

Parameters:

**delimiters** (*str*) – (new in v1.23.5) use these characters as *additional* word separators. By default, all white spaces (including the non-breaking space `0xA0`) indicate start and end of a word. Now you can specify more characters causing this. For instance, the default will return `"john.doe@outlook.com"` as **one** word. If you specify `delimiters="@."` then the **four** words `"john"`, `"doe"`, `"outlook"`, `"com"` will be returned. Other possible uses include ignoring punctuation characters `delimiters=string.punctuation`. The “word” strings will not contain any delimiting character.

This is a high-speed method which e.g. allows extracting text from within given areas or recovering the text reading sequence.

Return type:

list

extractHTML()[¶](#TextPage.extractHTML)

Textpage content as a string in HTML format. This version contains complete formatting and positioning information. Images are included (encoded as base64 strings). You need an HTML package to interpret the output in Python. Your internet browser should be able to adequately display this information, but see [Controlling Quality of HTML Output](app1.html#htmlquality).

Return type:

str

extractDICT(sort=False)[¶](#TextPage.extractDICT)

Textpage content as a Python dictionary. Provides same information detail as HTML. See below for the structure.

Parameters:

**sort** (*bool*) – (new in v1.19.1) sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order.

Return type:

dict

extractJSON(sort=False)[¶](#TextPage.extractJSON)

Textpage content as a JSON string. Created by `json.dumps(TextPage.extractDICT())`. It is included for backlevel compatibility. You will probably use this method ever only for outputting the result to some file. The  method detects binary image data and converts them to base64 encoded strings.

Parameters:

**sort** (*bool*) – (new in v1.19.1) sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order.

Return type:

str

extractXHTML()[¶](#TextPage.extractXHTML)

Textpage content as a string in XHTML format. Text information detail is comparable with [`extractTEXT()`](#TextPage.extractTEXT), but also contains images (base64 encoded). This method makes no attempt to re-create the original visual appearance.

Return type:

str

extractXML()[¶](#TextPage.extractXML)

Textpage content as a string in XML format. This contains complete formatting information about every single character on the page: font, size, line, paragraph, location, color, etc. Contains no images. You need an XML package to interpret the output in Python.

Return type:

str

extractRAWDICT(sort=False)[¶](#TextPage.extractRAWDICT)

Textpage content as a Python dictionary – technically similar to [`extractDICT()`](#TextPage.extractDICT), and it contains that information as a subset (including any images). It provides additional detail down to each character, which makes using XML obsolete in many cases. See below for the structure.

Parameters:

**sort** (*bool*) – (new in v1.19.1) sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order.

Return type:

dict

extractRAWJSON(sort=False)[¶](#TextPage.extractRAWJSON)

Textpage content as a JSON string. Created by `json.dumps(TextPage.extractRAWDICT())`. You will probably use this method ever only for outputting the result to some file. The  method detects binary image data and converts them to base64 encoded strings.

Parameters:

**sort** (*bool*) – (new in v1.19.1) sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order.

Return type:

str

search(needle, quads=False)[¶](#TextPage.search)

- 
Changed in v1.18.2

Search for *string* and return a list of found locations.

Parameters:

- 
**needle** (*str*) – the string to search for. Upper and lower cases will all match if needle consists of ASCII letters only – it does not yet work for “Ä” versus “ä”, etc.

- 
**quads** (*bool*) – return quadrilaterals instead of rectangles.

Return type:

list

Returns:

a list of [Rect](rect.html#rect) or [Quad](quad.html#quad) objects, each surrounding a found *needle* occurrence. As the search string may contain spaces, its parts may be found on different lines. In this case, more than one rectangle (resp. quadrilateral) are returned. **(Changed in v1.18.2)** The method **now supports dehyphenation**, so it will find e.g. “method”, even if it was hyphenated in two parts “meth-” and “od” across two lines. The two returned rectangles will contain “meth” (no hyphen) and “od”.

Note

**Overview of changes in v1.18.2:**

- 
The `hit_max` parameter has been removed: all hits are always returned.

- 
The [Rect](rect.html) parameter of the [TextPage](#textpage) is now respected: only text inside this area is examined. Only characters with fully contained bboxes are considered. The wrapper method [`Page.search_for()`](page.html#Page.search_for) correspondingly supports a *clip* parameter.

- 
**Hyphenated words** are now found.

- 
**Overlapping rectangles** in the same line are now automatically joined. We assume that such separations are an artifact created by multiple marked content groups, containing parts of the same search needle.

Example Quad versus Rect: when searching for needle “pymupdf”, then the corresponding entry will either be the blue rectangle, or, if *quads* was specified, the quad *Quad(ul, ur, ll, lr)*.

rect[¶](#TextPage.rect)

The rectangle associated with the text page. This either equals the rectangle of the creating page or the `clip` parameter of [`Page.get_textpage()`](page.html#Page.get_textpage) and text extraction / searching methods.

Note

The output of text searching and most text extractions **is restricted to this rectangle**. (X)HTML and XML output will however always extract the full page.

## Structure of Dictionary Outputs[¶](#structure-of-dictionary-outputs)

Methods [`TextPage.extractDICT()`](#TextPage.extractDICT), [`TextPage.extractJSON()`](#TextPage.extractJSON), [`TextPage.extractRAWDICT()`](#TextPage.extractRAWDICT), and [`TextPage.extractRAWJSON()`](#TextPage.extractRAWJSON) return dictionaries, containing the page’s text and image content. The dictionary structures of all four methods are almost equal. They strive to map the text page’s information hierarchy of blocks, lines, spans and characters as precisely as possible, by representing each of these by its own sub-dictionary:

- 
A **page** consists of a list of **block dictionaries**.

- 
A (text) **block** consists of a list of **line dictionaries**.

- 
A **line** consists of a list of **span dictionaries**.

- 
A **span** either consists of the text itself or, for the RAW variants, a list of **character dictionaries**.

- 
RAW variants: a **character** is a dictionary of its origin, bbox and unicode.

All PyMuPDF geometry objects herein (points, rectangles, matrices) are represented by there **“like”** formats: a [`rect_like`](glossary.html#rect_like) *tuple* is used instead of a [Rect](rect.html#rect), etc. The reasons for this are performance and memory considerations:

- 
This code is written in C, where Python tuples can easily be generated. The geometry objects on the other hand are defined in Python source only. A conversion of each Python tuple into its corresponding geometry object would add significant – and largely unnecessary – execution time.

- 
A 4-tuple needs about 168 bytes, the corresponding [Rect](rect.html#rect) 472 bytes - almost three times the size. A “dict” dictionary for a text-heavy page contains 300+ bbox objects – which thus require about 50 KB storage as 4-tuples versus 140 KB as [Rect](rect.html#rect) objects. A “rawdict” output for such a page will however contain **4 to 5 thousand** bboxes, so in this case we talk about 750 KB versus 2 MB.

Please also note, that only **bboxes** (= [`rect_like`](glossary.html#rect_like) 4-tuples) are returned, whereas a [TextPage](#textpage) actually has the **full position information** – in [Quad](quad.html#quad) format. The reason for this decision is again a memory consideration: a [`quad_like`](glossary.html#quad_like) needs 488 bytes (3 times the size of a [`rect_like`](glossary.html#rect_like)). Given the mentioned amounts of generated bboxes, returning [`quad_like`](glossary.html#quad_like) information would have a significant impact.

In the vast majority of cases, we are dealing with **horizontal text only**, where bboxes provide entirely sufficient information.

In addition, **the full quad information is not lost**: it can be recovered as needed for lines, spans, and characters by using the appropriate function from the following list:

- 
[`recover_quad()`](functions.html#recover_quad) – the quad of a complete span

- 
[`recover_span_quad()`](functions.html#recover_span_quad) – the quad of a character subset of a span

- 
[`recover_line_quad()`](functions.html#recover_line_quad) – the quad of a line

- 
[`recover_char_quad()`](functions.html#recover_char_quad) – the quad of a character

As mentioned, using these functions is ever only needed, if the text is **not written horizontally** – `line["dir"] != (1, 0)` – and you need the quad for text marker annotations ([`Page.add_highlight_annot()`](page.html#Page.add_highlight_annot) and friends).

### Page Dictionary[¶](#page-dictionary)

**Key**

**Value**

width

width of the `clip` rectangle *(float)*

height

height of the `clip` rectangle *(float)*

blocks

*list* of block dictionaries

### Block Dictionaries[¶](#block-dictionaries)

Block dictionaries come in different formats for **vector blocks**, **image blocks** and **text blocks**. Vector blocks are included only if the extraction flag bit [`TEXT_COLLECT_VECTORS`](vars.html#TEXT_COLLECT_VECTORS) is set. Image blocks are included only if the extraction flag bit [`TEXT_PRESERVE_IMAGES`](vars.html#TEXT_PRESERVE_IMAGES) is set.

**Vector block:**

**Key**

**Value**

type

3 = vector (`int`)

bbox

vector bbox on page ([`rect_like`](glossary.html#rect_like))

number

block count (`int`)

stroked

either stroked (`True`) or filled (`False`) (`bool`)

isrect

whether the vector is axis-parallel (`bool`). Can be a line or a rectangle. Curves or diagonal lines are `False`.

continues

whether the vector is (not the last) part of a sequence of vectors in a *path* (`bool`).

color

sRGB integer, e.g. 0xRRGGBB (`int`).

alpha

Transparency, a value in `range(256)` (`int`).

This information is a true subset of the output of [`Page.get_drawings()`](page.html#Page.get_drawings). Its advantage is its speed (because it is extracted alongside one [TextPage](#textpage) creation) and the fact that vector blocks are included in the overall page content sequence together with text and images.

**Image block:**

**Key**

**Value**

type

1 = image (`int`)

bbox

image bbox on page ([`rect_like`](glossary.html#rect_like))

number

block count (`int`)

ext

image type (`str`), as file extension, see below

width

original image width (`int`)

height

original image height (`int`)

colorspace

colorspace component count (`int`)

xres

resolution in x-direction (`int`) [[3]](#f3)

yres

resolution in y-direction (`int`) [[3]](#f3)

bpc

bits per component (`int`)

transform

matrix transforming image rect to bbox ([`matrix_like`](glossary.html#matrix_like))

size

size of the image in bytes (`int`)

image

image content (`bytes`)

mask

image mask content (`bytes`) for transparent images

Possible values of the “ext” key are “bmp”, “gif”, “jpeg”, “jpx” (JPEG 2000), “jxr” (JPEG XR), “png”, “pnm”, and “tiff”.

Note

- 
An image block is generated for **all and every image occurrence** on the page. Hence there may be duplicates, if an image is shown at different locations.

- 
[TextPage](#textpage) and corresponding method [`Page.get_text()`](page.html#Page.get_text) are **available for all document types**. Only for PDF documents, methods [`Document.get_page_images()`](document.html#Document.get_page_images) / [`Page.get_images()`](page.html#Page.get_images) offer some overlapping functionality as far as image lists are concerned. But both lists **may or may not** contain the same items. Any differences are most probably caused by one of the following:

- 
“Inline” images (see page 214 of the [Adobe PDF References](app3.html#adobemanual)) of a PDF page are contained in a textpage, but **do not appear** in [`Page.get_images()`](page.html#Page.get_images).

- 
Annotations may also contain images – these will **not appear** in [`Page.get_images()`](page.html#Page.get_images).

- 
Image blocks in a textpage are generated for **every** image location – whether or not there are any duplicates. This is in contrast to [`Page.get_images()`](page.html#Page.get_images), which will list each image only once (per reference name).

- 
Images mentioned in the page’s [`object`](glossary.html#object) definition will **always** appear in [`Page.get_images()`](page.html#Page.get_images) [[1]](#f1). But it may happen, that there is no “display” command in the page’s [`contents`](glossary.html#contents) (erroneously or on purpose). In this case the image will **not appear** in the textpage.

- 
The image’s “transformation matrix” is defined as the matrix, for which the expression `bbox / transform == pymupdf.Rect(0, 0, 1, 1)` is true, lookup details here: [Image Transformation Matrix](app3.html#imagetransformation).

- 
A transparent image may be accompanied by a mask image. This is stored under key `"mask"` and has the format of a `DeviceGray` PNG image. Otherwise the value of this key is `None`. If present, you may be able to recover (an equivalent of) the original image – i.e. with transparency – by creating [Pixmap](pixmap.html#pixmap) objects from the “image”, respectively “mask” values and overlay them. This is not guaranteed to always work because mask images come in multiple formats, of which not all qualify for the conditions under which overlaying Pixmaps are supported. Here is a code snippet:

>>> base = pymupdf.Pixmap(block["image"])
>>> mask = pymupdf.Pixmap(block["mask"])
>>> result = pymupdf.Pixmap(base, mask)

**Text block:**

**Key**

**Value**

type

0 = text *(int)*

bbox

block rectangle, [`rect_like`](glossary.html#rect_like)

number

block count *(int)*

lines

*list* of text line dictionaries

### Line Dictionary[¶](#line-dictionary)

**Key**

**Value**

bbox

line rectangle, [`rect_like`](glossary.html#rect_like)

wmode

writing mode *(int)*: 0 = horizontal, 1 = vertical

dir

writing direction, [`point_like`](glossary.html#point_like)

spans

*list* of span dictionaries

The value of key *“dir”* is the **unit vector** `dir = (cosine, -sine)` of the angle, which the text has relative to the x-axis [[2]](#f2). See the following picture: The word in each quadrant (counter-clockwise from top-right to bottom-right) is rotated by 30, 120, 210 and 300 degrees respectively.

### Span Dictionary[¶](#span-dictionary)

Spans contain the actual text. A line contains **more than one span only**, if it contains text with different font properties.

- 
Changed in version 1.14.17 Spans now also have a *bbox* key (again).

- 
Changed in version 1.17.6 Spans now also have an *origin* key.

**Key**

**Value**

bbox

span rectangle, [`rect_like`](glossary.html#rect_like)

origin

the first character’s origin, [`point_like`](glossary.html#point_like)

font

font name *(str)*

ascender

ascender of the font *(float)*

descender

descender of the font *(float)*

size

font size *(float)*

flags

font characteristics *(int)*

char_flags

char characteristics *(int)*

color

text color in sRGB format 0xRRGGBB *(int)*.

alpha

text opacity 0..255 *(int)*.

text

(only for `extractDICT()`) text *(str)*

chars

(only for `extractRAWDICT()`) *list* of character dictionaries

Show/hide history

*(New in version 1.25.3.0):* Added *“alpha”* item.

*(New in version 1.16.0):* *“color”* is the text color encoded in sRGB (int) format, e.g. 0xFF0000 for red. There are functions for converting this integer back to formats (r, g, b) (PDF with float values from 0 to 1) [`sRGB_to_pdf()`](functions.html#sRGB_to_pdf), or (R, G, B), [`sRGB_to_rgb()`](functions.html#sRGB_to_rgb) (with integer values from 0 to 255).

*(New in v1.18.5):* *“ascender”* and *“descender”* are font properties, provided relative to [`fontsize`](glossary.html#fontsize) 1. Note that descender is a negative value. The following picture shows the relationship to other values and properties.

These numbers may be used to compute the minimum height of a character (or span) – as opposed to the standard height provided in the “bbox” values (which actually represents the **line height**). The following code recalculates the span bbox to have a height of **fontsize** exactly fitting the text inside:

>>> a = span["ascender"]
>>> d = span["descender"]
>>> r = pymupdf.Rect(span["bbox"])
>>> o = pymupdf.Point(span["origin"])  # its y-value is the baseline
>>> r.y1 = o.y - span["size"] * d / (a - d)
>>> r.y0 = r.y1 - span["size"]
>>> # r now is a rectangle of height 'fontsize'

Caution

The above calculation may deliver a **larger** height! This may e.g. happen for OCRed documents, where the risk of all sorts of text artifacts is high. MuPDF tries to come up with a reasonable bbox height, independently from the [`fontsize`](glossary.html#fontsize) found in the PDF. So please ensure that the height of `span["bbox"]` is **larger** than `span["size"]`.

Note

You may request PyMuPDF to do all of the above automatically by executing `pymupdf.TOOLS.set_small_glyph_heights(True)`. This sets a global parameter so that all subsequent text searches and text extractions are based on reduced glyph heights, where meaningful.

The following shows the original span rectangle in red and the rectangle with re-computed height in blue.

*“flags”* is an integer, which represents font properties except for the first bit 0. They are to be interpreted like this:

- 
bit 0: superscripted ([`TEXT_FONT_SUPERSCRIPT`](vars.html#TEXT_FONT_SUPERSCRIPT)) – not a font property, detected by MuPDF code.

- 
bit 1: italic ([`TEXT_FONT_ITALIC`](vars.html#TEXT_FONT_ITALIC))

- 
bit 2: serifed ([`TEXT_FONT_SERIFED`](vars.html#TEXT_FONT_SERIFED))

- 
bit 3: monospaced ([`TEXT_FONT_MONOSPACED`](vars.html#TEXT_FONT_MONOSPACED))

- 
bit 4: bold ([`TEXT_FONT_BOLD`](vars.html#TEXT_FONT_BOLD))

Test these characteristics like so:

>>> if flags & pymupdf.TEXT_FONT_BOLD & pymupdf.TEXT_FONT_ITALIC:
        print(f"{span['text']=} is bold and italic")

Bits 1 thru 4 are font properties, i.e. encoded in the font program. Please note, that this information is not necessarily correct or complete: fonts quite often contain wrong data here.

*“char_flags”* is an integer, which represents extra character properties:

- 
bit 0: strikeout.

- 
bit 1: underline.

- 
bit 2: synthetic (always 0, see char dictionary).

- 
bit 3: filled.

- 
bit 4: stroked.

- 
bit 5: clipped.

For example if not filled and not stroked (if not (char_flags & 2**3 & 2**4):
...) then the text will be invisible.

(`char_flags` is new in v1.25.2.)

### Character Dictionary for `extractRAWDICT()`[¶](#character-dictionary-for-extractrawdict)

**Key**

**Value**

origin

character’s left baseline point, [`point_like`](glossary.html#point_like)

bbox

character rectangle, [`rect_like`](glossary.html#rect_like)

synthetic

bool.

c

the character (unicode)

(`synthetic` is new in v1.25.3.)

This image shows the relationship between a character’s bbox and its quad: [](_images/img-textpage-char.png)

Footnotes

[[1](#id4)]

Image specifications for a PDF page are done in a page’s (sub-) [`dictionary`](glossary.html#dictionary), called `/Resources`. Resource dictionaries can be **inherited** from any of the page’s parent objects (usually the [`catalog`](glossary.html#catalog) – the top-level parent). The PDF creator may e.g. define one `/Resources` on file level, naming all images and / or all fonts ever used by any page. In these cases, [`Page.get_images()`](page.html#Page.get_images) and [`Page.get_fonts()`](page.html#Page.get_fonts) will consequently return the same lists for all pages. If desired, this situation can be reverted using [`Page.clean_contents()`](functions.html#Page.clean_contents). After execution, the page’s object definition will show fonts and images that are actually used.

[[2](#id5)]

The coordinate systems of MuPDF and PDF are different in that MuPDF uses the page’s top-left point as `(0, 0)`. In PDF, this is the bottom-left point. Therefore, the positive direction for MuPDF’s y-axis is **from top to bottom**. This causes the sign change for the sine value here: a **negative** value indicates anti-clockwise rotation of the text.

[3]
([1](#id2),[2](#id3))

This value is always 96, the default of the PDF interpreter. It **does not reflect** the resolution of the image itself. If you need the image’s resolution, use the [`Pixmap.xres()`](pixmap.html#Pixmap.xres) and [`Pixmap.yres()`](pixmap.html#Pixmap.yres) attributes of the [Pixmap](pixmap.html#pixmap) created from the returned image binary.

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

This documentation covers all versions up to 1.27.1.

        
      
      
        
        
          
              
                
                  Next
                
                TextWriter
              
              
            
          
              
              
                
                  Previous
                
                
                Story
                
              
            
        
        
          
            
                Copyright © 2015-2026, Artifex
            
            Made with 
            [Furo](https://github.com/pradyunsg/furo)
            
              Last updated on 16. Feb 2026
          
          
            
          
        
        
      
    
    
      
      
      
        
          
            On this page
          
        
        
          
            

- [TextPage](#)

- [`TextPage`](#TextPage)

- [`TextPage.extractText()`](#TextPage.extractText)

- [`TextPage.extractTEXT()`](#TextPage.extractTEXT)

- [`TextPage.extractBLOCKS()`](#TextPage.extractBLOCKS)

- [`TextPage.extractWORDS()`](#TextPage.extractWORDS)

- [`TextPage.extractHTML()`](#TextPage.extractHTML)

- [`TextPage.extractDICT()`](#TextPage.extractDICT)

- [`TextPage.extractJSON()`](#TextPage.extractJSON)

- [`TextPage.extractXHTML()`](#TextPage.extractXHTML)

- [`TextPage.extractXML()`](#TextPage.extractXML)

- [`TextPage.extractRAWDICT()`](#TextPage.extractRAWDICT)

- [`TextPage.extractRAWJSON()`](#TextPage.extractRAWJSON)

- [`TextPage.search()`](#TextPage.search)

- [`TextPage.rect`](#TextPage.rect)

- [Structure of Dictionary Outputs](#structure-of-dictionary-outputs)

- [Page Dictionary](#page-dictionary)

- [Block Dictionaries](#block-dictionaries)

- [Line Dictionary](#line-dictionary)

- [Span Dictionary](#span-dictionary)

- [Character Dictionary for `extractRAWDICT()`](#character-dictionary-for-extractrawdict)
