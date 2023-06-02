from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from shop.models import Transaction, Address


# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'index.html'


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'user/addresses.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context




