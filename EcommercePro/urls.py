from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EcommerceApp.urls')),
    path('account/', include('Accounts.urls')),
    path('product/', include('EcommProduct.urls')),
    path('order/', include('EcommOrder.urls')),
    path('blog/', include('Blog.urls')),
    path('strip/', include('StripeApp.urls')),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
