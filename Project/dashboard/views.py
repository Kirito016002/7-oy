from django.shortcuts import render, redirect
from main import models


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


# Category
def list_category(request):
    categorys = models.Category.objects.all()
    return render(request, 'category/list.html', {'categorys':categorys})


def create_category(request):
    if request.method == "POST":
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:list_category')
    return render(request, 'category/create.html')


def detail_category(request, id):
    category = models.Category.objects.get(id=id)
    if request.method == "POST":
        category.name = request.POST['name']
        category.save()
        return redirect('dashboard:list_category')
    return render(request, 'category/detail.html', {'category':category})


def delete_category(request, id):
    models.Category.objects.get(id=id).delete()
    return redirect('dashboard:list_category')