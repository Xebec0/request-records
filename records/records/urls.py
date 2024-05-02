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
from onlinerequest.views import user_approval_view

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

    # User - Dashboard
    path('user/dashboard/', views.user_dashboard),
    path('user/', views.user_dashboard),

    # Request - Admin
    path('request/', request.index),
    path('admin-panel/request/', request.index),
    path('admin-panel/user-request/', request.display_user_requests),
    path('admin-panel/user-request/<int:id>/delete', request.delete_user_request),
    path('admin-panel/user-request/<int:id>', request.display_user_request),
    path('request/list/', request.get_requests),
    path('request/<int:id>/delete/', request.delete_request),

    # Request - User
    path('request/user/', request_user.index),
    path('request/<int:id>/', request_user.get_request),
    path('get-document-description/<str:doc_code>/', request_user.get_document_description),
    path('request/user/create/', request_user.create_request),
    path('user/create-request/', request_user.index),
    path('user/view-request/', request_user.display_user_requests),

    # Code Table (This is where to update code tables)
    path('codetable/', codetable.index),
    path('admin-panel/codetable/', codetable.index),

    path('admin-panel/user-accounts/', user_approval_view.index),
]
