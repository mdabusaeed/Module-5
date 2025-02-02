from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard, create_task, view_task,update_task,delete_task,task_details
from core.views import no_permission

urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name = 'manager-dashboard'),
    path('employee-dashboard/', employee_dashboard,name = 'employee-dashboard'),
    path('create-task/', create_task,name='create-task'),
    path('create-task/', create_task,name='create-task'), 
    path('view-task/', view_task),
    path('task/<int:task_id>/details/', task_details, name='task-detail'),
    path('update-task/<int:id>/', update_task,name='update-task'),
    path('delete-task/<int:id>/', delete_task,name='delete-task'),
    path('no-permission/', no_permission, name = 'no-permission'),

]
