from django.shortcuts import render
from .models import Products
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
# Create your views here.
@cache_page(60 * 15)
@vary_on_headers("User-Agent")
def index(request):
    products = Products.objects.all()
    paginator = Paginator(products,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'myapp/index.html',{"page_obj":page_obj})

@cache_page(60 * 15)
def detail(request, slug):
    product = Products.objects.get(slug=slug)
    return render(request,'myapp/detail.html',{'product':product})

