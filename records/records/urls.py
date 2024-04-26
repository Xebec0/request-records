from django.contrib import admin
from django.urls import path
from onlinerequest.views import views
from onlinerequest.views import register
from onlinerequest.views import login
from onlinerequest.views import dummy
from onlinerequest.views import request
from onlinerequest.views import request_user

# Define URL paths here
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main index page
    path('', views.index),

    # Register
    path('register/', register.index),

    # Login
    path('login/', login.index),

    # Populate table
    path('dummy/', dummy.index),

    # Signup - Login with Register
    path('signup/', views.signup_view, name="signup"),

    # Request - Admin
    path('request/', request.index),
    path('request/list/', request.get_requests),
    path('request/<int:id>/delete/', request.delete_request),

    # Request - User
    path('request/user/', request_user.index),
    path('request/<int:id>/', request_user.get_request),
    path('request/user/create/', request_user.create_request),
]
