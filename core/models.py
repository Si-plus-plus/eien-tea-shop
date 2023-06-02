from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=150)
    shipping_notes = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="Indonesia")
    postal_code = models.CharField(max_length=10)

    is_deleted = models.BooleanField(default=False)

    def get_address(self):
        address = f"{self.shipping_address}, {self.city}, {self.country}, {self.postal_code}"
        if self.shipping_notes:
            address += f" [Notes: {self.shipping_notes}]"
        return address
    def __str__(self):
        return f"{self.label_name}: {self.get_address()}"
