from rest_framework import serializers
from shop.models import Product, Category
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","category", "name","description","image","price"]
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]