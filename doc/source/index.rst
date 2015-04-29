.. django-excel documentation master file, created by
   sphinx-quickstart on Tue Jan 27 08:20:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-excel's documentation!
========================================

:Author: C.W.
:Source code: http://github.com/chfw/django-excel
:Issues: http://github.com/chfw/django-excel/issues
:License: New BSD License
:Version: |version|
:Generated: |today|

**django-excel** is based on `pyexcel <https://github.com/chfw/pyexcel>`_ and makes it easy to consume/produce information stored in excel files over HTTP protocol as well as on file system. This library can turn the excel data into Pythonic a list of lists, a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it lets you focus on data in Django web development, instead of file formats.

The highlighted features are:

#. excel data import into and export from databases
#. turn uploaded excel file directly into Python data struture
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via the following plugins:

.. _file-format-list:

.. table:: A list of file formats supported by external plugins

   ================ ========================================================================
   Plugins          Supported file formats                                      
   ================ ========================================================================
   `xls`_           xls, xlsx(r), xlsm(r)
   `xlsx`_          xlsx
   `ods`_           ods (python 2.6, 2.7)                                       
   `ods3`_          ods (python 2.7, 3.3, 3.4)                                  
   ================ ========================================================================
   
.. _xls: https://github.com/chfw/pyexcel-xls
.. _xlsx: https://github.com/chfw/pyexcel-xlsx
.. _ods: https://github.com/chfw/pyexcel-ods
.. _ods3: https://github.com/chfw/pyexcel-ods3
.. _text: https://github.com/chfw/pyexcel-text

This library makes infomation processing involving various excel files as easy as processing array, dictionary when processing file upload/download, data import into and export from SQL databases, information analysis and persistence. It uses **pyexcel** and its plugins: 1) to provide one uniform programming interface to handle csv, tsv, xls, xlsx, xlsm and ods formats. 2) to provide one-stop utility to import the data in uploaded file into a database and to export tables in a database as excel files for file download 3) to provide the same interface for information persistence at server side: saving a uploaded excel file to and loading a saved excel file from file system.


Installation
--------------
You can install it via pip::

    $ pip install django-excel


or clone it and install it::

    $ git clone http://github.com/chfw/django-pyexcel.git
    $ cd django-excel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Setup
---------

You will need to update your *settings.py*::

    FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                            "django_excel.TemporaryExcelFileUploadHandler")


Tutorial
--------------

In order to dive in django-excel and get hands-on experience quickly, the test application for django-excel will be introduced here. So, it is advisable that you should check out the code from `github <https://github.com/chfw/django-excel>`_ ::

    git clone https://github.com/chfw/django-excel.git

The test application is written according to `Part 1 <https://docs.djangoproject.com/en/1.7/intro/tutorial01/>`_, `Part 2 <https://docs.djangoproject.com/en/1.7/intro/tutorial02/>`_ and `Part 3 <https://docs.djangoproject.com/en/1.7/intro/tutorial03/>`_ of django tutorial version 1.7.1. If you should wonder how the test application was written, please visit django documentation and come back.

Once you have the code, please change to django-excel directory and then install all dependencies::

    $ cd django-excel
    $ pip install -r requirements.txt
    $ pip install -r test_requirements.txt

Then run the test application::
   
    $ python manage.py runserver
    Performing system checks...
    
    System check identified no issues (0 silenced).
    January 29, 2015 - 18:11:06
    Django version 1.7.1, using settings 'mysite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.


Handle excel file upload and download
++++++++++++++++++++++++++++++++++++++

This example shows how to process uploaded excel file and how to make data download as an excel file. Open your browser and visit http://localhost:8000/polls/upload, you shall see this upload form:

.. image :: upload-form.png

Choose an excel sheet, for example an xls file, and press "Submit". You will get a csv file for download.

.. image :: download-file.png

Please open the file `polls/views.py <https://github.com/chfw/django-excel/blob/master/polls/views.py#L27>`_ and focus on the following code section::

    class UploadFileForm(forms.Form):
        file = forms.FileField()
    
    # Create your views here.
    def upload(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filehandle = request.FILES['file']
                return excel.make_response(filehandle.get_sheet(), "csv")
        else:
            form = UploadFileForm()
        return render_to_response('upload_form.html', {'form': form}, context_instance=RequestContext(request))

**UploadFileForm** is html widget for file upload form in the html page. Then look down at **filehandle**. It is an instance of either ExcelInMemoryUploadedFile or TemporaryUploadedExcelFile, which inherit ExcelMixin and hence have a list of conversion methods to call, such as get_sheet, get_array, etc.

For the response, :meth:`~django_excel.make_response` converts :class:`pyexcel.Sheet` instance obtained via :meth:`~django_excel.ExcelMixin.get_sheet` into a csv file for download.

Please feel free to change those functions according to :ref:`the mapping table <data-types-and-its-conversion-funcs>`.

Handle data import
++++++++++++++++++++++++++++++

This example shows how to import uploaded excel file into django models. We are going to import `sample-data.xls <https://github.com/chfw/django-excel/blob/master/sample-data.xls>`_

.. table:: Sheet 1 of sample-data.xls

    ============================================    ============    =================
    Question Text                                   Publish Date    Unique Identifier
    ============================================    ============    =================
    What is your favourite programming language?    28/01/15        language
    What is your favourite IDE?                     29/01/15        ide
    ============================================    ============    =================

.. table:: Sheet 2 of sample-data.xls

    ==========  ==============  ======         
    Question    Choice          Votes
    ==========  ==============  ======         
    language    Java            0
    language    C++             0
    language    C               0
    ide         Eclipse         0
    ide         Visual Studio   0
    ide         PyCharm         0
    ide         IntelliJ        0
    ==========  ==============  ======

into the following data models::
    
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        slug = models.CharField(max_length=10, unique=True, default="question")
    
    
    class Choice(models.Model):
        question = models.ForeignKey(Question)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

.. note::
   Except the added "slug" field, **Question** and **Choice** are copied from Django tutoial part 1.

Please visit this link http://localhost:8000/polls/import/, you shall see this upload form:

.. image:: import-page.png

Please then select `sample-data.xls <https://github.com/chfw/django-excel/blob/master/sample-data.xls>`_ and upload. Then visit the admin page http://localhost:8000/admin/polls/question, you shall see questions have been populated:

.. image:: question-admin.png

.. note::
   The admin user credentials are: user name: admin, password: admin

And choices too:

.. image:: choice-admin.png

You may use admin interface to delete all those objects and try again. 

Now please open `polls/views.py <https://github.com/chfw/django-excel/blob/master/polls/views.py#L54>`_ and focus on this part of code::

    def import_data(request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            def choice_func(row):
                print row[0]
                q = Question.objects.filter(slug=row[0])[0]
                row[0] = q
                return row
            if form.is_valid():
                request.FILES['file'].save_book_to_database(
                    models=[
                        (Question, ['question_text', 'pub_date', 'slug'], None, 0),
                        (Choice, ['question', 'choice_text', 'votes'], choice_func, 0) 
                     ]
                    )
                return HttpResponse("OK", status=200)
            else:
                return HttpResponseBadRequest()
        else:
        ...

The star is :meth:`~django_excel.save_book_to_database`. The parameter **models** can be a list of django models or a list of tuples, each of which contains:

1. django model (**compulsory**)
2. an array of model fields or a dicionary of key maps
3. custom formating fuction
4. the index of the row that has the field names
5. the index of the column that has the field names

When an array of model fields is supplied in the second member in the tuple, the names of the supplied fields should match the field names of the corresponding django model(the first member in the tuple) and the sequence of the supplied fields shall match the one in the uploaded excel sheet. For example::

    (Question, ['question_text', 'pub_date', 'slug'], None, 0)

When a dictionary of key maps is supplied, its keys should be the field names in the uploaded excel sheet and the value should be the actual field name in the corresponding django model. For example::

    (Question,{"Question Text": "question_text",
              "Publish Date": "pub_date",
              "Unique Identifier": "slug"}, None, 0)

The custom formatting function is needed when the data from the excel sheet needs translation before data import. For example, **Choice** has a foreign key to **Question**. When choice data are to be imported, "Question" column needs to be translated to a question instance. In our example, "Question" column in "Sheet 2" contains the values appeared in "Unique Identifier" column in "Sheet 1".

Handle data export
++++++++++++++++++++++++++++++

This section shows how to export the data in your models as an excel file. After you have completed the previous section, you can visit http://localhost:8000/polls/export/book and you shall get a file download dialog:

.. image:: download-dialog.png

Please save and open it. You shall see these data in your window:

.. image:: question-sheet.png
.. image:: choice-sheet.png

Now let's examine the code behind this in `polls/views.py <https://github.com/chfw/django-excel/blob/master/polls/views.py#L48>`_::

    def export_data(request, atype):
        if atype == "sheet":
            return excel.make_response_from_a_table(Question, 'xls')
        elif atype == "book":
            return excel.make_response_from_tables([Question, Choice], 'xls')
        
:meth:`~django_excel.make_response_from_tables` does all what is needed: read out the data, convert them into xls and give it the browser. And what you need to do is to give a list of models to be exported and a file type. As you have noticed, you can visit http://localhost:8000/polls/export/sheet and will get **Question** exported as a single sheet file.

Handle custom data export
+++++++++++++++++++++++++++++++

It is also quite common to download a portion of the data in a database table, for example the result of a search query. With version 0.0.2, you can pass on a query sets to to :meth:`~django_excel.make_response_from_query_sets` and generate an excel sheet from it::

    def export_data(request, atype):
	    ...
        elif atype == "custom":
            question = Question.objects.get(slug='ide')
            query_sets = Choice.objects.filter(question=question)
            column_names = ['choice_text', 'id', 'votes']
            return excel.make_response_from_query_sets(query_sets, column_names, 'xls')

You can visit http://localhost:8000/polls/export/custom and will get the query set exported as a single sheet file as:

.. image:: custom-export.png

.. _data-types-and-its-conversion-funcs:

All supported data types
--------------------------

Here is table of functions for all supported data types:

=========================== ======================================================== ===================================================
data structure              from file to data structures                             from data structures to response
=========================== ======================================================== ===================================================
dict                        :meth:`~django_excel.ExcelMixin.get_dict`                :meth:`~django_excel.make_response_from_dict`
records                     :meth:`~django_excel.ExcelMixin.get_records`             :meth:`~django_excel.make_response_from_records`
a list of lists             :meth:`~django_excel.ExcelMixin.get_array`               :meth:`~django_excel.make_response_from_array`
dict of a list of lists     :meth:`~django_excel.ExcelMixin.get_book_dict`           :meth:`~django_excel.make_response_from_book_dict`
:class:`pyexcel.Sheet`      :meth:`~django_excel.ExcelMixin.get_sheet`               :meth:`~django_excel.make_response`
:class:`pyexcel.Book`       :meth:`~django_excel.ExcelMixin.get_book`                :meth:`~django_excel.make_response`
database table              :meth:`~django_excel.ExcelMixin.save_to_database`        :meth:`~django_excel.make_response_from_a_table` 
a list of database tables   :meth:`~django_excel.ExcelMixin.save_book_to_database`   :meth:`~django_excel.make_response_from_tables`
a database query sets                                                                :meth:`~django_excel.make_response_from_query_sets`
=========================== ======================================================== ===================================================

See more examples of the data structures in :ref:`pyexcel documentation<pyexcel:a-list-of-data-structures>`

API Reference
---------------

**django-excel** attaches **pyexcel** functions to **InMemoryUploadedFile** and **TemporaryUploadedFile**.

.. module:: django_excel

.. autoclass:: ExcelMixin

   .. method:: get_sheet(sheet_name=None, **keywords)

      :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
      :param keywords: additional keywords to :meth:`pyexcel.get_sheet`
      :returns: A sheet object

   .. method:: get_array(sheet_name=None, **keywords)

      :param sheet_name: same as :meth:`~django_excel.ExcelMixin.get_sheet`
      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: get_dict(sheet_name=None, name_columns_by_row=0, **keywords)

      :param sheet_name: same as :meth:`~django_excel.ExcelMixin.get_sheet`
      :param name_columns_by_row: uses the first row of the sheet to be column headers by default.
      :param keywords: additional keywords to pyexcel library
      :returns: a dictionary of the file content

   .. method:: get_records(sheet_name=None, name_columns_by_row=0, **keywords)

      :param sheet_name: same as :meth:`~django_excel.ExcelMixin.get_sheet`
      :param name_columns_by_row: uses the first row of the sheet to be record field names by default.
      :param keywords: additional keywords to pyexcel library
      :returns: a list of dictionary of the file content

   .. method:: get_book(**keywords)

      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: get_book_dict(**keywords)

      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: save_to_database(model=None, initializer=None, mapdict=None, **keywords)

      :param model: a django model
      :param initializer: a custom table initialization function if you have one
      :param mapdict: the explicit table column names if your excel data do not have the exact column names
      :param keywords: additional keywords to :meth:`pyexcel.Sheet.save_to_django_model`

   .. method:: save_book_to_database(models=None, initializers=None, mapdicts=None, **keywords)

      :param models: a list of django models
      :param initializers: a list of model initialization functions.
      :param mapdicts: a list of explicit table column names if your excel data sheets do not have the exact column names
      :param keywords: additional keywords to :meth:`pyexcel.Book.save_to_django_models`

Response methods
-----------------

.. automodule:: django_excel

   .. method:: make_response(pyexcel_instance, file_type, status=200)

      :param pyexcel_instance: :class:`pyexcel.Sheet` or :class:`pyexcel.Book`
      :param file_type: one of the following strings:
                        
                        * 'csv'
                        * 'tsv'
                        * 'csvz'
                        * 'tsvz'
                        * 'xls'
                        * 'xlsx'
                        * 'xlsm'
                        * 'ods'
                          
      :param status: unless a different status is to be returned.
            
   .. method:: make_response_from_array(array, file_type, status=200)

      :param array: a list of lists
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`
            
   .. method:: make_response_from_dict(dict, file_type, status=200)

      :param dict: a dictinary of lists
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`
            
   .. method:: make_response_from_records(records, file_type, status=200)

      :param records: a list of dictionaries
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`
            
                
   .. method:: make_response_from_book_dict(book_dict, file_type, status=200)

      :param book_dict: a dictionary of two dimensional arrays
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`

   .. autofunction:: make_response_from_a_table(model, file_type status=200)


   .. method:: make_response_from_query_sets(query_sets, column_names, file_type status=200)

      Produce a single sheet Excel book of *file_type* from your custom database queries

      :param query_sets: a query set
      :param column_names: a nominated column names. It could not be None, otherwise no data is returned.
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`

   .. autofunction:: make_response_from_tables(models, file_type status=200)

Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
