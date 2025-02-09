
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from core.views import home 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include("tasks.urls")),
    path('__debug__/', include('debug_toolbar.urls')),  
    path('users/', include("users.urls")),
    path('', home, name='home'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)