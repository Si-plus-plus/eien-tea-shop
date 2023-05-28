from django.shortcuts import render
from django.views import generic
from .models import Item


class CatalogueView(generic.ListView):
    template_name = 'shop/catalogue.html'
    queryset = Item.objects.all()

    context = {
        'item_list': queryset,
    }


class ItemDetailView(generic.DetailView):
    template_name = 'shop/item.html'
    queryset = Item.objects.all()

    context = {
        'item': queryset,
    }



