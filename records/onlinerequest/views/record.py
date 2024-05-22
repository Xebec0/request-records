from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Course
from ..models import Record
from django.core import serializers
from ..serializers import RecordSerializer


# Create records in this view
def index(request):
    if request.method == "POST":
        try:
            record_serializer = RecordSerializer(data = {
                'user_number' : request.POST.get('user_number'),
                'first_name' : request.POST.get('fname'),
                'last_name' : request.POST.get('lname'),
                'course_code' : request.POST.get('course'),
                'middle_name' : request.POST.get('middle_name'),
                'contact_no' : request.POST.get('contact_no'), 
                'entry_year_to' : request.POST.get('entry_year_to'),
                'entry_year_from': request.POST.get('entry_year_from'),
            })

            if record_serializer.is_valid():
                record_serializer.save()
                return JsonResponse({'status': True, 'message': "Record created."})
            else:
                return JsonResponse({'status': False, 'errors': record_serializer.errors})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error: ' + str(e)})
    else:
        courses = Course.objects.all()
        return render(request, 'record/index.html', {'courses': courses})
    
def get_user_data(request):
    users = Record.objects.all()
    users_json = serializers.serialize('json',users)
    return JsonResponse(users_json, safe=False)
        