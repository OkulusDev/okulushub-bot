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
from configparser import ConfigParser									# Импорт парсера ini-файла

# Читаем конфиг и создаем константы
config = ConfigParser()
config.read('config.ini')
TOKEN = config["Telegram"]["token"] 									# Токен бота
ADMIN_ID = config["Telegram"]["admin_id"]								# ID администратора
BOTNAME = config["Telegram"]["bot_username"]							# Никнейм бота
CHANNEL = config["Telegram"]["channel_name"]							# Ссылка на канал


if __name__ == '__main__':
	"""Данное условие отрабатывает если файл запускается, а не импортируется"""
	print('Телеграм бот для администрирования канала Okulus Hub. Copyright 2023 Okulus Dev')
	print(f'[+] Старт {BOTNAME}')
	print(f'[+] CTRL+C для выключения\n')
else:
	"""Это условие уже отработает если файл импортируется"""
	print('Телеграм бот для администрирования канала Okulus Hub. Copyright 2023 Okulus Dev')
	print('[!] Данная программа не преднозначена для импортирования, могут возникнуть ошибки')
