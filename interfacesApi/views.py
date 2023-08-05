from hashlib import new
from pathlib import Path
import mimetypes
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse,JsonResponse
from .azure_messages_hndlr import send_request_messagses
from .azure_file_controller import ALLOWED_EXTENTIONS, download_blob, upload_file_to_blob

from . import models


def index(request):
    return render(request, "interfacesApi/index.html", {})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "interfacesApi/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
        return render(request, "interfacesApi/upload_file.html", {}) 

    return render(request, "interfacesApi/upload_file.html", {})

def list_files(request):
    files = models.File.objects.filter(deleted=0)
    context = {"files": files}
    return render(request, "interfacesApi/list_files.html", context=context)

def download_file(request, file_id):
    file = models.File.objects.get(pk=file_id)
    file_name = file.file_name
    file_type, _ = mimetypes.guess_type(file_name)
    url = file.file_url
    blob_name = url.split("/")[-1]
    blob_content = download_blob(blob_name)
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        return response
    return Http404


def delete_file(request,file_id):
    file = models.File.objects.get(pk=file_id)
    file.deleted = 1
    file.save()
    return redirect("list_files")


def get_diag_messages(request):
    print("trigger")
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': 
        diag_messages_input = request.POST.get('diag_service')
        send_request_messagses(diag_messages_input,'Diag')
        return redirect("index")
    #     response_data = {'message':'Text input received successfully'}
    #     return HttpResponse(response_data)
    # else:
    #     return HttpResponse({'error':'INvalid request.'},status=400)
