from django.shortcuts import render
from .models import Products
from orders.models import Address, Order, OrderItem
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, OrderSerializer, AddressSerializer, OrderItemSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
logger = logging.getLogger(__name__)
# Create your views here.
#@cache_page(60 * 15)
#@vary_on_headers("User-Agent")
def index(request):
    logger.info("getting products from database")
    products = Products.objects.all()
    logger.debug(f"found {products.count()} found")
    paginator = Paginator(products,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'myapp/index.html',{"page_obj":page_obj})

#@cache_page(60 * 15)
def detail(request, slug):
    logger.info(f"Fetching a product with id")
    try:
        product = get_object_or_404(Products, slug=slug)
        logger.debug(f"founs product{product.name} (${product.price})")
    except Exception as e:
        logger.error(f"Error fetching the product with the id{slug}")
        raise 
    return render(request,'myapp/detail.html',{'product':product})

#API Views
#Product API
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter]
    #filterset_fields = ['name', 'price', 'description', 'seller__username']
    #ordering_fields = ['name', 'price', 'description', 'seller__username']
    search_fields = ['name', 'price', 'description', 'seller__username']
    throttle_classes = [AnonRateThrottle,UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    

#Order API

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return Address.objects.filter(user=user)
        return Address.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return OrderItem.objects.filter(order__user=user)
        return OrderItem.objects.none()

    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        if order.user != self.request.user:
            raise PermissionDenied("You can only add items to your own orders.")
        serializer.save()
