import telebot
import sqlite3


token = '6613120527:AAH9ieRB_xFpZkBus4VLD_5QpamLc0wnV2U'
bot = telebot.TeleBot(token)
login = None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(message, enter_login)


@bot.callback_query_handler(func=lambda mess: True)
def enter_login(message):
    global login
    login = message.text.strip()
    bot.reply_to(message, 'Введите пароль')
    bot.register_next_step_handler(message, enter_password)


@bot.callback_query_handler(func=lambda mess: True)
def enter_password(message):
    password = message.text.strip()
    conn = sqlite3.connect('bd.bd')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (login, password) VALUES ("%s", "%s")' % (login, password))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'{login} - успешно зарегистрирован')
    get_users_info()


def get_users_info():
    conn = sqlite3.connect('bd.bd')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    res = cur.fetchall()

    info = ''

    for user in res:
        info += f'логин - {user[1]}, пароль - {user[2]}.\n'

    print(info)

    cur.close()
    conn.close()


if __name__ == '__main__':
    bot.infinity_polling()
