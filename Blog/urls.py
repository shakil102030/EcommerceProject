from django.urls import path
from Blog.views import BlogView, BlogGridDetails, CommentDel
urlpatterns = [
  path('', BlogView, name = 'BlogView'),
  path('details/<int:id>/', BlogGridDetails, name = 'BlogGridDetails'),
  path('commentdel/<int:id>/', CommentDel, name = 'CommentDel'),
]