from django.contrib import admin
from django.urls import path
from onlinerequest.views import views, register, login, dummy, request, request_user, record, codetable, user_approval_view, profile

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
    path('send-verification-email/', register.send_verification_email, name='send_verification_email'),

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
    # User Approval
    path('admin-panel/user-accounts/', user_approval_view.index),
    # Logout
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/user-accounts/', user_approval_view.index),
    # Profile
    path('profile/', profile.index)
]
