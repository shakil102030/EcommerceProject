from django.shortcuts import render, HttpResponse, reverse, get_object_or_404, redirect #, HttpResponseRedirect,
from EcommProduct.models import Category, Product, Images, Variants
from django.contrib import messages, auth
from EcommOrder.models import ShopCart, ShopingCartForm, OderForm, Order, OderProduct
from EcommerceApp.models import Setting, ContactMessage, ContactForm
from Accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import MakePaymentForm
from django.conf import settings
from django.utils import timezone
import stripe
from django.template.context_processors import csrf




stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='/account/login')
def AddtoShopingcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopingCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shop_cart(request):
    current_user = request.user
    category = Category.objects.all()
    setting = get_object_or_404(Setting, id = 1)
    shop_cart_product  = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for p in shop_cart_product:
        totalamount += p.product.new_price*p.quantity
    
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
        'shop_cart_product': shop_cart_product,
        'totalamount': totalamount,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------

    }
    return render(request, 'shop_cart.html', context)



@login_required(login_url='/account/login')
def delete_from_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    shop_cart_product = ShopCart.objects.filter(id=id, user_id=current_user.id)
    shop_cart_product.delete()
    messages.warning(request, 'Your product has been deleted.')
    return HttpResponseRedirect(url)

@login_required(login_url='/account/login')
def update_cart(request, cartID):
    food = Food.objects.filter(id=cartID)[0]
    if request.method == "POST":
        if request.POST['base_price'] != "":
            food.base_price = request.POST['base_price']
        
        if request.POST['discount'] != "":
            food.discount = request.POST['discount'] 
        if request.POST['base_price'] != "":
            food.base_price = request.POST['base_price']

        status = request.POST.get('Out Stock')
        print(status)
        if status == 'on':
            food.status = "Out Stock"
        else:
            food.status = "In Stock"
        
        food.save()
    return redirect('foods_admin')


@login_required(login_url='/account/login')
def OrderCart(request):
    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    total_amount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity*rs.product.new_price  
    if request.method == "POST":
        form = OderForm(request.POST, request.FILES)
        payment_form = MakePaymentForm(request.POST)
        print("checkout...")
        if form.is_valid() and payment_form.is_valid():
            dat = Order()
            # get product quantity from form
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.email = form.cleaned_data['email']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.description = form.cleaned_data['description']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  
            dat.code = ordercode
            dat.save()
            form = OderForm()
            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = OderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            

            ShopCart.objects.filter(user_id=current_user.id).delete()
            messages.success(request, 'Your oder has been completed')
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            context = {
                 'category':category,
                'ordercode': ordercode,
                'category': category,
                'setting': setting,
            }
            for p in shoping_cart:
                total_amount += p.product.new_price*p.quantity
                total_amount = int(total_amount)

            try:
                print("Just about to charge the customer...")
                customer = stripe.Charge.create(
                    description=dat.description,
                    shipping={
                        'name': dat.first_name,
                        'address': {
                        'line1': dat.address,
                        'postal_code': '98140',
                        'city': dat.city,
                        'state': 'CA',
                        'country': dat.country,
                        },
                    },
                    amount=total_amount*100,
                    currency='usd',
                    #payment_method_types=['card'],
                    card=payment_form.cleaned_data['stripe_id'],
                    
                    #mode='payment',
                    
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            
            if customer.paid:
                print("Customer has paid...")
                messages.error(request, "You have successfully paid")
                #return redirect(reverse('home'))
                return render(request, 'oder_completed.html', context)
            else:
                messages.error(request, "Unable to take payment")
                #return redirect(reverse('home'))
        else:
            print("There are errors...")
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        print("Method isn't post...")
        payment_form = MakePaymentForm()

    profile = UserProfile.objects.get(user_id=current_user.id)
    for p in shoping_cart:
                total_amount += p.product.new_price*p.quantity
    category = Category.objects.all()
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
    
    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        allProds.append(prod)

    #-------------------------

    
    context = {
        # 'category':category,
        'shoping_cart': shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'category': category,
        'setting': setting,
        'total_amount': total_amount,
        "payment_form": payment_form,
        "publishable": settings.STRIPE_PUBLISHABLE_KEY,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------

        
    }
    return render(request, "order_form.html", context)
    

    

def Order_showing(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)

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
        'orders': orders,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------

    }

    return render(request, 'user_order_showing.html', context)


@login_required(login_url='/account/login')
def user_oder_details(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_products = OderProduct.objects.filter(order_id=id)

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

        'order': order,
        'order_products': order_products,
        'category': category,
        'setting': setting,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
    }
    return render(request, 'user_order_details.html', context)


def Order_Product_showing(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order_product = OderProduct.objects.filter(user_id=current_user.id)

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
        'order_product': order_product,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------

    }

    return render(request, 'OrderProducList.html', context)


@login_required(login_url='/account/login')
def useroderproduct_details(request, id, oid):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    order_products = OderProduct.objects.get(user_id=current_user.id, id=id)

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

        'order': order,
        'order_products': order_products,
        'category': category,
        'setting': setting,

        # TotalOrderQuentity TotalAmount Total Quentity
        'totalorderquantity':totalorderquantity,
        'totalamount': totalamount,
        'totalquantity': totalquantity,
        'productcart': productcart,
        'allProds':allProds,
        #-------------------------
    }
    return render(request, 'user_order_pro_details.html', context)







