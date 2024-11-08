from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings  # Para acceder a las configuraciones de MEDIA_URL y MEDIA_ROOT
from django.conf.urls.static import static  # Para servir archivos estáticos y multimedia
from . import views
from django.conf.urls.i18n import i18n_patterns

# Rutas que no deben tener prefijo de idioma (como las APIs)
urlpatterns = [path('messaging/', include('Messaging.urls')),]  # Incluye las rutas de la app Messaging sin i18n]

# Rutas con soporte de internacionalización
urlpatterns += i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),  # Incluye las urls de la app Users
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Ruta para cerrar sesión
    path('auth/', include('social_django.urls', namespace='social')),  # Ruta para autenticación social (Google, etc.)
    path('', views.home, name='home'),  # Ruta para la página principal
    path('projects/', include('Projects.urls')),  # Incluye las rutas de la app Projects
    path('notifications/', include('Notifications.urls')),  # Incluye las rutas de la app Notifications sin i18n
)

# Configuración para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
