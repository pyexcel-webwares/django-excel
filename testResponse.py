# -*- coding: utf-8 -*-

import os
import sys
import json
from textwrap import dedent
from polls.models import Question, Choice
from django.test import Client, TestCase
from django.test.utils import override_settings
import pyexcel as pe
import pyexcel.ext.xls  # noqa
import pyexcel.ext.xlsx  # noqa
import pyexcel.ext.ods3  # noqa
from django_excel._compact import urllib_quote
from django_excel import ExcelInMemoryUploadedFile
from nose.tools import eq_

PY2 = sys.version_info[0] == 2
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO


_XLSX_MIME = "application/" + "vnd.openxmlformats-officedocument.spreadsheetml.sheet"

FILE_TYPE_MIME_TABLE = {
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "csvz": "application/zip",
    "tsvz": "application/zip",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "xls": "application/vnd.ms-excel",
    "xlsx": _XLSX_MIME,
    "xlsm": "application/vnd.ms-excel.sheet.macroenabled.12",
}


class ExcelResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = [[1, 2, 3], [4, 5, 6]]
        self.single_sheet = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        self.book_content = OrderedDict()
        self.book_content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        self.book_content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        self.book_content.update(
            {"Sheet3": [[u"X", u"Y", u"Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]]}
        )

    def test_download(self):
        for file_type in FILE_TYPE_MIME_TABLE.keys():
            response = self.client.get("/polls/download/" + file_type)
            assert response["Content-Type"] == FILE_TYPE_MIME_TABLE[file_type]
            sheet = pe.get_sheet(file_type=file_type, file_content=response.content)
            sheet.format(int)
            array = sheet.to_array()
            assert array == self.data

    def test_download_attachment_with_ascii_name(self):
        test_file_name = "test"
        self._download_and_verify_file_name(test_file_name)

    def test_download_attachment_with_unicode_name(self):
        test_file_name = u"中文文件名"
        self._download_and_verify_file_name(test_file_name.encode("utf-8"))

    def test_download_attachment_with_unicode_name_as_string(self):
        test_file_name = "中文文件名"
        self._download_and_verify_file_name(test_file_name)

    def _download_and_verify_file_name(self, file_name):
        for file_type in FILE_TYPE_MIME_TABLE.keys():
            url_encoded_file_name = urllib_quote(file_name)
            response = self.client.get(
                (
                    "/polls/download_attachment/%s/%s"
                    % (file_type, url_encoded_file_name)
                )
            )
            assert response["Content-Type"] == FILE_TYPE_MIME_TABLE[file_type]
            assert response["Content-Disposition"] == (
                "attachment; filename=%s.%s;filename*=utf-8''%s.%s"
                % (url_encoded_file_name, file_type, url_encoded_file_name, file_type)
            )
            sheet = pe.get_sheet(file_type=file_type, file_content=response.content)
            sheet.format(int)
            array = sheet.to_array()
            assert array == self.data

    def test_parse_single_sheet(self):
        test_sample = {
            "array": {
                u"result": [[u"X", u"Y", u"Z"], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
            },
            "dict": {u"Y": [2.0, 5.0], u"X": [1.0, 4.0], u"Z": [3.0, 6.0]},
            "records": {
                u"result": [
                    {u"Y": 2.0, u"X": 1.0, u"Z": 3.0},
                    {u"Y": 5.0, u"X": 4.0, u"Z": 6.0},
                ]
            },
        }
        for data_struct_type in test_sample.keys():
            sheet = pe.Sheet(self.single_sheet)
            tmp_filename = "test.file.xls"
            sheet.save_as(tmp_filename)
            with open(tmp_filename, "rb") as fp:
                response = self.client.post(
                    "/polls/parse/" + data_struct_type, data={"file": fp}
                )
                self.assertEqual(
                    json.loads(response.content.decode("utf-8")),
                    test_sample[data_struct_type],
                )
            os.unlink(tmp_filename)

    def test_parse_book(self):
        test_sample = ["book", "book_dict"]
        expected_dict = {
            u"Sheet1": [
                [1.0, 1.0, 1.0, 1.0],
                [2.0, 2.0, 2.0, 2.0],
                [3.0, 3.0, 3.0, 3.0],
            ],
            u"Sheet3": [
                [u"X", u"Y", u"Z"],
                [1.0, 4.0, 7.0],
                [2.0, 5.0, 8.0],
                [3.0, 6.0, 9.0],
            ],
            u"Sheet2": [
                [4.0, 4.0, 4.0, 4.0],
                [5.0, 5.0, 5.0, 5.0],
                [6.0, 6.0, 6.0, 6.0],
            ],
        }
        for data_struct_type in test_sample:
            sheet = pe.Book(self.book_content)
            tmp_filename = "test.xls"
            sheet.save_as(tmp_filename)
            with open(tmp_filename, "rb") as fp:
                response = self.client.post(
                    "/polls/parse/" + data_struct_type, data={"file": fp}
                )
                self.assertEqual(
                    json.loads(response.content.decode("utf-8")), expected_dict
                )
            os.unlink(tmp_filename)

    def test_exchange(self):
        for in_file_type in FILE_TYPE_MIME_TABLE.keys():
            sheet = pe.Sheet(self.data)
            tmp_filename = "test.%s" % in_file_type
            sheet.save_as(tmp_filename)
            for file_type in FILE_TYPE_MIME_TABLE.keys():
                with open(tmp_filename, "rb") as fp:
                    response = self.client.post(
                        "/polls/exchange/" + file_type, data={"file": fp}
                    )
                    self.assertEqual(
                        response["Content-Type"], FILE_TYPE_MIME_TABLE[file_type]
                    )
                    sheet = pe.get_sheet(
                        file_type=file_type, file_content=response.content
                    )
                    sheet.format(int)
                    array = sheet.to_array()
                    assert array == self.data
            os.unlink(tmp_filename)


class DatabaseOperationsTestCase(TestCase):
    def setUp(self):
        self.testfile = "sample-data.xls"
        self.maxDiff = None
        Question.objects.all().delete()
        Choice.objects.all().delete()

    def testBook(self):
        fp = open(self.testfile, "rb")
        response = self.client.post("/polls/import/", data={"file": fp})
        eq_(response.status_code, 302)
        response2 = self.client.get("/polls/export/book")
        assert response2.status_code == 200
        book = pe.get_book(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+
        choice:
        +---------------+----+-------------+-------+
        | choice_text   | id | question_id | votes |
        +---------------+----+-------------+-------+
        | Java          | 1  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C++           | 2  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C             | 3  | 1           | 0     |
        +---------------+----+-------------+-------+
        | Eclipse       | 4  | 2           | 0     |
        +---------------+----+-------------+-------+
        | Visual Studio | 5  | 2           | 0     |
        +---------------+----+-------------+-------+
        | PyCharm       | 6  | 2           | 0     |
        +---------------+----+-------------+-------+
        | IntelliJ      | 7  | 2           | 0     |
        +---------------+----+-------------+-------+"""
        ).strip(
            "\n"
        )  # noqa
        self.assertEqual(str(book), content)

    def testBookWithoutBulkSave(self):
        fp = open(self.testfile, "rb")
        response = self.client.post("/polls/import/", data={"file": fp})
        eq_(response.status_code, 302)
        response2 = self.client.get("/polls/export/book")
        assert response2.status_code == 200
        book = pe.get_book(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+
        choice:
        +---------------+----+-------------+-------+
        | choice_text   | id | question_id | votes |
        +---------------+----+-------------+-------+
        | Java          | 1  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C++           | 2  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C             | 3  | 1           | 0     |
        +---------------+----+-------------+-------+
        | Eclipse       | 4  | 2           | 0     |
        +---------------+----+-------------+-------+
        | Visual Studio | 5  | 2           | 0     |
        +---------------+----+-------------+-------+
        | PyCharm       | 6  | 2           | 0     |
        +---------------+----+-------------+-------+
        | IntelliJ      | 7  | 2           | 0     |
        +---------------+----+-------------+-------+"""
        ).strip(
            "\n"
        )  # noqa
        self.assertEqual(str(book), content)

    def testBookUsingIsave(self):
        fp = open(self.testfile, "rb")
        response = self.client.post("/polls/import_using_isave/", data={"file": fp})
        eq_(response.status_code, 302)
        response2 = self.client.get("/polls/export/book")
        assert response2.status_code == 200
        book = pe.get_book(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+
        choice:
        +---------------+----+-------------+-------+
        | choice_text   | id | question_id | votes |
        +---------------+----+-------------+-------+
        | Java          | 1  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C++           | 2  | 1           | 0     |
        +---------------+----+-------------+-------+
        | C             | 3  | 1           | 0     |
        +---------------+----+-------------+-------+
        | Eclipse       | 4  | 2           | 0     |
        +---------------+----+-------------+-------+
        | Visual Studio | 5  | 2           | 0     |
        +---------------+----+-------------+-------+
        | PyCharm       | 6  | 2           | 0     |
        +---------------+----+-------------+-------+
        | IntelliJ      | 7  | 2           | 0     |
        +---------------+----+-------------+-------+"""
        ).strip(
            "\n"
        )  # noqa
        self.assertEqual(str(book), content)

    def testSheet(self):
        fp = open(self.testfile, "rb")
        response = self.client.post("/polls/import/", data={"file": fp})
        eq_(response.status_code, 302)
        response2 = self.client.get("/polls/export/sheet")
        assert response2.status_code == 200
        sheet = pe.get_sheet(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+"""
        ).strip(
            "\n"
        )  # noqa
        assert str(sheet) == content

    def testImportSheet(self):
        fp = open("sample-sheet.xls", "rb")
        response = self.client.post("/polls/import_sheet/", data={"file": fp})
        eq_(response.status_code, 200)
        response2 = self.client.get("/polls/export/sheet")
        eq_(response2.status_code, 200)
        sheet = pe.get_sheet(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+"""
        ).strip(
            "\n"
        )  # noqa
        self.assertEqual(str(sheet), content)

    def testImportSheetUsingISave(self):
        fp = open("sample-sheet-for-isave.xls", "rb")
        response = self.client.post(
            "/polls/import_sheet_using_isave/", data={"file": fp}
        )
        eq_(response.status_code, 200)
        response2 = self.client.get("/polls/export/sheet")
        eq_(response2.status_code, 200)
        sheet = pe.get_sheet(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        question:
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+"""
        ).strip(
            "\n"
        )  # noqa
        self.assertEqual(str(sheet), content)

    def testCustomExport(self):
        fp = open(self.testfile, "rb")
        response = self.client.post("/polls/import/", data={"file": fp})
        eq_(response.status_code, 302)
        response2 = self.client.get("/polls/export/custom")
        eq_(response2.status_code, 200)
        sheet = pe.get_sheet(file_type="xls", file_content=response2.content)
        content = dedent(
            """
        pyexcel_sheet1:
        +---------------+----+-------+
        | choice_text   | id | votes |
        +---------------+----+-------+
        | Eclipse       | 4  | 0     |
        +---------------+----+-------+
        | Visual Studio | 5  | 0     |
        +---------------+----+-------+
        | PyCharm       | 6  | 0     |
        +---------------+----+-------+
        | IntelliJ      | 7  | 0     |
        +---------------+----+-------+"""
        ).strip("\n")
        self.assertEqual(str(sheet), content)


@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1)
class ExcelResponseUsingFileTestCase(ExcelResponseTestCase):
    pass


@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1)
class DatabaseOperationsUsingFileTestCase(DatabaseOperationsTestCase):
    pass


class TestUploadedFile(TestCase):
    def test_in_memory_file(self):
        test_content = "a,b,c"
        strio = StringIO(test_content)
        strio.read()
        in_memory_file = ExcelInMemoryUploadedFile(
            file=strio,
            field_name="test",
            name="test_file",
            content_type="text",
            size=3,
            charset=None,
        )
        params = in_memory_file.get_params()
        eq_(params["file_content"], test_content)
