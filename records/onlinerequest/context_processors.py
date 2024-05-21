from onlinerequest.models import Record, Request

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