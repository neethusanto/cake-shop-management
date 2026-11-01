from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:order_id>/', views.payment_view, name='payment'),
    path('<int:order_id>/success/', views.payment_success_view, name='success'),
    path('<int:order_id>/cod/', views.cod_payment_view, name='cod'),
    path('webhook/', views.razorpay_webhook_view, name='webhook'),
]
