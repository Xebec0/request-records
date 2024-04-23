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

