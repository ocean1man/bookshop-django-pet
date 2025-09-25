from typing import Any, Dict

from django.shortcuts import get_object_or_404

from bookshop.models import Book, CartItem, WishlistItem
from bookshop.services.session_store import get_wishlist_and_cart


def build_book_context(session_id, user, *, book_id: int) -> Dict[str, Any]:
    wishlist, cart = get_wishlist_and_cart(session_id, user)
    book = get_object_or_404(Book, pk=book_id)

    wishlist_item = None
    cart_item = None

    if wishlist:
        wishlist_item = (
            WishlistItem.objects
            .filter(wishlist=wishlist, book=book)
            .first()
        )

    if cart:
        cart_item = (
            CartItem.objects
            .filter(cart=cart, book=book)
            .first()
        )

    return {
        "book": book,
        "wishlist_item": wishlist_item,
        "cart_item": cart_item,
    }