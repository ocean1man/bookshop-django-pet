from typing import Optional, Tuple
from django.contrib.auth import authenticate

from bookshop.models import Cart, Wishlist

def authenticate_and_merge(session_id, *, username: str, password: str) -> Tuple[Optional[object], str]:
    user = authenticate(username=username, password=password)
    if user is None:
        return None, "invalid"

    user_wishlist = Wishlist.objects.filter(user=user).first()
    session_wishlist = Wishlist.objects.filter(session_id=session_id).first()
    if user_wishlist is None:
        if session_wishlist:
            session_wishlist.user = user
            session_wishlist.session_id = None
            session_wishlist.save()
    else:
        if session_wishlist:
            session_wishlist.delete()

    user_cart = Cart.objects.filter(user=user).first()
    session_cart = Cart.objects.filter(session_id=session_id).first()
    if user_cart is None:
        if session_cart:
            session_cart.user = user
            session_cart.session_id = None
            session_cart.save()
    else:
        if session_cart:
            session_cart.delete()

    return user, "ok"