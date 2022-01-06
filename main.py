import json

import telebot

import db_interaction
import utils


config = utils.read_config()
bot = telebot.TeleBot(config['telegram_bot_token'])


def add_accounts(user_id, message):
    if 'accounts' not in message:
        bot.send_message(user_id, 'No key accounts')
        return
    try:
        db_interaction.add_accounts(message['accounts'])
    except Exception as e:
        bot.send_message(user_id, e)
        return
    bot.send_message(user_id, 'Accounts added')

def return_2fa_code(user_id, message):
    shared_secret = db_interaction.get_shared_secret(message)
    if len(shared_secret) > 0:
        code = utils.generate_one_time_code(shared_secret[0][0])
        bot.send_message(user_id, code)
    else:
        bot.send_message(user_id, 'Unknown username')


def handle_admin_json_message(user_id, message):
    json_message = json.loads(message)
    if 'action' not in json_message:
        bot.send_message(user_id, 'No key action')
        return
    action = json_message['action']
    if action == 'add':
        add_accounts(user_id, json_message)
    else:
        bot.send_message(user_id, 'Unknown action')


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Hello, write account username')

@bot.message_handler()
def get_message(message):
    user_id = message.chat.id
    message = message.text
    if user_id in config['admin_ids'] and utils.is_json(message):
        handle_admin_json_message(user_id, message)
        return
    return_2fa_code(user_id, message)


if __name__ == '__main__':
    bot.infinity_polling()