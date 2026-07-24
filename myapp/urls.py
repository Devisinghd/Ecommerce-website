
from django.urls import path,include
from . import views
from django.views import View as auth_view

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:slug>',views.detail,name='detail'),

    #API url patterns
    path('product-api/',views.product_API,name='product-api'),
    path('product/api/<int:pk>',views.product_detail_API,name='product-detail-api'),
]