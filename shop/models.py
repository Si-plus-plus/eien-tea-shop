import hashlib

from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from math import ceil
from datetime import timedelta
from django.utils import timezone

from core.models import Address
import datetime

User = get_user_model()


class Category(models.Model):
    # Red, Black, Green Tea, Tisane
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Type(models.Model):
    # Teabags, Loose-leaf
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, blank=True)
    price = models.IntegerField()
    discounted_price = models.IntegerField(null=True, blank=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    variation = models.ManyToManyField(Variation)
    description = models.TextField(max_length=10000)

    stock = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)

    image = models.ImageField(upload_to='item_images', default='none/none.jpg', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:item-detail", kwargs={'slug': self.slug})

    def in_stock(self):
        return self.stock > 0

    def is_active(self):
        return self.active

    def is_newly_added(self):
        return timezone.now() < self.created_at + timedelta(days=1)

    #TODO implement functions to get formatted price/discounted price

    def is_discounted(self):
        if not self.discounted_price:
            return False
        if self.price <= self.discounted_price:
            return False
        return True

    def get_discount_value(self):
        return self.price - self.discounted_price

    def get_discount_percentage(self) -> str:
        return f"-{ceil(self.get_discount_value()/self.price * 100)}%"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}"


class Transaction(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    invoice_no = models.CharField(null=True, blank=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.DO_NOTHING)
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    def get_date(self):
        return self.created_at.strftime("%d-%B-%Y")

    def get_items_summary(self) -> str:
        summary = ""
        for cart_items in self.cart.all():
            name = cart_items.item.name
            if len(cart_items.item.name) > 12:
                name = name[:12]
                name += "..."
            item = f"{name}, {cart_items.variation}"
            summary += item + '\n'
        return summary

    def get_total_price(self):
        total = 0
        for cart_items in self.cart.all():
            total += cart_items.get_total_item_price()
        return total

    def get_total_discounted_price(self):
        total = 0
        for cart_items in self.cart.all():
            if cart_items.item.is_discounted():
                total += cart_items.get_total_item_discounted_price()
            else:
                total += cart_items.get_total_item_price()
        return total

    def get_total_discount_value(self):
        return self.get_total_price() - self.get_total_discounted_price()


class Cart(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='cart', null=True, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    buy_price = models.IntegerField(null=True, blank=True)
    variation = models.ForeignKey(Variation, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} pc(s)"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discounted_price(self):
        return self.quantity * self.item.discounted_price

