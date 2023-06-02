from django.contrib import admin

from core.models import Address

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'label_name',
        'shipping_address',
        'shipping_notes',
        'city',
        'country',
        'postal_code',
        'is_deleted',
    ]

admin.site.register(Address, AddressAdmin)
