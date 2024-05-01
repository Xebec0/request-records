from django.contrib import admin
from django.urls import path
from onlinerequest.views import views
from onlinerequest.views import register
from onlinerequest.views import login
from onlinerequest.views import dummy
from onlinerequest.views import request
from onlinerequest.views import request_user
from onlinerequest.views import record
from onlinerequest.views import codetable
from onlinerequest.views import admin_user_requests

# Define URL paths here
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main index page
    path('', views.index),

    # Student/User Records
    path('record/', record.index),
    path('record/list/', record.get_user_data),
    path('admin-panel/user-records/', record.index),

    # Register
    path('register/', register.index),

    # Login
    path('login/', login.index),

    # Populate table
    path('dummy/', dummy.index),

    # Signup - Login with Register
    path('signup/', views.signup_view, name="signup"),

    # Admin - Dashboard
    path('admin-panel/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin-panel/', views.admin_dashboard, name="admin_dashboard"),

    # Request - Admin
    path('request/', request.index),
    path('admin-panel/request/', request.index),
    path('request/list/', request.get_requests),
    path('request/<int:id>/delete/', request.delete_request),

    # Request - User
    path('request/user/', request_user.index),
    path('request/<int:id>/', request_user.get_request),
    path('request/user/create/', request_user.create_request),

    # Code Table (This is where to update code tables)
    path('codetable/', codetable.index),
    path('admin-panel/codetable/', codetable.index),

    path('admin-panel/users/requests/', admin_user_requests.index),
]
