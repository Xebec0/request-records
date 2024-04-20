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
            return HttpResponse("Posted")
        else:
            # Get error messages from the form
            error_messages = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
            return HttpResponse(f"Not valid: {error_messages}")
        
    else:
        return render(request, "register.html")
