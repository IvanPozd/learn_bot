#!usr/bin/env python3
""" Simple Echo Bot """

import logging
import settings

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher

PROXY = {
	'proxy_url': settings.PROXY_URL,
	'urllib3_proxy_kwargs': {
		'username': settings.PROXY_USERNAME,
		'password': settings.PROXY_PASSWORD
	}
}

logging.basicConfig(filename="logs/bot.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
	logger.info(f'Starting bot. {update.effective_user}')
	user = update.effective_user
	update.message.reply_markdown_v2(
		fr"Hi, {user.username}!",
		reply_markup=ForceReply(selective=True)
	)


def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text('Help!')


def echo_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(update.message.text)


def main() -> None:
	updater = Updater(settings.TOKEN, use_context=True, request_kwargs=PROXY)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start_command))
	dp.add_handler(CommandHandler("help", help_command))
	dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_command))

	updater.start_polling()
	updater.idle()


if __name__ == "__main__":
	main()