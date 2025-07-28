from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Author(models.Model):
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'Авторы'


class AgeLimit(models.Model):
    value = models.CharField(max_length=3, unique=True, verbose_name='Возрастной рейтинг')

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = 'возрастной рейтинг'
        verbose_name_plural = 'Возрастной рейтинг'


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    year = models.IntegerField(null=True, blank=True, verbose_name='Год публикации')
    ISBN = models.CharField(max_length=50, null=True, blank=True)
    age_limit = models.ForeignKey(AgeLimit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Возрастной рейтинг')
    price = models.IntegerField(verbose_name='Цена')
    count = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    img_path = models.CharField(max_length=255, null=True, blank=True, verbose_name='Путь к изображению')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сессия')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Пользователь {self.user.username}' if self.user else f'Сессия {self.session_id}'
    
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return ''
    
    class Meta:
        verbose_name = 'товар корзины'
        verbose_name_plural = 'Товары корзины'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сессия')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Пользователь {self.user.username}' if self.user else f'Сессия {self.session_id}'
    
    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return ''
    
    class Meta:
        verbose_name = 'избранный товар'
        verbose_name_plural = 'Избранные товары'

 
class Order(models.Model):
    STATUSES = [
        ('В обработке', 'В обработке'),
        ('Отправлен', 'Отправлен'),
        ('Готов к получению', 'Готов к получению'),
        ('Получен', 'Получен'),
        ('Отменён', 'Отменён')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сессия')
    fullname = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.CharField(max_length=255, verbose_name='Электронная почта')
    mail_index = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    status = models.CharField(max_length=17, choices=STATUSES, default='В обработке', verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status}, заказ №{self.id}, пользователь {self.user.username}' if self.user else f'{self.status}, заказ №{self.id}, сессия {self.session_id}'
    
    def save(self, *args, **kwargs):
        if self.status == 'Отменён':
            for item in self.orderitem_set.all():
                item.book.count += item.quantity
                item.book.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return ''
    
    class Meta:
        verbose_name = 'товар заказа'
        verbose_name_plural = 'Товары заказ'