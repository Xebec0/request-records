from django import forms
from .models import User
from .models import Record
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserRegistrationForm(forms.ModelForm):
    student_number = forms.CharField(
        max_length=64,
        error_messages={
            'required': 'Please enter your student number.',
            'unique': 'Invalid student number.'
        }
    )

    email = forms.CharField(
        max_length=64,
        error_messages={
            'required': 'Please enter your email.',
            'unique': 'Invalid student email.'
        }
    )
 
    password = forms.CharField(
        max_length=64,
        error_messages={
            'required': 'Please enter your password.',
        }
    ) 

    user_type = forms.IntegerField(
        error_messages={
            'required': 'Please enter your user type.',
        }
    )

    verification_code = forms.CharField(max_length=6)

    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')

        if student_number:
            # Check if the student number exists in your model
            if not Record.objects.filter(user_number = student_number).exists():
                raise forms.ValidationError('Invalid student number.')

        return student_number

    class Meta:
        model = User
        fields = ['email', 'student_number', 'password', 'user_type']

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password"])

        if commit == True:
            user.save()
        return user


# For modifying user form
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'student_number', 'is_active')

    def clean_password(self):
        return self.initial["password"]