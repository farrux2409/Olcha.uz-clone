from django.contrib import admin
from django.contrib.auth.models import Group,User

from app.models import Product, Category, Groups, Image,Comment

# Register your models here.

# admin.site.register(Product)
# admin.site.register(User)
admin.site.register(Comment)
admin.site.unregister(Group)
admin.site.register(Image)
@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'category']
    search_fields = ['group_name']
    prepopulated_fields = {'slug': ('group_name',)}
    list_filter = ['category']


@admin.register(Category)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    search_fields = ['category_name']
    prepopulated_fields = {'slug': ('category_name',)}
    list_filter = ['category_name',]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'group', 'quantity']
    search_fields = ['product_name']
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ['group', 'price']
