from flask import Flask, request
import os
import telebot
import travel_visa_bot


server = Flask(__name__)
bot = travel_visa_bot.bot
travel_visa_bot.main()


@server.route('/' + bot.token, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://travel-visa-bot.herokuapp.com/' + bot.token)
    return 'Hello from bot', 200


@server.route('/admin')
def helloadmin():
    return 'Hello admin', 200


@server.route('/rwh')
def remove_webhook():
    bot.remove_webhook()
    return 'webhook delete - ok', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
