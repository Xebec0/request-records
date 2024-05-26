from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
from ..models import Request, User_Request, Requirement, User
from ..serializers import RequestSerializer
from ..utilities import get_if_exists

from django.core import serializers
import os

def index(request):
    all_requests = Request.objects.all()
    return render(request, 'user/request/index.html', {'all_requests': all_requests})

def create_request(request):
    request_form = Request.objects.get(id = request.POST.get('id'))
    user = request.user
    status = "Payment not yet settled"
    uploads = ""

    user_request = User_Request(
        user = user,
        request = request_form,
        status = status,
        purpose = request.POST.get("purpose"),
    )

    # Pre-save the object
    user_request.save()

    # Upload required files
    for file_name in request.FILES:
        file = request.FILES.get(file_name)
        file_path = handle_uploaded_file(file, str(user_request.id))
        file_prefix = "<" + file_name + "&>"
        uploads += file_prefix + file_path + ","

    user_request.uploads = uploads.rstrip(',')
    user_request.save()
    
    return JsonResponse({"success" : True, "message": "Redirecting checkout...", 'id': user_request.id})

def display_user_requests(request):
    user_requests = User_Request.objects.filter(user = request.user)
    return render(request, 'user/request/view-user-request.html', {'user_requests': user_requests})

def get_request(request, id): 
    request = Request.objects.get(id = id)
    request_serializer = RequestSerializer(request)
    return JsonResponse(request_serializer.data, safe= False)

def handle_uploaded_file(file, source, source2 = ""):

    # Define the path where you want to save the file
    static_dir = os.path.join(settings.MEDIA_ROOT, 'onlinerequest', 'static', 'user_request', str(source))

    if source2:
        static_dir = os.path.join(settings.MEDIA_ROOT, 'onlinerequest', 'static', 'user_request', str(source), str(source2))

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
    

def display_payment(request, id):
    if request.method == "POST":
        user_request = get_if_exists(User_Request, id = id)

        if user_request:
            # Upload required files
            for file_name in request.FILES:
                file = request.FILES.get(file_name)
                file_path = handle_uploaded_file( file, str(user_request.id), 'uploaded_payment')

                user_request.uploaded_payment = file_path
                user_request.status = "Waiting"
                user_request.save()
            
            return JsonResponse({"status": True, "message": "Submission successful. Closing the window now..."})

        return JsonResponse({"status": False, "message": "Invalid payment detected. Please contact your administrator."})
    elif request.method == "GET":
        user = get_if_exists(User, id = request.user.id)
        requested_document = get_if_exists(User_Request, id = id)

        if user and requested_document:
            return render(request, "payment.html", {"user": user, "requested_document": requested_document})

        return HttpResponse("Unauthorized access. Please contact your administrator.")

