#!venv/bin/python
import logging
import config
import random
import asyncio
import randomizer as rz
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply("Просто старт, команды есть в предложке (Menu)\n\n"
                        "На текущий момент бот работает с данным кошельком на транкзакции за всё время:\n\n"
                        "💳0x3FD025ac173954778251699dacB2Ca126932841F💳\n\n"
                        "Позже будет возможен выбор нужного вам кошелька и даты")


@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    num1 = await message.answer_dice()
    num2 = await message.answer_dice()
    await asyncio.sleep(5)
    if num1.dice.value + num2.dice.value <= 9:
        await message.answer(f'Первое число {(num1.dice.value + num2.dice.value)}')
    else:
        await message.answer('Сумма больше 9-ти, переброс кубика')


@dp.message_handler(commands="users")
async def cmd_users(message: types.Message):
    await rz.get_transactions()
    await message.answer(f'На текущий момент в конкурсе участвует {rz.users} человек')


@dp.message_handler(commands="last")
async def cmd_last(message: types.Message):
    await rz.get_transactions()
    text = ''
    user = rz.scans[-1]
    text += 'Последний пользователь🔚\n\n'
    text += f'Адрес пользователя:\n\n💳{user[0]}💳 \n\n'
    text += f'Сумма платежа: {user[1]}$ \n'
    text += f'Дата платежа: {user[3]} \n'
    await message.answer(text)


@dp.message_handler(commands="check")  # Сделать поиск информации по кошельку
async def cmd_check(message: types.Message):
    if message.get_args():
        await rz.get_transactions()
        text = ''
        found = False
        for i in rz.scans:
            if message.get_args().lower() in i:
                text += f'Адрес пользователя:\n\n💳{i[0]}💳 \n\n'
                text += f'Сумма платежа: {i[1]}$ \n'
                text += f'Дата платежа: {i[3]} \n'
                found = True
                await message.answer(text)
        if not found:
            await message.answer('Такой кошелёк не найден')


@dp.message_handler(commands="users_list")
async def cmd_users_list(message: types.Message):
    await rz.get_transactions()
    text = ''
    await message.answer('Подготовка файла...')
    for i in rz.scans:
        if i[0] not in text:
            text += i[0] + '\n'
    with open("users.txt", "w") as f:
        f.write(text)

    await message.answer_document(open('users.txt', 'rb'))

    await message.answer('Файл собран')


# @dp.message_handler(commands="random")
# async def cmd_random(message: types.Message):
#     if message.get_args():
#         await message.answer(message.get_args())
#     else:
#         await rz.get_transactions()
#         text = ''
#         user = rz.scans[random.randint(0, rz.users)]
#         text += '🥇Победитель🥇\n\n'
#         text += f'Адрес пользователя:\n\n💳{user[0]}💳 \n\n'
#         text += f'Сумма платежа: {user[1]}$ \n'
#         text += f'Дата платежа: {user[3]} \n'
#         await message.answer(text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
