import logging
from telegram.error import InvalidToken
from bot import Bot
import secret

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logger = logging.getLogger(__name__)

BOT_TOKEN = secret.BOT_TOKEN
def main(bot_token):
    bot = Bot(bot_token)
    bot.run_polling()



if __name__ == "__main__":
    try:
        logger.info("Obtained token successfully")
        main(BOT_TOKEN)
    except InvalidToken:
        logger.error("Error occurred while obtaining Bot token form environment")