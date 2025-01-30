from django import forms
from django.contrib.auth.models import User
import re
from tasks.forms import StyleForMixin
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(StyleForMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        errors = []

        # Check if passwords match
        if password1 != password2:
            errors.append('Passwords do not match.')

        # Check password length
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')

        # Check password contains allowed characters and enforce rules
        if not re.search(r'[A-Z]', password1):
            errors.append('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password1):
            errors.append('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password1):
            errors.append('Password must contain at least one digit.')
        if not re.search(r'[@#$%^&+=]', password1):
            errors.append('Password must contain at least one special character (@#$%^&+=).')

        if errors:
            raise forms.ValidationError(errors)

        return password2
    
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     allowed_domains = ['gmail.com','hotmail.com','outlook.com','yahoo.com','aol.com','bltiwd.com']

    #     email_domain = email.split('@')[-1]

    #     if email_domain not in allowed_domains:
    #         raise forms.ValidationError('Please use a valid email address.')
        
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Email already in use.')
        
    #     return email
    
class LoginForm(StyleForMixin, AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    

        












