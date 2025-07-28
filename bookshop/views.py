import json
from django.http import JsonResponse

import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_GET

from .models import Book, Cart, CartItem, Author, Genre, Wishlist, WishlistItem, Order, OrderItem, AgeLimit
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage

from django.db.models import Q, Max, Min

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# Create your views here.

@require_GET
def catalog_view(request):
    create_session(request)

    session_id, user = get_session_and_user(request)
    wishlist, cart = get_wishlist_and_cart(session_id, user)
    wishlist_books = []
    cart_books = []

    if wishlist:
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        wishlist_books = [item.book.id for item in wishlist_items]

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        cart_books = [item.book.id for item in cart_items]

    is_catalog = True

    query = request.GET.get('search', '')
    view_type = request.GET.get('view', '') 
    sort_order = request.GET.get('sort', '')
    author_id = int(request.GET.get('author', '')) if request.GET.get('author', '') else ''
    genre_ids = [int(genre_id) for genre_id in request.GET.getlist('genre') if genre_id.strip() != '']
    age_limit_id = int(request.GET.get('age_limit', '')) if request.GET.get('age_limit', '') else ''
    century_publication = request.GET.get('century_publication', '')
    min_price_value = request.GET.get('min_price', '')
    max_price_value = request.GET.get('max_price', '')
    show_hide_filters = request.GET.get('show_filters', '')

    books = Book.objects.all()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    age_limits = AgeLimit.objects.all()
    century_publications = ['21 век', '20 век', '19 век', 'Раньше']
    show_hide_text = "Показать фильтры"

    if show_hide_filters:
        show_hide_text = "Скрыть фильтры"

    if genre_ids:
        books = books.filter(genres__id__in=genre_ids)

    if author_id:
        books = books.filter(author_id=author_id)

    if age_limit_id:
        books = books.filter(age_limit=age_limit_id)

    if query:
        books = books.filter(Q(title__iregex=query) | Q(ISBN__iregex=query) | Q(author__fullname__iregex=query))

    if century_publication:
        if century_publication == '21 век':
            books = books.filter(year__gt=1999)
        elif century_publication == '20 век':
            books = books.filter(year__gt=1899, year__lt=2000)
        elif century_publication == '19 век':
            books = books.filter(year__gt=1799, year__lt=1900)
        else:
            books = books.filter(year__lt=1800)

    if max_price_value:
        books = books.filter(price__lte=int(max_price_value))

    if min_price_value:
        books = books.filter(price__gte=int(min_price_value))

    if sort_order == 'low_to_high':
        books = books.order_by('price')
    elif sort_order == 'high_to_low':
        books = books.order_by('-price')

    total_count = len(books)

    if 11 <= total_count % 100 <= 19:
        total_count_word = 'товаров'
    else:
        last_digit = total_count % 10
        if last_digit == 1:
            total_count_word = 'товар'
        elif 2 <= last_digit <= 4:
            total_count_word = 'товара'
        else:
            total_count_word = 'товаров'

    max_price = Book.objects.aggregate(Max('price'))['price__max']
    min_price = Book.objects.aggregate(Min('price'))['price__min']

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    context = {
        'page': page,
        'total_count': total_count,
        'query': query,
        'view_type': view_type,
        'sort_order': sort_order, 
        'is_catalog': is_catalog,
        'authors': authors,
        'genres': genres,
        'age_limits': age_limits,
        'author_id': author_id,
        'genre_ids': genre_ids,
        'age_limit_id': age_limit_id,
        'century_publications': century_publications,
        'century_publication': century_publication,
        'max_price': max_price,
        'min_price': min_price,
        'min_price_value': min_price_value,
        'max_price_value': max_price_value,
        'wishlist_books': wishlist_books,
        'cart_books': cart_books,
        'total_count_word': total_count_word,
        'show_hide_filters': show_hide_filters,
        'show_hide_text': show_hide_text
    }

    return render(request, 'bookshop/catalog.html', context)


@require_GET
def book_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    wishlist, cart = get_wishlist_and_cart(session_id, user)
    book = get_object_or_404(Book, pk=book_id)
    
    wishlist_item = None
    cart_item = None

    if wishlist:
        wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, book=book).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, book=book).first()

    return render(request, 'bookshop/product.html', {'book': book, 'wishlist_item': wishlist_item, 'cart_item': cart_item})


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

    wishlist, cart = get_wishlist_and_cart(session_id, user)

    wishlist_books = []

    if wishlist:
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        wishlist_books = [item.book.id for item in wishlist_items]

    cart_items = CartItem.objects.filter(cart=cart).order_by('id')
    count_items = len(cart_items)
    
    return render(request, 'bookshop/cart.html', {'cart_items': cart_items, 'count_items': count_items, 'wishlist_books': wishlist_books})


def cart_post_view(request):
    user = get_session_and_user(request)[1]
    if user is None:
        return JsonResponse({'message': 'Для оформления заказа необходимо войти в свой профиль!'})

    data = json.loads(request.body)
    fullname = data.get('fullName')
    email = data.get('email')
    mail_index = data.get('mailIndex')
    
    if not is_email(email):
        return JsonResponse({'message': 'Электронная почта введёна неверно!'}) 

    session_id, user = get_session_and_user(request)

    if user:
        order = Order.objects.create(user=user, fullname=fullname, email=email, mail_index=mail_index)
    else:
        order = Order.objects.create(session_id=session_id, fullname=fullname, email=email, mail_index=mail_index)

    cart = get_wishlist_and_cart(session_id, user)[1]

    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
        item.book.count -= item.quantity
        item.book.save()

    cart.delete()

    return JsonResponse({'message': 'Заказ успешно создан! В ближайшее время с вами свяжутся по электронной почте!'})


@require_POST
def add_to_cart_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)        

    if user:
        cart = Cart.objects.get_or_create(user=user)[0]
    else:
        cart = Cart.objects.get_or_create(session_id=session_id)[0]

    CartItem.objects.create(cart=cart, book=book, quantity=1)
    cart.save()

    return JsonResponse({'message': 'Товар добавлен в корзину'})


@require_http_methods(["PUT"])
def update_cart_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    data = json.loads(request.body)
    book = get_object_or_404(Book, pk=book_id)
    action = data.get('action')

    cart = get_wishlist_and_cart(session_id, user)[1]

    cart_item = CartItem.objects.filter(cart=cart, book_id=book).first()

    if action == 'addQuantity':
        if cart_item.quantity < cart_item.book.count:
            cart_item.quantity += 1
            cart_item.save()
            cart.save()

        return JsonResponse({'message': 'Количество товара увеличено'})

    elif action == 'reduceQuantity':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            cart.save()

        return JsonResponse({'message': 'Количество товара уменьшено'})
    
    else:
        return JsonResponse({'message': 'Некорректное действие'}, status=400)
    
    
@require_http_methods(["DELETE"])
def delete_cartitem_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)
    cart = get_wishlist_and_cart(session_id, user)[1]

    cart_item = CartItem.objects.filter(cart=cart, book_id=book).first()

    cart_item.delete()
    cart.save()
    if not CartItem.objects.filter(cart=cart):
        cart.delete()

    return JsonResponse({'message': 'Товар удалён из корзины'})


@require_GET
def wishlist_view(request):
    create_session(request)

    session_id, user = get_session_and_user(request)
                
    view_type = request.GET.get('view', '') 
    sort_order = request.GET.get('sort', '')

    cart_books = []

    wishlist, cart = get_wishlist_and_cart(session_id, user)

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        cart_books = [item.book.id for item in cart_items]

    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist).order_by('id')

    if sort_order == 'low_to_high':
        wishlist_items = wishlist_items.order_by('book__price')
    elif sort_order == 'high_to_low':
        wishlist_items = wishlist_items.order_by('-book__price')

    return render(request, 'bookshop/wishlist.html', {'view_type':view_type, 'sort_order':sort_order, 'wishlist_items': wishlist_items, 'cart_books': cart_books})
    

@require_POST
def add_to_wishlist_view(request, book_id):
    create_session(request)

    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)

    if user:
        wishlist = Wishlist.objects.get_or_create(user=user)[0]
    else:
        wishlist = Wishlist.objects.get_or_create(session_id=session_id)[0]

    WishlistItem.objects.create(wishlist=wishlist, book=book)
    wishlist.save()
    return JsonResponse({'message': 'Товар добавлен в избранное'})


@require_http_methods(["DELETE"])
def delete_wishlistitem_view(request, book_id):

    session_id, user = get_session_and_user(request)
    book = get_object_or_404(Book, pk=book_id)

    wishlist = get_wishlist_and_cart(session_id, user)[0]

    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, book_id=book.id).first()

    wishlist_item.delete()
    wishlist.save()
    if not WishlistItem.objects.filter(wishlist=wishlist):
        wishlist.delete()

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

    session_id = get_session_and_user(request)[0]

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        user_wishlist = Wishlist.objects.filter(user=user).first()
        if user_wishlist is None:
            session_wishlist = Wishlist.objects.filter(session_id=session_id).first()
            if session_wishlist:
                session_wishlist.user = user
                session_wishlist.session_id = None
                session_wishlist.save()
        else:
            if Wishlist.objects.filter(session_id=session_id).first() is not None:
                Wishlist.objects.filter(session_id=session_id).first().delete()

        user_cart = Cart.objects.filter(user=user).first()
        if user_cart is None:
            session_cart = Cart.objects.filter(session_id=session_id).first()
            if session_cart:
                session_cart.user = user
                session_cart.session_id = None
                session_cart.save()
        else:
            if Cart.objects.filter(session_id=session_id).first() is not None:
                Cart.objects.filter(session_id=session_id).first().delete()

        login(request, user)

        return JsonResponse({'message': 'ok'})
    else:
        return JsonResponse({'message': 'invalid'})


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
    user = get_session_and_user(request)[1]
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


def get_wishlist_and_cart(session_id, user):
    if user:
        wishlist = Wishlist.objects.filter(user=user).first()
        cart = Cart.objects.filter(user=user).first()
    else:
        wishlist = Wishlist.objects.filter(session_id=session_id).first()
        cart = Cart.objects.filter(session_id=session_id).first()

    return wishlist, cart


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