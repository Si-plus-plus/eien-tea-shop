from django.contrib import admin
from .models import Item, Category, Type, Transaction, Cart, Variation, PaymentMethod, Payment, AdditionalItemImage

@admin.action(description="Set selected items as inactive")
def item_set_inactive(modeladmin, request, queryset):
    queryset.update(active=False)

@admin.action(description="Set selected items as active")
def item_set_active(modeladmin, request, queryset):
    queryset.update(active=True)

class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'active',
        'slug',
        'category',
        'type',
        'price',
        'discounted_price',
        'stock',
        'sold_count',
        'created_at'
    ]
    actions = [
        item_set_inactive,
        item_set_active
    ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'shipping_address',
        'finished',
    ]


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'transaction',
        'item',
        'variation',
        'quantity',
        'buy_price',
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'payment_method',
        'timestamp',
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(AdditionalItemImage)
admin.site.register(Variation)
admin.site.register(Type)
admin.site.register(Category)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Payment, PaymentAdmin)
