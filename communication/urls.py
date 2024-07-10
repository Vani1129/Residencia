from django.urls import path
from . import views

urlpatterns = [
    path('main/<int:id>/', views.main_comm, name='main'),
    path('create_comm/<int:id>/', views.create_communication, name='create_comm'),
    path('comm/edit_comm/<int:pk>/<int:id>/', views.edit_communication, name='edit_comm'),
    path('comm/delete_comm/<int:pk>/<int:id>/', views.delete_comm, name='delete_comm'),
    # Other URL patterns...

    # Add other URL patterns here
]
