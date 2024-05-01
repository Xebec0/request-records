from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import User

def index(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = User.objects.get(id = user_id)
        user.is_active = True
        user.save()

        return JsonResponse({'status' : True, 'message': str(user) + " approved."})
    else: 
        users = User.objects.filter(is_active = False)
        return render(request, 'admin/user/index.html', {'users': users})