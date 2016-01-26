"""
    django_excel
    ~~~~~~~~~~~~~~~~~~~

    A django middleware that provides one application programming interface
    to read and write data in different excel file formats

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from django.core.files.uploadhandler import (
    MemoryFileUploadHandler, TemporaryFileUploadHandler)
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile)
from django.http import HttpResponse
import pyexcel as pe
import pyexcel_webio as webio


class ExcelMixin(webio.ExcelInput):
    """
    Provide additional pyexcel-webio methods to Django's UploadedFiles
    """
    def get_params(self, **keywords):
        extension = self.name.split(".")[-1]
        keywords['file_type'] = extension
        keywords['file_content'] = self.file.read()
        return keywords

    def save_to_database(self, model=None, initializer=None, mapdict=None,
                         **keywords):
        """
        Save data from a sheet to a nominated django model
        """        
        params = self.get_params(**keywords)
        if 'name_columns_by_row' not in params:
            params['name_columns_by_row'] = 0
        if 'name_rows_by_column' not in params:
            params['name_rows_by_column'] = -1
        params['dest_model'] = model
        params['dest_initializer'] = initializer
        params['dest_mapdict'] = mapdict
        pe.save_as(**params)

    def save_book_to_database(self, models=None, initializers=None,
                              mapdicts=None, batch_size=None,
                              **keywords):
        """
        Save data from a book to a nominated django models
        """
        params = self.get_params(**keywords)
        params['dest_models'] = models
        params['dest_initializers']=initializers
        params['dest_mapdicts'] = mapdicts
        params['dest_batch_size'] = batch_size
        pe.save_book_as(**params)


class ExcelInMemoryUploadedFile(ExcelMixin, InMemoryUploadedFile):
    """
    Mix-in pyexcel-webio methods in InMemoryUploadedFile
    """
    pass


class TemporaryUploadedExcelFile(ExcelMixin, TemporaryUploadedFile):
    """
    Mix-in pyexcel-webio methods in TemporaryUploadedFile    
    """
    pass


class ExcelMemoryFileUploadHandler(MemoryFileUploadHandler):
    """
    Override MemoryFileUploadHandler to bring in ExcelInMemoryUploadedFile
    """
    def file_complete(self, file_size):
        if not self.activated:
            return
        self.file.seek(0)
        return ExcelInMemoryUploadedFile(
            file=self.file,
            field_name=self.field_name,
            name=self.file_name,
            content_type=self.content_type,
            size=file_size,
            charset=self.charset,
            content_type_extra=self.content_type_extra
        )


class TemporaryExcelFileUploadHandler(TemporaryFileUploadHandler):
    """
    Override TemporaryFileUploadHandler to bring in TemporaryUploadedExcelFile
    """
    def new_file(self, file_name, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super(TemporaryFileUploadHandler, self).new_file(
            file_name,
            *args,
            **kwargs)
        self.file = TemporaryUploadedExcelFile(
            self.file_name,
            self.content_type,
            0,
            self.charset,
            self.content_type_extra)


def _make_response(content, content_type, status, file_name=None):
    """
    Custom response function that is called by pyexcel-webio
    """
    response = HttpResponse(content, content_type=content_type, status=status)
    if file_name:
        response["Content-Disposition"] = "attachment; filename=%s" % (file_name)
    return response


webio.ExcelResponse = _make_response


from pyexcel_webio import (
    make_response,
    make_response_from_array,
    make_response_from_dict,
    make_response_from_records,
    make_response_from_book_dict,
    make_response_from_query_sets
)


def make_response_from_a_table(model, file_type,
                               status=200, file_name=None, **keywords):
    """
    Produce a single sheet Excel book of *file_type*

    :param model: a Django model
    :param file_type: same as :meth:`~django_excel.make_response`
    :param status: same as :meth:`~django_excel.make_response`
    """
    sheet = pe.get_sheet(model=model, **keywords)
    return make_response(sheet, file_type, status, file_name=file_name, **keywords)


def make_response_from_tables(models, file_type,
                              status=200, file_name=None, **keywords):
    """
    Produce a multiple sheet Excel book of *file_type*. It becomes the same
    as :meth:`~django_excel.make_response_from_a_table` if you pass *tables*
    with an array that has a single table

    :param models: a list of Django models
    :param file_type: same as :meth:`~django_excel.make_response`
    :param status: same as :meth:`~django_excel.make_response`
    """
    book = pe.get_book(models=models, **keywords)
    return make_response(book, file_type, status, file_name=file_name, **keywords)
