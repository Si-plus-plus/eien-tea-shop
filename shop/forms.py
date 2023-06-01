from django import forms
from .models import Cart, Variation, Item, Address

from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Button, Column, MultiField, Fieldset, Submit


User = get_user_model()


class AddToCartForm(forms.ModelForm):
    variation = forms.ModelChoiceField(queryset=Variation.objects.none())

    class Meta:
        model = Cart
        fields = ['variation', 'quantity']

        labels = {
            'quantity': 'Qty',
        }

    def __init__(self, *args, **kwargs):
        item_id = kwargs.pop('item_id')
        item = Item.objects.get(id=item_id)

        #TODO: implement in crispy

        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Row(
        #         Field('variation', css_class="w-2/3"),
        #         Field('quantity', css_class="w-1/3"),
        #     ),
        #     Row(
        #         Submit('submit', 'Add to cart',
        #                css_class='px-4 py-2 cursor-pointer bg-transparent hover:bg-green-700 text-green-700 font-semibold hover:text-white border border-green-700 hover:border-transparent rounded'),
        #         wrapper_class="content-end"
        #     )
        # )

        super(AddToCartForm, self).__init__(*args, **kwargs)

        self.fields['variation'].queryset = item.variation.all().order_by('name')


class AddressForm(forms.Form):
    label_name = forms.CharField(max_length=100, required=False)
    shipping_address = forms.CharField(max_length=150, required=False)
    shipping_notes = forms.CharField(max_length=150, required=False)
    city = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'type': 'number'}), required=False)

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=False
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)
        shipping_address_queryset = Address.objects.filter(user=user)

        self.fields['selected_shipping_address'].queryset = shipping_address_queryset

    def clean(self):
        data = self.cleaned_data
        selected_shipping_address = data.get('selected_shipping_address', None)

        if selected_shipping_address is None:
            if not data.get('label_name', None):
                self.add_error('label_name', 'This field is required')
            if not data.get('shipping_address', None):
                self.add_error('shipping_address', 'This field is required')
            if not data.get('city', None):
                self.add_error('city', 'This field is required')
            if not data.get('postal_code', None):
                self.add_error('postal_code', 'This field is required')
