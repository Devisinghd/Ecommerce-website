from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get("product_id")
        product_quantity = request.POST.get("product_quantity")
        print("product to the cart has an id",product_id)
        print("product has the quantity",product_quantity)
    return JsonResponse({'error': 'Method not allowed'}, status=405)