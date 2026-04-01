from django.shortcuts import render
from .models import Products
# Create your views here.
def index(request):
    products = Products.objects.all()
    return render(request,'myapp/index.html',{"products":products})

def detail(request, slug):
    product = Products.objects.get(slug=slug)
    return render(request,'myapp/detail.html',{'product':product})

