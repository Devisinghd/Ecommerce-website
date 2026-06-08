from django.db import models

class ProductsManager(models.Manager):
    def cheap_products(self):
        return self.filter(price__lt=5)
    def expensive_products(self):
        return self.filter(price__gt=5)
    def search(self,keyword):
        return self.filter(name__icontains=keyword)