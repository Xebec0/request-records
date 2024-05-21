import os
import json
import random
import string
import smtplib
from email.mime.text import MIMEText
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from ..forms import UserRegistrationForm
from ..models import RegisterRequest
from ..models import Course
from ..models import Record
from ..models import User
from ..models import Profile

def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code

@require_POST
def send_verification_email(request):
    email = request.POST.get('email')
    if email:
        verification_code = generate_verification_code()
        request.session['verification_code'] = verification_code
        request.session['user_email'] = email
        expiry_time = 5  # 5 minutes
        request.session.set_expiry(expiry_time * 60)

        send_email_with_code(email, verification_code, expiry_time)

        return JsonResponse({'status': True, 'message': 'Verification code sent to your email'})
    else:
        return JsonResponse({'status': False, 'message': 'Email is required'})

def send_email_with_code(email, verification_code, expiry_time):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    subject = 'Email Verification Code'
    message = f"""
    <html>
    <body>
        <p>This code will expire in <strong style="font-size: 1.2em; color: #c00;">{expiry_time} minutes</strong> or when you leave the registration page.</p>
        <p style="font-size: 1.1em; color: #333;">Your verification code is:</p>
        <h1 style="text-align: center; font-size: 3em; color: #007bff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);"> {verification_code} </h1>
    </body>
    </html>
    """

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = 'Academic Online Request System<{}>'.format(smtp_username)
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())

def index(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('verification_code')
            user = form.save(commit=False)
            user.is_active = False

            stored_code = request.session.get('verification_code')

            print(f"Entered code: {entered_code}")  # Log the entered code
            print(f"Stored code: {stored_code}")  # Log the stored code

            if entered_code == stored_code:
                user.is_active = False
                user.save()
                return JsonResponse({'status': True, 'message': 'Registration successful'})
            else:
                return JsonResponse({'status': False, 'message': 'Invalid verification code'})
        else:
            return JsonResponse({'status': False, 'message': 'Please fillup all form requirements'})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
    
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
