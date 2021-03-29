from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import BlogGrid
from EcommerceApp.models import Setting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from EcommProduct.models import Category
from .models import CommentForm, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from EcommProduct.models import Product, Category
from EcommOrder.models import ShopCart, OderProduct
from django.db.models import Q
from .forms import BlogSearchForm
from django.http import HttpResponseRedirect

@login_required(login_url='/account/login')
def BlogView(request):
    bloggrid = BlogGrid.objects.all()
    recentpost = BlogGrid.objects.all().order_by('-id')[:3]
    queryset = BlogGrid.objects.filter(status="Publish").order_by('-created_at')
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    comments = Comment.objects.count()

    

    context = {
        'recentpost':recentpost,
        'page_obj':page_obj,
        'comments': comments,
        }
    return render(request, 'blog-view.html', context)

@login_required(login_url='/account/login')
def BlogGridDetails(request, id):
    bloggrid = BlogGrid.objects.get(id=id)
    bloggrids = BlogGrid.objects.all().order_by('-id')[:3]
    form = CommentForm(request.POST or None)
    recentpost = BlogGrid.objects.all().order_by('-id')[:3]
    comments = Comment.objects.count()
    
    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            parent = form['parent'].value()
            
            if parent == '':
                temp.path = 0
                temp.save()
                temp.path = temp.id 
                
            else:
                node = Comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path
                temp.save()
                temp.path = temp.id
                
            temp.save()
    
    comment_tree = Comment.objects.all().order_by('path')
    
    context = {
        'bloggrid': bloggrid,
        'bloggrids': bloggrids,
        'comment_tree': comment_tree,
        'recentpost': recentpost,
        'comments': comments,
    }
    return render(request, 'blog-details.html', locals())


def Search(request): 
    if request.method == 'POST':
        form = BlogSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            if query == None or query == '':
                object_list = BlogGrid.objects.filter(status="Publish").order_by('-created_at')
                
            else:
                print('query = ', query)  
                object_list = []
                for que in query.split():

                    pos_list = BlogGrid.objects.filter(
                        Q(title__icontains=que) | Q(details__icontains=que) | Q(tags__icontains=que),
                        status="Publish"
                    ).order_by('-created_at')
                    object_list.extend(pos_list)
                    print(object_list)
            object_list = list(set(object_list))
            comments = Comment.objects.count()

            context = {
                'object_list': object_list,
                'comments': comments,  
            }
            return render(request, 'blog_search.html', context)   
    return HttpResponseRedirect('/') 



