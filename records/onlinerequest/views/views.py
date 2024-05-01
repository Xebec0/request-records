from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup_view(request):
    return render(request, 'signup.html')

def admin_dashboard(request):
    return render (request, "admin/dashboard.html")

def user_dashboard(request):
    return render (request, "user/dashboard.html")