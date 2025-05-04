from django.contrib import admin
from .models import Recipe, Category


class CategoryAdmin(admin.ModelAdmin):
    ...
    
admin.site.register(Category, CategoryAdmin)
