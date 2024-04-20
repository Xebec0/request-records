from django.contrib import admin
from django.urls import path
from onlinerequest.views import views
from onlinerequest.views import register
from onlinerequest.views import login
from onlinerequest.views import dummy

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
    path('dummy/', dummy.index)
]
