from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from ..models import Course, Record, User, Profile, TempRecord
from django.core import serializers
from ..serializers import RecordSerializer
import json


# Main record view
def index(request):
    courses = Course.objects.all()
    return render(request, 'record/index.html', {'courses': courses})
    
def get_user_data(request):
    # Get all users except admins (user_type=5)
    users = User.objects.exclude(user_type=5)
    
    # Create a list to hold user data with record status
    user_data = []
    
    for user in users:
        # Check if user has a record
        has_record = Record.objects.filter(user_number=user.student_number).exists()
        
        user_dict = {
            'id': user.id,
            'student_number': user.student_number,
            'email': user.email,
            'user_type': user.get_user_type_display(),
            'is_active': user.is_active,
            'has_record': has_record
        }
        
        # Try to get user's name from Record or Profile if available
        try:
            if has_record:
                record = Record.objects.get(user_number=user.student_number)
                user_dict['first_name'] = record.first_name
                user_dict['last_name'] = record.last_name
            elif hasattr(user, 'profile'):
                user_dict['first_name'] = user.profile.first_name
                user_dict['last_name'] = user.profile.last_name
            else:
                user_dict['first_name'] = "Unknown"
                user_dict['last_name'] = "Unknown"
        except:
            user_dict['first_name'] = "Unknown"
            user_dict['last_name'] = "Unknown"
            
        user_data.append(user_dict)
    
    return JsonResponse(json.dumps(user_data), safe=False)
def get_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    courses = Course.objects.all()
    
    # Check for existing record
    record_type = "new"
    profile_data = {
        'user_id': user.id,
        'student_number': user.student_number,
        'email': user.email,
        'record_type': 'new'
    }
    
    # Try to find record in Record table
    try:
        record = Record.objects.get(user_number=user.student_number)
        profile_data.update({
            'first_name': record.first_name,
            'middle_name': record.middle_name,
            'last_name': record.last_name,
            'course_code': record.course_code,
            'contact_no': record.contact_no,
            'entry_year_from': record.entry_year_from,
            'entry_year_to': record.entry_year_to,
            'record_type': 'existing'
        })
    except Record.DoesNotExist:
        # Check if user has a temp record from a request
        try:
            # Get the most recent temp record if multiple exist
            temp_record = TempRecord.objects.filter(
                user_request__user=user
            ).order_by('-user_request__created_at').first()
            
            if temp_record:
                profile_data.update({
                    'first_name': temp_record.first_name,
                    'middle_name': temp_record.middle_name,
                    'last_name': temp_record.last_name,
                    'course_code': temp_record.course_code,
                    'contact_no': temp_record.contact_no,
                    'entry_year_from': temp_record.entry_year_from,
                    'entry_year_to': temp_record.entry_year_to,
                    'record_type': 'temp_record'
                })
        except:
            pass
    
    return render(request, 'admin/user/profile_form.html', {
        'profile': profile_data,
        'courses': courses
    })

def save_user_profile(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get('user_id')
            record_type = request.POST.get('record_type')
            user = get_object_or_404(User, id=user_id)
            
            # Prepare data for creating/updating record
            record_data = {
                'user_number': user.student_number,
                'first_name': request.POST.get('first_name'),
                'middle_name': request.POST.get('middle_name'),
                'last_name': request.POST.get('last_name'),
                'course_code': request.POST.get('course_code'),
                'contact_no': request.POST.get('contact_no'),
                'entry_year_from': request.POST.get('entry_year_from'),
                'entry_year_to': request.POST.get('entry_year_to'),
            }
            
            # Create or update record
            record, created = Record.objects.update_or_create(
                user_number=user.student_number,
                defaults=record_data
            )
            
            return JsonResponse({
                'status': True,
                'message': 'Profile updated successfully.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'status': False,
        'message': 'Invalid request method.'
    })

def delete_record(request, id):
    if request.method == "POST":
        try:
            record = Record.objects.get(id=id)
            record_number = record.user_number
            record.delete()
            return JsonResponse({
                'status': True, 
                'message': f'Record {record_number} has been deleted successfully.'
            })
        except Record.DoesNotExist:
            return JsonResponse({
                'status': False, 
                'message': 'Record not found.'
            })
        except Exception as e:
            return JsonResponse({
                'status': False, 
                'message': f'An error occurred: {str(e)}'
            })
    else:
        return JsonResponse({
            'status': False, 
            'message': 'Invalid request method.'
        })
