from django.contrib import admin
from .models import Item, Favorite, Review, Purchased, Post

admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(Purchased)
admin.site.register(Post)