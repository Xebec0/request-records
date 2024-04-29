from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import Course
from ..models import Record

# Create records in this view
def index(request):
    if request.method == "POST":

        record = Record.objects.create(
            user_number = request.POST.get('user_number'),
            first_name = request.POST.get('fname'),
            last_name = request.POST.get('lname'),
            course_code = request.POST.get('course')
        )

        if record:
            return JsonResponse({'status': True, 'message': str(record) + " created."})
        else:
            return JsonResponse({'status' : True, 'message': "Invalid."})
    else:
        courses = Course.objects.all()
        return render(request, 'student/index.html', {'courses': courses})
    