from django.urls import path
from .views import Home, product_single, category_product, Aboutus, contact, searchView, Faq_details, password_reset_request
from django.contrib.auth import views as auth_views 
from . import views
urlpatterns = [
    path('', Home, name='home'),
    path('about/', Aboutus, name='about'),
    path('contact/', contact, name='contact_dat'),
    path('product/<int:id>/', product_single, name='product_single'),
    path('product/<int:id>/<slug:slug>/', category_product, name='category_product'),
    path('search/', searchView, name='searchView'),
    path('faq/', Faq_details, name='Faq_details'),
    path('subscribe', views.subscribe, name='subscribe'),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),     

   
   
]