
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import   TokenObtainPairView,TokenRefreshView

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')
router.register(r'addresses', views.AddressViewSet, basename='address')

urlpatterns = [
    path('',views.index,name='index'),
    path('<slug:slug>',views.detail,name='detail'),

    #API url patterns
    path("api/",include(router.urls)),
    path("api/token",TokenObtainPairView.as_view()),
    path("api/token/refresh",TokenRefreshView.as_view()),
]