from typing import Optional, Tuple

from bookshop.models import Cart, Wishlist

def get_wishlist_and_cart(session_id, user) -> Tuple[Optional[Wishlist], Optional[Cart]]:
    if user:
        wishlist = Wishlist.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=user).first()
    else:
        wishlist = Wishlist.objects.filter(session_id=session_id).first()
        cart = Cart.objects.filter(session_id=session_id).first()

    return wishlist, cart