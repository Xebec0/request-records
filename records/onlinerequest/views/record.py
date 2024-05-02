from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Course
from ..models import Record
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create records in this view
@login_required
def index(request):
    if request.user.user_type != "5":
        return HttpResponseForbidden("You do not have permission to access this route.")
    
    if request.method == "POST":

        try:
            record = Record(
                user_number = request.POST.get('user_number'),
                first_name = request.POST.get('fname'),
                last_name = request.POST.get('lname'),
                course_code = request.POST.get('course')
            )

            record.save()
            return JsonResponse({'status': True, 'message': str(record) + " created."})
        except Exception as e:
            return JsonResponse({'status': False, 'message': 'Error: ' + str(e)})
    else:
        courses = Course.objects.all()
        return render(request, 'record/index.html', {'courses': courses})

@login_required
def get_user_data(request):
    if request.user.user_type != "5":
        return HttpResponseForbidden("You do not have permission to access this route.")
    
    users = Record.objects.all()
    users_json = serializers.serialize('json',users)
    return JsonResponse(users_json, safe=False)
        