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
    def _get_file_extension(self):
        extension = self.name.split(".")[-1]
        return extension

    def load_single_sheet(self, sheet_name=None, **keywords):
        return pe.get_sheet(
            file_type=self._get_file_extension(),
            file_content=self.file.read(),
            sheet_name=sheet_name,
            **keywords)

    def load_book(self, **keywords):
        return pe.get_book(
            file_type=self._get_file_extension(),
            file_content=self.file.read(),
            **keywords)

    def save_to_database(self, model=None,
                         sheet_name=None,
                         name_columns_by_row=0,
                         name_rows_by_column=-1,
                         **keywords):
        """
        Save data from a sheet to a nominated django model
        """        
        sheet = self.load_single_sheet(
            sheet_name=sheet_name,
            name_columns_by_row=name_columns_by_row,
            name_rows_by_column=name_rows_by_column,
            **keywords)
        if sheet:
            sheet.save_to_django_model(model, **keywords)

    def save_book_to_database(self, models=None, **keywords):
        """
        Save data from a book to a nominated django models
        """        
        book = self.load_book(**keywords)
        if book:
            book.save_to_django_models(models, **keywords)


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


webio.ExcelResponse = HttpResponse


from pyexcel_webio import (
    make_response,
    make_response_from_array,
    make_response_from_dict,
    make_response_from_records,
    make_response_from_book_dict,
    make_response_from_query_sets
)


def make_response_from_a_table(model, file_type, status=200, **keywords):
    """
    Produce a single sheet Excel book of *file_type*

    :param model: a Django model
    :param file_type: same as :meth:`~django_excel.make_response`
    :param status: same as :meth:`~django_excel.make_response`
    """
    sheet = pe.get_sheet(model=model, **keywords)
    return make_response(sheet, file_type, status, **keywords)


def make_response_from_tables(models, file_type, status=200, **keywords):
    """
    Produce a multiple sheet Excel book of *file_type*. It becomes the same
    as :meth:`~django_excel.make_response_from_a_table` if you pass *tables*
    with an array that has a single table

    :param models: a list of Django models
    :param file_type: same as :meth:`~django_excel.make_response`
    :param status: same as :meth:`~django_excel.make_response`
    """
    book = pe.get_book(models=models, **keywords)
    return make_response(book, file_type, status, **keywords)
