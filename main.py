# -*- coding: UTF-8 -*-
###################################################################################
import configparser
from aiogram import Bot, Dispatcher, executor, types
import datetime
import os
import asyncio
import colorama
import matplotlib.pyplot as plt
import sqlite3
from loguru import logger
from art import *
###################################################################################
config = configparser.ConfigParser()
config.read("config.ini")

bot = Bot(token=config["bot"]["token"])
dp = Dispatcher(bot)

conn = sqlite3.connect(config["data"]["db"])
cur = conn.cursor()

towns_stat = []
players_stat = []


async def town_stat():
    j = 0
    towns_names = []
    towns_balance = []

    cur.execute("SELECT * FROM xconomynon")
    all_data = cur.fetchall()

    print(colorama.Fore.BLUE + "Towns Stat")
    for i in all_data:
        town_check = i[0].find("town-")
        if town_check == 0:
            print(colorama.Fore.BLUE + f"город: {i[0].partition('-')[2]}")
            print(colorama.Fore.GREEN + f"  банк: {i[1]}")
            towns_names.append(i[0].partition('-')[2])
            towns_balance.append(i[1])
            j += 1

        else:
            pass
    plt.figure(figsize=(10, 4))
    plt.barh(towns_names, towns_balance)
    plt.savefig("png/towns.png")
    print(colorama.Fore.RESET)

async def nations_stat():
    j = 0
    nations_names = []
    nations_balance = []

    cur.execute("SELECT * FROM xconomynon")
    all_data = cur.fetchall()

    print(colorama.Fore.BLUE + "Nations Stat")
    for i in all_data:
        nation_check = i[0].find("nation-")
        if nation_check == 0:
            print(colorama.Fore.BLUE + f"нация: {i[0].partition('-')[2]}")
            print(colorama.Fore.GREEN + f"  банк: {i[1]}")
            nations_names.append(i[0].partition('-')[2])
            nations_balance.append(i[1])
            j += 1

        else:
            pass
    plt.figure(figsize=(10, 4))
    plt.barh(nations_names, nations_balance)
    plt.savefig("png/nations.png")
    print(colorama.Fore.RESET)

async def player_stat():
    j = 0
    players_names = []
    players_balance = []

    cur.execute("SELECT * FROM xconomy")
    all_data = cur.fetchall()

    print(colorama.Fore.BLUE + "Players Stat")
    for i in all_data:
        town_check = i[1].find("town-")
        nations_check = i[1].find("nation-")
        if town_check == 0:
            pass

        elif nations_check == 0:
            pass

        else:
            print(colorama.Fore.BLUE + f"игрок: {i[1]}")
            print(colorama.Fore.GREEN + f"  баланс: {i[2]}")
            players_names.append(i[1])
            players_balance.append(i[2])
            j += 1
    plt.figure(figsize=(10, 4))
    plt.barh(players_names, players_balance)
    plt.savefig("png/players.png")
    print(colorama.Fore.RESET)

async def chk_date():
    await player_stat()
    await nations_stat()
    await town_stat()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    try:
        logger.info(f"{username} подключился к боту")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Получить Статистику"]
        keyboard.add(*buttons)
        await message.answer(f"Добро Пожаловать, {username}.", reply_markup=keyboard)
        while True:
            chk_date()
            await asyncio.sleep(86400)

    except:
        logger.info(f"{username} снова подключился к боту")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Получить Статистику"]
        keyboard.add(*buttons)
        await message.answer(f"Добро Пожаловать, {username}.", reply_markup=keyboard)
        while True:
            chk_date()
            await asyncio.sleep(86400)

@dp.message_handler(lambda message: message.text == "Получить Статистику")
async def send_stat(message: types.Message):
    username = message.from_user.username if message.from_user.username else None
    logger.info(f"{username} запросил статистику")
    # os.remove("png/players.png")
    # os.remove("png/towns.png")
    # os.remove("png/nations.png")
    await chk_date()
    await message.answer("Статистика Игроков")
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/players.png'))
    await message.answer("Статистика Городов")
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/towns.png'))
    await message.answer("Статистика Наций")
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/nations.png'))


if __name__ == "__main__":
    chkdir = os.path.isdir("png")
    colorama.init()
    if chkdir == True:
        executor.start_polling(dp, skip_updates=True)
    else:
        os.mkdir("png")
        print("создание директории 'png'")
        executor.start_polling(dp, skip_updates=True)
