from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.CatalogueView.as_view(), name='catalogue'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('item/<slug>/', views.ItemDetailView.as_view(), name='item-detail')
]
