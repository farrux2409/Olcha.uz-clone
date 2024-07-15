from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='index'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListApiView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('group/<slug:slug>/',views.GroupsDetailView.as_view(),name='group_detail'),
]
