"""tecweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = "gestione"

urlpatterns = [
    path('mezzo/<int:pk>/', MezzoDetailView.as_view(), name='mezzo-detail'),
    path('listamezzi/', MezzoListView.as_view(), name='mezzo-list'),
    path('accessorio/<int:pk>/', AccDetailView.as_view(), name='acc-detail'),
    path('listaacc/', AccListView.as_view(), name='acc-list'),
    path('creamezzo/', CreateMezzoView.as_view(), name="mezzo-crea"),
    path('creaimmmacc/<int:car_id>/', CreateImmaginiMacchinaView.as_view(), name="IM-crea"),
    path('creaaccessorio/', CreateAccView.as_view(), name="acc-crea"),
    path('creaIA/<int:acc_id>/', CreateImmaginiAccessorioView.as_view(), name="IA-crea"),
    path('dashboard/', dashbord, name="dashboard"),
    path('venditore/oggetti/', login_required(oggetti_venditore), name='ogg-vend'),
    path('venditore/oggetti/update/mezzo/<int:pk>/', MezzoUpdateView.as_view(), name='update_mezzo'),
    path('venditore/oggetti/update/accessorio/<int:pk>/', AccessorioUpdateView.as_view(), name='update_accessorio'),

]