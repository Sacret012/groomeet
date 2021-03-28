"""groomeet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from groomeet_backend import views, likes, bandas
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('',views.index, name='index'),
    path('listado/',views.listadoMusicos),
    path("like/<int:pk>/", likes.postLike, name="like"),
    path("noLike/<int:pk>/", likes.postNoLike, name="noLike"),
    path('createBanda/',bandas.bandaCreate),
    path('createMiembroNoRegistrado/<int:pk>',bandas.miembroNoRegistradoCreate),
    path('misBandas/',views.listadoMisBandas),
    path('updateBanda/<int:id>', bandas.bandaUpdate, name='updateBanda'),
    path('deleteBanda/<int:id>', bandas.bandaDelete, name='deleteBanda'),
    path('invitacionBanda/<int:receptor_id>/<int:banda_id>/', bandas.enviarInvitacionBanda),
    path('aceptarInvitacion/<int:banda_id>/', bandas.aceptarInvitacionBanda),
]
