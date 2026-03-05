# Source: https://pymupdf.readthedocs.io/en/latest/installation.html
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
        Installation - PyMuPDF documentation
      
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

- [Installation](#)

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
    

# Installation[¶](#installation)

## Requirements[¶](#requirements)

All the examples below assume that you are running inside a Python virtual
environment. See: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html) for details.
We also assume that `pip` is up to date.

For example:

- 
Windows:

py -m venv pymupdf-venv
.\pymupdf-venv\Scripts\activate
python -m pip install --upgrade pip

- 
Linux, MacOS:

python -m venv pymupdf-venv
. pymupdf-venv/bin/activate
python -m pip install --upgrade pip

## Installation[¶](#id1)

PyMuPDF should be installed using pip with:

pip install --upgrade pymupdf

This will install from a Python wheel if one is available for your platform.

## Installation when a suitable wheel is not available[¶](#installation-when-a-suitable-wheel-is-not-available)

If a suitable Python wheel is not available, pip will automatically build from
source using a Python sdist.

**This requires C/C++ development tools to be installed**:

- 
On Windows:

- 
Install Visual Studio 2019. If not installed in a standard location, set
environmental variable `PYMUPDF_SETUP_DEVENV` to the location of the
`devenv.com` binary.

- 
Having other installed versions of Visual Studio, for example Visual Studio
2022, can cause problems because one can end up with MuPDF and PyMuPDF code
being compiled with different compiler versions.

The build will automatically download and build MuPDF.

## Problems after installation[¶](#problems-after-installation)

- 
On Windows, Python error:

ImportError: DLL load failed while importing _extra

This has been occasionally seen if `MSVCP140.dll` is missing, and appears
to be caused by a bug in some versions (2015-2017) of Microsoft Visual C++
Redistributables.

It is recommended to search for `MSVCP140.dll` in [https://msdn.com](https://msdn.com)
to find instructions for how to reinstall it. For example
[https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist) has
permalinks to the latest supported versions.

See [https://github.com/pymupdf/PyMuPDF/issues/2678](https://github.com/pymupdf/PyMuPDF/issues/2678) for more details.

- 
Python error:

ModuleNotFoundError: No module named 'frontend'

This can happen if PyMuPDF’s legacy name `fitz` is used (for example import
fitz instead of `import pymupdf`), and an unrelated Python package called
`fitz` ([https://pypi.org/project/fitz/](https://pypi.org/project/fitz/)) is installed.

The fitz package appears to be no longer maintained (the latest release is
from 2017), but unfortunately it does not seem possible to remove it from
pypi.org. It does not even work on its own, as well as breaking the use of
PyMuPDF’s legacy name.

There are a few ways to avoid this problem:

- 
Use `import pymupdf` instead of `import fitz`, and update one’s code to
match.

- 
Or uninstall the `fitz` package and reinstall PyMuPDF:

pip uninstall fitz
pip install --force-reinstall pymupdf

- 
Or use `import pymupdf as fitz`. However this has not been well tested.

- 
With Jupyter labs on Apple Silicon (arm64), Python error:

ImportError: /opt/conda/lib/python3.11/site-packages/pymupdf/libmupdf.so.24.4: undefined symbol: fz_pclm_write_options_usage

This appears to be a problem in Jupyter labs; see:
[https://github.com/pymupdf/PyMuPDF/issues/3643#issuecomment-2210588778](https://github.com/pymupdf/PyMuPDF/issues/3643#issuecomment-2210588778).

- 
On Windows, Python error:

ImportError: dynamic module does not define module export function (PyInit__extra)

This was reported 2025-03-26 in [https://github.com/pymupdf/PyMuPDF/issues/4405](https://github.com/pymupdf/PyMuPDF/issues/4405).

The fix appears to be to install the latest `VC_redist.x64.exe`.

## Notes[¶](#notes)

- 
Wheels are available for the following platforms:

- 
Windows 32-bit Intel.

- 
Windows 64-bit Intel.

- 
Linux 64-bit Intel.

- 
Linux 64-bit ARM.

- 
MacOS 64-bit Intel.

- 
MacOS 64-bit ARM.

Details:

- 
We release a single wheel for each of the above platforms.

- 
Each wheel uses the Python Stable ABI of the current oldest supported
Python version (currently 3.10), and so works with all later Python
versions, including new Python releases.

- 
Wheels are tested on all Python versions currently marked as “Supported”
on [https://devguide.python.org/versions/](https://devguide.python.org/versions/), currently 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14.

- 
Wheels are not available for Python installed with [Chocolatey](https://chocolatey.org/) on Windows. Instead install Python
using the Windows installer from the python.org website, see:
[http://www.python.org/downloads](http://www.python.org/downloads)

- 
Wheels are not available for Linux-aarch64 with [Musl libc](https://musl.libc.org/) (For example [Alpine Linux](https://alpinelinux.org/) on aarch64), and building from source is known
to fail.

- 
There are no **mandatory** external dependencies. However, some optional feature are available only if additional components are installed:

- 
[Pillow](https://pypi.org/project/Pillow/) is required for [`Pixmap.pil_save()`](pixmap.html#Pixmap.pil_save) and [`Pixmap.pil_tobytes()`](pixmap.html#Pixmap.pil_tobytes).

- 
[fontTools](https://pypi.org/project/fonttools/) is required for [`Document.subset_fonts()`](document.html#Document.subset_fonts).

- 
[pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/) is a collection of nice fonts to be used for text output methods.

- 
[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) for optical
character recognition in images and document pages. Tesseract is separate
software, not a Python package. To enable OCR functions in PyMuPDF,
Tesseract must be installed and the `tessdata` folder name specified; see
below.

Note

You can install these additional components at any time – before or after installing PyMuPDF. PyMuPDF will detect their presence during import or when the respective functions are being used.

## Build and install from a local PyMuPDF source tree[¶](#build-and-install-from-a-local-pymupdf-source-tree)

Initial setup:

- 
Install C/C++ development tools as described above.

- 
Enter a Python venv and update pip, as described above.

- 
Get a PyMuPDF source tree:

- 
Clone the PyMuPDF git repository:

git clone https://github.com/pymupdf/PyMuPDF.git

- 
Or download and extract a `.zip` or `.tar.gz` source release from
[https://github.com/pymupdf/PyMuPDF/releases](https://github.com/pymupdf/PyMuPDF/releases).

Then one can build PyMuPDF in two ways:

- 
Build and install PyMuPDF with default MuPDF version:

cd PyMuPDF && pip install .

This will automatically download a specific hard-coded MuPDF source
release, and build it into PyMuPDF.

- 
Or build and install PyMuPDF using a local MuPDF source tree:

- 
Clone the MuPDF git repository:

git clone --recursive https://git.ghostscript.com/mupdf.git

- 
Build PyMuPDF, specifying the location of the local MuPDF tree with the
environmental variables `PYMUPDF_SETUP_MUPDF_BUILD`:

cd PyMuPDF && PYMUPDF_SETUP_MUPDF_BUILD=../mupdf pip install .

Also, one can build for different Python versions in the same PyMuPDF tree:

- 
PyMuPDF will build for the version of Python that is being used to run
`pip`. To run `pip` with a specific Python version, use `python -m pip`
instead of `pip`.

So for example on Windows one can build different versions with:

cd PyMuPDF && py -3.10 -m pip install .

or:

cd PyMuPDF && py -3.10-32 -m pip install .

## Running tests[¶](#running-tests)

Having a PyMuPDF tree available allows one to run PyMuPDF’s `pytest` test
suite:

pip install pytest fontTools
pytest PyMuPDF/tests

### Notes about using a non-default MuPDF[¶](#notes-about-using-a-non-default-mupdf)

Using a non-default build of MuPDF by setting environmental variable
`PYMUPDF_SETUP_MUPDF_BUILD` can cause various things to go wrong and so is
not generally supported:

- 
If MuPDF’s major version number differs from what PyMuPDF uses by default,
PyMuPDF can fail to build, because MuPDF’s API can change between major
versions.

- 
Runtime behaviour of PyMuPDF can change because MuPDF’s runtime behaviour
changes between different minor releases. This can also break some PyMuPDF
tests.

- 
If MuPDF was built with its default config instead of PyMuPDF’s customised
config (for example if MuPDF is a system install), it is possible that
`tests/test_textbox.py:test_textbox3()` will fail. One can skip this
particular test by adding `-k 'not test_textbox3'` to the `pytest`
command line.

## Official PyMuPDF Linux wheels may not install on older Linux systems[¶](#official-pymupdf-linux-wheels-may-not-install-on-older-linux-systems)

Releases of PyMuPDF are incompatible with older Linux systems.

For example as of 2025-09-03, `pip install pymupdf` does not work on some AWS
Lambda systems - see [https://github.com/pymupdf/PyMuPDF/discussions/4631](https://github.com/pymupdf/PyMuPDF/discussions/4631).

This is because official PyMuPDF Linux wheels are built with a version of
glibc determined by the current Python manylinux environment. These wheels are
incompatible with Linux systems that have an older glibc.

The official Python manylinux environment is updated periodically to use newer
glibc versions, so new releases of PyMuPDF become increasingly incompatible
with older Linux systems.

There is nothing that can be done about this, other than updating older Linux
systems, or building PyMuPDF locally from source.

For more details, please see: [Python Packaging Authority](https://www.pypa.io).

## Packaging[¶](#packaging)

See [Packaging for Linux distributions](packaging.html).

## Using with Pyodide[¶](#using-with-pyodide)

See [Pyodide](pyodide.html).

## Enabling Integrated OCR Support[¶](#enabling-integrated-ocr-support)

If you do not intend to use this feature, skip this step. Otherwise, it is required for both installation paths: **from wheels and from sources.**

PyMuPDF will already contain all the logic to support OCR functions. But it additionally does need [Tesseract’s language support data](https://github.com/tesseract-ocr/tessdata).

If not specified explicitly, PyMuPDF will attempt to find the installed
Tesseract’s tessdata, but this should probably not be relied upon.

Otherwise PyMuPDF requires that Tesseract’s language support folder is
specified explicitly either in PyMuPDF OCR functions’ `tessdata` arguments or
`os.environ["TESSDATA_PREFIX"]`.

So for a working OCR functionality, make sure to complete this checklist:

- 
Locate Tesseract’s language support folder. Typically you will find it here:

- 
Windows: `C:/Program Files/Tesseract-OCR/tessdata`

- 
Unix systems: `/usr/share/tesseract-ocr/4.00/tessdata`

- 
Specify the language support folder when calling PyMuPDF OCR functions:

- 
Set the `tessdata` argument.

- 
Or set `os.environ["TESSDATA_PREFIX"]` from within Python.

- 
Or set environment variable `TESSDATA_PREFIX` before running Python, for example:

- 
Windows: `setx TESSDATA_PREFIX "C:/Program Files/Tesseract-OCR/tessdata"`

- 
Unix systems: `declare -x TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata`

Note

Find out more on the [official documentation for installing Tesseract website](https://tesseract-ocr.github.io/tessdoc/Installation.html).

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

This documentation covers all versions up to 1.27.1.

        
      
      
        
        
          
              
                
                  Next
                
                The Basics
              
              
            
          
              
              
                
                  Previous
                
                
                PyMuPDF Pro
                
              
            
        
        
          
            
                Copyright © 2015-2026, Artifex
            
            Made with 
            [Furo](https://github.com/pradyunsg/furo)
            
              Last updated on 16. Feb 2026
          
          
            
          
        
        
      
    
    
      
      
      
        
          
            On this page
          
        
        
          
            

- [Installation](#)

- [Requirements](#requirements)

- [Installation](#id1)

- [Installation when a suitable wheel is not available](#installation-when-a-suitable-wheel-is-not-available)

- [Problems after installation](#problems-after-installation)

- [Notes](#notes)

- [Build and install from a local PyMuPDF source tree](#build-and-install-from-a-local-pymupdf-source-tree)

- [Running tests](#running-tests)

- [Notes about using a non-default MuPDF](#notes-about-using-a-non-default-mupdf)

- [Official PyMuPDF Linux wheels may not install on older Linux systems](#official-pymupdf-linux-wheels-may-not-install-on-older-linux-systems)

- [Packaging](#packaging)

- [Using with Pyodide](#using-with-pyodide)

- [Enabling Integrated OCR Support](#enabling-integrated-ocr-support)
