from django.urls import path
from .views import AddComment

urlpatterns = [
    path('addComment/<int:id>/', AddComment, name='AddComment'),
]
