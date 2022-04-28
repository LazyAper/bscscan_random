#!venv/bin/python
import logging
import config
import asyncio
import random
import randomizer as rz
from aiogram import Bot, Dispatcher, executor, types
import emoji

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


def get_info_about_user(message):
    text = f'ID: {message.from_user.id}, Text: {message.text}'
    try:
        text += f'\nUsername: {message.from_user.username},' \
                f' Name: {message.from_user.first_name},' \
                f' Surname: {message.from_user.last_name} '
    except Exception as e:
        logging.exception(e)
        text += 'Нет имени'
    return text


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    print(get_info_about_user(message))
    await message.reply("Просто старт, команды есть в предложке (Menu)\n\n"
                        "На текущий момент бот работает с данным кошельком на транкзакции за всё время:\n\n"
                        "💳0x3FD025ac173954778251699dacB2Ca126932841F💳\n\n"
                        "Позже будет возможен выбор нужного вам кошелька и даты")


@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    print(get_info_about_user(message))
    number = ''
    summer = 10
    cnt = [1, 2, 3]
    for j in cnt:
        while summer > 9:
            num1 = await message.answer_dice()
            num2 = await message.answer_dice()
            await asyncio.sleep(5)
            if num1.dice.value + num2.dice.value <= 9:
                summer = num1.dice.value + num2.dice.value
                if j == 1:
                    await message.answer(f'Первая цифра {(num1.dice.value + num2.dice.value)}')
                elif j == 2:
                    await message.answer(f'Вторая цифра {(num1.dice.value + num2.dice.value)}')
                elif j == 3:
                    await message.answer(f'Третья цифра {(num1.dice.value + num2.dice.value)}')
                number += str(summer)
            else:
                await message.answer('Сумма больше 9-ти, переброс кубика')
        summer = 10
    await message.answer('Итоговое число ' + number)


@dp.message_handler(commands="users")
async def cmd_users(message: types.Message):
    print(get_info_about_user(message))
    await rz.get_transactions(config.address)
    text = ''
    cnt = 1
    for i in rz.scans:
        if i[0] not in text and i[0] != '0x0000000000000000000000000000000000000000':
            text += f'{str(cnt)}. {i[0]}\n'
            cnt += 1
    await message.answer(f'На текущий момент в конкурсе участвует {cnt - 1} человек')


@dp.message_handler(commands="last")
async def cmd_last(message: types.Message):
    print(get_info_about_user(message))
    await rz.get_transactions(config.address)
    text = ''
    user = rz.scans[-1]
    text += 'Последний пользователь🔚\n\n'
    text += f'Адрес пользователя:\n\n💳{user[0]}💳 \n\n'
    text += f'Сумма платежа: {user[1]}$ \n'
    text += f'Дата платежа: {user[3]} \n'
    await message.answer(text)


@dp.message_handler(commands="check")  # Сделать поиск информации по кошельку
async def cmd_check(message: types.Message):
    print(get_info_about_user(message))
    if message.get_args():
        await rz.get_transactions(config.address)
        text = ''
        found = False
        for i in rz.scans:
            if message.get_args().lower() in i:
                text += f'Адрес пользователя:\n\n💳{i[0]}💳 \n\n'
                text += f'Сумма платежа: {i[1]}$ \n'
                text += f'Дата платежа: {i[3]} \n'
                found = True
                await message.answer(text)
            text = ''
        if not found:
            await message.answer('Такой кошелёк не найден')


@dp.message_handler(commands="users_list")
async def cmd_users_list(message: types.Message):
    print(get_info_about_user(message))
    await message.answer('Подготовка файла...')
    await rz.get_transactions(config.address)
    text = ''
    cnt = 1
    for i in rz.scans:
        if i[0] not in text and i[0] != '0x0000000000000000000000000000000000000000':
            text += f'{str(cnt)}. {i[0]}\n'
            cnt += 1
    with open("users.txt", "w") as f:
        f.write(text[:-1])

    await message.answer_document(open('users.txt', 'rb'))

    await message.answer('Файл собран')


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    await message.answer('Создаю рандомное число от 1 до 3')
    await message.answer_dice('🎰')
    seed = random.randint(1, 100000)
    random.seed(seed)
    num = random.randint(1, 3)
    await message.answer(f'Ваше число: {num}\nСид рандома: {seed}')


@dp.message_handler(commands="seed")
async def cmd_seed(message: types.Message):
    if message.get_args():
        random.seed(int(message.get_args()))
        await message.answer(random.randint(1, 3))
    else:
        await message.answer('Нет аргумента')


# @dp.message_handler(commands="random")
# async def cmd_random(message: types.Message):
#     if message.get_args():
#         await message.answer(message.get_args())
#     else:
#         await rz.get_transactions(config.address)
#         text = ''
#         user = rz.scans[random.randint(0, rz.users)]
#         text += '🥇Победитель🥇\n\n'
#         text += f'Адрес пользователя:\n\n💳{user[0]}💳 \n\n'
#         text += f'Сумма платежа: {user[1]}$ \n'
#         text += f'Дата платежа: {user[3]} \n'
#         await message.answer(text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
