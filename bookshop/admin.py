from django.contrib import admin
from .models import Author, Genre, Book, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, AgeLimit
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'book_price', 'quantity', 'total_price']

    def book_price(self, obj):
        return obj.book.price

    def total_price(self, obj):
        return obj.book.price * obj.quantity
    
    book_price.short_description = 'Цена за штуку'
    total_price.short_description = 'Сумма'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['book', 'book_price', 'quantity', 'total_price']

    def book_price(self, obj):
        return obj.book.price

    def total_price(self, obj):
        return obj.book.price * obj.quantity
    
    book_price.short_description = 'Цена за штуку'
    total_price.short_description = 'Сумма'


class WishListItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ['book']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_filter = ['status', 'user']
    search_fields = ['id']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['Отменён', 'Получен']:
            return [field.name for field in self.model._meta.fields] 
        return super().get_readonly_fields(request, obj)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_filter = ['user', 'session_id']


@admin.register(Wishlist)
class WishListAdmin(admin.ModelAdmin):
    inlines = [WishListItemInline]
    list_filter = ['user', 'session_id']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['fullname']


@admin.register(Genre)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(AgeLimit)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(Book)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['title']
    filter_horizontal = ['genres']