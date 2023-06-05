from random import randint

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic

from tea_shop import settings
from .filters import SearchFilter
from .forms import AddToCartForm, AddressForm, PaymentForm
from .models import Item, Cart, Address, Transaction, Payment, AdditionalItemImage, PaymentMethod
from .utils import get_or_set_session


def finalize_payment(transaction, payment_method):
    payment = Payment()
    payment.payment_method = payment_method
    payment.amount = transaction.get_total_discounted_price()
    payment.save()

    transaction.payment = payment
    transaction.finished = True
    transaction.save()


class CatalogueView(generic.ListView):
    template_name = 'shop/catalogue.html'
    queryset = Item.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        # TODO return items in stock, then items not in stock
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context['filter'] = SearchFilter(
            self.request.GET,
            queryset=self.queryset
        )
        return context


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
        context['alt_images'] = AdditionalItemImage.objects.filter(item=self.get_object())
        return context


class CartView(generic.TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        transaction = get_or_set_session(self.request)
        context['transaction'] = transaction
        context['cart'] = Cart.objects.filter(transaction=transaction, item__active=True)
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


class CheckoutView(LoginRequiredMixin, generic.FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse('shop:payment')

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def gen_invoice_no(self, transaction):
        # TODO proper invoicing
        prefix = transaction.created_at.strftime("%Y%m%d")
        prefix += '/'
        for i in range(3):
            prefix += chr(65 + randint(0, 25))
        prefix = prefix + '/' + str(transaction.pk)
        return prefix

    def freeze_buy_price(self, transaction):
        cart_items = Cart.objects.filter(transaction=transaction)

        for item in cart_items:
            if item.item.is_discounted():
                item.buy_price = item.item.discounted_price
            else:
                item.buy_price = item.item.price
            item.save()

    def form_valid(self, form):
        transaction = get_or_set_session(self.request)
        selected_shipping_address = form.cleaned_data.get('select_address')

        if selected_shipping_address:
            transaction.shipping_address = selected_shipping_address
        else:
            new_address = Address.objects.create(
                user=self.request.user,
                label_name=form.cleaned_data['label_name'],
                shipping_address=form.cleaned_data['shipping_address'],
                shipping_notes=form.cleaned_data['shipping_notes'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
            )
            transaction.shipping_address = new_address

        self.freeze_buy_price(transaction)
        transaction.invoice_no = self.gen_invoice_no(transaction)

        transaction.save()

        return super(CheckoutView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        transaction = get_or_set_session(self.request)
        context['transaction'] = transaction
        context['cart'] = Cart.objects.filter(transaction=transaction, item__active=True)
        return context


class TransactionsListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/transactions_list.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionsListView, self).get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(user=self.request.user, finished=True).order_by('-created_at')
        return context


class PaymentView(LoginRequiredMixin, generic.FormView):
    template_name = 'shop/payment.html'
    form_class = PaymentForm

    def get_success_url(self):
        return reverse('shop:transactions-list')

    def get_form_kwargs(self):
        kwargs = super(PaymentView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        transaction = get_or_set_session(self.request)
        payment_method = form.cleaned_data['payment_method']
        finalize_payment(transaction, payment_method)

        return super(PaymentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        transaction = get_or_set_session(self.request)
        context['order'] = transaction
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context['IDR_amount'] = transaction.get_total_discounted_price()
        context['USD_amount'] = round(transaction.get_total_discounted_price() / 15000, 2) #TODO convert properly
        context['CALLBACK_URL'] = self.request.build_absolute_uri(reverse("shop:transactions-list"))
        return context


def capture_transaction_view(request, *args, **kwargs):
    transaction = get_or_set_session(request)
    payment_method = PaymentMethod.objects.get(id=4)
    finalize_payment(transaction, payment_method)

    return JsonResponse({"data": "Success"})

