from django.db import models
from django.utils.safestring import mark_safe
from EcommProduct.models import Category
from django.contrib.auth.models import User
from django import forms
#from dbarray import IntegerArrayField

class BlogGrid(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length = 200)
    blogcategory = models.ForeignKey(Category, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'blog/')
    details = models.TextField()
    status = models.CharField(max_length = 40, choices = STATUS)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def authorname(self):
        return self.author.username

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""
    
    def image_tag(self):
        return mark_safe('<img src="{}" heigths="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'image'



 
class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    path = models.IntegerField(null=True, blank=True)
    depth = models.PositiveSmallIntegerField(default=0)
    
    def __unicode__(self):
        return self.content


    
    def __unicode__(self):
        return self.content
    
class CommentForm(forms.ModelForm):
    #Hidden value to get a child's parent
    parent = forms.CharField(widget=forms.HiddenInput(
                            attrs={'class': 'parent'}), required=False)
    
    class Meta:
        model = Comment
        fields = ('content',)

