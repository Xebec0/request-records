from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from onlinerequest.models import Request, Requirement, User_Request

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

