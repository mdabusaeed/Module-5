from django.urls import path
from users.views import activate_user,admin_dashboard,group_list,CustomLoginView,ProfileView,ChangePasswordView
from users.views import activate_user,CustomPasswordResetView,PasswordResetConfirmView,EditProfileView, SignUpView, AssignRoleView,CreateGroupView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView



urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'), 
   
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(), name='edit-profile')
]


  