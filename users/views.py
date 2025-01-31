from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from users.forms import LoginForm, AssignRollFrom
from django.contrib.auth.tokens import default_token_generator 


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
    
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRollFrom()

    if request.method == 'POST':
        form = AssignRollFrom(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"Role {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign-role.html', {'form': form, 'user': user})  

 
