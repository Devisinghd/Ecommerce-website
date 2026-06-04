from django.db import models
from django.contrib.auth.models import User
from myapp.models import Products
# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField( max_length=20)
    line1 = models.CharField( max_length=250)
    line2 = models.CharField( max_length=250)
    city = models.CharField( max_length=50)
    state = models.CharField( max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField( max_digits=10, decimal_places=2,default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def total_price(self):
        return self.product.price * self.quantity