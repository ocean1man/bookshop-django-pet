from typing import Dict, Any, Tuple
from django.shortcuts import get_object_or_404
from bookshop.models import Book, Cart, CartItem, Order, OrderItem, WishlistItem
from django.db import transaction
from django.db.models import F

from bookshop.services.session_store import get_wishlist_and_cart

def build_cart_context(session_id, user) -> Dict[str, Any]:
    wishlist, cart = get_wishlist_and_cart(session_id, user)

    wishlist_books = []

    if wishlist:
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        wishlist_books = [item.book.id for item in wishlist_items]

    cart_items = CartItem.objects.filter(cart=cart).order_by('id')
    count_items = cart_items.count()
    
    return {
        "cart_items": cart_items,
        "count_items": count_items,
        "wishlist_books": wishlist_books,
    }

def place_order_from_cart(session_id, user, *, fullname: str, email: str, mail_index: str) -> Order:
    if user is None:
        raise PermissionError("Пользователь должен быть аутентифицирован")
    
    _, cart = get_wishlist_and_cart(session_id=session_id, user=user)

    with transaction.atomic():
        order = Order.objects.create(
            user=user, fullname=fullname, email=email, mail_index=mail_index
        )
        
        cart_items = CartItem.objects.filter(cart=cart).select_related("book")

        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)

            Book.objects.filter(pk=item.book_id).update(count=F("count") - item.quantity)

        cart.delete()

    return order

def add_book_to_cart(session_id, user, *, book_id: int) -> CartItem:
    book = get_object_or_404(Book, pk=book_id)        

    with transaction.atomic():
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_id=session_id)

        cart_item = CartItem.objects.create(cart=cart, book=book, quantity=1)

    return cart_item

def change_cart_item_quantity(session_id, user, *, book_id: int, delta: int) -> int:
    _, cart = get_wishlist_and_cart(session_id, user)

    cart_item = CartItem.objects.filter(cart=cart, book_id=book_id).first()

    new_qty = cart_item.quantity + delta
    if new_qty < 1:
        raise ValueError("Количество не может быть меньше 1")

    book = cart_item.book
    if new_qty > book.count:
        raise ValueError("Недостаточно товара на складе")

    cart_item.quantity = new_qty
    cart_item.save(update_fields=["quantity"])
    return cart_item.quantity

def remove_book_from_cart(session_id, user, *, book_id: int) -> Tuple[bool, bool]:
    _, cart = get_wishlist_and_cart(session_id, user)

    with transaction.atomic():
        deleted, _ = CartItem.objects.filter(cart=cart, book_id=book_id).delete()
        cart_empty = not CartItem.objects.filter(cart=cart).exists()
        if cart_empty:
            cart.delete()
            
    return bool(deleted), cart_empty 