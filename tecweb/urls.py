"""
URL configuration for tecweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .initcmds import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$|^/$|^home/$", home_page, name="home"),
    path('gestione/', include('gestione.urls')),
    path('get_filtered_mezzi/', get_filtered_mezzi, name='get_filtered_mezzi'),
    path('get_filtered_acc/', get_filtered_acc, name='get_filtered_acc'),
    path("register/", register_request, name="register"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('authHome/', authHome_page, name="authHome_page"),
    path('add_to_favorites/<str:object_type>/<int:object_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:object_type>/<int:object_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favoriti/', favorite_objects, name='favoriti'),
    path('add_to_cart/<str:object_type>/<int:object_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:object_type>/<int:object_id>/', remove_from_cart, name='remove_from_cart'),
    path('carrello/', view_cart, name='carrello'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#erase_db()
#init_db()