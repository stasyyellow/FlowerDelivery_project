from datetime import datetime
import telebot
from django.contrib.auth import get_user_model
from telebot import types

from config import BOT_TOKEN, TG_ID
from orders.models import Order
from catalog.models import Product

User = get_user_model()

TOKEN = BOT_TOKEN
ADMIN_CHAT_ID = TG_ID

WORKING_HOURS = (9, 24)
bot = telebot.TeleBot(TOKEN)

# Структура user_state[user_id] = { 'user': User или None, 'step': ..., и прочие данные заказа }
user_state = {}

def is_working_hours():
    now = datetime.now()
    return WORKING_HOURS[0] <= now.hour < WORKING_HOURS[1]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in user_state:
        del user_state[user_id]
    bot.reply_to(message, "Добро пожаловать в 🌸 Flower Delivery!\n"
                          "Чтобы оформить заказ, используйте команду /order.\n"
                          "Для помощи используйте /help.")

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    user_state[user_id] = 'help'
    bot.reply_to(message, "Похоже у вас возникла проблема, напишите боту с описанием проблемы, и мы отправим это админу.\n"
                          "Если проблемы нет, нажмите /start.")

@bot.message_handler(commands=['order'])
def take_order(message):
    user_id = message.from_user.id
    if user_id in user_state and user_state[user_id] == 'help':
        del user_state[user_id]

    if not is_working_hours():
        bot.reply_to(message, "❌ Заказы принимаются только с 9:00 до 20:00.")
        return

    # Проверим, знаем ли мы уже пользователя?
    if user_id not in user_state or not isinstance(user_state[user_id], dict) or 'user' not in user_state[user_id]:
        user_state[user_id] = {'step': 'ask_email'}
        bot.reply_to(message, "Для оформления заказа введите ваш email, под которым вы зарегистрированы на сайте:")
    else:
        # Пользователь известен, сразу переходим к выбору букета
        msg = bot.reply_to(message, "🌹 Введите название букета:")
        user_state[user_id]['step'] = 'bouquet_name'
        bot.register_next_step_handler(msg, process_bouquet_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def fallback_handler(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Если пользователь в состоянии 'help'
    if user_id in user_state and user_state[user_id] == 'help':
        # Отправляем проблему админу
        bot.send_message(ADMIN_CHAT_ID, f"❗ *Проблема от пользователя {user_id}*\n\n{text}", parse_mode="Markdown")
        bot.reply_to(message, "✅ Мы получили ваше сообщение и скоро разберёмся с проблемой!")
        del user_state[user_id]
        return

    # Если пользователь в процессе заказа
    if user_id in user_state and isinstance(user_state[user_id], dict):
        state = user_state[user_id]
        step = state.get('step')

        if step == 'ask_email':
            # Пользователь ввёл email, проверим есть ли такой
            email = text
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                bot.reply_to(message, "Пользователь с таким email не найден.\nПроверьте, что вы зарегистрированы на сайте и перезапустите бота командой /start")
                # Сбросим состояние
                del user_state[user_id]
            else:
                state['user'] = user
                # Переходим к выбору букета
                bot.reply_to(message, "🌹 Введите название букета:")
                state['step'] = 'bouquet_name'

        elif step == 'bouquet_name':
            bouquet_name = text
            product = Product.objects.filter(name__iexact=bouquet_name).first()
            if not product:
                bot.reply_to(message, "В базе данных не нашлось такого букета, проверьте каталог.\nВведите название букета снова:")
                return
            state['bouquet_name'] = bouquet_name
            # Запрашиваем адрес доставки
            bot.reply_to(message, "📍 Введите адрес доставки:")
            state['step'] = 'delivery_address'

        elif step == 'delivery_address':
            state['delivery_address'] = text
            # Спрашиваем про открытку
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Да', 'Нет')
            bot.reply_to(message, "Добавить открытку?", reply_markup=markup)
            state['step'] = 'add_card_question'

        elif step == 'add_card_question':
            if text.lower() == 'да':
                state['add_card'] = True
                bot.reply_to(message, "Введите текст для открытки:", reply_markup=types.ReplyKeyboardRemove())
                state['step'] = 'card_text'
            else:
                state['add_card'] = False
                state['card_text'] = ""
                # Открытка не нужна, сразу создаем заказ
                create_order_and_finish(message, state)

        elif step == 'card_text':
            state['card_text'] = text
            # После текста открытки сразу создаем заказ
            create_order_and_finish(message, state)

        else:
            # Шаг не определён, fallback
            bot.reply_to(message, "Извините, я не понял сообщение.\nДоступные команды:\n"
                                  "/start - начать\n"
                                  "/help - помощь\n"
                                  "/order - оформить заказ")
    else:
        # Пользователь не в процессе help или order
        bot.reply_to(message, "Извините, я не понял сообщение.\nДоступные команды:\n"
                              "/start - начать\n"
                              "/help - помощь\n"
                              "/order - оформить заказ")

def create_order_and_finish(message, state):
    user = state['user']
    # Создаём заказ из телеграма, указываем source='telegram'
    order = Order.objects.create(
        user=user,
        delivery_address=state['delivery_address'],
        add_card=state.get('add_card', False),
        card_text=state.get('card_text', ''),
        source='telegram'  # Устанавливаем источник заказа как "telegram"
    )

    order_text = (f"📩 *Сообщение админу*\n\n"
                  f"👤 *Пользователь*: {user.username} ({user.email})\n"
                  f"🌹 *Букет*: {state['bouquet_name']}\n"
                  f"📍 *Адрес*: {state['delivery_address']}\n"
                  f"Открытка: {'Да' if order.add_card else 'Нет'}\n"
                  f"Текст открытки: {order.card_text or 'Без открытки'}\n"
                  f"🕒 *Время*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    bot.send_message(ADMIN_CHAT_ID, order_text, parse_mode="Markdown")
    bot.reply_to(message, "✅ Ваш заказ успешно оформлен! Спасибо за ваш выбор! 🌸")

    user_id = message.from_user.id
    if user_id in user_state:
        del user_state[user_id]

def start_bot():
    print("Бот запущен и готов к работе...")
    bot.polling()


# Если вы захотите запустить скрипт напрямую (без manage.py),
# можно оставить строку:
# if __name__ == "__main__":
#     start_bot()
#
# Но если бот запускается только через manage.py runbot,
# можно это убрать или оставить по желанию.