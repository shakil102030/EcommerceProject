from django.urls import path
from Blog.views import BlogView, BlogGridDetails, Search
urlpatterns = [
  path('', BlogView, name = 'BlogView'),
  path('details/<int:id>/', BlogGridDetails, name = 'BlogGridDetails'),
  path('search/', Search, name = 'Search'),
]