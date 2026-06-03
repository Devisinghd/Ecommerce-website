from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('add/', views.cart_add, name='cart_add'),
    path('delete/',views.cart_delete,name='cart_delete'),
    path('update/',views.cart_update,name='cart_update'),
    path('cart-overview/',views.cart_overview,name='cart-overview'),
]