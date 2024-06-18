from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('send_otp/', views.send_otp_view, name='send_otp'),
    # path('generate_otp/', views.generate_otp, name='generate_otp'),
    # path('otp_verify/', views.otp_verify, name='otp_verify'),
    # path('cms/dashboard/', views.admin_dashboard, name='cms_dashboard'),
]
