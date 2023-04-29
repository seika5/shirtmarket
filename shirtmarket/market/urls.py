from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='market-home'),
    path('about/', views.about, name='market-about'),
=======
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
>>>>>>> parent of 2eba030 (Revert "initial commit")
]
