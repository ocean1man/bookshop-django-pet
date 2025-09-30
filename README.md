# 📚 Интернет-магазин литературы на Django

Когда-то это была моя ВКР для колледжа… Теперь я решил её выложить в открытый доступ, немного доработать и добавить развёртывание через docker-compose. Также я не стал скрывать файл .env, чтобы не усложнять вам развёртывание, так как приложение в данный момент локальное.

### 1️⃣ Развёртывание через docker-compose

1. Склонируйте репозиторий и перейдите в каталог проекта:  

   ```bash
   git clone https://github.com/ocean1man/bookshop-django-pet.git
   cd bookshop-django-pet
   ```

2. Соберите и запустите образы при помощи docker-compose:  

   ```bash
   docker-compose up -d
   ```

3. Перейдите в браузер по адресу: [http://localhost:8000](http://localhost:8000)

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

4. Создайте базу данных в локальном экземпляре PostgreSQL и при необходимости отредактируйте файл .env

5. Примените миграции и загрузите тестовые данные:  

   ```bash
   python manage.py migrate
   python manage.py import_data
   ```

6. Запустите сервер разработки:  

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. Перейдите в браузер по адресу: [http://localhost:8000](http://localhost:8000)