import django_filters
from itertools import chain
from django import forms

from shop.models import Item


class SearchFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Newer'),
        ('descending', 'Older')
    )
    ordering = django_filters.ChoiceFilter(
        label='Sort by',
        choices=CHOICES,
        method='filter_by_order'
    )
    availability = django_filters.BooleanFilter(
        label='Show sold out',
        method='filter_by_availability',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Item
        fields = {
            'name': ['icontains'],
            'category': ['exact'],
            'type': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super(SearchFilter, self).__init__(*args, **kwargs)
        self.form.initial['availability'] = True

    def filter_by_order(self, queryset, name, value):
        if value == 'ascending':
            expression = 'created_at'
        else:
            expression = '-created_at'
        return queryset.order_by(expression)

    def filter_by_availability(self, queryset, name, value):
        if not value:
            return queryset.filter(stock__gt=0)
        return queryset.all()
