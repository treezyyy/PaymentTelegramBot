import aiogram
import klava
from aiogram import Bot, Dispatcher, types,executor
import re

import tokeni
import oplat
import client

#инициализ бота
bot = Bot(tokeni.Token)
dp = Dispatcher(bot)

slovar = {}


@dp.message_handler(commands=['info'])
async def coins(message: types.Message):
    await message.answer('для пополнения счета введите команду /pay в формате: "/pay сумма_к_пополению почта_от_аккаунта"')


@dp.message_handler(regexp=r"^\/pay\s+\d+(\.\d{1,2})?\s+\S+@\S+\.\S+")
async def pay(message: types.Message):
    value = message.text.split()[1]
   # print(value)
   # print(value.isdigit())
    loggin = message.text.split()[2]
    slovar[message.chat.username] = loggin
    await message.answer('Ваш логин в приложении: ' + loggin)
    if value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit()):
        silka, payment = oplat.create_oplata(value)
        await message.answer('Вот ссылка', reply_markup=klava.oplata(silka, payment.id))
    else:
        await message.answer('Попробуйте еще раз')


@dp.message_handler()
async def invalid_pay(message: types.Message):
    # Обработчик для команд, которые не соответствуют регулярному выражению
    await bot.send_message(chat_id=message.chat.id, text='Некорректная команда. Пожалуйста, введите команду /pay с правильным форматом. \n Узнать формат: /info')


@dp.callback_query_handler()
async def proverka(call: types.CallbackQuery):
    if call.message['text'] == 'Вот ссылка':
        otvet, value = oplat.oplata_check(call.data)
        print(call.message.chat.username)
        print(slovar[call.message.chat.username])
        if otvet:
            await bot.send_message(chat_id=call.from_user.id, text='платеж прошел успешно')
            user_data = {
                'email': slovar[call.message.chat.username],
                'balance': float(value)
            }
            client.update_balance(user_data)
        else:
            await bot.send_message(chat_id=call.from_user.id, text='платеж не прошел')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)