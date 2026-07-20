
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:slug>',views.detail,name='detail'),

    #API url patterns
    path('product-api/',views.product_API,name='product-api'),
    path('api/products/<int:pk>',views.product_detail_API,name='product-detail-api'),
]