from django.shortcuts import render, redirect
from . import models
from django.db.models import Q


def index(request):
    q = request.GET.get('q')
    if q:
        products = models.Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else: 
        products = models.Product.objects.filter(quantity__gt=0)
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products.filter(category_id=category_id)
    context = {
        'products':products,
        'categorys':categorys
    }
    return render(request, 'index.html', context)




def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)


    context = {
        'product':product,
        'categorys':categorys,
        'recomendation':recomendation,
        'images':images,
        'range':range(product.review)
    }
    return render(request, 'product/detail.html', context)


def cart_create(request, id):
    is_active_cart = models.Cart.objects.filter(is_active=True, user=request.user)
    
    if not is_active_cart:
        models.Cart.objects.create(
            user = request.user
        )
        try:
            product1 = models.Product.objects.get(id=id)
            cart1 = models.Cart.objects.get(is_active=True)
            models.CartProduct.objects.create(
                card = cart1,
                product = product1
            )
        except:
            pass
    else:
        cart = models.Cart.objects.get(is_active=True)
        try:
            product = models.CartProduct.objects.get(card=cart)
            product.quantity += 1
            product.save()
        except:
            product = models.CartProduct.objects.get(id = id)
            models.CartProduct.objects.create(
                cart = cart,
                product = product
            ) 
    return redirect('main:index')


def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user)
    context = {
        'active':active,
        'in_active':in_active
    }
    return render(request, 'cart/carts.html', context)


def cart_detail(request, id):
    cart = models.Cart.objects.get(id=id)
    items = models.CartProduct.objects.filter(card=cart)
    context = {
        'cart':cart,
        'items':items
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_detail_delete(request):
    item_id = request.GET['items_id']
    item = models.CartProduct.objects.get(id=item_id)
    cart_id = item.card.id
    item.delete()
    return redirect('main:cart_detail', cart_id)

