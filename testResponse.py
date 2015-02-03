from polls.models import Question, Choice
from django.test import Client, TestCase
from django.test.utils import override_settings
from textwrap import dedent
import pyexcel as pe
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import json
import sys
import os
PY2 = sys.version_info[0] == 2
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
if PY2:
    import pyexcel.ext.ods
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO, StringIO
    import pyexcel.ext.ods3


FILE_TYPE_MIME_TABLE = {
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "csvz": "application/zip",
    "tsvz": "application/zip",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xlsm": "application/vnd.ms-excel.sheet.macroenabled.12"
}

class ExcelResponseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        self.single_sheet = [
            ['X', 'Y', 'Z'],
            [1, 2, 3],
            [4, 5, 6]
        ]
        self.book_content = OrderedDict()
        self.book_content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        self.book_content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        self.book_content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})

    def test_download(self):
        for file_type in FILE_TYPE_MIME_TABLE.keys():
            print(file_type)
            response = self.client.get("/polls/download/"+file_type)
            assert response['Content-Type'] == FILE_TYPE_MIME_TABLE[file_type]
            sheet = pe.load_from_memory(file_type, response.content)
            sheet.format(int)
            array = sheet.to_array()
            assert array == self.data

    def test_parse_single_sheet(self):
        test_sample = {
            "array": {u'result': [[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]},
            "dict": {u'Y': [2.0, 5.0], u'X': [1.0, 4.0], u'Z': [3.0, 6.0]},
            "records": {u'result': [{u'Y': 2.0, u'X': 1.0, u'Z': 3.0}, {u'Y': 5.0, u'X': 4.0, u'Z': 6.0}]}
        }
        for data_struct_type in test_sample.keys():
            sheet = pe.Sheet(self.single_sheet)
            tmp_filename = "test.xls"
            sheet.save_as(tmp_filename)
            with open(tmp_filename, "rb") as fp:
                response = self.client.post('/polls/parse/'+data_struct_type,
                                            data={"file": fp})
                assert json.loads(response.content.decode('utf-8')) == test_sample[data_struct_type]
            os.unlink(tmp_filename)

    def test_parse_book(self):
        test_sample = [
            "book",
            "book_dict"
        ]
        expected_dict = {
            u'Sheet1': [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0], [3.0, 3.0, 3.0, 3.0]],
            u'Sheet3': [[u'X', u'Y', u'Z'], [1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]],
            u'Sheet2': [[4.0, 4.0, 4.0, 4.0], [5.0, 5.0, 5.0, 5.0], [6.0, 6.0, 6.0, 6.0]]}
        for data_struct_type in test_sample:
            sheet = pe.Book(self.book_content)
            tmp_filename = "test.xls"
            sheet.save_as(tmp_filename)
            with open(tmp_filename, "rb") as fp:
                response = self.client.post('/polls/parse/'+data_struct_type,
                                            data={"file": fp})
                assert json.loads(response.content.decode('utf-8')) == expected_dict
            os.unlink(tmp_filename)

    def test_exchange(self):
        for in_file_type in FILE_TYPE_MIME_TABLE.keys():
            sheet = pe.Sheet(self.data)
            tmp_filename = "test.%s" % in_file_type 
            sheet.save_as(tmp_filename)
            for file_type in FILE_TYPE_MIME_TABLE.keys():
                print("Post %s -> Respond %s" % (in_file_type, file_type))
                with open(tmp_filename, "rb") as fp:
                    response = self.client.post('/polls/exchange/'+file_type,
                                                data={"file": fp})
                    assert response['Content-Type'] == FILE_TYPE_MIME_TABLE[file_type]
                    sheet = pe.load_from_memory(file_type, response.content)
                    sheet.format(int)
                    array = sheet.to_array()
                    assert array == self.data
            os.unlink(tmp_filename)


class DatabaseOperationsTestCase(TestCase):
    def setUp(self):
        self.testfile = "sample-data.xls"
        Question.objects.all().delete()
        Choice.objects.all().delete()

    def testBook(self):
        fp = open(self.testfile, "rb")
        response = self.client.post('/polls/import/', data={"file": fp})
        assert response.status_code == 200
        response2 = self.client.get('/polls/export/book')
        assert response2.status_code == 200
        book = pe.load_book_from_memory('xls', response2.content)
        content = dedent("""
        Sheet Name: question
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+
        Sheet Name: choice
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
        +---------------+----+-------------+-------+""").strip('\n')
        assert str(book) == content

    def testSheet(self):
        fp = open(self.testfile, "rb")
        response = self.client.post('/polls/import/', data={"file": fp})
        assert response.status_code == 200
        response2 = self.client.get('/polls/export/sheet')
        assert response2.status_code == 200
        sheet = pe.load_from_memory('xls', response2.content)
        content = dedent("""
        Sheet Name: question
        +----+---------------------------+----------------------------------------------+----------+
        | id | pub_date                  | question_text                                | slug     |
        +----+---------------------------+----------------------------------------------+----------+
        | 1  | 2015-01-28T00:00:00+00:00 | What is your favourite programming language? | language |
        +----+---------------------------+----------------------------------------------+----------+
        | 2  | 2015-01-29T00:00:00+00:00 | What is your favourite IDE?                  | ide      |
        +----+---------------------------+----------------------------------------------+----------+""").strip('\n')
        assert str(sheet) == content


@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1)
class ExcelResponseUsingFileTestCase(ExcelResponseTestCase):
    pass

@override_settings(FILE_UPLOAD_MAX_MEMORY_SIZE=1)
class DatabaseOperationsUsingFileTestCase(DatabaseOperationsTestCase):
    pass