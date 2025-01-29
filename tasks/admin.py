from django.contrib import admin
from tasks.models import Employee, Project, Task, TaskDetails

admin.site.register(Task)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(TaskDetails)