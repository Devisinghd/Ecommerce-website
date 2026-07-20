from decimal import Decimal

from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from myapp.models import Products


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
    addresses = []
    selected_address = None
    checkout_items = []
    total_amount = Decimal('0.00')

    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user).order_by('-id')
        selected_address = addresses.first() if addresses else None

    product_id = request.GET.get('product_id')
    quantity = request.GET.get('quantity', 1)

    if product_id:
        try:
            product = Products.objects.get(id=product_id)
            qty = int(quantity or 1)
            unit_price = Decimal(str(product.price))
            checkout_items.append({
                'product': product,
                'qty': qty,
                'price': unit_price,
                'total': unit_price * qty,
            })
        except Products.DoesNotExist:
            checkout_items = []
    else:
        cart = Cart(request)
        for item in cart:
            checkout_items.append({
                'product': item['product'],
                'qty': int(item['qty']),
                'price': Decimal(str(item['price'])),
                'total': Decimal(str(item['total'])),
            })

    total_amount = sum((item['total'] for item in checkout_items), Decimal('0.00'))

    request.session['checkout_items'] = [
        {
            'product_id': str(item['product'].id),
            'quantity': int(item['qty']),
            'unit_price': str(item['price']),
        }
        for item in checkout_items
    ]

    return render(
        request,
        'orders/checkout.html',
        {
            'addresses': addresses,
            'address': selected_address,
            'checkout_items': checkout_items,
            'total_amount': total_amount,
        },
    )


@login_required
def place_order(request):
    if request.method == 'POST':
        selected_items = request.session.get('checkout_items') or []
        total_amount = Decimal('0.00')
        order_items = []

        if selected_items:
            for item_data in selected_items:
                product = Products.objects.get(id=item_data['product_id'])
                quantity = int(item_data['quantity'])
                unit_price = Decimal(str(item_data['unit_price']))
                total_amount += unit_price * quantity
                order_items.append((product, quantity))
        else:
            cart = Cart(request)
            for item in cart:
                product = item['product']
                quantity = int(item['qty'])
                unit_price = Decimal(str(item['price']))
                total_amount += unit_price * quantity
                order_items.append((product, quantity))

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, total_amount=total_amount)
        else:
            order = Order.objects.create(total_amount=total_amount)

        for product, quantity in order_items:
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        request.session.pop('checkout_items', None)

    return JsonResponse({'message': 'order placed successfully'})


def order_success(request):
    return render(request,'orders/order-success.html')


def order_failed(request):
    return render(request,'orders/order-failed.html')

def orders_view(request):
    order = OrderItem.objects.all()
    return render(request,'orders/orderlist.html',{'order':order})
