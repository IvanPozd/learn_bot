#!usr/bin/env python3
""" Simple Echo Bot """

import logging
import settings

from glob import glob
from random import randint, choice
from telegram import Update, ForceReply
from telegram.ext import (
	Updater,
	CommandHandler,
	MessageHandler,
	Filters,
	CallbackContext
)

PROXY = {
	"proxy_url": settings.PROXY_URL,
	"urllib3_proxy_kwargs": {
		"username": settings.PROXY_USERNAME,
		"password": settings.PROXY_PASSWORD,
	},
}

logging.basicConfig(
	filename="logs/bot.log",
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
	logger.info(f"Starting bot. {update.effective_user}")
	user = update.effective_user
	update.message.reply_markdown_v2(
		rf"Hi, {user.username}!", reply_markup=ForceReply(selective=True)
	)


def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text("Help!")


def play_random_numbers(user_number: int) -> str:
	bot_number = randint(user_number - 10, user_number + 10)
	if user_number > bot_number:
		message = f"Ваше число - {user_number}, Моё число - {bot_number}. Поздравляю!!! Вы выиграли!"
	elif user_number == bot_number:
		message = f"Ваше число - {user_number}, Моё число - {bot_number}. Ничья!! Давай еще раз?"
	else:
		message = f"Ваше число - {user_number}, Моё число - {bot_number}. Я выиграл! Сожалею! Повезет в следующий раз!"

	return message


def guess_number(update: Update, context: CallbackContext) -> None:
	print(context.args)
	if context.args:
		try:
			user_number = int(context.args[0])
			message = play_random_numbers(user_number)

		except (TypeError, ValueError):
			message = "Введите целое число!"
	else:
		message = "Введите число. Например - /guess 15"
	update.message.reply_text(message)


def echo_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(update.message.text)


def send_car_pic(update: Update, context: CallbackContext):
	cars_list = glob('images/car*.jp*g')
	car_pic = choice(cars_list)
	chat_id = update.effective_chat.id
	context.bot.send_photo(chat_id=chat_id, photo=open(car_pic, 'rb'))


def main() -> None:
	updater = Updater(settings.TOKEN, use_context=True, request_kwargs=PROXY)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start_command))
	dp.add_handler(CommandHandler("help", help_command))
	dp.add_handler(CommandHandler("guess", guess_number))
	dp.add_handler(CommandHandler("car", send_car_pic))
	dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_command))

	updater.start_polling()
	updater.idle()


if __name__ == "__main__":
	main()
