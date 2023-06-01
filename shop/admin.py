from django.contrib import admin
from .models import Item, Category, Type, Transaction, Cart, Address, Variation


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'category',
        'type',
        'price',
        'discounted_price',
        'stock',
        'sold_count'
    ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'paid_at',
        'shipping_address',
    ]


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'item',
        'variation',
        'quantity',
        'buy_price',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'label_name',
        'shipping_address',
        'shipping_notes',
        'city',
        'postal_code',
        'default',
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Variation)
admin.site.register(Type)
admin.site.register(Category)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Address, AddressAdmin)
