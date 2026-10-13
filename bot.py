import telebot
from telebot import types

TOKEN = '8975614389:AAEkZidItJdbzNBkw0DKw1CLoVjxM7i4c_w'
ADMIN_ID = 1010374112

bot = telebot.TeleBot(TOKEN)
user_data = {}


def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('💼 Презентации', callback_data='price_pres'))
    markup.add(types.InlineKeyboardButton('📝 Оформление текста/отчёта', callback_data='price_text'))
    markup.add(types.InlineKeyboardButton('📋 Рефераты и доклады', callback_data='price_ref'))
    markup.add(types.InlineKeyboardButton('📐 Проекты', callback_data='price_proj'))
    markup.add(types.InlineKeyboardButton('📄 Порядок работы', callback_data='rules'))
    markup.add(types.InlineKeyboardButton('💬 Отзывы', callback_data='reviews'))
    markup.add(types.InlineKeyboardButton('📢 Подписаться на канал', url='https://t.me/presentationssale'))
    markup.add(types.InlineKeyboardButton('📩 Оставить заявку', callback_data='order'))
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Привет! Меня зовут Полина 🌸\n\n"
        "Я создаю красивые и качественные презентации, рефераты и доклады.\n"
        "Помогаю студентам и не только.\n\n"
        "Выберите, что вас интересует:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "Выберите услугу в меню /start", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data == 'price_pres')
def price_pres(call):
    text = (
        "💼 ПРЕЗЕНТАЦИИ\n\n"
        "❀ 1 стандартный слайд (текст, картинки, фото) — 110 руб.\n"
        "❀ Простой слайд (заголовок без дизайна) — 100 руб.\n\n"
        "❀ Доплата за срочность:\n"
        "   за 24 часа + 450 руб.\n"
        "   за 48 часов + 350 руб.\n\n"
        "❀ Создание уникального шаблона — от 450 руб.\n"
        "❀ Анимации (все) — +400 руб.\n\n"
        "Правки из-за вашей ошибки — доплата.\n\n"
        "Полная предоплата без возврата."
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'price_text')
def price_text(call):
    text = (
        "📝 ОФОРМЛЕНИЕ ТЕКСТА / ОТЧЁТА\n\n"
        "❀ Оформление текста: 1 страница — 300 руб.\n"
        "❀ Оформление отчёта — индивидуальная консультация: @ppyll1"
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'price_ref')
def price_ref(call):
    text = (
        "📋 РЕФЕРАТЫ И ДОКЛАДЫ\n\n"
        "❀ 1 страница — 160 руб.\n\n"
        "Для точной стоимости напишите @ppyll1"
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'price_proj')
def price_proj(call):
    text = (
        "📐 ПРОЕКТЫ\n\n"
        "Грантовые и индивидуальные проекты.\n"
        "Стоимость рассчитывается индивидуально.\n\n"
        "Напишите @ppyll1 для обсуждения."
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'rules')
def rules_btn(call):
    text = (
        "📄 ПОРЯДОК РАБОТЫ\n\n"
        "Помогает избежать недопонимания и гарантирует результат.\n\n"
        "1. Обсуждение задачи\n"
        "Напишите мне, и я задам несколько вопросов, чтобы понять ваши цели.\n\n"
        "2. Референсы и стиль\n"
        "Отправьте примеры, которые вам нравятся. Если нет предпочтений — доверьтесь мне.\n\n"
        "3. Стоимость и оплата\n"
        "Рассчитаю стоимость. Требуется полная предоплата.\n"
        "Важно: возврат после начала работы невозможен.\n\n"
        "4. Согласование\n"
        "Отправлю первые слайды. На этом этапе можно принять дизайн или запросить правки.\n\n"
        "5. Получение результата\n"
        "После согласования завершу работу и отправлю итог."
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'reviews')
def reviews_btn(call):
    text = (
        "💬 ОТЗЫВЫ\n\n"
        "1. Перейдите на наш канал: https://t.me/presentationssale\n"
        "2. Нажмите на хэштег #отзывы\n"
        "3. Смотрите все отзывы"
    )
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: call.data == 'order')
def order_start(call):
    user_data[call.message.chat.id] = {}
    bot.send_message(call.message.chat.id, "Сколько нужно слайдов?")
    bot.register_next_step_handler(call.message, ask_deadline)


def ask_deadline(message):
    user_data[message.chat.id]['slides'] = message.text
    bot.send_message(message.chat.id, "Какой срок?")
    bot.register_next_step_handler(message, ask_style)


def ask_style(message):
    user_data[message.chat.id]['deadline'] = message.text
    bot.send_message(message.chat.id, "Какое оформление? (минимализм, яркое, деловое)")
    bot.register_next_step_handler(message, ask_text)


def ask_text(message):
    user_data[message.chat.id]['style'] = message.text
    bot.send_message(message.chat.id, "Есть готовый текст для презентации? (да/нет)")
    bot.register_next_step_handler(message, ask_contact)


def ask_contact(message):
    user_data[message.chat.id]['text_ready'] = message.text
    bot.send_message(message.chat.id, "Ваш контакт для связи?")
    bot.register_next_step_handler(message, finish_order)


def finish_order(message):
    d = user_data[message.chat.id]
    d['contact'] = message.text
    admin_text = (
        "🔔 НОВАЯ ЗАЯВКА!\n\n"
        "👤 От: " + str(message.from_user.first_name) + "\n"
        "🆔 ID: " + str(message.chat.id) + "\n\n"
        "📊 Слайдов: " + d.get('slides', '') + "\n"
        "⏰ Срок: " + d.get('deadline', '') + "\n"
        "🎨 Оформление: " + d.get('style', '') + "\n"
        "📄 Текст готов: " + d.get('text_ready', '') + "\n"
        "📩 Контакт: " + d.get('contact', '')
    )
    bot.send_message(ADMIN_ID, admin_text)
    bot.send_message(
        message.chat.id,
        "Спасибо за ваши ответы! 🌸\nЗаявка отправлена — я скоро свяжусь с вами."
    )
    user_data.pop(message.chat.id, None)


print("Бот запущен...")
bot.infinity_polling()
