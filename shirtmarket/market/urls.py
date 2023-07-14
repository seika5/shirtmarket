from django.urls import path
from .views import ItemUpdateView, ItemDeleteView, ItemListView, ItemDetailView, ItemCreateView
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='market-home'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/<int:pk>/create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
    path('success/', views.purchaseSuccess),
    path('config/', views.stripe_config),
    path('about/', views.about, name='market-about'),
]
