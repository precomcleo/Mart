from django.contrib import admin
from .models import Product, Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]