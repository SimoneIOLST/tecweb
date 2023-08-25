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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#erase_db()
#init_db()