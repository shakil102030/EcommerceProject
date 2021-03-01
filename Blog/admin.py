from django.contrib import admin
from Blog.models import BlogGrid, Comment

class BlogGridAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']

admin.site.register(BlogGrid, BlogGridAdmin)
admin.site.register(Comment)
