from django.contrib import admin
from .models import Order, OrderItem, Booking


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    list_editable = ['status']
    readonly_fields = ['order_number', 'created_at']
    inlines = [OrderItemInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'cake', 'delivery_date', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'delivery_date']
    search_fields = ['user__username', 'cake__name']
    list_editable = ['status']
