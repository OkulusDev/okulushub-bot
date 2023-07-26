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
import json
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

TAG = '⚡️ Okulus Hub - твой проводник в мир хакинга!'


def generate_useragent() -> str:
	"""Функция генерации случайного User-Agent

	Вывод: str"""
	fua = UserAgent()

	return str(fua.random)


def get_currency_price(currency):
	url = f"https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies=usd"
	response = requests.get(url)
	data = response.json()
	price = data[currency]['usd']
	return price


def display_currency_prices():
	btc_price = get_currency_price('bitcoin')
	eth_price = get_currency_price('ethereum')
	bnb_price = get_currency_price('binancecoin')
	usdt_price = get_currency_price('tether')
	ada_price = get_currency_price('cardano')
	doge_price = get_currency_price('dogecoin')
	
	print("Bitcoin (BTC) Price: $", btc_price)
	print("Ethereum (ETH) Price: $", eth_price)
	print("Binance Coin (BNB) Price: $", bnb_price)
	print("Tether (USDT) Price: $", usdt_price)
	print("Cardano (ADA) Price: $", ada_price)
	print("Dogecoin (DOGE) Price: $", doge_price)


class Habr:
	"""Парсер сайта habr.com"""
	def __init__(self, url='https://habr.com/ru/all/'):
		"""Инициализация класса
		Аргументы"""
		headers = {
			'User-Agent': generate_useragent()
		}

		self.response = requests.get(url, headers=headers).text
		self.soup = BeautifulSoup(self.response, "html.parser")

	def get_first_article(self):
		article = self.soup.find('h2', class_='tm-title tm-title_h2')
		description = self.soup.find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
		title = article.a.span.text.strip()
		link = f'https://habr.com{article.a["href"]}'
		article_id = f'{link.split("/")[:-1][-1]}'

		full_article = f'{title}\n{description}\n\nЧитать на хабре: {link}\n\n{TAG}'

		print(full_article)
		print(article_id)
		print('\n\n\n')

	def get_all_articles(self):
		data = {}

		for article in self.soup.find_all("h2", class_="tm-title tm-title_h2"):
			title = article.a.span.text.strip()
			link = f'https://habr.com{article.a["href"]}'
			article_id = f'{link.split("/")[:-1][-1]}'

			full_article = f'{title}\n\nЧитать на хабре: {link}\n\n{TAG}'

			print(full_article)
			print(article_id)
			print('\n')

			data[article_id] = {
				'title': title,
				'link': link,
				'tag': TAG,
				'full': full_article
			}

		# Записываем данные в JSON-файл
		with open("habr.json", "w", encoding='utf-8') as file:
			json.dump(data, file, indent=4)


class SecurityLab:
	def __init__(self, url='https://www.securitylab.ru/news/'):
		headers = {
			'User-Agent': generate_useragent()
		}

		self.response = requests.get(url, headers=headers).text
		self.soup = BeautifulSoup(self.response, "lxml")

	def get_all_articles(self):
		article_cards = self.soup.find_all("a", class_="article-card")

		articles_dict = {}

		for article in article_cards:
			article_title = article.find("h2", class_="article-card-title").text.strip()
			article_desc = article.find("p").text.strip()
			article_url = f'https://www.securitylab.ru{article.get("href")}'
			
			article_date_time = article.find("time").get("datetime")
			date_from_iso = datetime.fromisoformat(article_date_time)
			date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
			article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

			article_id = article_url.split('/')[-1]
			article_id = article_id[:-4]

			articles_dict[article_id] = {
				'article_date_timestamp': article_date_timestamp,
				'article_title': article_title,
				'article_url': article_url,
				'article_desc': article_desc,
				'tag': TAG
			}

		with open('securitylab.json', 'w') as file:
			json.dump(articles_dict, file, indent=4)


if __name__ == '__main__':
	habr = Habr()
	seclab = SecurityLab()
	habr.get_all_articles()
	seclab.get_all_articles()
	display_currency_prices()
	# with open("habr.json", "r") as file:
	# 	data = json.load(file)
	# print(data)
