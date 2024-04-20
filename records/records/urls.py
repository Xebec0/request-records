
from django.contrib import admin
from django.urls import path
from onlinerequest.views import views


# Define URL paths here
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main index page
    path('', views.index)
]
