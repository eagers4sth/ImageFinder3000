import logging
import os
import tempfile

import telegram.ext
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from search import search
from imutils import read_image
from imutils import get_text_from_image
from image_info import ImageInfo

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
    update.message.reply_text('Help!\n/search <text> to find the image\n')

def make_text_command(update: Update, context: CallbackContext) -> None:
    logging.info("I see a picture")
    picture = update.message.photo[-1]
    file = picture.get_file()
    logging.info("received an image")
    with tempfile.TemporaryDirectory() as d:
        file_path = os.path.join(d, "image.png")
        file.download(file_path)
        logging.info("saved the image")
        image, hash_ = read_image(file_path)
        context.chat_data[update.message.message_id] = ImageInfo(hash_, get_text_from_image(file_path, image))

def sticker_to_text_command(update: Update, context: CallbackContext) -> None:
    logging.info("I see a sticker")
    stick = update.message.sticker
    file = stick.get_file()
    logging.info("received a sticker")
    with tempfile.TemporaryDirectory() as d:
        file_path = os.path.join(d, "image.png")
        file.download(file_path)
        logging.info("saved the stciker")
        image, hash_ = read_image(file_path)
        context.chat_data[update.message.message_id] = ImageInfo(hash_, get_text_from_image(file_path, image))
        logging.info(len(context.chat_data))

def search_command(update: Update, context: CallbackContext) -> None:
    if not context.chat_data:
        update.message.reply_text('No photo data')
        return
    logging.info("going to find an image")
    logging.info(len(context.chat_data))
    logging.info(' '.join(context.args))
    context.bot.send_message(chat_id=update.message.chat_id, text='image', reply_to_message_id=search(' '.join(context.args), context.chat_data))

def main() -> None:
    """Start the bot."""
    my_persistence = telegram.ext.PicklePersistence(filename='data.pickle')
    updater = Updater("5074946865:AAFUXJ20UVO618nGVUPqk3xr2yfBvQ6tKE0", persistence=my_persistence, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_command))

    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, make_text_command))
    dispatcher.add_handler(MessageHandler(Filters.sticker & ~Filters.command, sticker_to_text_command))
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()