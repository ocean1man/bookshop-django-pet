from typing import Dict, Any, Tuple
from bookshop.models import Book, CartItem, Wishlist, WishlistItem
from django.db import transaction

from bookshop.services.session_store import get_wishlist_and_cart

def build_wishlist_context(session_id,user, *, sort_order: str = "", view_type: str = "") -> Dict[str, Any]:

    if sort_order not in {"", "low_to_high", "high_to_low"}:
        sort_order = ""
    
    wishlist, cart = get_wishlist_and_cart(session_id, user)
    
    cart_books = []
    if cart:
        cart_books = list(CartItem.objects.filter(cart=cart).values_list("book_id", flat=True))

    wishlist_items = WishlistItem.objects.none()
    if wishlist:
        wishlist_items = (WishlistItem.objects.filter(wishlist=wishlist).select_related("book").order_by("id"))
        if sort_order == "low_to_high":
            wishlist_items = wishlist_items.order_by("book__price")
        elif sort_order == "high_to_low":
            wishlist_items = wishlist_items.order_by("-book__price")

    return {
        "view_type": view_type,
        "sort_order": sort_order,
        "wishlist_items": wishlist_items,
        "cart_books": cart_books,
    }


def add_book_to_wishlist(session_id, user, *, book: Book) -> Tuple[WishlistItem, bool]:
    with transaction.atomic():
        if user:
            wishlist, _ = Wishlist.objects.get_or_create(user=user)
        else:
            wishlist, _ = Wishlist.objects.get_or_create(session_id=session_id)

        item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, book=book)

    return item, created


def remove_book_from_wishlist(session_id, user, *, book_id: int) -> Tuple[bool, bool]:
    wishlist, _ = get_wishlist_and_cart(session_id, user)
    if not wishlist:
        return False, True

    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, book_id=book_id).first()
    if not wishlist_item:
        return False, False

    with transaction.atomic():
        wishlist_item.delete()

        wishlist_empty = not WishlistItem.objects.filter(wishlist=wishlist).exists()
        if wishlist_empty:
            wishlist.delete()

    return True, wishlist_empty