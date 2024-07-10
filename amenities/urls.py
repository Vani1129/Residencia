from django.urls import path

from . import views

urlpatterns = [
    # path('amenities/', views.AmenityListView.as_view(), name='amenities'),
    path('amen/amenities/<int:id>/', views.amenities, name='amenities'),
    path('amenity/add/<int:id>/', views.add_amenity, name='add_amenity'),
    path('amenity/edit/<int:id>/<int:pk>/', views.edit_amenity, name='edit_amenity'),
    path('amenity/delete/<int:id>/<int:pk>/', views.delete_amenity, name='delete_amenity'),
    # Other URLs as needed
]
