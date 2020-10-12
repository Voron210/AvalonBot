import random

import telebot
from telebot import types

bot = telebot.TeleBot('1285966353:AAEIQ7RYIqx9rcV0Fm6om5RZeRSKy70Xpgc')

def generate_markup():
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Создаем лист (массив) и записываем в него все элементы
    list_items = ["1", "2", "3"]
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup

@bot.message_handler(commands=['game'])
def game(message):
    # Формируем разметку
    markup = generate_markup()
    bot.send_message(message.chat.id, 'Угадай число от 1 до 3', reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = str(random.randint(1, 3))
        # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз! Ответ: ' + answer,
                             reply_markup=keyboard_hider)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Отзыв о настольной версии игры", url="https://www.nastolki-na-polke.ru/obzory/resistance-avalon/")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Можешь пока глянуть вот это", reply_markup=keyboard)
    elif message.text == "/hello":
        bot.send_message(message.chat.id, "Привет. Тут пока идёт стройка. Возвращайся позже!")
    else:
        bot.send_message(message.chat.id, "спам")

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)