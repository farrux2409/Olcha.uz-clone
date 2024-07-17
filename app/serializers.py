from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField

from app.models import Product, Category, Groups, Image, Comment


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_fields = ('user',)


class ProductModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='group.group_name')
    group_id = serializers.IntegerField(source='group.id')
    group_slug = serializers.CharField(source='group.slug')
    category_name = serializers.CharField(source='group.category.category_name', read_only=True)
    category_slug = serializers.CharField(source='group.category.slug', read_only=True)
    comments = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()

    def get_all_images(self, instance):
        images = Image.objects.filter(product=instance).all()
        images_list = []
        request = self.context.get('request')
        for image in images:
            images_list.append(request.build_absolute_uri(image.get_absolute_url))

        return images_list

    # product_images = serializers.SerializerMethodField()

    def get_comments(self, instance):
        comments = Comment.objects.filter(product=instance)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['group_name', 'group_slug', 'group_id', 'group', 'category_name', 'category_slug',
                        'comments']


class GroupModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    products = ProductModelSerializer(many=True, read_only=True)

    def get_image(self, instance):
        image = Image.objects.filter(group=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

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
        request = self.context.get('request')
        if image:
            image_url = image.get_absolute_url
            return request.build_absolute_uri(image_url)

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
