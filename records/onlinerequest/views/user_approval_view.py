from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import User, Record, Course, Profile

def index(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = User.objects.get(id = user_id)

        # Create a profile on create
        created_profile = create_profile(user)

        if created_profile is None:
           return JsonResponse({'status' : False, 'message': "Profile not created. Aborting action, please consult your administrator."})
        
        # Approve user
        user.is_active = True
        user.save()

        return JsonResponse({'status' : True, 'message': str(user) + " approved."})
    else: 
        users = User.objects.filter(is_active = False)
        return render(request, 'admin/user/index.html', {'users': users})
    
def create_profile(user):
    user_record = Record.objects.get(user_number = user.student_number) # Fetch record object
    course = Course.objects.get(code = user_record.course_code) # Get course name
    profile = Profile(
        user=user, 
        course = course, 
        first_name = user_record.first_name, 
        last_name = user_record.last_name,
        middle_name = user_record.middle_name,
        contact_no = user_record.contact_no,
        entry_year_from = user_record.entry_year_from,
        entry_year_to= user_record.entry_year_to
    )
    
    profile.save();
    return profile