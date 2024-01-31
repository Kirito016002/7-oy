from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.product_detail, name='product_detail')
]