#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""okulushub-bot - Телеграм бот для администрирования канала Okulus Hub
Copyright 2023 Okulus Dev
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""
import logging
import json
from datetime import datetime
from configparser import ConfigParser									# Импорт парсера ini-файла
from aiogram import Bot, Dispatcher, executor, types
from parser import display_currency_prices

# Читаем конфиг и создаем константы
config = ConfigParser()
config.read('config.ini')
TOKEN = config["Telegram"]["token"] 									# Токен бота
ADMIN_ID = config["Telegram"]["admin_id"]								# ID администратора
BOTNAME = config["Telegram"]["bot_username"]							# Никнейм бота
CHANNEL = config["Telegram"]["channel_name"]							# Ссылка на канал

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
	await message.reply(f"<i>Приветствую</i>!\nNemesis Bot - это отличный профессиональный инструмент! Поиск данных, OSINT, поиск уязвимостей, парсинг новостей и многое другое - и это только начало!", parse_mode='html')


@dp.message_handler(commands='cryptocurrency')
async def cryptoget(message: types.Message):
	if str(message.from_user.id) == str(ADMIN_ID):
		await message.reply(f'Высылаем пост в {CHANNEL}')
		currency = display_currency_prices()
		await bot.send_message(CHANNEL, currency)
	else:
		currency = display_currency_prices()
		await bot.send_message(CHANNEL, currency)


@dp.message_handler(commands='news')
async def post_all_news(message: types.Message):
	if str(message.from_user.id) == str(ADMIN_ID):
		await bot.reply(f'Высылаем посты в {CHANNEL}')
		with open('res/securitylab.json', 'r') as file:
			seclab_news = json.load(file)

		for k, v in sorted(seclab_news.items()):
			news = f'''<i>{v["article_title"]}</i>
{v["article_desc"]}
<b><a href="{v["article_url"]}">Читать полностью</a></b> | {datetime.fromtimestamp(v["article_date_timestamp"])}

{v["tag"]}'''

			await bot.send_message(CHANNEL, news, parse_mode='html')

		with open('res/habr.json', 'r') as file:
			habr_news = json.load(file)

		for k, v in sorted(habr_news.items()):
			news = f'''<i>{v["title"]}</i>
<b><a href="{v["link"]}">Читать полностью</a></b>

{v["tag"]}'''

			await bot.send_message(CHANNEL, news, parse_mode='html')
	else:
		with open('res/securitylab.json', 'r') as file:
			seclab = json.load(file)

		for k, v in sorted(seclab.items()):
			news = f'''<i>{v["article_title"]}</i>
{v["article_desc"]}
<b><a href="{v["article_url"]}">Читать полностью</a></b> | {datetime.fromtimestamp(v["article_date_timestamp"])}

{v["tag"]}'''

			await message.answer(news, parse_mode='html')

		with open('res/habr.json', 'r') as file:
			habr_news = json.load(file)

		for k, v in sorted(habr_news.items()):
			news = f'''<i>{v["title"]}</i>
<b><a href="{v["link"]}">Читать полностью</a></b>

{v["tag"]}'''
			await message.answer(news, parse_mode='html')


if __name__ == '__main__':
	"""Данное условие отрабатывает если файл запускается, а не импортируется"""
	try:
		logging.basicConfig(level=logging.INFO)
		print('Телеграм бот для администрирования канала Okulus Hub. Copyright 2023 Okulus Dev')
		print(f'[+] Старт {BOTNAME}')
		print(f'[+] CTRL+C для выключения\n')
		executor.start_polling(dp)
	except KeyboardInterrupt:
		exit()
else:
	"""Это условие уже отработает если файл импортируется"""
	print('Телеграм бот для администрирования канала Okulus Hub. Copyright 2023 Okulus Dev')
	print('[!] Данная программа не преднозначена для импортирования, могут возникнуть ошибки')
