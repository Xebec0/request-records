from django.shortcuts import render
from django.http import HttpResponse
from ..models import Course
from ..models import Record
import random

def index(request):

    if request.method == "POST":
        codes = ['BSCS', 'BSA', 'BSN']

        Record.objects.create(
            student_number = "20189",
            first_name = "Set",
            last_name = "Vergara",
            course_code = random.choice(codes)        
        )

        return HttpResponse("Populated")
    else:
        return render(request, "dummy.html")