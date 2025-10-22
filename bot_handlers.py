import datetime
import functools
import logging
import os
import time
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler

import connect_to_esp
import telegram_services


def get_handlers() -> list:
    return [
        CommandHandler("get_image", get_image),
        CommandHandler("get_food", get_food),
        CommandHandler("off_sensor", off_sensor),
        CommandHandler("on_sensor", on_sensor)
    ]


def _response(text_func):
    @functools.wraps(text_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = await text_func(update, context)
        await telegram_services.response(update, context, text)

    return wrapper


async def get_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connect_to_esp.get_image()
    print(update.effective_chat.id)
    await telegram_services.send_image(update, context, 'output.jpeg')


@_response
async def get_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connect_to_esp.move()
    return "success"


@_response
async def off_sensor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connect_to_esp.off_sensor()
    return "success"


@_response
async def on_sensor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connect_to_esp.on_sensor()
    return "success"
