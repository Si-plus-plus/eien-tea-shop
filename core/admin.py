from django.contrib import admin

from core.models import Address

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'label_name',
        'is_deleted',
        'shipping_address',
        'shipping_notes',
        'city',
        'country',
        'postal_code',
    ]

admin.site.register(Address, AddressAdmin)
