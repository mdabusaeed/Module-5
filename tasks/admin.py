from django.contrib import admin
from tasks.models import  Project, Task, TaskDetails

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(TaskDetails)