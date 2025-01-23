from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def generate_key_from_user(user_id):
    return hashlib.sha256(str(user_id).encode()).digest()

def encrypt_data(data, key):
    if not data:
        return ''
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    data_bytes = data.encode()
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)
    return base64.b64encode(nonce + tag + ciphertext).decode('utf-8')

def decrypt_data(encrypted_data, key):
    if not encrypted_data:
        return ''
    try:
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        nonce = encrypted_bytes[:16]
        tag = encrypted_bytes[16:32]
        ciphertext = encrypted_bytes[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data.decode('utf-8')
    except:
        return ''

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
    
class Course(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)

class Requirement(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.code} - {self.description}"
    
class Code(models.Model):
    table_name = models.CharField(max_length=64)

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
      (3, 'secretary'),
      (4, 'supervisor'),
      (5, 'admin'),
      (6, 'guest'),
    )

    student_number = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=256)  # Increased length for hash
    is_active = models.BooleanField(default=False)
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, default = 1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_number']

    def __str__(self):
        return self.student_number

    def get_user_type_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, 'Unknown')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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

class Document(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class Request(models.Model):
    description = models.CharField(max_length=256)
    files_required = models.CharField(max_length=256)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    price = models.CharField(max_length=6, default=1.00)

    def __str__(self):
        return self.document.description
    
    def delete(self, *args, **kwargs):
        deleted_title = self.description
        super().delete(*args, **kwargs)
        return f"Request '{deleted_title}' has been deleted"
    
    def files_required_as_list(self):
        return self.files_required.split(',')

class User_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requests')
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='user_requests')
    status = models.CharField(max_length=64)
    uploads = models.TextField()  
    requested = models.CharField(max_length=256, default="")
    purpose = models.CharField(max_length=256, blank=True)
    number_of_copies = models.IntegerField(default=1)
    uploaded_payment = models.TextField(blank=True)
    payment_status = models.CharField(max_length=10, default="Processing", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_uploads(self, uploads_list):
        if not uploads_list:
            self.uploads = ''
            return
        
        key = generate_key_from_user(self.user.id)
        encrypted_paths = [encrypt_data(path, key) for path in uploads_list]
        self.uploads = ','.join(encrypted_paths)

    def get_uploads(self):
        if not self.uploads:
            return []
        
        key = generate_key_from_user(self.user.id)
        encrypted_paths = self.uploads.split(',')
        return [decrypt_data(path, key) for path in encrypted_paths]

    def uploads_as_list(self):
        return self.get_uploads()
    
class Purpose(models.Model):
    description = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to='reports/templates/')
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
