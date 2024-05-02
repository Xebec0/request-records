from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from ..models import Request
from ..models import User_Request
from ..models import Document
from ..models import Requirement
from django.core import serializers
import os

def index(request):
    all_requests = Request.objects.all()
    return render(request, 'user/request/index.html', {'all_requests': all_requests})

def create_request(request):
    request_form = Request.objects.get(id = request.POST.get('id'))
    user = request.user
    status = "Waiting"
    uploads = ""

    user_request = User_Request(
        user = user,
        request = request_form,
        status = status,
    )

    # Pre-save the object
    user_request.save()

    # Upload required files
    for file_name in request.FILES:
        file = request.FILES.get(file_name)
        file_path = handle_uploaded_file(str(user_request.id), file)
        file_prefix = "<" + file_name + "&>"
        uploads += file_prefix + file_path + ","

    user_request.uploads = uploads.rstrip(',')
    user_request.save()
    
    return JsonResponse({"success" : True})

def display_user_requests(request):
    user_requests = User_Request.objects.filter(user = request.user)
    return render(request, 'user/request/view-user-request.html', {'user_requests': user_requests})

def get_request(request, id): 
    request = Request.objects.get(id = id)
    request_json = serializers.serialize('json', [request])
    return JsonResponse(request_json, safe=False)

def handle_uploaded_file(source, file):
    # Define the path where you want to save the file
    static_dir = os.path.join(settings.MEDIA_ROOT, 'onlinerequest', 'static', 'user_request', str(source))
    print(static_dir)

    # Create the upload directory if it doesn't exist
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the file
    file_path = os.path.join(static_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

def get_document_description(request, doc_code):
    try:
        document = Requirement.objects.get(code=doc_code)
        return JsonResponse({'description': document.description})
    except Requirement.DoesNotExist:
        return JsonResponse({'description': 'Document not found'}, status=404)

