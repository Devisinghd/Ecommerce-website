from decimal import Decimal

from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from myapp.models import Products
from django.shortcuts import get_object_or_404
from django.contrib import messages


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

    # Determine selected address id and object.
    selected_address_id = None
    # Keep the default selected_address (addresses.first()) unless POST overrides it
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address_id')
        if addresses and selected_address_id:
            selected_address = addresses.filter(id=selected_address_id).first()
        else:
            # if user POSTed but provided no/invalid address, keep selected_address None
            selected_address = None
    else:
        # for GET, ensure selected_address_id reflects the default selected_address
        if selected_address:
            selected_address_id = str(selected_address.id)

    if request.method == 'POST':
        if not checkout_items:
            messages.warning(request, 'No items were found in your cart. Please add items before placing an order.')
            return redirect('checkout_warning')

        if addresses and not selected_address:
            messages.error(request, 'Please select a valid delivery address before placing your order.')
            return redirect('checkout')

        order = Order.objects.create(user=request.user, total_amount=total_amount)
        for item in checkout_items:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['qty'])

        request.session.pop('checkout_items', None)
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('order-success')

    return render(
        request,
        'orders/checkout.html',
        {
            'addresses': addresses,
            'address': selected_address,
            'checkout_items': checkout_items,
            'total_amount': total_amount,
            'selected_address_id': selected_address_id,
        },
    )


@login_required
def place_order(request):
    if request.method == 'POST':
        selected_items = request.session.get('checkout_items') or []
        selected_address_id = request.POST.get('selected_address_id')
        addresses = Address.objects.filter(user=request.user).order_by('-id')
        selected_address = addresses.filter(id=selected_address_id).first() if selected_address_id else None

        if not selected_items:
            return JsonResponse({'error': 'No items were found in your cart.'}, status=400)

        if addresses and not selected_address:
            return JsonResponse({'error': 'Please select a valid delivery address.'}, status=400)

        total_amount = Decimal('0.00')
        order_items = []

        for item_data in selected_items:
            product = Products.objects.get(id=item_data['product_id'])
            quantity = int(item_data['quantity'])
            unit_price = Decimal(str(item_data['unit_price']))
            total_amount += unit_price * quantity
            order_items.append((product, quantity))

        order = Order.objects.create(user=request.user, total_amount=total_amount)

        for product, quantity in order_items:
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        request.session.pop('checkout_items', None)
        return JsonResponse({'message': 'order placed successfully'})

    return JsonResponse({'error': 'Invalid method'}, status=405)


def order_success(request):
    return render(request,'orders/order-success.html')


def order_failed(request):
    return render(request,'orders/order-failed.html')

def orders_view(request):
    order = OrderItem.objects.filter(order__user=request.user)
    return render(request,'orders/orderlist.html',{'order':order})

def checkout_warning(request):
    return render(request,'orders/checkout_warning.html')

@login_required
def cancel_order(request, id):
    order_item = get_object_or_404(OrderItem, id=id, order__user=request.user)
    order = order_item.order

    if request.method == "POST":
        order_item.delete()
        # If the parent order has no more items, remove the order as well
        if not OrderItem.objects.filter(order=order).exists():
            order.delete()
        messages.success(request, "Order cancelled successfully.")
        return redirect("order_view")

    messages.info(request, "Cancellation not confirmed.")
    return redirect("order_view")