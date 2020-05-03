# import imagehash
import re
# from urllib.request import urlopen
# from PIL import Image
from telegram.ext import *
from telegram.error import *
import random
from time import sleep

token = "1080219429:AAEkVWuHws-jLWDqRQ3KSZnRuFXzbzWHPKk"
updater = Updater(token=token)
dispatcher = updater.dispatcher

bannedIDs = [1102559661]
bannedHashs = ['0303393f7f7d1a18']
bannedfileIDs = []


def delete(bot, update):
    if (update.message.from_user.id != 312612598):
        update.message.reply_to_message.delete()

def pt_sticker(bot, update):
    chat_id = update.message.chat_id
    if (int(chat_id) > 0):
        id = update.message.sticker.file_id
        update.message.reply_text(id)

def pt(bot, update):
    chat_id = update.message.chat_id
    if (int(chat_id) > 0):
        id = update.message.document.file_id
        update.message.reply_text(id)

def wenhao(bot, update):
    text = update.message.text
    if re.match(".*(炼铜|恋童).*", text) and random.randint(0, 101) > 75:
        update.message.reply_sticker("CAACAgUAAxkBAAIBxl6uzdewE0FQ5PUOwBSvptXKhG9IAALLAAP2FqISt4EfanE73D4ZBA")
    if re.match(".*[吗|嗎|?|？]$", text) and random.randint(0, 101) > 75:
        if text[0] == "你":
            text = "她" + text[1:]
        for i in range(1,len(text)):
            if text[i] == "你":
                text = text[:i] + "她" + text[i + 1 :]

        if re.match(".*[吗|嗎][|?|？]$", text):
            update.message.reply_text(text[:-2])
        else:
            update.message.reply_text(text[:-1])

def e(bot, update):
    id = update.message.chat_id
    update.message.reply_sticker("CAACAgEAAxkBAAIBhl6uYnAS14MmIKbILNr0GdiyTcFOAAIrAANWTBARd0FcUozlAwMZBA")
    bot.send_sticker(id, "CAACAgUAAxkBAAIBgF6uYXEzpwU8DH13lBYDmmFLJBooAAK-AAOouQABDf7BMVmdMWncGQQ")
    bot.send_sticker(id, "CAACAgUAAxkBAAIBiF6uYnQHNzrlLHsd5Uaczido9LJNAAK_AAOouQABDZFOpOSJdY-CGQQ")


def yaoyaoling(bot, update):
    try:
        update.message.reply_text("欢迎您致电东京都警视厅北泽警察署（03-3324-0110)")
        time = random.randint(0,11)
        sleep(time)
        id = update.message.chat_id
        time = random.randint(10, 31)
        bot.send_message(id, "您的来电已收悉，我们将在 " + str(time) + " 秒后到达")
        sleep(time)
        if (update.message.reply_to_message != None):
            if (update.message.reply_to_message.from_user.id == 312612598):
                update.message.reply_to_message.reply_text("我们是北泽警察署民警。根据《刑事诉讼法》第79条的规定，现在依法逮捕你，这是《逮捕证》，请在《逮捕证》上签名、捺指印")
            else:
                update.message.reply_to_message.reply_text("我们是北泽警察署民警。现接到报案，依法口头传唤你，请跟我们到警察署接受调查")
        else:
            update.message.reply_text("我们是北泽警察署民警。根据规定，传唤对象不能为空，你涉嫌报假警，现依法口头传唤你，请跟我们到警察署接受调查")
            #bot.send_message(id, "我们是北泽警察署民警，现接到报案，依法对你群进行检查，请你们配合。")

    except Exception as e:
        bot.send_message(update.message.chat_id, 'Error: ' + str(e))

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
dispatcher.add_handler(CommandHandler('110', yaoyaoling))
dispatcher.add_handler(CommandHandler('e', e))
dispatcher.add_handler(CommandHandler('del', delete))
dispatcher.add_handler(CommandHandler('delete', delete))
dispatcher.add_handler(MessageHandler(Filters.regex(".*(炼铜|恋童).*") & (~Filters.command), wenhao))
dispatcher.add_handler(MessageHandler(Filters.regex(".*[吗|嗎|?|？]$") & (~Filters.command), wenhao))
dispatcher.add_handler(MessageHandler(Filters.document, pt))
dispatcher.add_handler(MessageHandler(Filters.sticker, pt_sticker))

dispatcher.add_handler(MessageHandler(
    Filters.status_update.new_chat_members, checkAvatar))
updater.start_polling()
updater.idle()
