# FlowerDelivery_project
 basic Zerocoder project

ТЗ:
Сайт с доставкой цветов и получение заказов через Telegram бота



Цель проекта:
Создание простого веб-сайта для заказа доставки цветов с базовой интеграцией заказов через Telegram бота.

Общая информация о проекте:
Проект включает разработку простого веб-сайта для заказа цветов и простого Telegram бота для приема заказов.



Область применения
Описание проблемы:
Необходимость упрощенного способа заказа цветов через интернет и мессенджер.



Пользователи системы:
Частные лица, заказывающие цветы.



Основные ограничения и допущения:
Пользователи должны иметь доступ к интернету и Telegram. Заказы принимаются только в рабочее время.



Функциональные требования
- Веб-сайт:
    - Регистрация пользователей.
    - Просмотр каталога цветов.
    - Оформление заказа.
- Telegram бот:
    - Получение заказов с информацией о букетах и доставке.



Общая архитектура системы:
- Веб-приложение на Django.
- Серверная часть на Python с использованием Django.
- Описание подсистем и модулей:
- Модуль регистрации.
- Модуль каталога товаров.
- Модуль оформления заказа.



Модель данных
- Таблица пользователей (ID, имя, email).
- Таблица товаров (ID, название, цена).
- Таблица заказов (ID, пользователь, товары).



Методы и стратегии тестирования:
- Юнит-тестирование.






(.venv) PS C:\_Python AI\github\FlowerDelivery_project\flower_delivery> python manage.py shell
Python 3.12.8 (tags/v3.12.8:2dc476b, Dec  3 2024, 19:30:04) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from users.models import CustomUser
>>> print(CustomUser.objects.count())  # Количество пользователей
2
>>> print(CustomUser.objects.all())    # Список пользователей
<QuerySet [<CustomUser: stasy_yellow (Телефон не указан)>, <CustomUser: anastasia.n (+37477444234)>]>
>>> from orders.models import Order
>>> print(Order.objects.count())  # Количество заказов
2
>>> print(Order.objects.all())    # Список заказов
<QuerySet [<Order: Заказ 1 от stasy_yellow>, <Order: Заказ 2 от anastasia.n>]>
>>> from catalog.models import Product
>>> print(Product.objects.count())  # Количество товаров
31
>>> print(Product.objects.all())    # Список товаров
<QuerySet [<Product: Летний луг>, <Product: Огненный закат>, <Product: Осенний уют>, <Product: Кремовое совершенство>, <Product: Розовый каприз>, <Product: Белосн
ежная элегантность>, <Product: Ромашковое настроение>, <Product: Лавандовая дымка>, <Product: Сдержанная гармония>, <Product: Розовый букет мечты>, <Product: Летн
яя грация>, <Product: Природная гармония>, <Product: Богатство оттенков>, <Product: Полевая магия>, <Product: Винтажная гармония>, <Product: Тропическая фантазия>, <Product: Романтика природы>, <Product: Осенний вечер>, <Product: Вдохновение>, <Product: Королевское сияние>, '...(remaining elements truncated)...']>
>>> from cart.models import Cart, CartItem
>>> print(Cart.objects.count())         # Количество корзин
2
>>> print(CartItem.objects.all())       # Все элементы корзины
<QuerySet [<CartItem: CartItem object (26)>, <CartItem: CartItem object (28)>, <CartItem: CartItem object (29)>]>
>>> from flower_delivery.models import Review
>>> print(Review.objects.count())  # Количество отзывов
1
>>> print(Review.objects.all())    # Список отзывов
<QuerySet [<Review: Отзыв от anastasia.n>]>
>>> from flower_delivery.models import Slide
>>> print(Slide.objects.count())   # Количество слайдов
5
>>> print(Slide.objects.all())     # Список слайдов
<QuerySet [<Slide: #candy_flowers>, <Slide: #эффект_дождя>, <Slide: #neon_vibes>, <Slide: #корейская_бумага>, <Slide: #композиционные_букеты>]>
>>>
