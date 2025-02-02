from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='sign-in')  # ✅ Redirects if not logged in
def home(request):
    print(f"User accessing home: {request.user}")  # ✅ Debug print
    return render(request, 'home.html', {'user': request.user})

def no_permission(request):
    return render(request,'no-permission.html')