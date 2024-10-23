from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('jobseeker', 'Job Seeker'),
        ('hr', 'HR'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Register as")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  # Assign the role from the form
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())




#----------------------------------jobseeker form for apply-------------------------------------------------------
# forms.py

from django import forms
from .models import JobSeeker

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['full_name', 'email', 'resume', 'applied_position']  # Ensure these fields match your model
