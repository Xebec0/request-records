from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from ..models import Request
from ..models import Document
from django.core import serializers

import os

def index(request):
    all_requests = Request.objects.all()
    return render(request, 'user/request/index.html', {'all_requests': all_requests})

def create_request(request):

    # Upload required files
    for file_name in request.FILES:
        file = request.FILES.get(file_name)
        file_path = handle_uploaded_file(file)
        print(file_path)
        
    return JsonResponse({"success" : True})


def get_request(request, id): 
    request = Request.objects.get(id = id)
    request_json = serializers.serialize('json', [request])
    return JsonResponse(request_json, safe=False)

def handle_uploaded_file(file):
    # Define the path where you want to save the file
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'user_uploads')

    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the file
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path