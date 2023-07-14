from django.contrib import admin
from .models import Item, Favorite, Review, Order

admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(Order)