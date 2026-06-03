from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from myapp.models import Products

# Create your views here.
def cart_add(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product_quantity = request.POST.get('product_quantity', 1)
    
    if not product_id:
        return JsonResponse({'error': 'Missing product_id'}, status=400)
    
    try:
        product_quantity = int(product_quantity)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid quantity'}, status=400)
    
    product = get_object_or_404(Products, id=product_id)
    cart.add(product=product, product_qty=product_quantity)
    cart_quantity = cart.__len__()
    return JsonResponse({'success': True, 'cart': cart.cart, 'cart_quantity': cart_quantity})

def cart_overview(request):
    cart = Cart(request)
    return render(request,'cart/cart-overview.html',{'cart':cart})

def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('product_id'):
        product_id = request.POST.get('product_id')
        cart.delete(product_id=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
        return JsonResponse({'message':'item delete', 'cart_quantity': cart_quantity,'total':cart_total})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        
        cart.update(product=product_id, product_qty=product_quantity)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total_price()
        return JsonResponse({'message':'item updated', 'cart_quantity': cart_quantity,'total':cart_total})