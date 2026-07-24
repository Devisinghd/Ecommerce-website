
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products',views.ProductViewSet,basename='product')

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:slug>',views.detail,name='detail'),

    #API url patterns
    path("api/",include(router.urls)),
    #path('product-api/',views.ProductListCreateAPI.as_view(),name='product-api'),
    #path('product/api/<int:pk>',views.ProductRetrieveUpdateDelete.as_view(),name='product-detail-api'),
]