from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    LogoutView, PasswordResetDoneView
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_panel, name='admin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name="users/password_reset_form.html"), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
    path('change-role/<int:user_id>/', views.change_role, name='change_role'),

    # Додайте інші URL-шляхи, якщо потрібно
]