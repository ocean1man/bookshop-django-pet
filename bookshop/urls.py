from django.urls import path

from . import views

app_name = 'bookshop'

urlpatterns = [
    path('', views.main_view, name='main'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/<int:book_id>/', views.book_view, name='book'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:book_id>/', views.update_cart_view, name='update_cart'),
    path('cart/delete/<int:book_id>/', views.delete_cartitem_view, name='delete_cartitem'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('wishlist/delete/<int:book_id>/', views.delete_wishlistitem_view, name='delete_wishlistitem'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile')
]