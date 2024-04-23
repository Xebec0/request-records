from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from ..models import User



def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username = email, password = password)

        if user is not None:
            if not user.is_active:
                return JsonResponse({'status': False, 'message': 'Account not yet activated. Please contact your administrator.'})
        
            login(request, user)
            return JsonResponse({'status': True, 'message': 'Logged in'})
        else:
            return JsonResponse({'status': False, 'message': 'Invalid email and password'})
    else:
        return render(request, 'login.html')