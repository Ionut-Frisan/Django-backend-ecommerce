from statistics import quantiles
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from product.models import Product
from account.models import Account


class OrderStatus(models.Model):
    status = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(
        Account, related_name='Orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    status = models.ForeignKey(
        OrderStatus, related_name='Orders', on_delete=models.DO_NOTHING, null=False, default=1)
    stripe_token = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.id}'
