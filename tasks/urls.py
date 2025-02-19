from django.urls import path
from tasks.views import task_detail,dashboard, Grettings, CreateTask,UpdateView, ViewProject,DeleteTaskView
from core.views import no_permission
from tasks.views import ManagerDashboar,EmployeeDashboardView

urlpatterns = [
    path('manager-dashboard/', ManagerDashboar.as_view(),name = 'manager-dashboard'),
    path('employee-dashboard/', EmployeeDashboardView.as_view(),name = 'employee-dashboard'),
    path('create-task/', CreateTask.as_view(),name='create-task'), 
    path('view-task/', ViewProject.as_view(), name='view-task'),
    path('task/<int:pk>/details/', task_detail.as_view(), name='task-detail'),
    path('update-task/<int:pk>/', UpdateView.as_view(), name='update-task'),
    path('delete-task/<int:id>/', DeleteTaskView.as_view(),name='delete-task'),
    path('no-permission/', no_permission, name = 'no-permission'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('grettings/', Grettings.as_view(), name='grettings'),
]
