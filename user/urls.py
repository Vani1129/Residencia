from django.urls import path
from .views import add_member, logout_view, show_societies, add_society, edit_society, add_subadmin, subadmin_list, edit_subadmin
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('add-member/', add_member, name='add_member'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('generate_otp/', views.generate_otp, name='generate_otp'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('cms/dashboard/', views.admin_dashboard, name='cms_dashboard'),
    path('send_otp/', views.send_otp_view, name='send_otp'), 
    # path('delete_user/', delete_user, name='delete_user'),
    path('logout/', logout_view, name='logout'),
    path('add_society/', add_society, name='add_society'),
    path('show_societies/', show_societies, name='show_societies'),
    # path('update-society/<int:society_id>/', update_society, name='update_society'),
    path('society/edit/<int:id>/', edit_society, name='edit_society'),
    path('add-subadmin/', add_subadmin, name='add_subadmin'),
    path('subadmin-list/', subadmin_list, name='subadmin_list'),
    path('subadmin/<int:pk>/edit/', edit_subadmin, name='edit_subadmin'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_subadmin/<int:subadmin_id>/', views.delete_subadmin, name='delete_subadmin'),  
    path('delete_society/<int:society_id>/', views.delete_society, name='delete_society'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    # path('societies/', views.show_societies, name='show_societies'),
    # path('society/<int:society_id>/', views.show_society, name='show_society'),
    # path('show_societies/<int:society_id>/', views.show_societies, name='show_societies_with_id'),
    path('society_details/<int:society_id>/', views.society_details, name='society_details'),
    path('society_details/<int:society_id>/subadmin-list/', views.society_id_subadmin_list, name='society_id_subadmin_list'),
    path('society_details/<int:society_id>/admin_dashboard/', views.society_id_admin_dashboard, name='society_id_admin_dashboard'),

]


