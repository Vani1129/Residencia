from django.urls import path
from . import views
from user.views import add_resident,delete_resident

urlpatterns = [
    path('', views.home, name='home'),
    path('create-society-profile/<int:society_id>/', views.soc_profile, name='society_id_soc_profile'),
    
    path('society-profile-admin/', views.society_profile_admin_view, name='society_id_soc_profile_admin'),
    path('society/<int:society_id>/buildings/', views.building_list_view, name='building_list'),
    path('society/<int:society_id>/add_building/', views.add_building_view, name='add_building'),
    path('buildings/edit/<int:building_id>/', views.edit_building, name='edit_building'),
    path('buildings/delete/<int:building_id>/', views.delete_building, name='delete_building'),
    path('buildings/<int:building_id>/', views.floor_data_view, name='buildig_floor_data'),
    path('units/add/', views.add_unit, name='add_unit'),
    path('units/edit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    path('units/delete/<int:unit_id>/', views.delete_unit, name='delete_unit'),
    # path('floor-data/<int:society_id>/<int:building_id>/', views.resident_list, name='floor_data'),
    # path('floor-data/<int:building_id>/<int:society_id>/', views.floor_data_view ,name='floor_data'),
    path('add_resident/<int:building_id>/<int:society_id>/', add_resident, name='add_resident'),
    path('delete_resident/<int:resident_id>/', delete_resident, name='delete_resident'),
    
    # Uncomment these if you want to include them
    # path('user/society_details/<int:society_id>/soc_profile/', views.soc_profile, name='society_id_soc_profile'),
    # path('user/society_details/<int:society_id>/society_profile_list/', views.society_profile_list, name='society_id_society_profile_list'),
    # path('add_society_profile/', views.add_society_profile, name='add_society_profile'),
    # path('edit_society_profile/<int:society_profile_id>/', views.edit_society_profile, name='edit_society_profile'),
    # path('delete_society_profile/<int:society_profile_id>/', views.delete_society_profile, name='delete_society_profile'),
    # path('society_profile_list/', views.society_profile_list, name='society_profile_list'),
]