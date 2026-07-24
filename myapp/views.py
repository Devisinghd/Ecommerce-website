from django.shortcuts import render
from .models import Products
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging
from django.shortcuts import get_object_or_404
from .managers import ProductsManager
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets


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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer 
    






"""class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

"""