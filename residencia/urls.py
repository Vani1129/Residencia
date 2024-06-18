from django.contrib import admin
from django.urls import path, include
from user import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('society.urls')),
    path('user/', include('user.urls')),
    path('home/', include('home.urls')),
    path('amen/', include('amenities.urls')),
    # path('comm/', include('communication.urls')),
    # path('main/', include('maintenance.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_society/', views.add_society, name='add_society'),
    path('show_societies/', views.show_societies, name='show_societies'),
    path('add_subadmin/', views.add_subadmin, name='add_subadmin'),   
    path('subadmin_list/', views.subadmin_list, name='subadmin_list'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
