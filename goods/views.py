# from django.core.paginator import Paginator
# from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
#
# from goods.models import Products, Comment
# from goods.utils import q_search
# from .forms import CommentForm
#
#
# def catalog(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
#
#     if category_slug == 'all':
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#     if order_by and order_by != 'default':
#         goods = goods.order_by(order_by)
#
#     paginator = Paginator(goods, 6)
#     current_page = paginator.page(int(page))
#
#     context = {
#         'title': 'Home -Каталог',
#         'goods': current_page,
#         'slug_url': category_slug,
#     }
#     return render(request, 'goods/catalog.html', context)
#
#
# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)
#     comments = product.comments.all()  # Получаем все комментарии к продукту
#     context = {
#         'product': product,
#         'comments': comments,
#     }
#     return render(request, 'goods/product.html', context=context)
#
#
# def product_comments(request, product_slug):
#     comments = Comment.objects.filter(product__slug=product_slug)
#     return render(request, 'goods/product_comments.html', {'comments': comments})
#
#
# def add_comment(request, product_slug):
#     product = Products.objects.get(slug=product_slug)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             author = request.user
#             text = form.cleaned_data['text']
#             Comment.objects.create(product=product, author=author, text=text)
#             return redirect('product_comments', product_slug=product_slug)
#     else:
#         form = CommentForm()
#
#     comments = product.comments.all()
#     context = {
#         'product': product,
#         'comments': comments,
#         'form': form,
#     }
#     return render(request, 'goods/product.html', context=context)


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from goods.models import Products, Comment
from goods.utils import q_search
from .forms import CommentForm


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    goods_list = list(goods)  # Преобразуем QuerySet в список

    paginator = Paginator(goods_list, 6)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    comments = product.comments.all()
    context = {
        'product': product,
        'comments': comments,
    }
    return render(request, 'goods/product.html', context=context)


def product_comments(request, product_slug):
    comments = Comment.objects.filter(product__slug=product_slug)
    return render(request, 'goods/product_comments.html', {'comments': comments})


def add_comment(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            text = form.cleaned_data['text']
            Comment.objects.create(product=product, author=author, text=text)
            return redirect('product_comments', product_slug=product_slug)
    else:
        form = CommentForm()

    comments = product.comments.all()
    context = {
        'product': product,
        'comments': comments,
        'form': form,
    }
    return render(request, 'goods/product.html', context=context)