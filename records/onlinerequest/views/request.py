from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Document
from ..models import Request
from ..models import Requirement
from ..serializers import RequestSerializer
from django.core import serializers


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