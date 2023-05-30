from django import forms
from .models import Cart, Variation, Item

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Button, Column, MultiField, Fieldset, Submit


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


