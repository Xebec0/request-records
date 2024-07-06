from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from ..models import Record, User

def index(request):
    if request.method == "POST":
        print(request.POST)
        if (request.POST):
            command_name = request.POST.get("command-name") # Will server as command key

            if (command_name == "REQUEST"):
                reference_number = request.POST.get("reference-number")
                user_record = Record.objects.filter(user_number=reference_number).first()

                if (user_record):
                    # Get user reference
                    user = User.objects.filter(student_number=reference_number).first()
                    login(request, user)

                    # If user is logged in redirect user
                    return HttpResponse("Logged in")
                else:
                    return HttpResponse("User does not exists")

        return HttpResponse("Posted Successfully")
    else:
        return render(request, 'reference-login.html')