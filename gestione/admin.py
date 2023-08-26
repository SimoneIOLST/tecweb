from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Mezzo)
admin.site.register(ImmaginiMacchina)
admin.site.register(Venditore)
admin.site.register(Accessorio)
admin.site.register(ImmaginiAccessorio)
admin.site.register(FavouriteMezzo)
admin.site.register(FavouriteAccessorio)