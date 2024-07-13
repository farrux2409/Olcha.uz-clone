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
    category = CategoryModelSerializer(read_only=True)

    class Meta:
        model = Groups
        fields = ['id', 'group_name', 'slug', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        group = Groups.objects.create(category=category, **validated_data)
        return group
