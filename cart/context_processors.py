from .models import Cart, Wishlist


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_count': cart.get_item_count()}
        except Cart.DoesNotExist:
            pass
    return {'cart_count': 0}


def wishlist_count(request):
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            return {'wishlist_count': wishlist.cakes.count()}
        except Wishlist.DoesNotExist:
            pass
    return {'wishlist_count': 0}
