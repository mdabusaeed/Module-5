from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from users.forms import CustomUserCreationForm, PasswordChangeFormView,PasswordResetFormView,SetPasswordForm,EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from users.forms import LoginForm, AssignRollFrom, CreateGroupForm
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model() 

'''
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user = self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user = self.request.user)
        context['form'] = self.form_class(instance = self.object, userprofile = user_profile)

        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
'''

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.is_superuser or user.groups.filter(name__iexact='admin').exists()



def sign_up(request):
    if request.method == 'POST':
        print("Received CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, "Please check your email to activate your account.") 
            return redirect('sign-in')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def sign_in(request): 
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'registration/login.html', {'form': form})  


class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeFormView 
    

class CustomLoginView(LoginView):
    authentication_form = LoginForm 

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid Token")
        
    except User.DoesNotExist:
        return HttpResponse ("User Not Found")
    
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name 
        else: 
            user.group_name = 'No Groupe Assigned'
        

    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRollFrom()

    if request.method == 'POST':
        form = AssignRollFrom(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username} has been assigned to the {role.name} role")
            return redirect('assign-role', user_id=user.id)
        
    return render(request, 'admin/assign-role.html', {'form': form, 'user': user})  

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} has been created.")
            return redirect('create-group')
        
    return render(request, 'admin/create-group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group-list.html', {'groups': groups})

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profileImage'] = user.profileImage
        context['join_since'] = user.date_joined
        context['last_joined'] = user.last_login

        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetFormView
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Please check your email to reset your password.")
        return super().form_valid(form) 
    
class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Please check your email to reset your password.")
        return super().form_valid(form) 