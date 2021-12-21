import logging
import os
import tempfile

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from search import search
from imutils import read_image
from imutils import get_text_from_image
from PIL import Image
import imagehash
import numpy

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class ImageInfo:
    def __init__(self, my_hash, my_text):
        hash_ = my_hash
        text = my_text

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!\n/search <text> to find the image\n')

def make_text_command(update: Update, context: CallbackContext) -> None:
    picture = update.message.photo[-1]
    file = picture.get_file()
    #update.message.reply_text("Я бы сохранил, если бы мог")
    with tempfile.TemporaryDirectory() as d:
        file_path = os.path.join(d, "image.png")
        file.download(file_path)
        #update.message.reply_text("Я сохранил изображение в" + file_path)
        image, hash_ = read_image(file_path, context.chat_data, update.message.message_id)
        context.chat_data[update.message.message_id] = ImageInfo(hash_, get_text_from_image(file_path, image))

def search_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_to_message(search(context.args, context.chat_data))

def main() -> None:
    """Start the bot."""
    updater = Updater("5074946865:AAFUXJ20UVO618nGVUPqk3xr2yfBvQ6tKE0")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_command))

    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, make_text_command))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()