from django import template
from shop.utils import get_or_set_session

register = template.Library()


@register.filter
def cart_item_count(request):
    transaction = get_or_set_session(request)
    count = transaction.cart.count()
    return count