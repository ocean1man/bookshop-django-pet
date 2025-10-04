from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from bookshop.models import AgeLimit, Author, Book, CartItem, Genre, WishlistItem
from bookshop.services.session_store import get_wishlist_and_cart
from django.db.models import Q, Max, Min
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache

CACHE_TIMEOUT = 60 * 5
CACHE_VERSION = 1

@dataclass(frozen=True)
class CatalogFilters:
    query: str = ""
    view_type: str = ""
    sort_order: str = ""
    author_id: Optional[int] = None
    genre_ids: List[int] = None
    age_limit_id: Optional[int] = None
    century_publication: str = ""
    min_price_value: Optional[int] = None
    max_price_value: Optional[int] = None
    show_hide_filters: bool = False
    page_number: Optional[str] = None

def _russian_goods_word(n: int) -> str:
    if 11 <= n % 100 <= 19:
        return 'товаров'
    last = n % 10
    if last == 1:
        return 'товар'
    if 2 <= last <= 4:
        return 'товара'
    return 'товаров'

def get_books_cached(book_ids: List[int]) -> List[Book]:
    if not book_ids:
        return []

    keys = {book_id: f"book:{book_id}" for book_id in book_ids}

    cached_data: Dict[str, Book] = cache.get_many(keys.values())

    cached_books: Dict[int, Book] = {}
    for book_id, key in keys.items():
        if key in cached_data:
            cached_books[book_id] = cached_data[key]

    missing_ids = [bid for bid in book_ids if bid not in cached_books]

    if missing_ids:
        fresh_books = (
            Book.objects
            .filter(id__in=missing_ids)
            .select_related("author", "age_limit")
            .prefetch_related("genres")
        )

        cache.set_many(
            {f"book:{b.id}": b for b in fresh_books},
            timeout=CACHE_TIMEOUT,
            version=CACHE_VERSION
        )

        for b in fresh_books:
            cached_books[b.id] = b

    return [cached_books[bid] for bid in book_ids if bid in cached_books]

def build_catalog_context(session_id, user, *, filters: CatalogFilters, page_size: int = 12) -> Dict[str, Any]:
    wishlist_books: List[int] = []
    cart_books: List[int] = []

    wishlist, cart = get_wishlist_and_cart(session_id=session_id, user=user)

    if wishlist:
        wishlist_books = list(
            WishlistItem.objects.filter(wishlist=wishlist)
                                .values_list("book_id", flat=True)
        )
    if cart:
        cart_books = list(
            CartItem.objects.filter(cart=cart)
                            .values_list("book_id", flat=True)
        )

    books = Book.objects.all().values_list("id", flat=True)

    if filters.genre_ids:
        books = books.filter(genres__id__in=filters.genre_ids)

    if filters.author_id:
        books = books.filter(author_id=filters.author_id)

    if filters.age_limit_id:
        books = books.filter(age_limit=filters.age_limit_id)

    if filters.query:
        q = filters.query
        books = books.filter(
            Q(title__iregex=q) | Q(ISBN__iregex=q) | Q(author__fullname__iregex=q)
        )

    if filters.century_publication:
        cp = filters.century_publication
        if cp == '21 век':
            books = books.filter(year__gt=1999)
        elif cp == '20 век':
            books = books.filter(year__gt=1899, year__lt=2000)
        elif cp == '19 век':
            books = books.filter(year__gt=1799, year__lt=1900)
        else:
            books = books.filter(year__lt=1800)

    if filters.max_price_value is not None:
        books = books.filter(price__lte=int(filters.max_price_value))

    if filters.min_price_value is not None:
        books = books.filter(price__gte=int(filters.min_price_value))

    sort = filters.sort_order if filters.sort_order in {"", "low_to_high", "high_to_low"} else ""
    if sort == "low_to_high":
        books = books.order_by("price")
    elif sort == "high_to_low":
        books = books.order_by("-price")

    total_count = books.count()
    total_count_word = _russian_goods_word(total_count)

    max_price = Book.objects.aggregate(Max('price'))['price__max']
    min_price = Book.objects.aggregate(Min('price'))['price__min']

    paginator = Paginator(books, page_size)
    try:
        page = paginator.get_page(filters.page_number)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    show_hide_text = "Скрыть фильтры" if filters.show_hide_filters else "Показать фильтры"

    authors = Author.objects.all()
    genres = Genre.objects.all()
    age_limits = AgeLimit.objects.all()

    ids_on_page = list(page.object_list)
    books_on_page = get_books_cached(ids_on_page)
    page.object_list = books_on_page

    return {
        "page": page,
        "total_count": total_count,
        "query": filters.query,
        "view_type": filters.view_type,
        "sort_order": sort,
        "is_catalog": True,
        "authors": authors,
        "genres": genres,
        "age_limits": age_limits,
        "author_id": filters.author_id or "",
        "genre_ids": filters.genre_ids or [],
        "age_limit_id": filters.age_limit_id or "",
        "century_publications": ['21 век', '20 век', '19 век', 'Раньше'],
        "century_publication": filters.century_publication,
        "max_price": max_price,
        "min_price": min_price,
        "min_price_value": filters.min_price_value or "",
        "max_price_value": filters.max_price_value or "",
        "wishlist_books": wishlist_books,
        "cart_books": cart_books,
        "total_count_word": total_count_word,
        "show_hide_filters": filters.show_hide_filters,
        "show_hide_text": show_hide_text,
    }