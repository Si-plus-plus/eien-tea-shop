from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from tea_shop import settings
from .forms import ContactForm
from .models import Address


class HomeView(generic.TemplateView):
    template_name = 'index.html'


class ContactView(generic.FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    # TODO prepopulate the email input for logged in users

    def get_success_url(self):
        return reverse("core:contact-sent")

    def form_valid(self, form):
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f'Contact Form Submission from {name} ({email})',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )

            return super(ContactView, self).form_valid(form)


class ContactSentView(generic.TemplateView):
    template_name = 'pages/contact_sent.html'


class AddressView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/addresses.html'

    def get_context_data(self, **kwargs):
        context = super(AddressView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user, is_deleted=False)
        return context


class DeleteAddress(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        address = get_object_or_404(Address, id=kwargs['pk'])
        address.is_deleted = True
        address.save()
        return redirect('core:address')

