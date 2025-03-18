from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from onlinerequest.models import Request, Requirement, User_Request, Profile

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

def user_reports(request):
    user_records = User_Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/reports.html', {'user_records': user_records})

# Analytics
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractDay, ExtractHour

def request_analytics(request):
    return render(request, 'admin/analytics.html')

def get_request_stats(request):
    filter_type = request.GET.get('filter', 'week')
    
    # Date filtering
    now = timezone.now()
    if filter_type == 'day':
        start_date = now - timedelta(days=1)
    elif filter_type == 'week':
        start_date = now - timedelta(weeks=1)
    else:  # month
        start_date = now - timedelta(days=30)
        
    # Get requests within date range
    requests = User_Request.objects.filter(created_at__gte=start_date)
    
    # Most requested documents
    doc_stats = requests.values('request__document__description')\
                       .annotate(count=Count('id'))\
                       .order_by('-count')
    
    # Processing time stats
    completed_requests = requests.filter(status='Completed')
    processing_times = []
    
    for req in completed_requests:
        time_diff = req.updated_at - req.created_at
        days = time_diff.days
        hours = time_diff.seconds // 3600
        status = 'Completed'
        
        if time_diff > timedelta(days=3):
            status = 'late'
            
        processing_times.append({
            'request_id': req.id,
            'days': days,
            'hours': hours,
            'status': status
        })

    return JsonResponse({
        'total_requests': requests.count(),
        'document_stats': list(doc_stats),
        'processing_times': processing_times
    })

# Add the new API endpoint for detailed request data
def get_request_details(request):
    # Get all user requests
    user_requests = User_Request.objects.select_related(
        'user', 'request', 'request__document'
    ).prefetch_related(
        'user__profile'
    ).order_by('-created_at')
    
    # Prepare data for DataTable
    data = []
    for req in user_requests:
        # Calculate processing time
        processing_time = ""
        date_completed = ""
        
        if req.status == "Completed":
            # Use updated_at as completion date for completed requests
            date_completed = req.updated_at.strftime('%b %d, %Y')
            
            # Calculate processing time
            time_diff = req.updated_at - req.created_at
            days = time_diff.days
            hours = time_diff.seconds // 3600
            processing_time = f"{days} days, {hours} hours"
        
        # Get profile information if available
        try:
            profile = Profile.objects.get(user=req.user)
            name = f"{profile.first_name} {profile.middle_name} {profile.last_name}"
            contact = profile.contact_no
        except Profile.DoesNotExist:
            name = req.user.student_number
            contact = "N/A"
        
        # Add request to data
        data.append({
            'reference_number': f"REQ-{req.id:06d}",
            'date_requested': req.created_at.strftime('%b %d, %Y'),
            'client_type': req.user.get_user_type_display(),
            'requested_by': name,
            'contact_details': contact,
            'email': req.user.email,
            'service_type': req.request.document.description,
            'purpose': req.purpose,
            'status': req.status,
            'schedule': "N/A",  # This field isn't available in the current model
            'date_completed': date_completed,
            'date_released': "N/A",  # This field isn't available in the current model
            'processing_time': processing_time
        })
    
    return JsonResponse(data, safe=False)