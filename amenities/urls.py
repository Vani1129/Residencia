from django.urls import path
from . import views

urlpatterns = [
    path('', views.AmenityListView.as_view(), name='amenities'),  # Main page to list amenities
    path('add/', views.add_amenity, name='add_amenity'),         # Page to add a new amenity
    path('edit/<int:pk>/', views.edit_amenity, name='edit_amenity'),
    path('delete/<int:pk>/', views.delete_amenity, name='delete_amenity'),
]