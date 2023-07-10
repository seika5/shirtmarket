from django.urls import path
from .views import ItemUpdateView, ItemDeleteView, ItemListView, ItemDetailView, ItemCreateView
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='market-home'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('about/', views.about, name='market-about'),
]
