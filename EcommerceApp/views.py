from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
from .models import Setting, ContactMessage, ContactForm, FAQ
from django.contrib import messages
from EcommProduct.models import Product, Category, Images, Comment, Variants
from EcommOrder.models import ShopCart, OderProduct
from .models import Setting
from .forms import SearchForm
from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def Home(request):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    sliding_images = Product.objects.all().order_by('id')[:2]
    current_user  = request.user
    productcart = ShopCart.objects.filter(user_id=current_user.id)

    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProds.append(prod)

    totalamount = 0
    for p in productcart:
        totalamount += p.product.new_price * p.quantity

    order_product_cart = OderProduct.objects.filter(user_id=current_user.id)
    
    totalorderquantity = 0
    for p in order_product_cart:
        totalorderquantity +=  p.quantity

    products = Product.objects.all()
    sliderproducts  = Product.objects.all().order_by('id')[:2]
    latestproducts = Product.objects.all().order_by('-id')

    totalquantity = 0
    for p in productcart:
        totalquantity += p.quantity

    context = {
        'setting': setting,
        'category': category,
        'sliderproducts': sliderproducts,
        'latestproducts': latestproducts,
        'products': products,
        'productcart': productcart,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'totalorderquantity':totalorderquantity,
        'allProds':allProds,
        'sliding_images': sliding_images
    }
    return render(request, 'base.html', context)

def Aboutus(request):
    setting = Setting.objects.get(id=1)

    
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
    
    products = Product.objects.all()
    sliderproducts  = Product.objects.all().order_by('id')[:2]
    latestproducts = Product.objects.all().order_by('-id')

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
        
        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------



    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Profile details updated.')

            return redirect('contact_dat')

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

    form = ContactForm
    setting = Setting.objects.get(id=1)
    context = {
        'form': form,
        'setting': setting,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
    }
    return render(request, 'contact_form.html', context)


def searchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cat_id = form.cleaned_data['cat_id']
            if cat_id == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=cat_id)
        
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            sliding_images = Product.objects.all().order_by('id')[:2]
            prouct_catagory = Product.objects.filter(category_id=cat_id).order_by('id')[:4]
            
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
                'prouct_catagory': prouct_catagory,
                'sliding_images': sliding_images,

                 
                # TotalOrderQuentity TotalAmount Total Quentity
                'totalorderquantity':totalorderquantity,
                'totalamount': totalamount,
                'totalquantity': totalquantity,
                'productcart': productcart,
                'allProds':allProds,
                #-------------------------
                
            }
            return render(request, 'search.html', context)
    return HttpResponseRedirect('/')
    


def product_single(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    products = Product.objects.all()
    #products = Product.objects.filter(category_id=catid)
    comment_show = Comment.objects.filter(product_id=id, status='True')
    

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
        'single_product': single_product,
        'images': images,
        'products': products,
        'comment_show': comment_show,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
        
    }
    if single_product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query,
                        })

    return render(request, 'product-single.html', context)




def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def category_product(request, id, slug):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    sliding_images = Product.objects.all().order_by('id')[:2]
    prouct_cat = Product.objects.filter(category_id=slug)
    paginator = Paginator(prouct_cat, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products= Product.objects.all()

    

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
        'product_cat': prouct_cat,
        'sliding_images': sliding_images,
        'page_obj':page_obj,
        

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
    }
    return render(request, 'category_products.html', context)


    

def Faq_details(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    faq = FAQ.objects.filter(status=True).order_by('created_at')

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
        'faq': faq,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------

    }
    return render(request, 'faq.html', context)
