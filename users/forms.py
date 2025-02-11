from django import forms
from django.contrib.auth.models import User, Permission, Group
import re
from tasks.forms import StyleForMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
    
class LoginForm(StyleForMixin, AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRollFrom(StyleForMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        empty_label = "Select a role"
    )

class CreateGroupForm(StyleForMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField( 
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

        
class PasswordChangeFormView(StyleForMixin, PasswordChangeForm):
    pass
class PasswordResetFormView(StyleForMixin, PasswordResetForm):
    pass
class SetPasswordForm(StyleForMixin, SetPasswordForm):
    pass


'''
class EditProfileForm(StyleForMixin,forms.ModelForm):
    class Meta:
        model = User
        fields  = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profileImage = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profileImage'].initial = self.userprofile.profileImage

    def save(self, commit = True):
        user = super().save(commit=False)

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profileImage = self.cleaned_data.get('profileImage')

            if commit:
                self.userprofile.save()

        if commit:
            user.save()

        return user
'''

class EditProfileForm(StyleForMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields  = ['email', 'first_name', 'last_name', 'bio','profileImage']






