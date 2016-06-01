================================================================================
django-excel - Let you focus on data, instead of file formats
================================================================================

.. image:: https://api.travis-ci.org/pyexcel/django-excel.svg?branch=master
   :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://codecov.io/github/pyexcel/django-excel/coverage.png
    :target: https://codecov.io/github/pyexcel/django-excel

.. image:: https://readthedocs.org/projects/django-excel/badge/?version=latest
   :target: http://django-excel.readthedocs.org/en/latest/

**django-excel** is based on `pyexcel <https://github.com/pyexcel/pyexcel>`_ and makes
it easy to consume/produce information stored in excel files over HTTP protocol as
well as on file system. This library can turn the excel data into a list of lists,
a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it
lets you focus on data in Django based web development, instead of file formats.

The idea originated from the common usability problem when developing an excel file
driven web applications for non-technical office workers: such as office assistant,
human resource administrator. It is an un-deniable fact that not all people know the
difference among various excel formats: csv, xls, xlsx. Instead of training those people
about file formats, this library helps web developers to handle most of the excel file
formats by providing a common programming interface.

.. note::
 Here is a typical conversation between the developer and the user::

  User: "I have uploaded an excel file as instructed, but your application says un-supported file format"
  Developer: "Did you upload an xlsx file or a csv file?"
  User: "Well, I am not sure. I saved the data using Microsoft Excel. Surely, it must be in an excel format."

The highlighted features are:

#. excel data import into and export from databases
#. turn uploaded excel file directly into Python data struture
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via
   the following plugins:

.. _file-format-list:

.. table:: A list of file formats supported by external plugins

   ================ ========================================
   Plugins          Supported file formats
   ================ ========================================
   `pyexcel-xls`_   xls, xlsx(r), xlsm(r)
   `pyexcel-xlsx`_  xlsx
   `pyexcel-ods3`_  ods (python 2.6, 2.7, 3.3, 3.4)
   `pyexcel-ods`_   ods (python 2.6, 2.7)
   `pyexcel-text`_  (write only)json, rst, mediawiki, html
                    latex, grid, pipe, orgtbl, plain simple
   ================ ========================================

.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text

This library makes infomation processing involving various excel files as easy as
processing array, dictionary when processing file upload/download, data import into
and export from SQL databases, information analysis and persistence. It uses
**pyexcel** and its plugins:

#. to provide one uniform programming interface to handle csv, tsv, xls, xlsx, xlsm and ods formats.
#. to provide one-stop utility to import the data in uploaded file into a database and to export tables in a database as excel files for file download.
#. to provide the same interface for information persistence at server side: saving a uploaded excel file to and loading a saved excel file from file system.


Known constraints
==================

Fonts, colors and charts are not supported.

Tested Django Versions
========================

.. image:: https://img.shields.io/badge/django-1.9-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.8.2-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

.. image:: https://img.shields.io/badge/django-1.7.8-green.svg
    :target: http://travis-ci.org/pyexcel/django-excel

Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install django-excel


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/django-excel.git
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

License
================================================================================

New BSD License
