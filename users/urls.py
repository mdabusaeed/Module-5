from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user
from core.views import home
# from users.views import activate_user


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    path('home/', home, name='home'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 
]


