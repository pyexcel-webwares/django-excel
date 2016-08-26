{%extends 'WEB-README.rst.jj2' %}

{%block header %}
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

{%endblock%}

{%block setup%}
Setup
======

You will need to update your *settings.py*:

.. code-block:: python

    FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                            "django_excel.TemporaryExcelFileUploadHandler")

{%endblock%}


{% block usage %}
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
{% endblock %}
