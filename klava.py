from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def oplata(urls, id):
    klava = InlineKeyboardMarkup()
    klava.add((InlineKeyboardButton('Оплатить', url=urls)))
    klava.add((InlineKeyboardButton('Проверить оплату', callback_data=id)))
    return klava