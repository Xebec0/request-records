from onlinerequest.models import Record, Request, Profile

def user_record(request):
    if request.user.is_authenticated:
        try:
            user_record = Record.objects.get(user_number=request.user.student_number)
            return {'user_record': user_record}
        except Record.DoesNotExist:
            return {}
    return {}

def request_forms(request):
    request_forms = Request.objects.all()
    return {'request_forms': request_forms}

def user_profile(request):
    """Make the user's profile available to all templates if authenticated"""
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'user_profile': profile}
        except Profile.DoesNotExist:
            return {'user_profile': None}
    return {'user_profile': None}
    return {'request_forms': request_forms}