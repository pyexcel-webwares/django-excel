================================================================================
django-excel - Let you focus on data, instead of file formats
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/django-excel.svg?branch=master
   :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://codecov.io/github/pyexcel/django-excel/coverage.png
   :target: https://codecov.io/github/pyexcel/django-excel

.. image:: https://readthedocs.org/projects/django-excel/badge/?version=latest
   :target: http://django-excel.readthedocs.org/en/latest/

Known constraints
==================

Fonts, colors and charts are not supported.

Here is a typical conversation between the developer and the user::

 User: "I have uploaded an excel file"
       "but your application says un-supported file format"
 Developer: "Did you upload an xlsx file or a csv file?"
 User: "Well, I am not sure. I saved the data using "
       "Microsoft Excel. Surely, it must be in an excel format."
 Developer: "OK. Here is the thing. I were not told to support"
            "all available excel formats in day 1. Live with it"
            "or delay the project x number of days."

**django-excel** is based on `pyexcel <https://github.com/pyexcel/pyexcel>`_ and makes
it easy to consume/produce information stored in excel files over HTTP protocol as
well as on file system. This library can turn the excel data into a list of lists,
a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it
lets you focus on data in Django based web development, instead of file formats.

The idea originated from the common usability problem when developing an excel file
driven web applications for non-technical office workers: such as office assistant,
human resource administrator. The fact is that not all people know the
difference among various excel formats: csv, xls, xlsx. Instead of training those people
about file formats, this library helps web developers to handle most of the excel file
formats by providing a common programming interface. To add a specific excel file format
to you application, all you need is to install an extra pyexcel plugin. No code change
to your application. Looking at the community, this library and its associated ones try
to become a small and easy to install alternative to Pandas.


The highlighted features are:

#. excel data import into and export from databases
#. turn uploaded excel file directly into Python data structure
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via
   the following plugins:

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ======================== ======================= =============== ==================
   Package name              Supported file formats  Dependencies   Python versions
   ======================== ======================= =============== ==================
   `pyexcel-io`_            csv, csvz [#f1]_, tsv,                  2.6, 2.7, 3.3,
                            tsvz [#f2]_                             3.4, 3.5, 3.6
                                                                    pypy
   `pyexcel-xls`_           xls, xlsx(read only),   `xlrd`_,        same as above
                            xlsm(read only)         `xlwt`_
   `pyexcel-xlsx`_          xlsx                    `openpyxl`_     same as above
   `pyexcel-xlsxw`_         xlsx(write only)        `XlsxWriter`_   same as above
   `pyexcel-ods3`_          ods                     `ezodf`_,       2.6, 2.7, 3.3, 3.4
                                                    lxml            3.5, 3.6
   `pyexcel-ods`_           ods                     `odfpy`_        same as above
   `pyexcel-odsr`_          ods(read only)          lxml            same as above
   `pyexcel-text`_          (write only)json, rst,  `tabulate`_     2.6, 2.7, 3.3, 3.4
                            mediawiki, html,                        3.5, pypy, pypy3
                            latex, grid, pipe,
                            orgtbl, plain simple
   `pyexcel-handsontable`_  handsontable in html    `handsontable`_ same as above
   `pyexcel-chart`_         svg chart               `pygal`_        same as above
   ======================== ======================= =============== ==================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-odsr: https://github.com/pyexcel/pyexcel-odsr
.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw

.. _xlrd: https://github.com/python-excel/xlrd
.. _xlwt: https://github.com/python-excel/xlwt
.. _openpyxl: https://bitbucket.org/openpyxl/openpyxl
.. _XlsxWriter: https://github.com/jmcnamara/XlsxWriter
.. _ezodf: https://github.com/T0ha/ezodf
.. _odfpy: https://github.com/eea/odfpy

.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text
.. _tabulate: https://bitbucket.org/astanin/python-tabulate
.. _pyexcel-handsontable: https://github.com/pyexcel/pyexcel-handsontable
.. _handsontable: https://cdnjs.com/libraries/handsontable
.. _pyexcel-chart: https://github.com/pyexcel/pyexcel-chart
.. _pygal: https://github.com/Kozea/pygal

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file


This library makes information processing involving various excel files as easy as
processing array, dictionary when processing file upload/download, data import into
and export from SQL databases, information analysis and persistence. It uses
**pyexcel** and its plugins:

#. to provide one uniform programming interface to handle csv, tsv, xls, xlsx, xlsm and ods formats.
#. to provide one-stop utility to import the data in uploaded file into a database and to export tables in a database as excel files for file download.
#. to provide the same interface for information persistence at server side: saving a uploaded excel file to and loading a saved excel file from file system.



Tested Django Versions
========================

.. image:: https://img.shields.io/badge/django-1.10-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.9.9-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.8.14-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.7.11-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.6.11-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel


Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install django-excel


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/django-excel.git
    $ cd django-excel
    $ python setup.py install

Setup
======

You will need to update your *settings.py*:

.. code-block:: python

    FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                            "django_excel.TemporaryExcelFileUploadHandler")


Usage
=========
Here is the example viewing function codes:

.. code-block:: python

    from django.shortcuts import render_to_response
    from django.http import HttpResponseBadRequest
    from django import forms
    from django.template import RequestContext
    import django_excel as excel
    
    class UploadFileForm(forms.Form):
        file = forms.FileField()
    
    def upload(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filehandle = request.FILES['file']
                return excel.make_response(filehandle.get_sheet(), "csv")
            else:
                return HttpResponseBadRequest()
        else:
            form = UploadFileForm()
        return render_to_response('upload_form.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
    
    def download(request):
        sheet = excel.pe.Sheet([[1, 2],[3, 4]])
        return excel.make_response(sheet, "csv")

Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please `support me on patreon <https://www.patreon.com/bePatron?u=5537627>`_ to
maintain the project and develop it further.

If you are an individual, you are welcome to support me too on patreon and for however long
you feel like to. As a patreon, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Development guide
================================================================================

Development steps for code changes

#. git clone https://github.com/pyexcel/django-excel.git
#. cd django-excel

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools pip

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt


In order to update test environment, and documentation, additional steps are
required:

#. pip install moban
#. git clone https://github.com/pyexcel/pyexcel-commons.git commons
#. make your changes in `.moban.d` directory, then issue command `moban`

What is rnd_requirements.txt
-------------------------------

Usually, it is created when a dependent library is not released. Once the dependecy is installed(will be released), the future version of the dependency in the requirements.txt will be valid.

What is pyexcel-commons
---------------------------------

Many information that are shared across pyexcel projects, such as: this developer guide, license info, etc. are stored in `pyexcel-commons` project.

What is .moban.d
---------------------------------

`.moban.d` stores the specific meta data for the library.

How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make

On Windows systems, please issue this command::

    > test.bat


License
================================================================================

New BSD License
