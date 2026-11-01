from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Wishlist
from cakes.models import Cake


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('cake').all()
    subtotal = cart.get_total()
    delivery_charge = 0 if subtotal >= 500 else 50
    amount_needed_for_free_delivery = max(0, 500 - subtotal)
    total = subtotal + delivery_charge
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'amount_needed_for_free_delivery': amount_needed_for_free_delivery,
        'total': total,
    })


@login_required
def add_to_cart_view(request, cake_id):
    cake = get_object_or_404(Cake, pk=cake_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        cake=cake,
        defaults={
            'quantity': 1,
            'custom_message': request.POST.get('custom_message', ''),
            'flavor': request.POST.get('flavor', ''),
        }
    )
    if not created:
        cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()
        messages.success(request, f'"{cake.name}" quantity updated in cart.')
    else:
        messages.success(request, f'"{cake.name}" added to cart!')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.get_item_count()})
    return redirect(request.META.get('HTTP_REFERER', 'cart:view'))


@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cake_name = item.cake.name
    item.delete()
    messages.success(request, f'"{cake_name}" removed from cart.')
    return redirect('cart:view')


@login_required
def update_cart_view(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart:view')


@login_required
def clear_cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('cart:view')


@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'cart/wishlist.html', {'wishlist': wishlist})


@login_required
def toggle_wishlist_view(request, cake_id):
    cake = get_object_or_404(Cake, pk=cake_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if cake in wishlist.cakes.all():
        wishlist.cakes.remove(cake)
        added = False
        messages.info(request, f'"{cake.name}" removed from wishlist.')
    else:
        wishlist.cakes.add(cake)
        added = True
        messages.success(request, f'"{cake.name}" added to wishlist!')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'added': added, 'wishlist_count': wishlist.cakes.count()})
    return redirect(request.META.get('HTTP_REFERER', 'cart:wishlist'))
