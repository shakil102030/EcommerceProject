from django.shortcuts import render, get_object_or_404, redirect 
from django import template
from EcommerceApp.models import Setting
from EcommProduct.models import Product, Category
from EcommOrder.models import ShopCart, OderProduct
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from Blog.models import BlogGrid



register = template.Library()

@register.simple_tag
def ecom_cat():
    return Category.objects.all()
    
@register.simple_tag
def ecom_set():
    return get_object_or_404(Setting, id = 1)

@register.simple_tag
def ecom_shopcart(userid):
    return ShopCart.objects.filter(user_id=userid)
    
@register.simple_tag
def ecom_totalamount(userid):
    productcart = ShopCart.objects.filter(user_id=userid)
    totlamnt = 0
    for p in productcart:
        totlamnt += p.product.new_price * p.quantity     
    return totlamnt
    
@register.simple_tag
def ecom_totalquantity(userid):
    productcart = ShopCart.objects.filter(user_id=userid)
    totlqntity = 0
    for p in productcart:
        totlqntity += p.quantity
    return totlqntity

@register.simple_tag
def ecom_totalorderquantity(userid):
    order_product_cart = OderProduct.objects.filter(user_id=userid)
    totalordrqnty = 0
    for p in order_product_cart:
        totalordrqnty +=  p.quantity
    return totalordrqnty

@register.simple_tag
def ecom_catgoryproducts():
    allProducts=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProducts.append(prod)
    return allProducts

@register.simple_tag
def get_tags():
    tags = set()
    for post in BlogGrid.objects.filter(status="Publish").order_by('-created_at'):
        post_tags = post.tags
        post_tags = [tags.add(tag.lower()) for tag in post_tags.split()]
        print(tags)
    print('\n'*3)
    return tags 







    


            
            
            
                
            
            

              

            
            
           
           