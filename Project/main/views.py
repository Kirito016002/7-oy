from django.shortcuts import render
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