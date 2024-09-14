# NextTask/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),  # Asegúrate de incluir las urls de
    #Agregado segun el video
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')), #Agregamos esta línea
    path('', views.home_view, name='home'),


   
]
