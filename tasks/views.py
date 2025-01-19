from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user.dashboard.html")

def test(request):
    context={
        'names' : ['Mahmud','Jake','Jiko']
    }
    return render(request, "test.html",context)

def create_task(request):
    # employee = Employee.objects.all()
    form = TaskModelForm()
    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():

            ''' For Model Form Data '''
            form.save()
            return render(request,'task_form.html', {"form": form, "message": 'Task Added Successfully'})
            ''' For Djano Form Data '''


    context = {"form": form}
    return render(request,"task_form.html",context)

def view_task(request):
    tasks = Task.objects.all()
    return render(request,"show_task.html",{'tasks':tasks})
 