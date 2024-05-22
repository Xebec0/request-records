from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from onlinerequest.models import Request, Requirement

def index(request):
    request_forms = Request.objects.all()
    for request_form in request_forms:
        requirement_descriptions = []
        for requirement_code in request_form.files_required.split(','):
            try:
                requirement = Requirement.objects.get(code=requirement_code)
                requirement_descriptions.append(requirement.description)
            except Requirement.DoesNotExist:
                requirement_descriptions.append(requirement_code)
        request_form.requirement_descriptions = requirement_descriptions
    return render(request, 'index.html', {'request_forms': request_forms})

def signup_view(request):
    return render(request, 'signup.html')

def admin_dashboard(request):
    return render (request, "admin/dashboard.html")

def user_dashboard(request):
    return render (request, "user/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect('/signup/')