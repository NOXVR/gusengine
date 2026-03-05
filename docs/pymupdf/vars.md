# Source: https://pymupdf.readthedocs.io/en/latest/vars.html
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
        Constants and Enumerations - PyMuPDF documentation
      
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

- [Tools](tools.html)

- [Widget](widget.html)

- [Xml](xml-class.html)

- [Operator Algebra for Geometry Objects](algebra.html)

- [Low Level Functions and Classes](lowlevel.html)

- [Functions](functions.html)

- [Device](device.html)

- [Working together: DisplayList and TextPage](coop_low.html)

- [Glossary](glossary.html)

- [Constants and Enumerations](#)

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
    

# Constants and Enumerations[¶](#constants-and-enumerations)

Constants and enumerations of MuPDF as implemented by PyMuPDF. Each of the following values is accessible as `pymupdf.value`.

## Constants[¶](#constants)

Base14_Fonts[¶](#Base14_Fonts)

Predefined Python list of valid [PDF Base 14 Fonts](app3.html#base-14-fonts).

Type:

list

csRGB[¶](#csRGB)

Predefined RGB colorspace *pymupdf.Colorspace(pymupdf.CS_RGB)*.

Type:

[Colorspace](colorspace.html#colorspace)

csGRAY[¶](#csGRAY)

Predefined GRAY colorspace *pymupdf.Colorspace(pymupdf.CS_GRAY)*.

Type:

[Colorspace](colorspace.html#colorspace)

csCMYK[¶](#csCMYK)

Predefined CMYK colorspace *pymupdf.Colorspace(pymupdf.CS_CMYK)*.

Type:

[Colorspace](colorspace.html#colorspace)

CS_RGB[¶](#CS_RGB)

1 – Type of [Colorspace](colorspace.html#colorspace) is RGBA

Type:

int

CS_GRAY[¶](#CS_GRAY)

2 – Type of [Colorspace](colorspace.html#colorspace) is GRAY

Type:

int

CS_CMYK[¶](#CS_CMYK)

3 – Type of [Colorspace](colorspace.html#colorspace) is CMYK

Type:

int

mupdf_version[¶](#mupdf_version)

‘x.xx.x’ – MuPDF version that is being used by PyMuPDF.

Type:

string

mupdf_version_tuple[¶](#mupdf_version_tuple)

MuPDF version as a tuple of integers, `(major, minor, patch)`.

Type:

tuple

pymupdf_version[¶](#pymupdf_version)

‘x.xx.x’ – PyMuPDF version.

Type:

string

pymupdf_version_tuple[¶](#pymupdf_version_tuple)

PyMuPDF version as a tuple of integers, `(major, minor, patch)`.

Type:

tuple

pymupdf_date[¶](#pymupdf_date)

Disabled (set to None) in 1.26.1.

version[¶](#version)

(pymupdf_version, mupdf_version, timestamp) – combined version information where `timestamp` is the generation point in time formatted as “YYYYMMDDhhmmss”.

Type:

tuple

VersionBind[¶](#VersionBind)

Legacy equivalent to [`mupdf_version`](#mupdf_version).

VersionFitz[¶](#VersionFitz)

Legacy equivalent to [`pymupdf_version`](#pymupdf_version).

VersionDate[¶](#VersionDate)

Disabled (set to None) in 1.26.1.

## Document Permissions[¶](#document-permissions)

Code

Permitted Action

PDF_PERM_PRINT

Print the document

PDF_PERM_MODIFY

Modify the document’s contents

PDF_PERM_COPY

Copy or otherwise extract text and graphics

PDF_PERM_ANNOTATE

Add or modify text annotations and interactive form fields

PDF_PERM_FORM

Fill in forms and sign the document

PDF_PERM_ACCESSIBILITY

Obsolete, always permitted

PDF_PERM_ASSEMBLE

Insert, rotate, or delete pages, bookmarks, thumbnail images

PDF_PERM_PRINT_HQ

High quality printing

## PDF Optional Content Codes[¶](#pdf-optional-content-codes)

Code

Meaning

PDF_OC_ON

Set an OCG to ON temporarily

PDF_OC_TOGGLE

Toggle OCG status temporarily

PDF_OC_OFF

Set an OCG to OFF temporarily

## PDF encryption method codes[¶](#pdf-encryption-method-codes)

Code

Meaning

PDF_ENCRYPT_KEEP

do not change

PDF_ENCRYPT_NONE

remove any encryption

PDF_ENCRYPT_RC4_40

RC4 40 bit

PDF_ENCRYPT_RC4_128

RC4 128 bit

PDF_ENCRYPT_AES_128

*Advanced Encryption Standard* 128 bit

PDF_ENCRYPT_AES_256

*Advanced Encryption Standard* 256 bit

PDF_ENCRYPT_UNKNOWN

unknown

## Font File Extensions[¶](#font-file-extensions)

The table show file extensions you should use when saving fontfile buffers extracted from a PDF. This string is returned by [`Document.get_page_fonts()`](document.html#Document.get_page_fonts), [`Page.get_fonts()`](page.html#Page.get_fonts) and [`Document.extract_font()`](document.html#Document.extract_font).

Ext

Description

ttf

TrueType font

pfa

Postscript for ASCII font (various subtypes)

cff

Type1C font (compressed font equivalent to Type1)

cid

character identifier font (postscript format)

otf

OpenType font

n/a

not extractable, e.g. [PDF Base 14 Fonts](app3.html#base-14-fonts), Type 3 fonts and others

## Text Alignment[¶](#text-alignment)

TEXT_ALIGN_LEFT[¶](#TEXT_ALIGN_LEFT)

0 – align left.

TEXT_ALIGN_CENTER[¶](#TEXT_ALIGN_CENTER)

1 – align center.

TEXT_ALIGN_RIGHT[¶](#TEXT_ALIGN_RIGHT)

2 – align right.

TEXT_ALIGN_JUSTIFY[¶](#TEXT_ALIGN_JUSTIFY)

3 – align justify.

## Font Properties[¶](#font-properties)

Please note that the following bits are derived from what a font has to say about its properties. It may not be (and quite often is not) correct.

TEXT_FONT_SUPERSCRIPT[¶](#TEXT_FONT_SUPERSCRIPT)

1 – the character or span is a superscript. This property is computed by MuPDF and not part of any font information.

TEXT_FONT_ITALIC[¶](#TEXT_FONT_ITALIC)

2 – the font is italic.

TEXT_FONT_SERIFED[¶](#TEXT_FONT_SERIFED)

4 – the font is serifed.

TEXT_FONT_MONOSPACED[¶](#TEXT_FONT_MONOSPACED)

8 – the font is mono-spaced.

TEXT_FONT_BOLD[¶](#TEXT_FONT_BOLD)

16 – the font is bold.

## Text Extraction Flags[¶](#text-extraction-flags)

Option bits controlling the amount of data, that are parsed into a [TextPage](textpage.html#textpage).

For the PyMuPDF programmer, some combination (using Python’s `|` operator, or simply use `+`) of these values are aggregated in the `flags` integer, a parameter of all text search and text extraction methods. Depending on the individual method, different default combinations of the values are used. Please use a value that meets your situation. Especially make sure to switch off image extraction unless you really need them. The impact on performance and memory is significant!

TEXT_PRESERVE_LIGATURES[¶](#TEXT_PRESERVE_LIGATURES)

1 – If set, ligatures are passed through to the application in their original form. Otherwise ligatures are expanded into their constituent parts, e.g. the ligature “ffi” is expanded into three  eparate characters f, f and i. Default is “on” in PyMuPDF. MuPDF supports the following 7 ligatures: “ff”, “fi”, “fl”, “ffi”, “ffl”, , “ft”, “st”.

TEXT_PRESERVE_WHITESPACE[¶](#TEXT_PRESERVE_WHITESPACE)

2 – If set, whitespace is passed through. Otherwise any type of horizontal whitespace (including horizontal tabs) will be replaced with space characters of variable width. Default is “on” in PyMuPDF.

TEXT_PRESERVE_IMAGES[¶](#TEXT_PRESERVE_IMAGES)

4 – If set, then images will be stored in the [TextPage](textpage.html#textpage). This causes the presence of (usually large!) binary image content in the output of text extractions of types “blocks”, “dict”, “json”, “rawdict”, “rawjson”, “html”, and “xhtml” and is the default there. If used with “blocks” however, only image metadata will be returned, not the image itself.

TEXT_INHIBIT_SPACES[¶](#TEXT_INHIBIT_SPACES)

8 – If set, Mupdf will not try to add missing space characters where there are large gaps between characters. In PDF, the creator often does not insert spaces to point to the next character’s position, but will provide the direct location address. The default in PyMuPDF is “off” – so spaces **will be generated**.

TEXT_DEHYPHENATE[¶](#TEXT_DEHYPHENATE)

16 – Ignore hyphens at line ends and join with next line. Used internally with the text search functions. However, it is generally available: if on, text extractions will return joined text lines (or spans) with the ending hyphen of the first line eliminated. So two separate spans **“first meth-”** and **“od leads to wrong results”** on different lines will be joined to one span **“first method leads to wrong results”** and correspondingly updated bboxes: the characters of the resulting span will no longer have identical y-coordinates.

TEXT_PRESERVE_SPANS[¶](#TEXT_PRESERVE_SPANS)

32 – Generate a new line for every span. Not used (“off”) in PyMuPDF, but available for your use. Every line in “dict”, “json”, “rawdict”, “rawjson” will contain exactly one span.

TEXT_MEDIABOX_CLIP[¶](#TEXT_MEDIABOX_CLIP)

64 – Characters entirely outside a page’s **mediabox** or contained in other “clipped” areas will be ignored. This is default in PyMuPDF.

TEXT_USE_CID_FOR_UNKNOWN_UNICODE[¶](#TEXT_USE_CID_FOR_UNKNOWN_UNICODE)

128 – Use raw character codes instead of U+FFFD. This is the default for **text extraction** in PyMuPDF. If you **want to detect** when encoding information is missing or uncertain, toggle this flag and scan for the presence of U+FFFD (= `chr(0xfffd)`) code points in the resulting text.

TEXT_COLLECT_STRUCTURE[¶](#TEXT_COLLECT_STRUCTURE)

256 – Extract or generate the [Document](document.html#document) structure. Detail documentation pending.

TEXT_ACCURATE_BBOXES[¶](#TEXT_ACCURATE_BBOXES)

512 – Ignore metric values of all fonts when computing character boundary boxes – most prominently the [ascender](https://en.wikipedia.org/wiki/Ascender_(typography)) and [descender](https://en.wikipedia.org/wiki/Descender) values. Instead, follow the drawing commands of each character’s glyph and compute their rectangle hull as the bbox. This is the smallest rectangle wrapping all points used for drawing the visual appearance - see the [Shape](shape.html#shape) class for understanding the background. This will especially result in individual character heights. For instance a (white) space will have a **bbox of zero height** (because nothing is drawn) – in contrast to the non-zero boundary box generated when using font metrics. This option may be useful to cope with failures of getting meaningful boundary boxes, even for fonts containing errors. Its use will slow down text extraction somewhat because of the incurred computational effort.

Note that this has no effect by default - one must also disable the global quad corrections setting with `pymupdf.TOOLS.unset_quad_corrections(True)`.

TEXT_COLLECT_VECTORS[¶](#TEXT_COLLECT_VECTORS)

1024 – Collect vector drawings into the [TextPage](textpage.html#textpage). These are stored as blocks alongside text and image blocks, depending on other extraction flags. See [`TextPage.extractBLOCKS()`](textpage.html#TextPage.extractBLOCKS) and [`TextPage.extractDICT()`](textpage.html#TextPage.extractDICT) for details. Beyond these two methods, vector graphics extraction is also available for [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON), [`TextPage.extractRAWDICT()`](textpage.html#TextPage.extractRAWDICT), [`TextPage.extractRAWJSON()`](textpage.html#TextPage.extractRAWJSON) and [`TextPage.extractXML()`](textpage.html#TextPage.extractXML).

TEXT_IGNORE_ACTUALTEXT[¶](#TEXT_IGNORE_ACTUALTEXT)

2048 – Ignore built-in differences between text appearing in e.g. PDF viewers versus text stored in the PDF. See [Adobe PDF References](app3.html#adobemanual), page 615 for background. If set, the **stored** (“replacement” text) is ignored in favor of the displayed text.

TEXT_SEGMENT[¶](#TEXT_SEGMENT)

4096 – Attempt to segment page into different regions. Detail documentation pending.

TEXT_COLLECT_STYLES[¶](#TEXT_COLLECT_STYLES)

32768 – Request collecting text **decoration** properties. This includes text underlining and strikeout. In contrast to public awareness, these are not font properties, but are drawn separately as vector graphics or annotations on top of the text. In addition, the flag bit will also cause MuPDF to detect “fake bold” text. In many cases, Document creators **simulate bold** text by printing the same text multiple times with slight offsets. If this flag is set, such text will be marked as bold in the resulting text spans.

TEXT_LAZY_VECTORS[¶](#TEXT_LAZY_VECTORS)

1048576 – Delay vector blocks in the extraction slightly to avoid breaking what would otherwise be continuous lines of text.

The following constants represent the default combinations of the above for text extraction and searching:

TEXTFLAGS_TEXT[¶](#TEXTFLAGS_TEXT)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_WORDS[¶](#TEXTFLAGS_WORDS)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_BLOCKS[¶](#TEXTFLAGS_BLOCKS)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_DICT[¶](#TEXTFLAGS_DICT)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_RAWDICT[¶](#TEXTFLAGS_RAWDICT)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_HTML[¶](#TEXTFLAGS_HTML)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_XHTML[¶](#TEXTFLAGS_XHTML)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_XML[¶](#TEXTFLAGS_XML)

`TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS_SEARCH[¶](#TEXTFLAGS_SEARCH)

`TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_DEHYPHENATE`

## Link Destination Kinds[¶](#link-destination-kinds)

Possible values of [`linkDest.kind`](linkdest.html#linkDest.kind) (link destination kind).

LINK_NONE[¶](#LINK_NONE)

0 – No destination. Indicates a dummy link.

Type:

int

LINK_GOTO[¶](#LINK_GOTO)

1 – Points to a place in this document.

Type:

int

LINK_URI[¶](#LINK_URI)

2 – Points to a URI – typically a resource specified with internet syntax.

- 
PyMuPDF treats any external link that contains a colon and does not start
with `file:`, as [`LINK_URI`](#LINK_URI).

Type:

int

LINK_LAUNCH[¶](#LINK_LAUNCH)

3 – Launch (open) another file (of any “executable” type).

- 
PyMuPDF treats any external link that starts with `file:` or doesn’t
contain a colon, as [`LINK_LAUNCH`](#LINK_LAUNCH).

Type:

int

LINK_NAMED[¶](#LINK_NAMED)

4 – points to a named location.

Type:

int

LINK_GOTOR[¶](#LINK_GOTOR)

5 – Points to a place in another PDF document.

Type:

int

## Link Destination Flags[¶](#link-destination-flags)

Note

The rightmost byte of this integer is a bit field, so test the truth of these bits with the *&* operator.

LINK_FLAG_L_VALID[¶](#LINK_FLAG_L_VALID)

1  (bit 0) Top left x value is valid

Type:

bool

LINK_FLAG_T_VALID[¶](#LINK_FLAG_T_VALID)

2  (bit 1) Top left y value is valid

Type:

bool

LINK_FLAG_R_VALID[¶](#LINK_FLAG_R_VALID)

4  (bit 2) Bottom right x value is valid

Type:

bool

LINK_FLAG_B_VALID[¶](#LINK_FLAG_B_VALID)

8  (bit 3) Bottom right y value is valid

Type:

bool

LINK_FLAG_FIT_H[¶](#LINK_FLAG_FIT_H)

16 (bit 4) Horizontal fit

Type:

bool

LINK_FLAG_FIT_V[¶](#LINK_FLAG_FIT_V)

32 (bit 5) Vertical fit

Type:

bool

LINK_FLAG_R_IS_ZOOM[¶](#LINK_FLAG_R_IS_ZOOM)

64 (bit 6) Bottom right x is a zoom figure

Type:

bool

## Annotation Related Constants[¶](#annotation-related-constants)

See chapter 8.4.5, pp. 615 of the [Adobe PDF References](app3.html#adobemanual) for details.

### Annotation Types[¶](#annotation-types)

These identifiers also cover **links** and **widgets**: the PDF specification technically handles them all in the same way, whereas MuPDF (and PyMuPDF) treats them as three basically different types of objects.

PDF_ANNOT_TEXT 0
PDF_ANNOT_LINK 1  # <=== Link object in PyMuPDF
PDF_ANNOT_FREE_TEXT 2
PDF_ANNOT_LINE 3
PDF_ANNOT_SQUARE 4
PDF_ANNOT_CIRCLE 5
PDF_ANNOT_POLYGON 6
PDF_ANNOT_POLY_LINE 7
PDF_ANNOT_HIGHLIGHT 8
PDF_ANNOT_UNDERLINE 9
PDF_ANNOT_SQUIGGLY 10
PDF_ANNOT_STRIKE_OUT 11
PDF_ANNOT_REDACT 12
PDF_ANNOT_STAMP 13
PDF_ANNOT_CARET 14
PDF_ANNOT_INK 15
PDF_ANNOT_POPUP 16
PDF_ANNOT_FILE_ATTACHMENT 17
PDF_ANNOT_SOUND 18
PDF_ANNOT_MOVIE 19
PDF_ANNOT_RICH_MEDIA 20
PDF_ANNOT_WIDGET 21  # <=== Widget object in PyMuPDF
PDF_ANNOT_SCREEN 22
PDF_ANNOT_PRINTER_MARK 23
PDF_ANNOT_TRAP_NET 24
PDF_ANNOT_WATERMARK 25
PDF_ANNOT_3D 26
PDF_ANNOT_PROJECTION 27
PDF_ANNOT_UNKNOWN -1

### Annotation Flag Bits[¶](#annotation-flag-bits)

PDF_ANNOT_IS_INVISIBLE 1 << (1-1)
PDF_ANNOT_IS_HIDDEN 1 << (2-1)
PDF_ANNOT_IS_PRINT 1 << (3-1)
PDF_ANNOT_IS_NO_ZOOM 1 << (4-1)
PDF_ANNOT_IS_NO_ROTATE 1 << (5-1)
PDF_ANNOT_IS_NO_VIEW 1 << (6-1)
PDF_ANNOT_IS_READ_ONLY 1 << (7-1)
PDF_ANNOT_IS_LOCKED 1 << (8-1)
PDF_ANNOT_IS_TOGGLE_NO_VIEW 1 << (9-1)
PDF_ANNOT_IS_LOCKED_CONTENTS 1 << (10-1)

### Annotation Line Ending Styles[¶](#annotation-line-ending-styles)

PDF_ANNOT_LE_NONE 0
PDF_ANNOT_LE_SQUARE 1
PDF_ANNOT_LE_CIRCLE 2
PDF_ANNOT_LE_DIAMOND 3
PDF_ANNOT_LE_OPEN_ARROW 4
PDF_ANNOT_LE_CLOSED_ARROW 5
PDF_ANNOT_LE_BUTT 6
PDF_ANNOT_LE_R_OPEN_ARROW 7
PDF_ANNOT_LE_R_CLOSED_ARROW 8
PDF_ANNOT_LE_SLASH 9

## Widget Constants[¶](#widget-constants)

### Widget Types (*field_type*)[¶](#widget-types-field-type)

PDF_WIDGET_TYPE_UNKNOWN 0
PDF_WIDGET_TYPE_BUTTON 1
PDF_WIDGET_TYPE_CHECKBOX 2
PDF_WIDGET_TYPE_COMBOBOX 3
PDF_WIDGET_TYPE_LISTBOX 4
PDF_WIDGET_TYPE_RADIOBUTTON 5
PDF_WIDGET_TYPE_SIGNATURE 6
PDF_WIDGET_TYPE_TEXT 7

### Text Widget Subtypes (*text_format*)[¶](#text-widget-subtypes-text-format)

PDF_WIDGET_TX_FORMAT_NONE 0
PDF_WIDGET_TX_FORMAT_NUMBER 1
PDF_WIDGET_TX_FORMAT_SPECIAL 2
PDF_WIDGET_TX_FORMAT_DATE 3
PDF_WIDGET_TX_FORMAT_TIME 4

### Widget flags (*field_flags*)[¶](#widget-flags-field-flags)

**Common to all field types**:

PDF_FIELD_IS_READ_ONLY 1
PDF_FIELD_IS_REQUIRED 1 << 1
PDF_FIELD_IS_NO_EXPORT 1 << 2

**Text widgets**:

PDF_TX_FIELD_IS_MULTILINE  1 << 12
PDF_TX_FIELD_IS_PASSWORD  1 << 13
PDF_TX_FIELD_IS_FILE_SELECT  1 << 20
PDF_TX_FIELD_IS_DO_NOT_SPELL_CHECK  1 << 22
PDF_TX_FIELD_IS_DO_NOT_SCROLL  1 << 23
PDF_TX_FIELD_IS_COMB  1 << 24
PDF_TX_FIELD_IS_RICH_TEXT  1 << 25

**Button widgets**:

PDF_BTN_FIELD_IS_NO_TOGGLE_TO_OFF  1 << 14
PDF_BTN_FIELD_IS_RADIO  1 << 15
PDF_BTN_FIELD_IS_PUSHBUTTON  1 << 16
PDF_BTN_FIELD_IS_RADIOS_IN_UNISON  1 << 25

**Choice widgets**:

PDF_CH_FIELD_IS_COMBO  1 << 17
PDF_CH_FIELD_IS_EDIT  1 << 18
PDF_CH_FIELD_IS_SORT  1 << 19
PDF_CH_FIELD_IS_MULTI_SELECT  1 << 21
PDF_CH_FIELD_IS_DO_NOT_SPELL_CHECK  1 << 22
PDF_CH_FIELD_IS_COMMIT_ON_SEL_CHANGE  1 << 26

## PDF Standard Blend Modes[¶](#pdf-standard-blend-modes)

For an explanation see [Adobe PDF References](app3.html#adobemanual), page 324:

PDF_BM_Color "Color"
PDF_BM_ColorBurn "ColorBurn"
PDF_BM_ColorDodge "ColorDodge"
PDF_BM_Darken "Darken"
PDF_BM_Difference "Difference"
PDF_BM_Exclusion "Exclusion"
PDF_BM_HardLight "HardLight"
PDF_BM_Hue "Hue"
PDF_BM_Lighten "Lighten"
PDF_BM_Luminosity "Luminosity"
PDF_BM_Multiply "Multiply"
PDF_BM_Normal "Normal"
PDF_BM_Overlay "Overlay"
PDF_BM_Saturation "Saturation"
PDF_BM_Screen "Screen"
PDF_BM_SoftLight "Softlight"

## Stamp Annotation Icons[¶](#stamp-annotation-icons)

MuPDF has defined the following icons for **rubber stamp** annotations:

STAMP_Approved 0
STAMP_AsIs 1
STAMP_Confidential 2
STAMP_Departmental 3
STAMP_Experimental 4
STAMP_Expired 5
STAMP_Final 6
STAMP_ForComment 7
STAMP_ForPublicRelease 8
STAMP_NotApproved 9
STAMP_NotForPublicRelease 10
STAMP_Sold 11
STAMP_TopSecret 12
STAMP_Draft 13

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

This documentation covers all versions up to 1.27.1.

        
      
      
        
        
          
              
                
                  Next
                
                Color Database
              
              
            
          
              
              
                
                  Previous
                
                
                Glossary
                
              
            
        
        
          
            
                Copyright © 2015-2026, Artifex
            
            Made with 
            [Furo](https://github.com/pradyunsg/furo)
            
              Last updated on 16. Feb 2026
          
          
            
          
        
        
      
    
    
      
      
      
        
          
            On this page
          
        
        
          
            

- [Constants and Enumerations](#)

- [Constants](#constants)

- [`Base14_Fonts`](#Base14_Fonts)

- [`csRGB`](#csRGB)

- [`csGRAY`](#csGRAY)

- [`csCMYK`](#csCMYK)

- [`CS_RGB`](#CS_RGB)

- [`CS_GRAY`](#CS_GRAY)

- [`CS_CMYK`](#CS_CMYK)

- [`mupdf_version`](#mupdf_version)

- [`mupdf_version_tuple`](#mupdf_version_tuple)

- [`pymupdf_version`](#pymupdf_version)

- [`pymupdf_version_tuple`](#pymupdf_version_tuple)

- [`pymupdf_date`](#pymupdf_date)

- [`version`](#version)

- [`VersionBind`](#VersionBind)

- [`VersionFitz`](#VersionFitz)

- [`VersionDate`](#VersionDate)

- [Document Permissions](#document-permissions)

- [PDF Optional Content Codes](#pdf-optional-content-codes)

- [PDF encryption method codes](#pdf-encryption-method-codes)

- [Font File Extensions](#font-file-extensions)

- [Text Alignment](#text-alignment)

- [`TEXT_ALIGN_LEFT`](#TEXT_ALIGN_LEFT)

- [`TEXT_ALIGN_CENTER`](#TEXT_ALIGN_CENTER)

- [`TEXT_ALIGN_RIGHT`](#TEXT_ALIGN_RIGHT)

- [`TEXT_ALIGN_JUSTIFY`](#TEXT_ALIGN_JUSTIFY)

- [Font Properties](#font-properties)

- [`TEXT_FONT_SUPERSCRIPT`](#TEXT_FONT_SUPERSCRIPT)

- [`TEXT_FONT_ITALIC`](#TEXT_FONT_ITALIC)

- [`TEXT_FONT_SERIFED`](#TEXT_FONT_SERIFED)

- [`TEXT_FONT_MONOSPACED`](#TEXT_FONT_MONOSPACED)

- [`TEXT_FONT_BOLD`](#TEXT_FONT_BOLD)

- [Text Extraction Flags](#text-extraction-flags)

- [`TEXT_PRESERVE_LIGATURES`](#TEXT_PRESERVE_LIGATURES)

- [`TEXT_PRESERVE_WHITESPACE`](#TEXT_PRESERVE_WHITESPACE)

- [`TEXT_PRESERVE_IMAGES`](#TEXT_PRESERVE_IMAGES)

- [`TEXT_INHIBIT_SPACES`](#TEXT_INHIBIT_SPACES)

- [`TEXT_DEHYPHENATE`](#TEXT_DEHYPHENATE)

- [`TEXT_PRESERVE_SPANS`](#TEXT_PRESERVE_SPANS)

- [`TEXT_MEDIABOX_CLIP`](#TEXT_MEDIABOX_CLIP)

- [`TEXT_USE_CID_FOR_UNKNOWN_UNICODE`](#TEXT_USE_CID_FOR_UNKNOWN_UNICODE)

- [`TEXT_COLLECT_STRUCTURE`](#TEXT_COLLECT_STRUCTURE)

- [`TEXT_ACCURATE_BBOXES`](#TEXT_ACCURATE_BBOXES)

- [`TEXT_COLLECT_VECTORS`](#TEXT_COLLECT_VECTORS)

- [`TEXT_IGNORE_ACTUALTEXT`](#TEXT_IGNORE_ACTUALTEXT)

- [`TEXT_SEGMENT`](#TEXT_SEGMENT)

- [`TEXT_COLLECT_STYLES`](#TEXT_COLLECT_STYLES)

- [`TEXT_LAZY_VECTORS`](#TEXT_LAZY_VECTORS)

- [`TEXTFLAGS_TEXT`](#TEXTFLAGS_TEXT)

- [`TEXTFLAGS_WORDS`](#TEXTFLAGS_WORDS)

- [`TEXTFLAGS_BLOCKS`](#TEXTFLAGS_BLOCKS)

- [`TEXTFLAGS_DICT`](#TEXTFLAGS_DICT)

- [`TEXTFLAGS_RAWDICT`](#TEXTFLAGS_RAWDICT)

- [`TEXTFLAGS_HTML`](#TEXTFLAGS_HTML)

- [`TEXTFLAGS_XHTML`](#TEXTFLAGS_XHTML)

- [`TEXTFLAGS_XML`](#TEXTFLAGS_XML)

- [`TEXTFLAGS_SEARCH`](#TEXTFLAGS_SEARCH)

- [Link Destination Kinds](#link-destination-kinds)

- [`LINK_NONE`](#LINK_NONE)

- [`LINK_GOTO`](#LINK_GOTO)

- [`LINK_URI`](#LINK_URI)

- [`LINK_LAUNCH`](#LINK_LAUNCH)

- [`LINK_NAMED`](#LINK_NAMED)

- [`LINK_GOTOR`](#LINK_GOTOR)

- [Link Destination Flags](#link-destination-flags)

- [`LINK_FLAG_L_VALID`](#LINK_FLAG_L_VALID)

- [`LINK_FLAG_T_VALID`](#LINK_FLAG_T_VALID)

- [`LINK_FLAG_R_VALID`](#LINK_FLAG_R_VALID)

- [`LINK_FLAG_B_VALID`](#LINK_FLAG_B_VALID)

- [`LINK_FLAG_FIT_H`](#LINK_FLAG_FIT_H)

- [`LINK_FLAG_FIT_V`](#LINK_FLAG_FIT_V)

- [`LINK_FLAG_R_IS_ZOOM`](#LINK_FLAG_R_IS_ZOOM)

- [Annotation Related Constants](#annotation-related-constants)

- [Annotation Types](#annotation-types)

- [Annotation Flag Bits](#annotation-flag-bits)

- [Annotation Line Ending Styles](#annotation-line-ending-styles)

- [Widget Constants](#widget-constants)

- [Widget Types (*field_type*)](#widget-types-field-type)

- [Text Widget Subtypes (*text_format*)](#text-widget-subtypes-text-format)

- [Widget flags (*field_flags*)](#widget-flags-field-flags)

- [PDF Standard Blend Modes](#pdf-standard-blend-modes)

- [Stamp Annotation Icons](#stamp-annotation-icons)
