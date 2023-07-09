from django.urls import path
from .views import ItemListView, ItemDetailView, ItemCreateView
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='market-home'),
    #path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    #path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('about/', views.about, name='market-about'),
]
