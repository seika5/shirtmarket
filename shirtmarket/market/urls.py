from django.urls import path
from .views import LandingView, ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView, ItemDetailView, CategoryListView, CategoryCreateView, OrderListView
from . import views

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('store/', ItemListView.as_view(), name='market-home'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/<int:pk>/create-checkout-session/', views.create_checkout_session),
    path('purchase-success/<int:pk>/', views.purchaseSuccess),
    path('store/category/<int:pk>/', CategoryListView.as_view(), name='category-list'),
    path('category/new/', CategoryCreateView.as_view(), name='category-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('status-change/', views.status_change),
    path('webhook/', views.stripe_webhook),
    path('config/', views.stripe_config),
    path('contact/', views.contact, name='contact'),
]
