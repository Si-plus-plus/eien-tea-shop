from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

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


class Item(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, blank=True)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(null=True, blank=True)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)

    description = models.CharField(max_length=1000)
    stock = models.PositiveIntegerField()
    sold_count = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='product_images', default='none/none.jpg', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:item-detail", kwargs={'slug': self.slug})


class Transaction(models.Model):
    user = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=DO_NOTHING)

    def __str__(self):
        return f"O-{self.pk}"


class Cart(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    buy_price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} pc(s)"


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Paypal', 'VA BCA'),
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    amount_paid = models.PositiveIntegerField()
    raw_response = models.TextField()

    def __str__(self):
        return f"O-{self.transaction}/P-{self.pk}"


