from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,MessageEntity
from telegram import ParseMode as parseMode
import requests
import re
import logging
import os
import sys
import datetime
from datetime import timedelta

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
GROUP_ID= os.getenv("GROUP_ID")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)
def get_random_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def bop(bot, update):
    #sends cool random dog pictures
    url = get_random_dog_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def startBot(bot,update):
    msg="Hey, Good to meet you.\nWelcome To DCOR destined_TFS_bot"+" Telegram Bot.\nDesigned and maintained by DCOR."+"\nEnter the /help command to see available helps."
    update.message.reply_text(msg)
def showHelp(bot,update):
    msg="/help - to see available helps\n/schedule - to schedule next discussion.\n/bop - to get cool random dog pictures."
    update.message.reply_text(msg)
group_members=os.getenv("MEMBERS").split("-");
def generate_gm(dayAdd):
    dateObj=datetime.datetime.today()
    dateObj+=timedelta(days=dayAdd)
    if(dateObj.weekday()>=6):
        dateObj=dateObj+timedelta(days=1)
    wkObj=datetime.date(dateObj.year,dateObj.month,dateObj.day).isocalendar()
    d=wkObj[1]%5
    arr=[]
    for i in range(d,5):
        arr.append(i)
    if(len(arr)<5):
        lent=5-len(arr)
        for i in range(0,lent):
            arr.append(i)
    gs=globals()["group_members"]
    name_list=[gs[i] for i in arr]
    return name_list;
def generate_dt(dayAdd):
    datesArr=[]
    dateObj=datetime.date.today()
    dateObj+=timedelta(days=dayAdd)
    if(dateObj.weekday()>=6):
        dateObj=dateObj+timedelta(days=2)
    wk=datetime.date(dateObj.year,dateObj.month,dateObj.day)
    while wk.weekday()>0:
        wk=wk+timedelta(days=-1)
    while wk.weekday()<5:
        datesArr.append(wk)
        wk=wk+timedelta(days=1)
    return datesArr;
def generate_sch():
    names=generate_gm(7)
    days=generate_dt(7)
    return generate_sch_H(names,days,"next week")
def generate_sch_prev():
    names=generate_gm(-7)
    days=generate_dt(-7)
    return generate_sch_H(names,days,"last week")
def generate_sch_cur():
    names = generate_gm(0)
    days=generate_dt(0)
    return generate_sch_H(names,days,"this week")
def generate_sch_H(names,days,suffix_d):
    sch="*Discussion schedule for "+suffix_d+"*.\n\n"
    dd=["Monday","Tuesday","Wednesday","Thursday","Friday"]
    for i in range(0,len(names)):
        sch+=dd[i]+", "+"-".join((str(days[i]).split("-"))[::-1])+" -- *"+names[i]+"*\n\n"
    return sch
def day_basedSch(bot,update):
    day_basedsch="*Day-Based schedules*\n\n"
    day_basedsch+="*Monday* -- Pharmacology/Pathology\n\n"
    day_basedsch+="*Tuesday* -- Paediatrics\n\n"
    day_basedsch+="*Wednesday* -- Obstetrics&Gynaecology\n\n"
    day_basedsch+="*Thursday* -- Paediatrics\n\n"
    day_basedsch+="*Friday* -- Medicine/Surgery"
    update.message.reply_text(day_basedsch,parse_mode=parseMode.MARKDOWN)
def scheduleDisc(bot,update):
    update.message.reply_text(generate_sch(),parse_mode=parseMode.MARKDOWN)
def scheduleDiscCur(bot,update):
    update.message.reply_text(generate_sch_cur(),parse_mode=parseMode.MARKDOWN)
def scheduleDiscPrev(bot,update):
    update.message.reply_text(generate_sch_prev(),parse_mode=parseMode.MARKDOWN)
if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('help',showHelp))
    dp.add_handler(CommandHandler('start',startBot))
    dp.add_handler(CommandHandler('schedule',scheduleDisc))
    dp.add_handler(CommandHandler('currentschedule',scheduleDiscCur))
    dp.add_handler(CommandHandler('daybasedschedule',day_basedSch))

    run(updater)
