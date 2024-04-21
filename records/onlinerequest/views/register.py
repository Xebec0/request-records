from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import User
from ..forms import UserRegistrationForm

def index(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return JsonResponse({'status' : True, 'message' : "Registered succesfully"})
        else:
            last_error_message = list(form.errors.items())[0]
            return JsonResponse({'status' : False,'message' : last_error_message[1]})
    else:
        return render(request, "register.html")
    