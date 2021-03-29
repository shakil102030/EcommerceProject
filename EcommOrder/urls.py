from django.urls import path
from .views import(
    AddtoShopingcart, shop_cart, delete_from_cart,
    OrderCart, Order_showing, Order_Product_showing,
    user_oder_details, useroderproduct_details, 
)




urlpatterns = [
    path('addingcart/<int:id>/', AddtoShopingcart, name='AddtoShopingcart'),
    path('shop_cart/', shop_cart, name='shop_cart'),
    path('deletecart/<int:id>/', delete_from_cart, name='delete_from_cart'),
    path('oder_cart/', OrderCart, name="OrderCart"),
    path('orderlist/', Order_showing, name="orderlist"),
    path('OrderProduct/', Order_Product_showing, name="orderproduct"),
    path('OrderDetails/<int:id>/', user_oder_details, name="user_oder_details"),
    path('OrderProductDetails/<int:id>/<int:oid>/', useroderproduct_details, name="useroderproduct_details"),


    
]
