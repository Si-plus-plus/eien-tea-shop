from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from math import ceil

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


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=150)
    shipping_notes = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    def __str__(self):
        address_string = f"{self.name}: {self.shipping_address}, {self.city}, {self.postal_code}"

        if self.shipping_notes:
            address_string += f" [{self.shipping_notes}]"

        return address_string


class Variation(models.Model):
    name = models.CharField(max_length=20)
    stock = models.IntegerField()

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


class Transaction(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    shipping_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.pk)

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


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Paypal', 'VA BCA'),
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    amount_paid = models.IntegerField()
    raw_response = models.TextField()

    def __str__(self):
        return f"Order: {self.transaction}/ Payment:-{self.pk}"
