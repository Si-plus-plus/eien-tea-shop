from django.contrib import messages
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from .models import Item, Cart, Address
from .utils import get_or_set_session, get_or_set_transaction_session, set_payment
from .forms import AddToCartForm, AddressForm, PaymentForm
from django.utils import timezone

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


class PaymentView(generic.FormView):
    template_name = 'shop/payment.html'
    form_class = PaymentForm

    def get_success_url(self):
        return reverse('home') #TODO transaction history

    def get_form_kwargs(self):
        kwargs = super(PaymentView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        payment = set_payment(self.request)

        payment.payment_method = form.cleaned_data['payment_method']
        payment.success = True
        payment.save()

        transaction = get_or_set_transaction_session(self.request)
        transaction.payment = payment
        transaction.save()

        return super(PaymentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['transaction'] = get_or_set_transaction_session(self.request)
        return context


class CheckoutView(generic.FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse('shop:payment')

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def freeze_buy_price(self, transaction):
        cart_items = Cart.objects.filter(transaction=transaction)

        for item in cart_items:
            if item.item.is_discounted():
                item.buy_price = item.item.discounted_price
            else:
                item.buy_price = item.item.price
            item.save()

    def form_valid(self, form):
        transaction = get_or_set_transaction_session(self.request)
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')

        if selected_shipping_address:
            transaction.shipping_address = selected_shipping_address
        else:
            new_address = Address.objects.create(
                user = self.request.user,
                label_name = form.cleaned_data['label_name'],
                shipping_address = form.cleaned_data['shipping_address'],
                shipping_notes = form.cleaned_data['shipping_notes'],
                city = form.cleaned_data['city'],
                postal_code = form.cleaned_data['postal_code'],
            )
            transaction.shipping_address = new_address

        self.freeze_buy_price(transaction)

        transaction.save()

        return super(CheckoutView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['transaction'] = get_or_set_transaction_session(self.request)
        return context
