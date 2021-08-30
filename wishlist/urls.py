from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
    path('add/<item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('adjust/<item_id>/', views.adjust_wishlist, name='adjust_wishlist'),
    path('remove/<item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]