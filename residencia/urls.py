from django.contrib import admin
from django.urls import path, include
from user import views
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import permissions



schema_view = get_schema_view(
   openapi.Info(
      title="User API",
      default_version='v1',
      description="API documentation for User app",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@user.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('society.urls')),
    path('users/', include('user.urls')),
    path('home/', include('home.urls')),
    path('amen/', include('amenities.urls')),
    # path('comm/', include('communication.urls')),
    # path('main/', include('maintenance.urls')),
    path('login/', views.login_view, name='login'),
    path('society/<int:society_id>/register/', views.register, name='register'),
   #  path('send-otp/', views.send_otp_view, name='send_otp'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_society/', views.add_society, name='add_society'),
    path('show_societies/', views.show_societies, name='show_societies'),
   #  path('add_subadmin/', views.society_id_add_subadmin, name='society_id_add_subadmin'),   
    path('subadmin_list/', views.society_id_subadmin_list, name='subadmin_list'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('floor-data/<int:society_id>/<int:building_id>/', views.resident_list, name='floor_data'),
    path('add_resident/<int:building_id>/<int:society_id>/', views.add_resident, name='add_resident'),
    # other patterns...
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
