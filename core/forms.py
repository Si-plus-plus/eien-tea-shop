from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(max_length=10000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        if not data.get('name', None):
            self.add_error('name', 'This field is required')
        if not data.get('email', None):
            self.add_error('email', 'This field is required')
        if not data.get('message', None):
            self.add_error('message', 'This field is required')
