from django.contrib import admin

from .models import Category, MenuItem, Order, Rating

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Rating)