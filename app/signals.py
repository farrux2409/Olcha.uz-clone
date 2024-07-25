import json
import os

from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver

from app.models import Category, Product, Groups
from config.settings import BASE_DIR, DEFAULT_FROM_EMAIL


# For the Category
def post_save_category(sender, instance, created, **kwargs, ):
    if created:
        print(f'Category {instance.category_name} saved')
    else:
        print(f'Category {instance.category_name} updated')


post_save.connect(post_save_category, sender=Category)


@receiver(post_save, sender=Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print(f'Category created')
        subject = 'Category created'
        message = f'Category => {instance.category_name} created by Admin'
        from_email = DEFAULT_FROM_EMAIL
        to = 'farruxyoldoshov2409@gmail.com'
        send_mail(subject, message, from_email, [to, ], fail_silently=False)
    else:
        print(f'Category updated')


def pre_delete_category(sender, instance, **kwargs, ):
    print(kwargs)
    print('Category saved before deleting')


pre_delete.connect(pre_delete_category, sender=Category)


@receiver(post_delete, sender=Category)
def post_delete_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'app/delete_categories', f'category_{instance.id}.json')
    category_data = {
        'id': instance.id,
        'name': instance.category_name,
        'slug': instance.slug,

    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)
    print(f'Category {instance.category_name} saved json  before deleted')


# For Product
def post_save_product(sender, instance, created, **kwargs, ):
    if created:
        print(f'Product {instance.product_name} saved')
    else:
        print(f'Product {instance.product_name} updated')


post_save.connect(post_save_product, sender=Product)


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print(f'Product created')
        subject = 'Product created'
        message = f'Product => {instance.product_name} created by Admin'
        from_email = DEFAULT_FROM_EMAIL
        to = 'farruxyoldoshov2409@gmail.com'
        send_mail(subject, message, from_email, [to, ], fail_silently=False)
    else:
        print(f'Product updated')


@receiver(post_delete, sender=Product)
def post_delete_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'app/delete_products', f'category_{instance.id}.json')
    product_data = {
        'id': instance.id,
        'name': instance.product_name,
        'slug': instance.slug,
        'quantity': instance.quantity,
        'price': instance.price,

        'description': instance.description,
        'discount': instance.discount,


    }
    with open(file_path, 'w') as json_file:
        json.dump(product_data, json_file, indent=4)
    print(f'Product {instance.product_name} saved json  before deleted')


# For Groups
def post_save_group(sender, instance, created, **kwargs, ):
    if created:
        print(f'Groups {instance.group_name} saved')
    else:
        print(f'Groups {instance.group_name} updated')


post_save.connect(post_save_group, sender=Groups)


@receiver(post_save, sender=Groups)
def post_save_group(sender, instance, created, **kwargs):
    if created:
        print(f'Groups created')
        subject = 'Groups created'
        message = f'Groups => {instance.group_name} created by Admin'
        from_email = DEFAULT_FROM_EMAIL
        to = 'farruxyoldoshov2409@gmail.com'
        send_mail(subject, message, from_email, [to, ], fail_silently=False)
    else:
        print(f'Groups updated')


@receiver(post_delete, sender=Groups)
def post_delete_group(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'app/delete_groups', f'category_{instance.id}.json')
    group_data = {
        'id': instance.id,
        'name': instance.group_name,
        'slug': instance.slug,

    }
    with open(file_path, 'w') as json_file:
        json.dump(group_data, json_file, indent=4)
    print(f'Groups {instance.group_name} saved json  before deleted')
