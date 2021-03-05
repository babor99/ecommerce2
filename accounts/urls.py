from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import *
from .forms import *

urlpatterns = [
  path('user_register/', user_register, name='user_register'),
  path('user_login/', user_login, name='user_login'),
  path('user_logout/', user_logout, name='user_logout'),

  path('password_change/',  login_required(PasswordChangingView.as_view()), name='password_change'),
  path('password_change_success/', password_change_success, name='password_change_success'),

  path('password_reset/', 
  	auth_views.PasswordResetView.as_view(
  		template_name='accounts/password_reset.html',
  		form_class= MyPasswordResetForm), name='password_reset'),

  path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),

  path('reset/<uidb64>/<token>/', 
  	auth_views.PasswordResetConfirmView.as_view(
  		template_name='accounts/password_reset_confirm.html', 
  		form_class= MySetPasswordResetForm), name='password_reset_confirm'),

  path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

] 

# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']