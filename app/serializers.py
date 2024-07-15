from rest_framework import serializers
from app.models import Product, Category, Groups, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='group.group_name')
    group_id = serializers.IntegerField(source='group.id')
    group_slug = serializers.CharField(source='group.slug')


    def get_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        if image:
            serializer = ImageSerializer(image)
            return serializer.data['image']

        return None

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'group', 'description', 'image', 'rating', 'price',
                  'discount', 'group_name', 'group_id', 'group_slug']


class GroupModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    products = ProductModelSerializer(many=True, read_only=True)

    def get_image(self, instance):
        image = Image.objects.filter(group=instance, is_primary=True).first()
        if image:
            serializer = ImageSerializer(image)
            return serializer.data['image']

        return None

    class Meta:
        model = Groups
        fields = ['id', 'group_name', 'image', 'products']


class CategoryModelSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True,source='category_images')
    category_image = serializers.SerializerMethodField(method_name='get_image')
    groups = GroupModelSerializer(many=True, read_only=True)

    def get_image(self, instance):
        image = Image.objects.filter(category=instance, is_primary=True).first()
        if image:
            serializer = ImageSerializer(image)
            return serializer.data['image']

        return None

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'category_image', 'groups']

# class GroupModelSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category.category_name')
#     category_id = serializers.IntegerField(source='category.id')
#     # group_images = ImageSerializer(many=True, read_only=True)
#
#     image = serializers.SerializerMethodField()
#
#     def get_image(self, instance):
#         image = Image.objects.filter(group=instance, is_primary=True).first()
#         if image:
#             serializer = ImageSerializer(image)
#             return serializer.data['image']
#
#         return None
#
#
#
#     class Meta:
#         model = Groups
#         fields = ['id', 'group_name', 'slug', 'category_name', 'category_id', 'image']
