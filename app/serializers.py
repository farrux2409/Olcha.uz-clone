from rest_framework import serializers
from app.models import Product, Category, Groups


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'

