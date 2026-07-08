from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller-dashboard'),
    path('product/add/', views.product_create, name='seller-product-create'),
    path('product/<slug:slug>/', views.product_detail, name='seller-product-detail'),
    path('product/<slug:slug>/edit/', views.product_update, name='seller-product-update'),
    path('product/<slug:slug>/delete/', views.product_delete, name='seller-product-delete'),
]
