import logging
import os
import tempfile

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from search import search
from imutils import make_text
from caption import caption
from PIL import Image
import imagehash
import numpy
##3333
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def make_text_command(update: Update, context: CallbackContext) -> None:
    #update.message.reply_text(update.message.text)
    for element in update.message.photo:
        file = element.get_file()
        with tempfile.TemporaryDirectory() as d:
            file_path = os.path.join(d, "image.png")
            file.download(file_path)
            image, hash_ = read_image(file_path)
            #adding

def search_command(update: Update, context: CallbackContext) -> None:
    search(context.args, context.chat_data)

#def add_to_db(image, text, chat_data):


#def caption_command(update: Update, context: CallbackContext) -> None:
#    for (img in update.message.photo):


def main() -> None:
    """Start the bot."""
    updater = Updater("5074946865:AAFUXJ20UVO618nGVUPqk3xr2yfBvQ6tKE0")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()