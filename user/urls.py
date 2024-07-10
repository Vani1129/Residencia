from django.urls import path
from . import views
from .views import (
    add_resident, logout_view, show_societies, add_society, edit_society, id_subadmin_list,
    edit_subadmin, api_send_otp,api_verify_otp, register,  generate_otp,
    otp_verify, send_otp_view, id_add_subadmin, edit_user, delete_subadmin,
    delete_society, delete_user, society_details, id_subadmin_list, admin_dashboard,
    id_admin_dashboard,subadmin_list,add_subadmin,otp_page
) 
from django.contrib.auth import views as auth_views
from rest_framework import permissions


urlpatterns = [
    path('add_resident/<int:building_id>/<int:id>/', views.add_resident, name='add_resident'),
    path('society/<int:id>/register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin_dashboard/<int:id>/', admin_dashboard, name='admin_dashboard'),
    path('generate_otp/', generate_otp, name='generate_otp'),
    path('otp_verify/', otp_verify, name='otp_verify'),
    path('otp_page/', otp_page, name='otp_page'),
    path('cms/dashboard/', admin_dashboard, name='cms_dashboard'),
    path('send_otp/', send_otp_view, name='send_otp'),
    path('logout/', logout_view, name='logout'),
    path('add_society/', add_society, name='add_society'),
    path('show_societies/', show_societies, name='show_societies'),
    path('society/edit/<int:id>/', edit_society, name='edit_society'),
    path('society_details/<int:id>/add_subadmin/', id_add_subadmin, name='id_add_subadmin'),
  
    path('subadmin/<int:pk>/edit/', edit_subadmin, name='edit_subadmin'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),

    path('delete_subadmin/<int:subadmin_id>/', delete_subadmin, name='delete_subadmin'),
    path('user/delete_society/<int:id>/', views.delete_society, name='delete_society'),

    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('society_details/<int:id>/', society_details, name='society_details'),
    
    path('subadmin_list/',subadmin_list, name='subadmin_list'),
    path('add_subadmin/',add_subadmin, name='add_subadmin'),
    
    path('members/', views.member_list, name='member_list'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:pk>/update/', views.member_update, name='member_update'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('delete_resident/<int:resident_id>/', views.delete_resident, name='delete_resident'),

    path('family-members/', views.family_member_list, name='family_member_list'),
    path('family-members/<int:pk>/', views.family_member_detail, name='family_member_detail'),
    path('family-members/create/', views.family_member_create, name='family_member_create'),
    path('family-members/<int:pk>/update/', views.family_member_update, name='family_member_update'),
    path('family-members/<int:pk>/delete/', views.family_member_delete, name='family_member_delete'),
    
    path('society_details/<int:id>/subadmin_list/', views.id_subadmin_list, name='id_subadmin_list'),
    path('society_details/<int:id>/add_subadmin/', views.id_add_subadmin, name='id_add_subadmin'),
    path('society_details/<int:id>/admin_dashboard/', id_admin_dashboard, name='id_admin_dashboard'),

   
   
    # api 
    

    path('api/send-otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify-otp/', views.api_verify_otp, name='api_verify_otp'),
    path('api/member/profile/', views.api_member_profile, name='api_member_profile'),
   ]


