from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django import forms
from django.template import RequestContext
import django_excel as excel
from polls.models import Question, Choice
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    import pyexcel.ext.ods
else:
    import pyexcel.ext.ods3


data = [
    [1, 2, 3],
    [4, 5, 6]
]

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

def download(request, file_type):
    sheet = excel.pe.Sheet(data)
    return excel.make_response(sheet, file_type)

def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_model(Question, 'csv')
    elif atype == "book":
        return excel.make_response_from_a_model([Question, Choice], 'csv')
    
def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        def choice_func(row):
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
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response('upload_form.html', {'form': form}, context_instance=RequestContext(request))
    

def import_dataa(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=(Question,
                       ['question_text', 'pub_date']))
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response('upload_form.html', {'form': form}, context_instance=RequestContext(request))
    

def exchange(request, file_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        return excel.make_response(filehandle.get_sheet(), file_type)
    else:
        return HttpResponseBadRequest()

def parse(request, data_struct_type):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        filehandle = request.FILES['file']
        if data_struct_type == "array":
            return JsonResponse({"result":filehandle.get_array()})
        elif data_struct_type == "dict":
            return JsonResponse(filehandle.get_dict())
        elif data_struct_type == "records":
            return JsonResponse({"result":filehandle.get_records()})
        elif data_struct_type == "book":
            return JsonResponse(filehandle.get_book().to_dict())
        elif data_struct_type == "book_dict":
            return JsonResponse(filehandle.get_book_dict())
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

