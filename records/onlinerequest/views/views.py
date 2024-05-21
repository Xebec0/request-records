from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup_view(request):
    return render(request, 'signup.html')

def admin_dashboard(request):
    return render (request, "admin/dashboard.html")

def user_dashboard(request):
    return render (request, "user/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect('/signup/')