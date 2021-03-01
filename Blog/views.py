from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import BlogGrid
from EcommerceApp.models import Setting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from EcommProduct.models import Category
from .models import CommentForm, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#from itertools import ifilter
from EcommProduct.models import Product, Category
from EcommOrder.models import ShopCart, OderProduct


def BlogView(request):
    bloggrid = BlogGrid.objects.all()
    recentpost = BlogGrid.objects.all().order_by('-id')[:3]
    setting = get_object_or_404(Setting, id=1)
    paginator = Paginator(bloggrid, 6) # Show 3 images per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # TotalOrderQuentity TotalAmount Total Quentity
    current_user  = request.user
    order_product_cart = OderProduct.objects.filter(user_id=current_user.id)
    totalorderquantity = 0
    for p in order_product_cart:
        totalorderquantity +=  p.quantity


    productcart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for p in productcart:
        totalamount += p.product.new_price * p.quantity

    totalquantity = 0
    for p in productcart:
        totalquantity += p.quantity
    
    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProds.append(prod)

    #-------------------------


    context = {
        'setting': setting,
        'recentpost':recentpost,
        'page_obj':page_obj,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
        }
    return render(request, 'blog-view.html', context)

@login_required(login_url='/account/login')
def BlogGridDetails(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    bloggrid = BlogGrid.objects.get(id=id)
    bloggrids = BlogGrid.objects.all().order_by('id')[:7]
    form = CommentForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            parent = form['parent'].value()
            
            if parent == '':
                #temp.path = []
                #temp.save()
                #temp.path = [temp.id]
                temp.path = 0
                temp.save()
                temp.path = temp.id
                
                
            else:
                node = Comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path
                
                temp.save()
                temp.path.append(temp.id)
                
            temp.save()
    
    comment_tree = Comment.objects.all().order_by('path')

     # TotalOrderQuentity TotalAmount Total Quentity
    current_user  = request.user
    order_product_cart = OderProduct.objects.filter(user_id=current_user.id)
    totalorderquantity = 0
    for p in order_product_cart:
        totalorderquantity +=  p.quantity


    productcart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for p in productcart:
        totalamount += p.product.new_price * p.quantity

    totalquantity = 0
    for p in productcart:
        totalquantity += p.quantity
    
    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProds.append(prod)

    #-------------------------

    

    context = {
        'category': category,
        'setting': setting,
        'bloggrid': bloggrid,
        'bloggrids': bloggrids,
        'comment_tree': comment_tree,

         # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
        
    }
    return render(request, 'blog-details.html', locals())


def CommentDel(request, id):
    commentuser = Comment.objects.filter(id=id)
    commentuser.delete()
    messages.success(request, 'Your comment is successfully deleted')
    return redirect('BlogView')




