from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Document
from ..models import Request
from ..models import Requirement
from ..models import User_Request
from ..serializers import RequestSerializer
from django.conf import settings
import os


def index(request):
    if request.method == "POST":
        post_document = request.POST.get("documents")
        post_files_required = request.POST.get("requirements")
        post_description = request.POST.get("description")

        document = Document.objects.get(code = post_document)
        created_request = Request.objects.create(document = document, files_required = post_files_required, description = post_description)
        
        if created_request:
            return JsonResponse({"status": True, "message": "Request Created"})
        else:
            return JsonResponse({"status": False, "message": "Request not created. Please try again."})
    else:
        documents = Document.objects.all()
        requirements = Requirement.objects.all()
        return render(request, 'admin/request/index.html', {'documents': documents, 'requirements': requirements})

def display_user_requests(request):
    user_requests = User_Request.objects.all()
    return render(request, 'admin/request/user-request.html', {'user_requests': user_requests })

def display_user_request(request, id):
    if request.method == "POST":
        new_status = request.POST.get('new_status')
        requested_file = request.FILES.get('requested_file')

        # Update user_request
        user_request = User_Request.objects.get(id=id)

        if new_status.lower() == "completed":
            if requested_file is None:
                return JsonResponse({'status': False, 'message': "Please upload a file before marking the request as 'Completed'"})
            file_path = handle_uploaded_file(id, requested_file)
            user_request.requested = file_path

        user_request.status = new_status
        user_request.save()

        return JsonResponse({'status': True, 'message': 'Request status updated successfully.', 'request_status': user_request.status})
    else:
        user_request = User_Request.objects.get(id=id)

        uploads = []
        for record in user_request.uploads.split(','):
            if record:
                test = record.replace(">", "").replace("<", "").split('&')
                print(test[0] + "-" + test[1])

        for user_request_upload in user_request.uploads.split(','):
            if user_request_upload:
                upload = user_request_upload.replace("<", "").replace(">", "").split('&')
                uploads.append({
                    'code': getCodeDescription(Requirement, upload[0]),
                    'path': upload[1]
                })

        context = {
            'user_request': user_request,
            'uploads': uploads,
        }

    return render(request, 'admin/request/view-user-request.html', context)



def getCodeDescription(model, key):
    model_instance = model.objects.get(code = key)
    return model_instance.description


def delete_user_request(request, id):
    user_request = User_Request.objects.get(id = id)
    user_request.delete()

    return JsonResponse({'status' : True, 'message': "Deleted succesfully."})
    
def delete_request(request, id):
    request = Request.objects.get(id=id)
    deleted = request.delete()

    if deleted:
        return JsonResponse({'status': True, 'message': deleted})
    else:
        return JsonResponse({'False': True, 'message': 'Invalid row'})
    
def get_requests(request):
    requests = Request.objects.all()
    requests_json = RequestSerializer(requests, many=True).data  # Serialize the queryset
    return JsonResponse(requests_json, safe=False)

def handle_uploaded_file(source, file):
    # Define the path where you want to save the file
    static_dir = os.path.join(settings.MEDIA_ROOT, 'onlinerequest', 'static', 'user_request', str(source), 'approved')

    # Create the upload directory if it doesn't exist
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the file
    file_path = os.path.join(static_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path