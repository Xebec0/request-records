from django.shortcuts import redirect
from django.urls import reverse

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path.startswith('/admin-panel/') or request.path.startswith('/request/') or request.path.startswith('/user/'):
                return redirect('/signup')  # Redirect to login page for admin and request pages

        elif request.user.user_type == 5:
            if request.path.startswith('/user/'):
                return redirect('/admin-panel/')

        elif request.user.user_type != 5:
            if request.path.startswith('/admin-panel/'):
                return redirect('/user/dashboard/')  # Redirect non-admin users accessing admin pages

        response = self.get_response(request)
        return response
