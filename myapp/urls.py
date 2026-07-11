
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:slug>',views.detail,name='detail'),

    #API urls
    path('product-api/',views.productAPI,name='product-api'),
]