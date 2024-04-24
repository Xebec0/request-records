from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Document
from ..models import Request
from django.core import serializers


def index(request):
    if request.method == "POST":
        post_title = request.POST.get("title")
        post_document = request.POST.get("documents")
        post_no_of_files_required = request.POST.get("no_of_files_required")
        post_description = request.POST.get("description")

        document = Document.objects.get(code = post_document)
        created_request = Request.objects.create(document = document, title = post_title, no_of_files_required = post_no_of_files_required, description = post_description)
        
        if created_request:
            return JsonResponse({"status": True, "message": "Request Created"})
        else:
            return JsonResponse({"status": False, "message": "Request not created. Please try again."})
    else:
        documents = Document.objects.all()
        return render(request, 'admin/request/index.html', {'documents': documents})
    
def get_requests(request):
    requests = Request.objects.all()
    requests_json = serializers.serialize('json', requests)
    return JsonResponse(requests_json, safe=False)