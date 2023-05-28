from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.CatalogueView.as_view(), name='catalogue'),
    path('<slug>/', views.ItemDetailView.as_view(), name='item-detail')
]
