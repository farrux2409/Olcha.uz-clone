# Create your views here.
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Product, Category, Groups, Image, Comment
from .serializers import ProductModelSerializer, CategoryModelSerializer, GroupModelSerializer, ImageSerializer, \
    CommentSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# from rest_framework import generics
variable = generics.ListCreateAPIView


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()

        # first version
        serializers = ProductModelSerializer(products, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = ProductModelSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        # second version
        # product_list = [
        #     {
        #         'id': product.id,
        #         'title': product.title,
        #         'price': product.price,
        #         'image': product.image,
        #         'rating': product.rating,
        #         'is_liked': product.is_liked
        #     }
        #     for product in products
        # ]
        #
        # return Response(product_list, status=status.HTTP_200_OK)


class ProductDetailView(APIView):

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductModelSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        snippet = self.get_object(slug=slug)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListApiView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializers = CategoryModelSerializer(categories, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = CategoryModelSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategoryModelSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        snippet = self.get_object(slug=slug)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupListView(APIView):
    def get(self, request):
        groups = Groups.objects.all()
        serializers = GroupModelSerializer(groups, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = GroupModelSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class GroupsDetailView(APIView):

    def get_object(self, slug):
        try:
            return Groups.objects.get(slug=slug)
        except Groups.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        group = get_object_or_404(Groups, slug=slug)
        serializer = GroupModelSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        group = self.get_object(slug)
        serializer = GroupModelSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        snippet = self.get_object(slug=slug)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
