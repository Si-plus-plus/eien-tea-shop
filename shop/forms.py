from django import forms
from .models import Cart


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
