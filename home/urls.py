from django.urls import path
from . import views
from django.urls import path



# cms_patterns = [
#     path('cms', cms.home, name='cms_home'),
# ]

urlpatterns = [
    path('', views.home, name='home'),
    # path('db', views.db, name='db'),
    
] 
# + cms_patterns