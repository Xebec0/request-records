from django.shortcuts import render
from django.http import HttpResponse
from ..models import Course


def index(request):

    if request.method == "POST":
        Course.objects.create(course_code = 'BSCS', course_name = "COMPUTER SCIENCE")
        Course.objects.create(course_code = 'BSA', course_name = "Accountancy")
        Course.objects.create(course_code = 'BSN', course_name = "Nursing")
        return HttpResponse("Populated")
    else:
        return render(request, "dummy.html")