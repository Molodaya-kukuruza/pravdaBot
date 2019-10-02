import cherrypy 
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

tg_token = '947027312:AAFVxwkYgVRT2fkd5Ux7ExD9hxlu7-eCMj8'


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text= 'хуй')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


updater = Updater(token=tg_token, use_context=True)
updater.bot.set_webhook(url='https://5ff7580e.ngrok.io')
dp = updater.dispatcher

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

# log all errors
dp.add_error_handler(error)

class HelloWorld:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        update = Update.de_json(cherrypy.request.json, updater.bot)
        dp.process_update(update)
        return ""


def main():
    cherrypy.config.update(
        {
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 7771,
            "engine.autoreload.on": True,
        }
    )

    cherrypy.quickstart(HelloWorld(), '/',{})


if __name__ == '__main__':
    main()