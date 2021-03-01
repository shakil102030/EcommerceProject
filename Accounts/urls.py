from django.urls import path
from .views import (UserLogout, UserLogin,
                           UserSignUp, userProfile, userUpdate,
                           UserPassword, UserComments,
                           CommentDelete)

urlpatterns = [
    path('login/', UserLogin, name='UserLogin'),
    path('signup/', UserSignUp, name='UserSignUp'),
    path('logout/', UserLogout, name='UserLogout'),
    path('profile/', userProfile, name='userprofile'),
    path('user_update/', userUpdate, name="userUpdate"),
    path('password_update/', UserPassword, name="UserPassword"),
    path('usercomments/', UserComments, name="UserComments"),
    path('user_comment_delete/<int:id>/', CommentDelete, name="CommentDelete")

]
