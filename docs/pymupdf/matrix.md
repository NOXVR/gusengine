# Source: https://pymupdf.readthedocs.io/en/latest/matrix.html
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
        Matrix - PyMuPDF documentation
      
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

- [Matrix](#)

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
    

# Matrix[¶](#matrix)

Matrix is a row-major 3x3 matrix used by image transformations in MuPDF (which complies with the respective concepts laid down in the [Adobe PDF References](app3.html#adobemanual)). With matrices you can manipulate the rendered image of a page in a variety of ways: (parts of) the page can be rotated, zoomed, flipped, sheared and shifted by setting some or all of just six float values.

Since all points or pixels live in a two-dimensional space, one column vector of that matrix is a constant unit vector, and only the remaining six elements are used for manipulations. These six elements are usually represented by `[a, b, c, d, e, f]`. Here is how they are positioned in the matrix:

Please note:

- 
the below methods are just convenience functions – everything they do, can also be achieved by directly manipulating the six numerical values

- 
all manipulations can be combined – you can construct a matrix that rotates **and** shears **and** scales **and** shifts, etc. in one go. If you however choose to do this, do have a look at the **remarks** further down or at the [Adobe PDF References](app3.html#adobemanual).

**Method / Attribute**

**Description**

[`Matrix.prerotate()`](#Matrix.prerotate)

perform a rotation

[`Matrix.prescale()`](#Matrix.prescale)

perform a scaling

[`Matrix.preshear()`](#Matrix.preshear)

perform a shearing (skewing)

[`Matrix.pretranslate()`](#Matrix.pretranslate)

perform a translation (shifting)

[`Matrix.concat()`](#Matrix.concat)

perform a matrix multiplication

[`Matrix.invert()`](#Matrix.invert)

calculate the inverted matrix

[`Matrix.norm()`](#Matrix.norm)

the Euclidean norm

[`Matrix.a`](#Matrix.a)

zoom factor X direction

[`Matrix.b`](#Matrix.b)

shearing effect Y direction

[`Matrix.c`](#Matrix.c)

shearing effect X direction

[`Matrix.d`](#Matrix.d)

zoom factor Y direction

[`Matrix.e`](#Matrix.e)

horizontal shift

[`Matrix.f`](#Matrix.f)

vertical shift

[`Matrix.is_rectilinear`](#Matrix.is_rectilinear)

true if rect corners will remain rect corners

**Class API**

class Matrix[¶](#Matrix)

__init__(self)[¶](#Matrix.__init__)

__init__(self, zoom-x, zoom-y)[¶](#id0)

__init__(self, shear-x, shear-y, 1)[¶](#id2)

__init__(self, a, b, c, d, e, f)[¶](#id3)

__init__(self, matrix)[¶](#id4)

__init__(self, degree)[¶](#id5)

__init__(self, sequence)[¶](#id6)

Overloaded constructors.

Without parameters, the zero matrix *Matrix(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)* will be created.

*zoom-** and *shear-** specify zoom or shear values (float) and create a zoom or shear matrix, respectively.

For “matrix” a **new copy** of another matrix will be made.

Float value “degree” specifies the creation of a rotation matrix which rotates anti-clockwise.

A “sequence” must be any Python sequence object with exactly 6 float entries (see [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes)).

*pymupdf.Matrix(1, 1)* and *pymupdf.Matrix(pymupdf.Identity)* create modifiable versions of the [Identity](identity.html#identity) matrix, which looks like *[1, 0, 0, 1, 0, 0]*.

norm()[¶](#Matrix.norm)

- 
New in version 1.16.0

Return the Euclidean norm of the matrix as a vector.

prerotate(deg)[¶](#Matrix.prerotate)

Modify the matrix to perform a counter-clockwise rotation for positive *deg* degrees, else clockwise. The matrix elements of an identity matrix will change in the following way:

*[1, 0, 0, 1, 0, 0] -> [cos(deg), sin(deg), -sin(deg), cos(deg), 0, 0]*.

Parameters:

**deg** (*float*) – The rotation angle in degrees (use conventional notation based on Pi = 180 degrees).

prescale(sx, sy)[¶](#Matrix.prescale)

Modify the matrix to scale by the zoom factors sx and sy. Has effects on attributes *a* thru *d* only: *[a, b, c, d, e, f] -> [a*sx, b*sx, c*sy, d*sy, e, f]*.

Parameters:

- 
**sx** (*float*) – Zoom factor in X direction. For the effect see description of attribute *a*.

- 
**sy** (*float*) – Zoom factor in Y direction. For the effect see description of attribute *d*.

preshear(sx, sy)[¶](#Matrix.preshear)

Modify the matrix to perform a shearing, i.e. transformation of rectangles into parallelograms (rhomboids). Has effects on attributes *a* thru *d* only: *[a, b, c, d, e, f] -> [c*sy, d*sy, a*sx, b*sx, e, f]*.

Parameters:

- 
**sx** (*float*) – Shearing effect in X direction. See attribute *c*.

- 
**sy** (*float*) – Shearing effect in Y direction. See attribute *b*.

pretranslate(tx, ty)[¶](#Matrix.pretranslate)

Modify the matrix to perform a shifting / translation operation along the x and / or y axis. Has effects on attributes *e* and *f* only: *[a, b, c, d, e, f] -> [a, b, c, d, tx*a + ty*c, tx*b + ty*d]*.

Parameters:

- 
**tx** (*float*) – Translation effect in X direction. See attribute *e*.

- 
**ty** (*float*) – Translation effect in Y direction. See attribute *f*.

concat(m1, m2)[¶](#Matrix.concat)

Calculate the matrix product *m1 * m2* and store the result in the current matrix. Any of *m1* or *m2* may be the current matrix. Be aware that matrix multiplication is not commutative. So the sequence of *m1*, *m2* is important.

Parameters:

- 
**m1** ([Matrix](#matrix)) – First (left) matrix.

- 
**m2** ([Matrix](#matrix)) – Second (right) matrix.

invert(m=None)[¶](#Matrix.invert)

Calculate the matrix inverse of *m* and store the result in the current matrix. Returns *1* if *m* is not invertible (“degenerate”). In this case the current matrix **will not change**. Returns *0* if *m* is invertible, and the current matrix is replaced with the inverted *m*.

Parameters:

**m** ([Matrix](#matrix)) – Matrix to be inverted. If not provided, the current matrix will be used.

Return type:

int

a[¶](#Matrix.a)

Scaling in X-direction **(width)**. For example, a value of 0.5 performs a shrink of the **width** by a factor of 2. If a < 0, a left-right flip will (additionally) occur.

Type:

float

b[¶](#Matrix.b)

Causes a shearing effect: each `Point(x, y)` will become `Point(x, y - b*x)`. Therefore, horizontal lines will be “tilt”.

Type:

float

c[¶](#Matrix.c)

Causes a shearing effect: each `Point(x, y)` will become `Point(x - c*y, y)`. Therefore, vertical lines will be “tilt”.

Type:

float

d[¶](#Matrix.d)

Scaling in Y-direction **(height)**. For example, a value of 1.5 performs a stretch of the **height** by 50%. If d < 0, an up-down flip will (additionally) occur.

Type:

float

e[¶](#Matrix.e)

Causes a horizontal shift effect: Each *Point(x, y)* will become *Point(x + e, y)*. Positive (negative) values of *e* will shift right (left).

Type:

float

f[¶](#Matrix.f)

Causes a vertical shift effect: Each *Point(x, y)* will become *Point(x, y - f)*. Positive (negative) values of *f* will shift down (up).

Type:

float

is_rectilinear[¶](#Matrix.is_rectilinear)

Rectilinear means that no shearing is present and that any rotations are integer multiples of 90 degrees. Usually this is used to confirm that (axis-aligned) rectangles before the transformation are still axis-aligned rectangles afterwards.

Type:

bool

Note

- 
This class adheres to the Python sequence protocol, so components can be accessed via their index, too. Also refer to [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes).

- 
Matrices can be used with arithmetic operators almost like ordinary numbers: they can be added, subtracted, multiplied or divided – see chapter [Operator Algebra for Geometry Objects](algebra.html#algebra).

- 
Matrix multiplication is **not commutative** – changing the sequence of the multiplicands will change the result in general. So it can quickly become unclear which result a transformation will yield.

## Examples[¶](#examples)

Here are examples that illustrate some of the achievable effects. All pictures show some text, inserted under control of some matrix and relative to a fixed reference point (the red dot).

- 
The [Identity](identity.html#identity) matrix performs no operation.

- 
The scaling matrix `Matrix(2, 0.5)` stretches by a factor of 2 in horizontal, and shrinks by factor 0.5 in vertical direction.

- 
Attributes [`Matrix.e`](#Matrix.e) and [`Matrix.f`](#Matrix.f) shift horizontally and, respectively vertically. In the following 10 to the right and 20 down.

- 
A negative [`Matrix.a`](#Matrix.a) causes a left-right flip.

- 
A negative [`Matrix.d`](#Matrix.d) causes an up-down flip.

- 
Attribute [`Matrix.b`](#Matrix.b) tilts upwards / downwards along the x-axis.

- 
Attribute [`Matrix.c`](#Matrix.c) tilts left / right along the y-axis.

- 
Matrix `Matrix(beta)` performs counterclockwise rotations for positive angles `beta`.

- 
Show some effects on a rectangle:

import pymupdf

# just definitions and a temp PDF
RED = (1, 0, 0)
BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
doc = pymupdf.open()
page = doc.new_page()

# rectangle
r1 = pymupdf.Rect(100, 100, 200, 200)

# scales down by 50% in x- and up by 50% in y-direction
mat1 = pymupdf.Matrix(0.5, 1.5)

# shifts by 50 in both directions
mat2 = pymupdf.Matrix(1, 0, 0, 1, 50, 50)

# draw corresponding rectangles
page.draw_rect(r1, color=RED)  # original
page.draw_rect(r1 * mat1, color=GREEN)  # scaled
page.draw_rect(r1 * mat2, color=BLUE)  # shifted
doc.ez_save("matrix-effects.pdf")

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

This documentation covers all versions up to 1.27.1.

        
      
      
        
        
          
              
                
                  Next
                
                Outline
              
              
            
          
              
              
                
                  Previous
                
                
                linkDest
                
              
            
        
        
          
            
                Copyright © 2015-2026, Artifex
            
            Made with 
            [Furo](https://github.com/pradyunsg/furo)
            
              Last updated on 16. Feb 2026
          
          
            
          
        
        
      
    
    
      
      
      
        
          
            On this page
          
        
        
          
            

- [Matrix](#)

- [`Matrix`](#Matrix)

- [`Matrix.__init__()`](#Matrix.__init__)

- [`Matrix.__init__()`](#id0)

- [`Matrix.__init__()`](#id2)

- [`Matrix.__init__()`](#id3)

- [`Matrix.__init__()`](#id4)

- [`Matrix.__init__()`](#id5)

- [`Matrix.__init__()`](#id6)

- [`Matrix.norm()`](#Matrix.norm)

- [`Matrix.prerotate()`](#Matrix.prerotate)

- [`Matrix.prescale()`](#Matrix.prescale)

- [`Matrix.preshear()`](#Matrix.preshear)

- [`Matrix.pretranslate()`](#Matrix.pretranslate)

- [`Matrix.concat()`](#Matrix.concat)

- [`Matrix.invert()`](#Matrix.invert)

- [`Matrix.a`](#Matrix.a)

- [`Matrix.b`](#Matrix.b)

- [`Matrix.c`](#Matrix.c)

- [`Matrix.d`](#Matrix.d)

- [`Matrix.e`](#Matrix.e)

- [`Matrix.f`](#Matrix.f)

- [`Matrix.is_rectilinear`](#Matrix.is_rectilinear)

- [Examples](#examples)
