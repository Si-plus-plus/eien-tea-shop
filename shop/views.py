from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from .models import Item, Cart
from .utils import get_or_set_session
from .forms import AddToCartForm

from itertools import chain


class CatalogueView(generic.ListView):
    template_name = 'shop/catalogue.html'

    #TODO return items in stock, then items not in stock

    queryset = Item.objects.filter(active=True).order_by('-stock')

    context = {
        'item_list': queryset,
    }


class ItemDetailView(generic.FormView):
    template_name = 'shop/item.html'
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Item, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('shop:cart')

    def get_form_kwargs(self):
        kwargs = super(ItemDetailView, self).get_form_kwargs()
        kwargs['item_id'] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        transaction = get_or_set_session(self.request)
        item = self.get_object()

        item_filter = transaction.cart.filter(
            item=item,
            variation=form.cleaned_data['variation']
        )

        if item_filter.exists():
            entry = item_filter.first()
            entry.quantity = int(form.cleaned_data['quantity']) + entry.quantity
        else:
            entry = form.save(commit=False)
            entry.item = item
            entry.transaction = transaction

        entry.save()

        return super(ItemDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['item'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['transaction'] = get_or_set_session(self.request)
        return context


class AddQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop:cart')


class SubtractQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('shop:cart')


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])
        cart_item.delete()
        return redirect('shop:cart')