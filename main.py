# -*- coding: UTF-8 -*-
###################################################################################
import configparser
from aiogram import Bot, Dispatcher, executor, types
import datetime
import colorama
import matplotlib.pyplot as plt
import sqlite3
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

    cur.execute("SELECT * FROM xconomy")
    all_data = cur.fetchall()

    print(colorama.Fore.BLUE + text2art("Towns Stat"))
    for i in all_data:
        town_check = i[1].find("town-")
        if town_check == 0:
            print(colorama.Fore.GREEN + f" город: {i[1].partition('-')[2]}",
                  colorama.Fore.RED + f" банк: {i[2]}")
            towns_names.append(i[1].partition('-')[2])
            towns_balance.append(i[2])
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

    cur.execute("SELECT * FROM xconomy")
    all_data = cur.fetchall()

    print(colorama.Fore.BLUE + text2art("Nations Stat"))
    for i in all_data:
        town_check = i[1].find("nation-")
        if town_check == 0:
            print(colorama.Fore.GREEN +  f" нация: {i[1].partition('-')[2]}",
                  colorama.Fore.RED + f" банк: {i[2]}")
            nations_names.append(i[1].partition('-')[2])
            nations_balance.append(i[2])
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

    print(colorama.Fore.BLUE + text2art("Players Stat"))
    for i in all_data:
        town_check = i[1].find("town-")
        nations_check = i[1].find("nation-")
        if town_check == 0:
            pass

        elif nations_check == 0:
            pass

        else:
            print(colorama.Fore.GREEN +  f" игрок: {i[1]}",
                  colorama.Fore.RED + f" баланс: {i[2]}")
            players_names.append(i[1])
            players_balance.append(i[2])
            j += 1
    plt.figure(figsize=(10, 4))
    plt.barh(players_names, players_balance)
    plt.savefig("png/players.png")
    print(colorama.Fore.RESET)

@dp.message_handler(commands="check_stat")
async def send_stat(message: types.Message):
    await player_stat()
    await nations_stat()
    await town_stat()
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/players.png'))
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/nations.png'))
    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('png/towns.png'))





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
