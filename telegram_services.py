from telegram import Update
from telegram.ext import ContextTypes

import secret

id = secret.id


async def response(
        update: Update, context: ContextTypes.DEFAULT_TYPE, text: str
) -> None:
    print(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def send_image(
        update: Update, context: ContextTypes.DEFAULT_TYPE, file: str
) -> None:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)


def send_in_chat_image(context: ContextTypes.DEFAULT_TYPE, file: str) -> None:
    context.bot.send_photo(chat_id=id, photo=file)
