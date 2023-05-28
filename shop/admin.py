from django.contrib import admin
from .models import Item, Category, Type, Transaction, Cart, Address

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(Address)
