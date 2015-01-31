.. django-excel documentation master file, created by
   sphinx-quickstart on Tue Jan 27 08:20:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-excel's documentation!
========================================

**django-excel** is based on `pyexcel <https://github.com/chfw/pyexcel>`_ and makes it easy to consume/produce information stored in excel files over HTTP protocol as well as on file system. This library can turn the excel data into Pythonic a list of lists, a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it lets you focus on data in Flask based web development, instead of file formats.

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

This library make infomation processing involving various excel files as easy as processing array, dictionary when processing file upload/download, data import into and export from SQL databases, information analysis and persistence. It uses **pyexcel** and its plugins: 1) to provide one uniform programming interface to handle csv, tsv, xls, xlsx, xlsm and ods formats. 2) to provide one-stop utility to import the data in uploaded file into a database and to export tables in a database as excel files for file download 3) to provide the same interface for information persistence at server side: saving a uploaded excel file to and loading a saved excel file from file system.

Tutorial
--------------

In order to dive in django-excel and get hands-on experience quickly, the test application for django-excel will be introduced here. So, it is advisable that you should check out the code from `github <https://github.com/chfw/django-excel>`_ ::

    git clone https://github.com/chfw/django-excel.git

The test application is written according to Step 1, Step 2 and Step3 of django tutorial version 1.7.1. If you should wonder how the test application was written, please visit django documentation and come back.

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

This example shows how to process uploaded excel file and how to make data download as an excel file. Open your browser and visit http://localhost:8000/upload, you shall see this upload form:

.. image :: upload-form.png

Choose an excel sheet, for example an xls file, and press "Submit". You will get a csv file for download.

.. image :: download-file.png

Please open the file **polls/views.py** and focus on the following code section::

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

**UploadFileForm** is html widget for file upload form in the html page. Then look down at **filehandle**. It is an instance of either ExcelInMemoryUploadedFile or TemporaryUploadedExcelFile, which inherit ExcelMixin and hence have a list of conversion methods to call, such as get_sheet, get_array, etc. :meth:`~django_excel.make_response` converts :class:`~pyexcel.Sheet` instance obtained via :meth:`~django_excel.ExcelMixin.get_sheet` into a csv file for download. Please feel free to change those functions according to :ref:`the mapping table <data-types-and-its-conversion-funcs>`.

... to be continued ..

.. _data-types-and-its-conversion-funcs:

All supported data types
--------------------------

Here is table of functions for all supported data types:

=========================== ======================================================== ==================================================
data structure              from file to data structures                             from data structures to response
=========================== ======================================================== ==================================================
dict                        :meth:`~django_excel.ExcelMixin.get_dict`                :meth:`~django_excel.make_response_from_dict`
records                     :meth:`~django_excel.ExcelMixin.get_records`             :meth:`~django_excel.make_response_from_records`
a list of lists             :meth:`~django_excel.ExcelMixin.get_array`               :meth:`~django_excel.make_response_from_array`
dict of a list of lists     :meth:`~django_excel.ExcelMixin.get_book_dict`           :meth:`~django_excel.make_response_from_book_dict`
:class:`~pyexcel.Sheet`     :meth:`~django_excel.ExcelMixin.get_sheet`               :meth:`~django_excel.make_response`
:class:`~pyexcel.Book`      :meth:`~django_excel.ExcelMixin.get_book`                :meth:`~django_excel.make_response`
database table              :meth:`~django_excel.ExcelMixin.save_to_database`        :meth:`~django_excel.make_response_from_a_table` 
a list of database tables   :meth:`~django_excel.ExcelMixin.save_book_to_database`   :meth:`~django_excel.make_response_from_tables` 
=========================== ======================================================== ==================================================

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
      :param keywords: additional keywords to pyexcel library
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

   .. method:: save_to_database(table=None, **keywords)

      :param table: a database table or a tuple which have this sequence (table, table_init_func, mapdict, name_columns_by_row, name_rows_by_column)
      :param table_init_func: it is needed when your table had custom __init__ function
      :param mapdict: it is needed when the uploaded sheet had a different column headers than the table column names this mapdict tells which column of the upload sheet maps to which column of the table
      :param name_columns_by_row: uses the first row of the sheet to be column headers by default. if you use name_rows_by_column, please set this to -1
      :param name_rows_by_column: uses a column to name rows.
      :param keywords: additional keywords to pyexcel library


   .. method:: save_book_to_database(tables=None, **keywords)

      :param tables: a list of database tables or tuples which have this sequence (table, table_init_func, mapdict, name_columns_by_row, name_rows_by_column)
      :param table_init_funcs: it is needed when your table had custom __init__ function
      :param mapdict: it is needed when the uploaded sheet had a different column headers than the table column names. this mapdict tells which column of the upload sheet maps to which column of the table
      :param name_columns_by_row: uses the first row of each sheet to be column headers by default. if you use name_rows_by_column, please set this to -1
      :param name_rows_by_column: uses a column to name rows.
      :param keywords: additional keywords to pyexcel library


Response methods
-----------------

.. automodule:: django_excel

   .. method:: make_response(pyexcel_instance, file_type, status=200)

      :param pyexcel_instance: pyexcel.Sheet or pyexcel.Book
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

   .. method:: make_response_from_a_table(session, table, file_type status=200)

      Produce a single sheet Excel book of *file_type*

      :param session: SQLAlchemy session
      :param table: a SQLAlchemy table
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`

   .. method:: make_response_from_tables(session, tables, file_type status=200)

      Produce a multiple sheet Excel book of *file_type*. It becomes the same
      as :meth:`~django_excel.make_response_from_a_table` if you pass *tables*
      with an array that has a single table
      
      :param session: SQLAlchemy session
      :param tables: SQLAlchemy tables
      :param file_type: same as :meth:`~django_excel.make_response`
      :param status: same as :meth:`~django_excel.make_response`


Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

