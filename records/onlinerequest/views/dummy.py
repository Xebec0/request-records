from django.shortcuts import render
from django.http import HttpResponse
from ..models import Course
from ..models import Student
import random

def index(request):

    if request.method == "POST":
        codes = ['BSCS', 'BSA', 'BSN']


        for i in range(10):
            Student.objects.create(
                student_number = str(i),
                first_name = "fName " + str (i),
                last_name = "lName " + str (i),
                course_code = random.choice(codes)
            )

        return HttpResponse("Populated")
    else:
        return render(request, "dummy.html")