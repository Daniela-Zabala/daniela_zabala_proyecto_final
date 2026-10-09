"""
URL configuration for daniela_zabala_proyecto_final_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from catalogo import views


urlpatterns = [

    #panel de administracion de Django
    path('admin/', admin.site.urls),

    # Páginas principales de TechCovers
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),

    #gestion de productos
    path(
        'producto/nuevo/',
        views.crear_producto,
        name='crear_producto'
    ),

    path(
        'producto/editar/<int:producto_id>/',
        views.editar_producto,
        name='editar_producto'
    ),

    path(
        'producto/eliminar/<int:producto_id>/',
        views.eliminar_producto,
        name='eliminar_producto'
    ),

    #reservas
    path(
        'reserva/nueva/<int:producto_id>/',
        views.crear_reserva,
        name='crear_reserva'
    ),

    path(
        'reserva/editar/<int:reserva_id>/',
        views.editar_reserva,
        name='editar_reserva'
    ),

    path(
        'reserva/eliminar/<int:reserva_id>/',
        views.eliminar_reserva,
        name='eliminar_reserva'
    ),

    #registro de usuarios
    path(
        'accounts/registro/',
        views.registro,
        name='registro'
    ),

    #inicio de sesion
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registro/login.html'
        ),
        name='login'
    ),

    #cierre de sesion
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    #mis reservas
    path(
        'mis-reservas/',
        views.mis_reservas,
        name='mis_reservas'
    ),
]