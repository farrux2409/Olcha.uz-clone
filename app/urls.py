from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    # Product
    path('products/', views.ProductListView.as_view(), name='index'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    # Categories
    path('categories/', views.CategoryListApiView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    # Groups
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('group/<slug:slug>/', views.GroupsDetailView.as_view(), name='group_detail'),
    #  Images
    path('images/', views.ImageListView.as_view(), name='image_list'),
    # path('image/<pk:pk>/', views.ImageDetailView.as_view(), name='image_detail'),
    # Users
    path('users/', views.UserListView.as_view(), name='user_list'),
    # path('user/<pk:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    # Comments
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    # path('comment/<pk:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    # attributes
    path('attributes/', views.AttributeListView.as_view(), name='attribute_list'),
    path('product_attributes/', views.ProductAttributeListView.as_view(), name='product_attribute_list'),
    path('attribute_values/',views.ProductAttributeValueListView.as_view(), name='attribute_value_list'),
]
