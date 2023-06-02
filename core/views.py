from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Address


# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'index.html'


class AddressView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/addresses.html'

    def get_context_data(self, **kwargs):
        context = super(AddressView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user, is_deleted=False)
        return context


class DeleteAddress(generic.View):
    def get(self, request, *args, **kwargs):
        address = get_object_or_404(Address, id=kwargs['pk'])
        address.is_deleted = True
        address.save()
        return redirect('core:address')

