from django.contrib import admin

from .models import Category, MenuItem, Rating

# admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(MenuItem)
# admin.site.register(Order)
admin.site.register(Rating)