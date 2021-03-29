from django.shortcuts import render, get_object_or_404, redirect 
from .models import Setting, ContactMessage, ContactForm, FAQ
from django.contrib import messages
from EcommProduct.models import Product, Category, Images, Comment, Variants
from EcommOrder.models import ShopCart, OderProduct
from .models import Setting
from .forms import SearchForm
from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def Home(request):
    sliding_images = Product.objects.all().order_by('id')[:2]
    products = Product.objects.all()
    sliderproducts  = Product.objects.all().order_by('id')[:2]
    latestproducts = Product.objects.all().order_by('-id')
    
    context = {
        'sliderproducts': sliderproducts,
        'latestproducts': latestproducts,
        'products': products,
        'sliding_images': sliding_images
    }
    return render(request, 'base.html', context)


def subscribe(request):
    if request.method == 'POST':
        subs_email = request.POST.get('subs_email', None)
        next = request.POST.get('next', '/')
        if subs_email is not None:
            if Subscriber.objects.filter(email=subs_email).exists():
                next += '?email_status=exists#subscribe'
            else:
                subscriber = Subscriber.objects.create(email=subs_email)
                subscriber.save()
                next += '?email_status=added#subscribe'
    return HttpResponseRedirect(next)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'raziaromi50@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})


def Aboutus(request):
    setting = get_object_or_404(Setting, id = 1)
    context = {
        'setting': setting
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
    form = ContactForm

    context = {
        'form': form,
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
            sliding_images = Product.objects.all().order_by('id')[:2]
            prouct_catagory = Product.objects.filter(category_id=cat_id).order_by('id')[:4]
            prodt_count = Product.objects.filter(category_id=cat_id).count()

            context = {
                'prouct_catagory': prouct_catagory,
                'sliding_images': sliding_images,
                'prodt_count': prodt_count,
            }
            return render(request, 'search.html', context)
    return HttpResponseRedirect('/')
    


def product_single(request, id):
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    products = Product.objects.all()
    #products = Product.objects.filter(category_id=catid)
    comment_show = Comment.objects.filter(product_id=id, status='True')
        
    context = {
        'single_product': single_product,
        'images': images,
        'products': products,
        'comment_show': comment_show,
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
    sliding_images = Product.objects.all().order_by('id')[:2]
    prouct_cat = Product.objects.filter(category_id=slug)
    product_count = Product.objects.filter(category_id=slug).count()
    paginator = Paginator(prouct_cat, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products= Product.objects.all()

    context = {
        'product_cat': prouct_cat,
        'sliding_images': sliding_images,
        'page_obj':page_obj,
        'product_count': product_count,
    }
    return render(request, 'category_products.html', context)


def Faq_details(request):
    faq = FAQ.objects.filter(status=True).order_by('created_at')

    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)
