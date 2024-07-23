from django.contrib import admin
from django.urls import path, include

from app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'products', views.ProductModelViewSet, basename='product')
urlpatterns = [
    # Product
    # path('products/', views.ProductListView.as_view(), name='index'),
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
    path('attribute_values/', views.ProductAttributeValueListView.as_view(), name='attribute_value_list'),

    # Homework urls

    #  for Products
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('product-list/', views.ProductListGeneric.as_view(), name='product_list'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('product-detail-update/<int:pk>', views.ProductDetailUpdate.as_view(), name='product_detail'),
    path('product-detail-delete/<int:pk>', views.ProductDetailDelete.as_view(), name='product_detail'),
    path('product-update/<int:pk>', views.ProductUpdate.as_view(), name='product_update'),
    path('product-delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
    path('modelviewset-products/', include(router.urls)),

    #  for Categories
    path('categories/', views.CategoryList.as_view(), name='categories_list'),
    path('category-list/', views.CategoryListGeneric.as_view(), name='categories_list'),
    path('category-detail/<int:pk>', views.CategoryDetail.as_view(), name='category_detail'),
    path('category-detail-update/<int:pk>', views.CategoryDetailUpdate.as_view(), name='category_detail'),
    path('category-detail-delete/<int:pk>', views.CategoryDetailDelete.as_view(), name='category_detail'),
    path('category-update/<int:pk>', views.CategoryUpdate.as_view(), name='category_update'),
    path('category-delete/<int:pk>', views.CategoryDelete.as_view(), name='category_delete'),
    path('modelviewset-products/', include(router.urls)),

    #  for Groups
    path('categories/', views.GroupsList.as_view(), name='groups_list'),
    path('group-list/', views.GroupsListGeneric.as_view(), name='groups_list'),
    path('group-detail/<int:pk>', views.GroupsDetail.as_view(), name='group_detail'),
    path('group-detail-update/<int:pk>', views.GroupsDetailUpdate.as_view(), name='group_detail'),
    path('group-detail-delete/<int:pk>', views.GroupsDetailDelete.as_view(), name='group_detail'),
    path('group-update/<int:pk>', views.GroupsUpdate.as_view(), name='group_update'),
    path('group-delete/<int:pk>', views.GroupsDelete.as_view(), name='group_delete'),
    path('modelviewset-products/', include(router.urls)),


]
