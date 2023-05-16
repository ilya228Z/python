import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Укажите ваш токен
TOKEN = "YOUR_TOKEN_HERE"

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

# Создаем экземпляр диспетчера
dp = Dispatcher(bot)

# Настраиваем журналирование (не обязательно)
logging.basicConfig(level=logging.INFO)

# Счетчики побед пользователя и бота
user_score = 0
bot_score = 0


# Функция для выбора случайного действия
def generate_action():
    actions = ["Камень", "Ножницы", "Бумага", "Ящерица", "Спок"]
    return random.choice(actions)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_game(message: Message):
    # Создаем кнопки для выбора действий
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Камень")
    button2 = KeyboardButton("Ножницы")
    button3 = KeyboardButton("Бумага")
    button4 = KeyboardButton("Ящерица")
    button5 = KeyboardButton("Спок")
    keyboard.add(button1, button2, button3, button4, button5)

    # Отправляем сообщение с кнопками
    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработчик текстовых сообщений с действиями
@dp.message_handler(content_types=['text'])
async def process_action(message: Message):
    global user_score
    global bot_score

    user_action = message.text
    bot_action = generate_action()

    # Вычисляем результат игры
    winner = None
    if user_action == bot_action:
        result = "Ничья"
    elif user_action == "Камень" and bot_action in ["Ножницы", "Ящерица"] \
            or user_action == "Ножницы" and bot_action in ["Бумага", "Ящерица"] \
            or user_action == "Бумага" and bot_action in ["Камень", "Спок"] \
            or user_action == "Ящерица" and bot_action in ["Бумага", "Спок"] \
            or user_action == "Спок" and bot_action in ["Камень", "Ножницы"]:
        result = "Вы выиграли!"
        winner = "user"
    else:
        result = "Вы проиграли :("
        winner = "bot"

    # Обновляем счетчик побед
    if winner == "user":
        user_score += 1
    elif winner == "bot":
        bot_score += 1

    # Отправляем сообщение с результатом и действиями игроков
    result_message = f"Ваше действие: {user_action}\nДействие бота: {bot_action}\n\n{result}"
    await message.answer(result_message)

    # Обновляем статистику игры
    stats_button = KeyboardButton("Статистика")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(stats_button)
    if winner == "user":
        user_data = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if not user_data.is_bot:
            await message.answer(f"Поздравляем, {message.from_user.first_name}! Вы выиграли!", reply_markup=keyboard)
    elif winner == "bot":
        await message.answer("Прости, но бот победил. Попробуй еще раз!", reply_markup=keyboard)


# Обработчик команды "Статистика"
@dp.message_handler(func=lambda message: message.text 