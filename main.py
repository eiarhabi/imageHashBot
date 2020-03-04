import imagehash
import re
import re
from urllib.request import urlopen
from PIL import Image
from telegram.ext import *
from telegram.error import *

token = "1087954382:AAHdqZOqFBOXGitrj64to9SzJxhxCEkeL2k"
updater = Updater(token=token)
dispatcher = updater.dispatcher

bannedIDs = [1102559661]
bannedHashs = ['0303393f7f7d1a18']
bannedfileIDs = []


def no(bot, update):
    update.message.reply_text("不可以")


def checkAvatar(bot, update):
    try:
        if update.message.new_chat_members != []:
            id = update.message.new_chat_members[0].id

            if id in bannedIDs:
                bot.kick_chat_member(
                    chat_id=update.message.chat_id, user_id=id)
                bot.send_message(chat_id=update.message.chat_id, text='kicked')

            fileID = bot.get_user_profile_photos(
                id, limit=1).photos[0][-1].file_id

            if fileID in bannedfileIDs:
                bot.kick_chat_member(
                    chat_id=update.message.chat_id, user_id=id)
                bot.send_message(chat_id=update.message.chat_id, text='kicked')

            link = bot.getFile(fileID).file_path
            image = Image.open(urlopen(link))
            hash = imagehash.whash(image)

            if str(hash) in bannedHashs:
                bot.kick_chat_member(
                    chat_id=update.message.chat_id, user_id=id)
                bot.send_message(chat_id=update.message.chat_id, text='kicked')

    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Error: ' + str(e))


dispatcher.add_handler(CommandHandler('touch', no))
dispatcher.add_handler(MessageHandler(
    Filters.status_update.new_chat_members, checkAvatar))
updater.start_polling()
updater.idle()
