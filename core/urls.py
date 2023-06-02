from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('address/', views.AddressView.as_view(), name='address'),
    path('address/delete-address/<pk>', views.DeleteAddress.as_view(), name='delete-address'),
]
