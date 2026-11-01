from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('book/<slug:cake_slug>/', views.booking_view, name='book'),
    path('bookings/', views.my_bookings_view, name='my_bookings'),
    path('bookings/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.order_list_view, name='list'),
    path('<int:pk>/', views.order_detail_view, name='detail'),
    path('<int:pk>/cancel/', views.cancel_order_view, name='cancel'),
]
