from django.db import models

# Create your models here.


# Student
class Student(models.Model):
    student_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    course_code = models.IntegerField()

# Course
class Course(models.Model):
    course_code = models.CharField(max_length=64)
    course_name = models.CharField(max_length=64)

# User
class User(models.Model):
    student_number = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
