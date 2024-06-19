from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('create-society-profile/', views.create_society_profile, name='create_society_profile'),
    path('user/society_details/<int:society_id>/create_society_profile/', views.create_society_profile, name='society_id_create_society_profile'),
    path('user/society_details/<int:society_id>/society_profile_list/', views.society_profile_list, name='society_id_society_profile_list'),
    path('add_society_profile/', views.add_society_profile, name='add_society_profile'),
    path('edit_society_profile/<int:society_profile_id>/', views.edit_society_profile, name='edit_society_profile'),
    # path('delete_society_profile/<int:society_profile_id>/', views.delete_society_profile, name='delete_society_profile'),
    path('delete_society_profile/<int:society_profile_id>/', views.delete_society_profile, name='delete_society_profile'),
    path('society_profile_list/', views.society_profile_list, name='society_profile_list'),
    
]
