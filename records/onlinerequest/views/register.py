from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from ..forms import UserRegistrationForm
from ..models import RegisterRequest
from ..models import Course
from ..models import Record
from ..models import User
from ..models import Profile

import os

def index(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
    
        if form.is_valid():
            # User is saved
            user = form.save()

            # Profile is saved
            create_profile(user)

            # Access the uploaded file
            uploaded_file = request.FILES.get('formFile')

            if uploaded_file:
                # Save the file to a specific location
                file_path = handle_uploaded_file(uploaded_file)
                RegisterRequest.objects.create(user = user, valid_id = file_path)
            
            return JsonResponse({'status' : True, 'message' : "Registered succesfully"})
        else:
            last_error_message = list(form.errors.items())[0]
            return JsonResponse({'status' : False,'message' : last_error_message[1]})
    else:
        return render(request, "register.html")
    
def handle_uploaded_file(file):
    # Define the path where you want to save the file
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the file
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

def create_profile(user):
    user_record = Record.objects.get(user_number = user.student_number) # Fetch record object
    course = Course.objects.get(course_code = user_record.course_code) # Get course name
    profile = Profile.objects.create(user=user, course = course, first_name = user_record.first_name, last_name = user_record.last_name)
    return profile

    