from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')
    else:
        form = AddressForm()
    return render(request, 'orders/add_address.html', {'form': form})

@login_required
def checkout(request):
    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user).order_by('-id')
        selected_address = addresses.first() if addresses else None
        return render(request, 'orders/checkout.html', {'addresses': addresses, 'address': selected_address})
    return render(request, 'orders/checkout.html', {'addresses': []})

@login_required
def place_order(request):
    order_success = False
    if request.method == 'POST':
        cart = Cart(request)
        total_amount = cart.get_total_price()

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user,total_amount=total_amount)
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],quantity=item['qty'])
            order_success = True
        else:
            order = Order.objects.create(total_amount=total_amount)
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],quantity=item['qty'])
            order_success = True
    return JsonResponse({'message':"order placed successfully"})


def order_success(request):
    return render(request,'orders/order-success.html')


def order_failed(request):
    return render(request,'orders/order-failed.html')

