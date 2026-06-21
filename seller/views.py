from django.shortcuts import render,redirect
from myapp.models import Products
from .forms import ProductCreateForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

def seller_dashboard(request):
    product = Products.objects.filter(seller=request.user)
    paginator = Paginator(product,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'seller/seller-dashboard.html',{'page_obj':page_obj})

def product_detail(request, slug):
    product = Products.objects.get(slug=slug)
    return render(request,'seller/seller-product-detail.html',{'product':product})

@login_required  
def product_create(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller-dashboard')
    else:
        form = ProductCreateForm()
        
    return render(request, 'seller/product-create.html', {'form': form})