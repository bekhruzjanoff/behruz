from django.contrib import admin
from .models import Category, Product

# Показываем в админ панели
admin.site.register(Category)
admin.site.register(Product)
