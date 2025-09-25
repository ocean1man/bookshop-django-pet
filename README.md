# 📚 Интернет-магазин литературы на Django

Когда-то это была моя ВКР для колледжа… Теперь я решил её выложить в открытый доступ, немного доработать и добавить развёртывание через Docker. Также я не стал прятать django secret key и заранее создал суперпользователя, чтобы не усложнять вам развёртывание, так как приложение в данный момент локальное.

Основные особенности:
- настоящий MVC, во views и models нет работы с базой данных и бизнес-логики;  
- фильтрация и сортировка списка товаров;  
- добавление товаров в избранное и корзину;  
- личный профиль с историей заказов;
- динамическое обновление страниц с помощью Fetch API;
- адаптивная вёрстка.

---

### 1️⃣ Развёртывание через Docker

1. Склонируйте репозиторий и перейдите в каталог проекта:  

   ```bash
   git clone https://github.com/ocean1man/bookshop-django-pet.git
   cd bookshop-django-pet
   ```

2. Соберите Docker-образ:  

   ```bash
   docker build -t bookshop-django-pet .
   ```

3. Запустите контейнер:  

   ```bash
   docker run -p 8000:8000 bookshop-django-pet
   ```

4. Перейдите в браузере по адресу: [http://localhost:8000](http://localhost:8000)

---

### 2️⃣ Развёртывание через Python

📦 Требования: Python 3.10 и выше.

1. Склонируйте репозиторий и перейдите в каталог проекта:  

   ```bash
   git clone https://github.com/ocean1man/bookshop-django-pet.git
   cd bookshop-django-pet
   ```

2. Создайте и активируйте виртуальное окружение:  

   ```bash
   python -m venv .venv
   # Для Linux/MacOS
   source .venv/bin/activate
   # Для Windows
   .venv\Scripts\activate
   ```

3. Установите зависимости:  

   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции и загрузите тестовые данные:  

   ```bash
   python manage.py migrate
   python manage.py import_data
   ```

5. Запустите сервер разработки:  

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

6. Перейдите в браузере по адресу: [http://localhost:8000](http://localhost:8000)

---

### Логин и пароль суперпользователя

Логин: sadkfja2r2d8237sasjkhf3

Пароль: d?UQas2Y3'Y{;sx#%kF6x.\rJht[m#