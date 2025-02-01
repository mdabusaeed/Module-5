from django.shortcuts import render
from django.conf import settings

def home(request):
    return render(request,'home.html')

def no_permission(request):
    return render(request,'no-permission.html')