import logging

from telegram.ext import ApplicationBuilder

import connect_to_esp
from bot_handlers import get_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Bot:
    def __init__(self, token):
        self.TOKEN = token
        self.application = ApplicationBuilder().token(token).build()
        handlers = get_handlers()
        self._initialize_handlers(handlers)

    def _initialize_handlers(self, handlers):
        for handler in handlers:
            self.application.add_handler(handler)

    def run_polling(self):
        logging.info("Starting bot in polling mode")
        connect_to_esp.get_pir_image(self.get_context())
        self.application.run_polling()

    def get_context(self):
        return self.application.context_types