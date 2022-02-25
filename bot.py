#!usr/bin/env python3
""" Simple Echo Bot """

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TOKEN


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	update.message.reply_markdown_v2(
		fr"Hi {user.mention_markdown_v2()}\!",
		reply_markup=ForceReply(selective=True)
	)


def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text('Help!')


def echo_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(update.message.text)


def main() -> None:
	updater = Updater(TOKEN)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_command))

	updater.start_polling()
	updater.idle()


if __name__ == "__main__":
	main()