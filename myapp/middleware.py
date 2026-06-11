import time
from django.http import HttpResponseForbidden
class TimerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response


    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        print(f"[middleware] Request took: {duration:.2f} second")
        return response
    
class BlockIPMiddleware:
    BLOCKED_IPS = []
    def __init__(self,get_response):
        self.get_response = get_response


    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked")
        return self.get_response(request)