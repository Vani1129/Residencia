from django.urls import path
from .views import (
    add_member, logout_view, show_societies, add_society, edit_society, subadmin_list,
    edit_subadmin, api_send_otp, api_verify_otp, register, admin_dashboard, generate_otp,
    otp_verify, send_otp_view, society_id_add_subadmin, edit_user, delete_subadmin,
    delete_society, delete_user, society_details, society_id_subadmin_list,
    society_id_admin_dashboard
)
from django.contrib.auth import views as auth_views

from rest_framework import permissions


urlpatterns = [
    path('add-member/', add_member, name='add_member'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('generate_otp/', generate_otp, name='generate_otp'),
    path('otp_verify/', otp_verify, name='otp_verify'),
    path('cms/dashboard/', admin_dashboard, name='cms_dashboard'),
    path('send_otp/', send_otp_view, name='send_otp'),
    path('logout/', logout_view, name='logout'),
    path('add_society/', add_society, name='add_society'),
    path('show_societies/', show_societies, name='show_societies'),
    path('society/edit/<int:id>/', edit_society, name='edit_society'),
    path('society_details/<int:society_id>/add-subadmin/', society_id_add_subadmin, name='society_id_add_subadmin'),
    path('subadmin-list/', subadmin_list, name='subadmin_list'),
    path('subadmin/<int:pk>/edit/', edit_subadmin, name='edit_subadmin'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_subadmin/<int:subadmin_id>/', delete_subadmin, name='delete_subadmin'),
    path('delete_society/<int:society_id>/', delete_society, name='delete_society'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('society_details/<int:society_id>/', society_details, name='society_details'),
    path('society_details/<int:society_id>/subadmin-list/', society_id_subadmin_list, name='society_id_subadmin_list'),
    path('society_details/<int:society_id>/admin_dashboard/', society_id_admin_dashboard, name='society_id_admin_dashboard'),
   
    # api 
    
    path('api/send-otp/', api_send_otp, name='api_send_otp'),
    path('api/verify-otp/', api_verify_otp, name='api_verify_otp'),
    
]
