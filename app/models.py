from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, User

from app.managers import CustomUserManager


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'Categories'


class Groups(BaseModel):
    group_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group_name)

        super(Groups, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'Group'


class Product(BaseModel):
    product_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='products')
    user_likes = models.ManyToManyField(User, related_name='likes', blank=True, null=True, db_table='user_likes')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)

        return self.price

    @property
    def pay_monthly(self):
        return self.price / 12

    def get_attributes(self) -> list:
        product_attributes = ProductAttribute.objects.filter(product=self)
        attributes = []
        for pa in product_attributes:
            attributes.append({
                'attribute_name': pa.attribute.attribute_name,
                'attribute_value': pa.attribute_value.attribute_value
            })
        return attributes

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group_images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_images', null=True,
                                 blank=True)

    is_primary = models.BooleanField(default=False)

    @property
    def get_absolute_url(self):
        return self.image.url

    class Meta:
        db_table = 'images'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments', null=True,
                                blank=True)
    message = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value, null=True, blank=True)
    file = models.FileField(upload_to='comments/', null=True, blank=True)


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute_name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute_value


class ProductAttribute(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='attributes', null=True,
                                blank=True)
    key = models.ForeignKey('app.Attribute', on_delete=models.CASCADE, related_name='product_attributes',
                            null=True, blank=True)
    value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE,
                              related_name='product_attribute_value', null=True, blank=True)


