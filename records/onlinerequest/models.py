from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Records
class Record(models.Model):
    user_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    course_code = models.CharField(max_length=5)
    middle_name = models.CharField(max_length=64, default='De Guz Man')
    contact_no = models.IntegerField(default='09667614313')
    entry_year_from = models.IntegerField()
    entry_year_to = models.IntegerField()

    def __str__(self):
        return self.user_number
    
# Course
class Course(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)

# Requirement
class Requirement(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} - {self.description}"
    
# Code Table
class Code(models.Model):
    table_name = models.CharField(max_length=64)

# User
class User(AbstractBaseUser):

    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
      (3, 'secretary'),
      (4, 'supervisor'),
      (5, 'admin'),
      (6, 'guest'),  # Added guest user type
    )

    student_number = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=22)
    is_active = models.BooleanField(default=False)
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, default = 1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_number']

    def __str__(self):
        return self.student_number

    def get_user_type_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, 'Unknown')


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ForeignKey to Course (many students can enroll in one course)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, default='De Guz Man')
    contact_no = models.IntegerField(default='09667614313')
    entry_year_from = models.IntegerField(default='2018')
    entry_year_to = models.IntegerField(default='2024')

    def __str__(self):
        return self.first_name

class RegisterRequest(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "register_request")
    valid_id = models.CharField(max_length=254)

# Request
class Document(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

# Requirement
class Requirement(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description

# Request 
class Request(models.Model):
    description = models.CharField(max_length=256)
    files_required = models.CharField(max_length=256)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    price = models.CharField(max_length=6, default=1.00)

    def __str__(self):
        return self.document.description
    
    def delete(self, *args, **kwargs):
            # Store the title of the request before deletion
            deleted_title = self.description
            # Call the parent class delete method to perform the deletion
            super().delete(*args, **kwargs)
            # Return a string indicating that the request has been deleted
            return f"Request '{deleted_title}' has been deleted"
    
    def files_required_as_list(self):
        return self.files_required.split(',')


# User - Request Model
class User_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requests')
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='user_requests')
    status = models.CharField(max_length=64)
    uploads = models.CharField(max_length=999)
    requested = models.CharField(max_length=256, default="")
    purpose = models.CharField(max_length=256, blank=True)
    number_of_copies = models.IntegerField(default=1);
    uploaded_payment = models.CharField(max_length=999, blank=True)
    payment_status = models.CharField(max_length=10, default="Processing", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def uploads_as_list(self):
        return self.uploads.split('')

class Purpose(models.Model):
    description = models.CharField(max_length=256)
    active = models.BooleanField(default=True)