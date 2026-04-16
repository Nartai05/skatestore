from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # Добавляем название категории текстом для удобства в API
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        # Поля, которые будут видны в JSON-ответе
        fields = ['id', 'name', 'slug', 'category_name', 'price', 'description', 'image', 'available']