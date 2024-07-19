from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from app.models import Product, Category, Groups, Image, Comment, ProductAttribute, Attribute, AttributeValue


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('id', 'attribute_value')


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('id', 'attribute')


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()
    attribute_value = AttributeValueSerializer()

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ProductModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    group_name = serializers.CharField(source='group.group_name')
    group_id = serializers.IntegerField(source='group.id')
    group_slug = serializers.CharField(source='group.slug')
    category_name = serializers.CharField(source='group.category.category_name', read_only=True)
    category_slug = serializers.CharField(source='group.category.slug', read_only=True)
    # product_comments = CommentSerializer(many=True, read_only=True)
    all_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    # def get_attributes(self, obj):
    #     attributes = ProductAttribute.objects.filter(product=obj)
    #     # if attributes:
    #     serializer = ProductAttributeSerializer(attributes, many=True)
    #     #     return serializer.data
    #     return serializer.data

    # 1-version
    # def get_avg_rating(self, obj):
    #     comments = Comment.objects.filter(product=obj)
    #     try:
    #         avg_rating = round(sum([comment.rating for comment in comments]) / comments.count())
    #     except ZeroDivisionError:
    #         avg_rating = 0
    #     return avg_rating
    # 2-version
    def get_avg_rating(self, obj):
        avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating=Round(Avg('rating')))
        if avg_rating['avg_rating']:
            return avg_rating.get('avg_rating')
        return 0

    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.user_likes.all()
        if user in all_likes:
            return True
        return False

    def get_all_images(self, instance):
        images = Image.objects.filter(product=instance).all()
        images_list = []
        request = self.context.get('request')
        for image in images:
            images_list.append(request.build_absolute_uri(image.get_absolute_url))

        return images_list

    # product_images = serializers.SerializerMethodField()

    def get_comments_count(self, instance):
        count = Comment.objects.filter(product=instance).count()
        return count
        # comments_list = []
        # if comments_count > 0:
        #     for comment in instance.product_comments.all():
        #         serializer= CommentSerializer(comment)
        #         comments_list.append(serializer.data)
        #
        #     return comments_list
        # return False

    def get_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None

    class Meta:
        model = Product
        exclude = ('user_likes',)

        # extra_fields = ['group_name', 'group_slug', 'group_id', 'group', 'category_name', 'category_slug',
        #                 'all_comments', 'is_liked']
        # #


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


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
