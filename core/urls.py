from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/sent', views.ContactSentView.as_view(), name='contact-sent'),

    path('address/', views.AddressView.as_view(), name='address'),
    path('address/delete-address/<pk>', views.DeleteAddress.as_view(), name='delete-address'),
]
