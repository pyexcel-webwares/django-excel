==============================================================
django-excel - Let you focus on data, instead of file formats
==============================================================

.. image:: https://api.travis-ci.org/chfw/django-excel.svg?branch=master
    :target: http://travis-ci.org/chfw/django-excel

.. image:: https://coveralls.io/repos/chfw/django-excel/badge.svg?branch=master 
    :target: https://coveralls.io/r/chfw/django-excel?branch=master 

.. image:: https://readthedocs.org/projects/django-excel/badge/?version=latest
    :target: http://django-excel.readthedocs.org/en/latest/

.. image:: https://pypip.in/version/django-excel/badge.png
    :target: https://pypi.python.org/pypi/django-excel

.. image:: https://pypip.in/d/django-excel/badge.png
    :target: https://pypi.python.org/pypi/django-excel

.. image:: https://pypip.in/py_versions/django-excel/badge.png
    :target: https://pypi.python.org/pypi/django-excel

.. image:: http://img.shields.io/gittip/chfw.svg
    :target: https://gratipay.com/chfw/

**django-excel** is based on `pyexcel <https://github.com/chfw/pyexcel>`_ and makes it easy to consume/produce information stored in excel files over HTTP protocol as well as on file system. This library can turn the excel data into Pythonic a list of lists, a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it lets you focus on data in Django web development, instead of file formats.

The idea originated from the problem of the illiteracy of excel file formats of non-technical office workers: such as office assistant, human resource administrator. There is nothing with the un-deniable fact that some people do not know the difference among various excel formats. It becomes usability problem to those people when a web service cannot parse the excel file that they saved using Microsoft Excel. Instead of training those people about file formats, this library helps web developers to handle most of the excel file formats by unifying the programming interface to most of the excel readers and writers.

The highlighted features are:

#. turn uploaded excel file directly into Python data struture
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via the following plugins:

Available Plugins
=================

================ ========================================================================
Plugins          Supported file formats                                      
================ ========================================================================
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods`_   ods (python 2.6, 2.7)                                       
`pyexcel-ods3`_  ods (python 2.7, 3.3, 3.4)                                  
`pyexcel-text`_  (write only)json, rst, mediawiki,latex, grid, pipe, orgtbl, plain simple
================ ========================================================================

.. _pyexcel-xls: https://github.com/chfw/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/chfw/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/chfw/pyexcel-ods
.. _pyexcel-ods3: https://github.com/chfw/pyexcel-ods3
.. _pyexcel-text: https://github.com/chfw/pyexcel-text


Known constraints
==================

Fonts, colors and charts are not supported. 

Installation
============
You can install it from github only for now::

    $ pip install git+https://github.com/chfw/pyexcel.git # pyexcel v0.1.3 is not released yet
    $ git clone http://github.com/chfw/django-pyexcel.git
    $ cd django-excel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Setup
======

You will need to update your *settings.py*::

    FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                            "django_excel.TemporaryExcelFileUploadHandler")


Usage
======

Here is the example viewing function codes::

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

Dependencies
=============

* Django
* pyexcel >= 0.1.3
* pyexcel-webio
