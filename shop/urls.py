from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.CatalogueView.as_view(), name='catalogue'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('item/<slug>/', views.ItemDetailView.as_view(), name='item-detail'),

    path('add-quantity/<pk>/', views.AddQuantityView.as_view(), name='add-quantity'),
    path('subtract-quantity/<pk>/', views.SubtractQuantityView.as_view(), name='subtract-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),

    path('checkout/', views.CheckoutView.as_view(), name='cart-checkout'),
]
