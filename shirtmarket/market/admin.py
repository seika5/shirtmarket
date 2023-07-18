from django.contrib import admin
from .models import Item, Favorite, Order

admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Order)