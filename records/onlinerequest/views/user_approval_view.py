from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from ..models import User, Record, Course, Profile
from .register import send_email_with_code
import random
import string
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta

def index(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        action = request.POST.get('action', 'approve')  # Default to approve
        
        # Debug logging
        print(f"Received request - user_id: {user_id}, action: {action}")
        
        try:
            # Check if user_id is valid
            if not user_id:
                return JsonResponse({'status': False, 'message': "User ID is missing or invalid."})
                
            # Convert to int if it's a string
            user_id = int(user_id) if user_id.isdigit() else user_id
            
            # Try to get the user
            user = User.objects.get(id=user_id)
            
            if action == 'approve':
                # Create a profile on create
                created_profile = create_profile(user)

                if created_profile is None:
                   return JsonResponse({'status': False, 'message': "Profile not created. Aborting action, please consult your administrator."})
                
                # Generate random password
                import random
                import string
                random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
                # Update user password
                from django.contrib.auth.hashers import make_password
                user.password = make_password(random_password)
                
                # Approve user
                user.is_active = True
                user.save()
                
                # Send password email
                from .register import send_email_with_code
                send_email_with_code(user.email, random_password, 0, is_password=True)

                return JsonResponse({'status': True, 'message': str(user) + " approved and login credentials sent."})
            
            elif action == 'decline':
                # Send decline email
                send_decline_email(user.email)
                
                # Delete the user
                username = user.student_number
                user.delete()
                
                return JsonResponse({'status': True, 'message': username + " registration declined."})
                
        except User.DoesNotExist:
            return JsonResponse({'status': False, 'message': "User not found. They may have been deleted or never existed."})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'status': False, 'message': f"An error occurred: {str(e)}"})
    else: 
        users = User.objects.filter(is_active = False)
        return render(request, 'admin/user/index.html', {'users': users})
def send_decline_email(email):
    """Send an email notifying the user that their registration was declined"""
    subject = 'Registration Declined'
    message = f"""
    <html>
    <body>
        <h2>Registration Declined</h2>
        <p>We regret to inform you that your registration request has been declined.</p>
        <p>This may be due to one of the following reasons:</p>
        <ul>
            <li>The information provided could not be verified</li>
            <li>The student number does not match our records</li>
            <li>The email address provided is not associated with your student record</li>
        </ul>
        <p>If you believe this is an error, please contact the administration office for assistance.</p>
    </body>
    </html>
    """
    
    from email.mime.text import MIMEText
    import smtplib
    from django.conf import settings
    
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = 'Academic Online Request System<{}>'.format(settings.EMAIL_HOST_USER)
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
    
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