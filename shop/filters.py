import django_filters
from itertools import chain

from shop.models import Item


class SearchFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Newer'),
        ('descending', 'Older')
    )
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')
    price = django_filters.RangeFilter()

    class Meta:
        model = Item
        fields = {
            'name': ['icontains'],
            'category': ['exact'],
            'type': ['exact']
        }

    def __init__(self, *args, **kwargs):
        super(SearchFilter, self).__init__(*args, **kwargs)

    def filter_by_order(self, queryset, name, value):
        expression = ['stock']
        if value == 'ascending':
            expression = 'created_at'
        else:
            expression = '-created_at'
        return queryset.order_by(expression)
