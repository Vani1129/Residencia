from django.urls import path
from . import views
from user.views import add_resident, delete_resident, edit_resident

urlpatterns = [
    path('', views.home, name='home'),
    path('create-society-profile/<int:id>/', views.soc_profile, name='id_soc_profile'),
    path('society-profile-admin/', views.Societyprofile_admin_view, name='id_soc_profile_admin'),
    path('society/<int:id>/buildings/', views.building_list_view, name='building_list'),
    path('society/<int:id>/add_building/', views.add_building_view, name='add_building'),
    path('buildings/edit/<int:building_id>/', views.edit_building, name='edit_building'),
    
    path('delete_building/<int:building_id>/', views.delete_building, name='delete_building'),
    # path('buildings/<int:building_id>/', views.floor_data_view, name='building_floor_data'),
    # path('units/edit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    # path('units/delete/<int:unit_id>/', views.delete_unit, name='delete_unit'),
    path('add_resident/<int:building_id>/<int:id>/', add_resident, name='add_resident'),
    path('delete_resident/<int:resident_id>/', delete_resident, name='delete_resident'),
    path('edit_resident/<int:member_id>/<int:id>/<int:building_id>/', edit_resident, name='edit_resident'),
  
  
  #api
  
    path('api/society-profile/', views.soc_profile_api, name='soc_profile_api'),
]
