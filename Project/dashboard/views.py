from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main import models


def dashboard(request):
    categorys = models.Category.objects.all()
    products = models.Product.objects.filter(is_active=True)
    users = User.objects.filter(is_satff=False)
    context = {
        'categorys':categorys,
        'products':products,
        'users':users,
    }
    return render(request, 'index.html', context)


def category_list(request):
    categorys = models.Category.objects.all()
    return render(request, 'category/list.html', {'categorys':categorys})


def category_detail(request, id):
    category = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=category, is_active=True)
    context = {
        'category':category,
        'products':products
    }
    return render(request, 'category/list.html', context)


def category_update(request, id):
    category = models.Category.objects.get(id=id)
    category.name = request.POST['name']
    category.save()
    return redirect('category_detail', category.id)


def category_delete(request, id):
    category = models.Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')