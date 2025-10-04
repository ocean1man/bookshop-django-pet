from typing import Any, Dict

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from bookshop.models import Book, CartItem, WishlistItem
from bookshop.services.session_store import get_wishlist_and_cart


CACHE_TIMEOUT = 60 * 5
CACHE_VERSION = 1

def build_book_context(session_id, user, *, book_id: int) -> Dict[str, Any]:
    key = f"book:{book_id}"
    book = cache.get(key)
    if not book:
        book = get_object_or_404(Book, pk=book_id)
        cache.set(key, book, timeout=CACHE_TIMEOUT, version=CACHE_VERSION)

    wishlist, cart = get_wishlist_and_cart(session_id, user)

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