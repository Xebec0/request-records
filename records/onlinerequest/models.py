from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Records (Separate db, this is where main records for teachers and students are saved)
class Record(models.Model):
    student_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    course_code = models.CharField(max_length=5)

# Course
class Course(models.Model):
    course_code = models.CharField(max_length=64)
    course_name = models.CharField(max_length=64)

# User
class User(AbstractBaseUser):

    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
      (3, 'secretary'),
      (4, 'supervisor'),
      (5, 'admin'),
    )

    student_number = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=22)
    is_active = models.BooleanField(default=False)
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, default = 1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_number']

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ForeignKey to Course (many students can enroll in one course)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

class RegisterRequest(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "register_request")
    valid_id = models.CharField(max_length=254)

# Request
class Document(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.description}"

class Request(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    files_required = models.CharField(max_length=256)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
            # Store the title of the request before deletion
            deleted_title = self.title
            # Call the parent class delete method to perform the deletion
            super().delete(*args, **kwargs)
            # Return a string indicating that the request has been deleted
            return f"Request '{deleted_title}' has been deleted"
    
    def files_required_as_list(self):
        return self.files_required.split(',')
