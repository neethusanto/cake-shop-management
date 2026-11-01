from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:cake_id>/', views.add_to_cart_view, name='add'),
    path('remove/<int:item_id>/', views.remove_from_cart_view, name='remove'),
    path('update/<int:item_id>/', views.update_cart_view, name='update'),
    path('clear/', views.clear_cart_view, name='clear'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:cake_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),
]
