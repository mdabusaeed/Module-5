from django.urls import path
from tasks.views import manager_dashboard, employee_dashboard, create_task, view_task,update_task,delete_task,task_detail,dashboard, Grettings, CreateTask,UpdateView, ViewProject
from core.views import no_permission

urlpatterns = [
    path('manager-dashboard/', manager_dashboard,name = 'manager-dashboard'),
    path('employee-dashboard/', employee_dashboard,name = 'employee-dashboard'),
    # path('create-task/', create_task,name='create-task'),
    path('create-task/', CreateTask.as_view(),name='create-task'), 
    # path('view-task/', view_task, name='view-task'),
    path('view-task/', ViewProject.as_view(), name='view-task'),
    path('task/<int:pk>/details/', task_detail.as_view(), name='task-detail'),
    # path('update-task/<int:id>/', update_task,name='update-task'),
    path('update-task/<int:pk>/', UpdateView.as_view(), name='update-task'),
    path('delete-task/<int:id>/', delete_task,name='delete-task'),
    path('no-permission/', no_permission, name = 'no-permission'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('grettings/', Grettings.as_view(), name='grettings'),
]
