import json
from django.http import JsonResponse

import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_GET

from bookshop.services.auth import authenticate_and_merge
from bookshop.services.book import build_book_context
from bookshop.services.cart import add_book_to_cart, build_cart_context, change_cart_item_quantity, place_order_from_cart, remove_book_from_cart
from bookshop.services.catalog import CatalogFilters, build_catalog_context
from bookshop.services.wishlist import add_book_to_wishlist, build_wishlist_context, remove_book_from_wishlist

from .models import Book, Order
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# Create your views here.

@require_GET
def catalog_view(request):
    create_session(request)
    session_id, user = get_session_and_user(request)

    query = request.GET.get('search', '')
    view_type = request.GET.get('view', '')
    sort_order = request.GET.get('sort', '')

    def _to_int(s):
        try:
            return int(s)
        except (TypeError, ValueError):
            return None

    author_id = _to_int(request.GET.get('author'))
    age_limit_id = _to_int(request.GET.get('age_limit'))
    genre_ids = [g for g in ( _to_int(x) for x in request.GET.getlist('genre') ) if g is not None]

    century_publication = request.GET.get('century_publication', '')

    min_price_value = _to_int(request.GET.get('min_price'))
    max_price_value = _to_int(request.GET.get('max_price'))

    show_hide_filters = bool(request.GET.get('show_filters', ''))

    filters = CatalogFilters(
        query=query,
        view_type=view_type,
        sort_order=sort_order,
        author_id=author_id,
        genre_ids=genre_ids,
        age_limit_id=age_limit_id,
        century_publication=century_publication,
        min_price_value=min_price_value,
        max_price_value=max_price_value,
        show_hide_filters=show_hide_filters,
        page_number=request.GET.get('page'),
    )

    context = build_catalog_context(session_id, user, filters=filters, page_size=12)
    return render(request, 'bookshop/catalog.html', context)

@require_GET
def book_view(request, book_id):
    create_session(request)
    session_id, user = get_session_and_user(request)

    context = build_book_context(session_id, user, book_id=book_id)
    return render(request, "bookshop/product.html", context)


def cart_view(request):
    if request.method == 'GET':
        return cart_get_view(request)
    elif request.method == 'POST':
        return cart_post_view(request)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)


def cart_get_view(request):
    create_session(request)
    session_id, user = get_session_and_user(request)
    context = build_cart_context(session_id, user)
    return render(request, "bookshop/cart.html", context)


def cart_post_view(request):
    _, user = get_session_and_user(request)
    if user is None:
        return JsonResponse({'message': 'Для оформления заказа необходимо войти в свой профиль!'})
    
    data = json.loads(request.body)
    fullname = data.get('fullName')
    email = data.get('email')
    mail_index = data.get('mailIndex')

    if not is_email(email):
        return JsonResponse({'message': 'Электронная почта введёна неверно!'}, status=400)
    
    try:
        place_order_from_cart(
            None, user,
            fullname=fullname, email=email, mail_index=mail_index
        )
    except ValueError as e:
        return JsonResponse({'message': str(e)}, status=400)
    
    return JsonResponse({'message': 'Заказ успешно создан! В ближайшее время с вами свяжутся по электронной почте!'})


@require_POST
def add_to_cart_view(request, book_id):
    create_session(request)
    session_id, user = get_session_and_user(request)

    try:
        add_book_to_cart(session_id, user, book_id=book_id)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Товар добавлен в корзину"})


@require_http_methods(["PATCH"])
def update_cart_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    data = json.loads(request.body)
    action = data.get('action')
    if action not in {"addQuantity", "reduceQuantity"}:
        return JsonResponse({"message": "Некорректное действие"}, status=400)
    
    delta = 1 if action == "addQuantity" else -1

    try:
        change_cart_item_quantity(session_id, user, book_id=book_id, delta=delta)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)

    msg = "Количество товара увеличено" if delta == 1 else "Количество товара уменьшено"
    return JsonResponse({"message": msg})


@require_http_methods(["DELETE"])
def delete_cartitem_view(request, book_id):
    create_session(request)
    session_id, user = get_session_and_user(request)

    deleted, _ = remove_book_from_cart(session_id, user, book_id=book_id)
    if not deleted:
        return JsonResponse({"message": "Товар не найден в корзине"}, status=404)

    return JsonResponse({'message': 'Товар удалён из корзины'})


@require_GET
def wishlist_view(request):
    create_session(request)
    session_id, user = get_session_and_user(request)

    view_type = request.GET.get("view", "")
    sort_order = request.GET.get("sort", "")

    context = build_wishlist_context(
        session_id, user,
        sort_order=sort_order,
        view_type=view_type,
    )
    return render(request, "bookshop/wishlist.html", context)
    

@require_POST
def add_to_wishlist_view(request, book_id):
    create_session(request)
    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)

    add_book_to_wishlist(session_id, user, book=book)

    return JsonResponse({'message': 'Товар добавлен в избранное'})


@require_http_methods(["DELETE"])
def delete_wishlistitem_view(request, book_id):
    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)

    remove_book_from_wishlist(session_id, user, book_id=book.id) 

    return JsonResponse({'message': 'Товар удалён из избранного'})


def login_view(request):
    if request.method == 'GET':
        return login_get_view(request)
    elif request.method == 'POST':
        return login_post_view(request)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)


def login_get_view(request):
    if request.user.is_authenticated:
        return redirect('/profile/')

    create_session(request)
    return render(request, 'bookshop/login.html')


def login_post_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'already authenticated'}, status=400)

    create_session(request)

    session_id, _ = get_session_and_user(request)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user, msg = authenticate_and_merge(session_id, username=username, password=password)
    if user is None:
        return JsonResponse({'message': msg})

    login(request, user)
    return JsonResponse({'message': 'ok'}, status=200)


def signup_view(request):
    if request.method == 'GET':
        return signup_get_view(request)
    elif request.method == 'POST':
        return signup_post_view(request)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)


def signup_post_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'already authenticated'}, status=400)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'ok'})
    except IntegrityError:
        return JsonResponse({'message': 'exists'}, status=400)


def signup_get_view(request):
    if request.user.is_authenticated:
        return redirect('/profile/')
    create_session(request)

    return render(request, 'bookshop/signup.html')


@require_GET
@login_required
def profile_view(request):
    create_session(request)
    _, user = get_session_and_user(request)
    orders = Order.objects.filter(user=user)
    return render(request, 'bookshop/profile.html', {'orders': orders})

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'ok'})


@require_GET
def main_view(request):
    create_session(request)

    books = list(Book.objects.filter(count__gt=0, img_path__isnull=False).exclude(img_path=''))
    books = random.sample(books, 12)
    
    return render(request, 'bookshop/main.html', {'books': books})

def get_session_and_user(request):
    session_id = request.COOKIES.get('sessionid')
    user = request.user if request.user.is_authenticated else None

    return session_id, user


def create_session(request):
    if request.COOKIES.get('sessionid') is None:
        request.session.create()


def is_email(value):
    try:
        EmailValidator()(value)
        return True
    except ValidationError:
        return False