from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
import datetime
#from dbhelper import DBHelper
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#db = DBHelper()
#db.setup()

tg_token = '842308578:AAHu6MUSeIsfFOhOVJ6R9QsYxcN1so7qLM4'
HEY, CHOOSE, TIME, SIZE, ORDER, COMMENT = range (6)
#global variables
What = 'Nothing'
ttime = 'now'
ssize = 'Большой'
buttons2 = [] 
bar_id = 708316082

menuList = [['Капучино'], ['Латте'], ['Раф'], ['Флэт'], ['Эспрессо']]
menu = '1) Капучино\n 2) Латте \n 3) Раф  \n 4) Флэт  \n 5) Эспрессо'


def help(update, context):
    KeyboardButton(text = '/')
    context.bot.send_message(chat_id=update.message.chat_id, text="Всё, что тебе нужно знать - это как начать разговор, а это легко - просто 'привет'")

def balance(update, context):
    KeyboardButton(text = '/')
    '''items = db.get_items()
    db.add_item('hyi')
    items = db.get_items()
    context.bot.send_message(chat_id=update.message.chat_id, text="asdasd")'''

def start(update, context):
    KeyboardButton(text = '/')
    context.bot.send_message(chat_id=update.message.chat_id, text="Каждый раз, когда хочешь заказать, пиши 'привет')")
    return HEY

def hey(update, context):
    KeyboardButton(text = '/')
    What = 'Nothing'
    ttime = 'now'
    ssize = 'Большой'
    buttons2.clear()
    current_user = update.effective_user
    if (update.message.text == 'Привет'or update.message.text == 'привет'):
        context.bot.send_message(chat_id=current_user.id, text='Привет, мешок!! Уже бежишь или еще больше десяти минут?', 
            reply_markup=ReplyKeyboardMarkup([['Бегу'], ['Медленно бегу']]))
        return CHOOSE
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text='Пока ты не поздороваешься, я не буду ничего делать!')
        return HEY

def choose(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Бегу'):
        context.bot.send_message(chat_id=current_user.id, 
            text= menu)
        context.bot.send_message(chat_id=current_user.id, 
            text='Выбирай)', reply_markup=ReplyKeyboardMarkup(menuList))
        return SIZE
    elif (update.message.text == 'Медленно бегу'):
        current_time = datetime.datetime.now()
        minute = current_time.minute
        hrs = current_time.hour
        if (minute < 15):
            mints= 15
        elif (minute >= 15 and minute < 30):
            mints = 30
        elif (minute >= 30 and minute < 45):
            mints  = 45
        elif (minute >= 45):
            mints = 0
            if (hrs < 23):
                hrs += 1
            else:
                hrs = 0
        print_time = current_time.replace(minute = mints, hour = hrs)
        quarter_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=15, hours=0, weeks=0)
        buttons1 = []
        global buttons2
        for i in range (4):
            for j in range (4):
                if (print_time.minute < 10):
                    min_to_print = '0'+ str(print_time.minute)
                else:
                    min_to_print = str(print_time.minute)
                buttons1.append(str(print_time.hour) + ':' + min_to_print)
                print_time = print_time + quarter_time
            buttons2.append(buttons1[:])
            buttons1.clear()
        context.bot.send_message(chat_id=current_user.id, 
            text='Во сколько будешь?:)', 
            reply_markup=ReplyKeyboardMarkup(buttons2))
        return TIME
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text="Давай начнём сначала, дело не в тебе, дело во мне. Снова скажи 'привет'")
        return HEY


def time(update, context):
    current_user = update.effective_user
    global ttime
    global buttons2
    ttime = update.message.text
    ind = 0
    for i in range (4): 
        IN = ttime in buttons2[i]
        if (IN):
            ind = 1
    buttons2.clear()
    if not (ind):
        context.bot.send_message(chat_id=current_user.id, 
            text="Давай начнём сначала, что-то не так. Снова скажи 'привет'")
        return HEY
    context.bot.send_message(chat_id=current_user.id, 
            text=menu)
    context.bot.send_message(chat_id=current_user.id, 
            text='Выбирай)', reply_markup=ReplyKeyboardMarkup(menuList))
    return SIZE

def size(update, context):
    current_user = update.effective_user
    if (update.message.text in menu):
        context.bot.send_message(chat_id=current_user.id, 
             text='Хорошо, определяемся с размером', reply_markup=ReplyKeyboardMarkup([['Большой'], ['15 см'], ['Маленький']]))
        global What
        What = update.message.text
        return ORDER
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text="Не понял, давай еще раз начнем с 'привет'")
        return HEY

def order(update, context):
    current_user = update.effective_user
    if (update.message.text == 'Большой' or update.message.text == '15 см' or update.message.text == 'Маленький'):
        context.bot.send_message(chat_id=current_user.id, 
             text='Ага! Можешь добавить комментарий к заказу или просто отправь точку)', reply_markup=ReplyKeyboardRemove(True))
        global ssize
        ssize = update.message.text
        return COMMENT
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text="Не понял, давай еще раз начнем с 'привет'")
        return HEY

def comment(update, context):
    current_user = update.effective_user
    global What 
    global ttime
    print('Comment: ', update.message.text)
    print ('Order: ', What)
    if (update.message.text != '.'):
        context.bot.send_message(chat_id=current_user.id, 
            text='Спасибо! Ждем тебя) \n Заказ:  ' + ssize + ' ' + What + '  (' + update.message.text + ')')
    else:
        context.bot.send_message(chat_id=current_user.id, 
            text='Спасибо! Ждем тебя) \n Заказ:  ' + ssize + ' ' + What)
    context.bot.send_message(chat_id=bar_id, 
            text='Заказ от: ' + current_user.first_name + ' ' + str(current_user.id) +
               '\nЗаказ: ' + ssize + ' ' + What + '  (' + update.message.text + '), ' + '\nбудет в: ' + ttime)
    What = 'Nothing'
    ttime = 'now'
    return HEY

def cancel(update, context):

    return ConversationHandler.END

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_user.id, text="Таааак, такой команды я не знаю")

def main():
    update = Updater(token=tg_token, use_context=True)
    dp = update.dispatcher

    help_handler = CommandHandler('help', help)
    dp.add_handler(help_handler)

    balance_handler = CommandHandler('balance', balance)
    dp.add_handler(balance_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            HEY: [MessageHandler(Filters.text, hey)],

            CHOOSE: [MessageHandler(Filters.text, choose)],

            TIME: [MessageHandler(Filters.text, time)],

            SIZE: [MessageHandler(Filters.text, size)],

            ORDER: [MessageHandler(Filters.text, order)],

            COMMENT: [MessageHandler(Filters.text, comment)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)



    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    update.start_polling()
    update.idle()
    #update.stop()


if __name__ == '__main__':
    main()