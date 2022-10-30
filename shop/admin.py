from django.contrib import admin
from shop.models import Product, Category
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug":("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["category", "name","available"]
    prepopulated_fields = {"slug":("name",)}
