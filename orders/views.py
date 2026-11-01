from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderItem, Booking
from .forms import BookingForm, CheckoutForm
from cart.models import Cart, CartItem
from cakes.models import Cake
import uuid


@login_required
def booking_view(request, cake_slug):
    cake = get_object_or_404(Cake, slug=cake_slug, is_active=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.cake = cake
            booking.total_amount = cake.get_effective_price() * form.cleaned_data['quantity']
            booking.save()
            messages.success(request, f'Booking confirmed! Booking ID: #{booking.pk}')
            return redirect('orders:booking_detail', pk=booking.pk)
    else:
        form = BookingForm(initial={'delivery_address': request.user.address})
    return render(request, 'orders/booking.html', {'cake': cake, 'form': form})


@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'orders/booking_detail.html', {'booking': booking})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'orders/my_bookings.html', {'bookings': bookings})


@login_required
def checkout_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('cake').all()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view')

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view')

    subtotal = sum(item.total_price() for item in cart_items)
    delivery_charge = 0 if subtotal >= 500 else 50
    total = subtotal + delivery_charge

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_date=form.cleaned_data.get('delivery_date'),
                notes=form.cleaned_data.get('notes', ''),
                subtotal=subtotal,
                delivery_charge=delivery_charge,
                total_amount=total,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    cake=item.cake,
                    quantity=item.quantity,
                    unit_price=item.cake.get_effective_price(),
                    total_price=item.total_price(),
                    custom_message=item.custom_message or '',
                    flavor=item.flavor or '',
                )
            cart_items.delete()
            return redirect('payments:payment', order_id=order.pk)
    else:
        form = CheckoutForm(initial={'delivery_address': request.user.address})

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'total': total,
        'form': form,
    })


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in ('pending', 'confirmed'):
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:detail', pk=pk)
