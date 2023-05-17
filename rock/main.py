import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot('5764483920:AAFWIoSRFWlO35hgelVkMUJJnVhh6cTrdWM')
dp = Dispatcher(bot)

stats = {'wins': 0, 'losses': 0, 'draws': 0, 'gaming': 0}


async def start_game(message: types.Message):
    await message.answer('Привет!\nДавай поиграем в "Камень, ножницы, бумага"?\nНажми на нужную кнопку ниже и посмотрим, кто победит!')

    btns_text = ['Камень', 'Ножницы', 'Бумага', 'Спок', 'Ящерица']
    btns = [types.KeyboardButton(text) for text in btns_text]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*btns)

    await message.answer('Твой выбор:', reply_markup=markup)


async def repeat_game(message: types.Message):
    btns_text = ['Камень', 'Ножницы', 'Бумага', 'Спок', 'Ящерица']
    btns = [types.KeyboardButton(text) for text in btns_text]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*btns)

    await message.answer('Новый раунд!\nТвой выбор:', reply_markup=markup)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await start_game(message)


@dp.message_handler(lambda message: message.text.lower() == 'играть еще раз')
async def play_again(message: types.Message):
    await start_game(message)


@dp.message_handler(lambda message: message.text.lower() in ['камень', 'ножницы', 'бумага', 'спок', 'ящерица'])
async def process_choice(message: types.Message):
    user_choice = message.text.lower()

    # Выбор компьютера
    computer_choices = ['камень', 'ножницы', 'бумага', 'cпок', 'ящерица']
    computer_choice = random.choice(computer_choices)

    # Определение победителя
    if user_choice == computer_choice:
        result = 'Ничья!'
        stats['draws'] += 1
    elif user_choice == 'камень' and (computer_choice == 'ножницы' or computer_choice == 'ящерица') or \
            user_choice == 'ножницы' and (computer_choice == 'бумага' or computer_choice == 'ящерица') or \
            user_choice == 'бумага' and (computer_choice == 'камень' or computer_choice == 'cпок') or \
            user_choice == 'спок' and (computer_choice == 'камень' or computer_choice == 'ножницы') or \
            user_choice == 'ящерица' and (computer_choice == 'бумага' or computer_choice == 'cпок'):
        result = 'Победа!'
        stats['wins'] += 1
    else:
        result = 'Поражение!'
        stats['losses'] += 1
    stats["gaming"] += 1
    # Вывод результатов
    await message.answer(f'Ты выбрал: {user_choice.capitalize()}.\n'
                         f'Компьютер выбрал: {computer_choice.capitalize()}.\n'
                         f'Результат: {result}\n\n'
                         f'Статистика:\n'
                         f'Побед: {stats["wins"]}\n'
                         f'Поражений: {stats["losses"]}\n'
                         f'Ничьих: {stats["draws"]}\n'
                         f'Игр сыграно: {stats["gaming"]}')

    # Предложение поиграть снова
    btns_text = ['Играть ещё раз']
    btns = [types.KeyboardButton(text) for text in btns_text]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*btns)

    await repeat_game(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
