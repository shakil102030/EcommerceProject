from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from django.forms import ModelForm
from django.db.models import Avg, Count, Sum
from django.utils.safestring import mark_safe

class Category(MPTTModel):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )

    parent = TreeForeignKey('self',  null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=190)
    keywords = models.CharField(blank = True, max_length=100)
    description = models.TextField(blank = True)
    image = models.ImageField(blank = True, upload_to='category_img/cat_image')
    status = models.CharField(max_length=30, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
        






class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ProductStatus = (
        ('In Stock', 'In Stock'),
        ('Out Stock', 'Out Stock'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=190)
    keywords = models.CharField(blank = True, max_length=100)
    description = models.TextField(blank = True)
    manufacture = models.CharField(blank = True, max_length=100)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    old_price = models.DecimalField(decimal_places=2, max_digits=15)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    image = models.ImageField(upload_to='product_image/pro_img')
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    product_status = models.CharField(max_length=30, choices=ProductStatus)
    status = models.CharField(max_length=30, choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    

    def image_tag(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def average_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(average=Avg('rate'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
        else:
            return avg

    def count_review(self):
        reviews = Comment.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = (reviews['count'])
            return cnt


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='product_img/images')

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),

    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    comment = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=40, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
