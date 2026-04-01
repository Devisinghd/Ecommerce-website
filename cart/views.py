from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def cart_add(request):
    if request.method == 'POST':
        # Return a non-dict JSON object (list) and allow it with safe=False
        return JsonResponse(['product added in cart'], safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)