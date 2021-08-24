import sqlite3 as sql
from datetime import date, datetime
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, \
    InputMediaPhoto


class User:
    def __init__(self, user_id=None, user_name=None, msg=None, photo_1=None, photo_2=None, photo_3=None, payment=None,
                 exp_date=None):
        self.user_id = user_id
        self.user_name = user_name
        self.msg = msg
        self.photo_1 = photo_1
        self.photo_2 = photo_2
        self.photo_3 = photo_3
        self.payment = payment
        self.exp_date = exp_date


def make_connection():
    connection = sql.connect('../slivki_data_base.sqlite3')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS messages ('
                   'msg_id INTEGER PRIMARY KEY,'
                   'user_name TEXT DEFAULT "null",'
                   'msg_text TEXT DEFAULT "null",'
                   'photo_1 TEXT DEFAULT "null",'
                   'photo_2 TEXT DEFAULT "null",'
                   'photo_3 TEXT DEFAULT "null",'
                   'payment INTEGER DEFAULT 0,'
                   'exp_date TEXT DEFAULT "null",'
                   'user_id INTEGER,'
                   'FOREIGN KEY ("user_id") REFERENCES users("user_id") ON DELETE CASCADE ON UPDATE CASCADE )')
    cursor.execute('CREATE TABLE IF NOT EXISTS users ('
                   'user_id INTEGER PRIMARY KEY UNIQUE )')
    connection.commit()
    return True

# Create sql database
make_connection()


date_now = date(datetime.now().year, datetime.now().month, datetime.now().day).isoformat()

TELEGRAM_TOKEN = '1921813733:AAHL9ad8LwPUbXBxpUlj_-7QlmyaD0VmUlA'
bot = telebot.TeleBot(TELEGRAM_TOKEN)
s = User


def gen_yes_no_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes ✅", callback_data="cb_yes"),
               InlineKeyboardButton("No ‼️", callback_data="cb_no"),
               InlineKeyboardButton("Редактировать", callback_data="cb_edit"))
    return markup


def gen_start_markup():
    markup = ReplyKeyboardMarkup()
    buttonA = KeyboardButton('Создать анкету ✅')
    buttonB = KeyboardButton('Написать администратору ✍🏼')
    buttonC = KeyboardButton('Мои анкеты 🔹')
    markup.row(buttonA)
    markup.row(buttonB)
    markup.row(buttonC)
    markup.resize_keyboard = True
    return markup


def gen_edit_markup():
    markup = ReplyKeyboardMarkup()
    buttonA = KeyboardButton('Редактировать ✅')
    # buttonB = KeyboardButton('Отменить')
    markup.row(buttonA)
    # markup.row(buttonB)
    markup.resize_keyboard = True
    return markup


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id,
                     text='Отправьте рекламное сообщение, обязательно укажите телефон или ваш аккаунт в телеграмме',
                     reply_markup=gen_start_markup())


@bot.message_handler(regexp='Создать анкету ✅')
def create(message):
    msg = bot.reply_to(message, 'Введите рекламное сообщение: ', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_first_photo)


def process_first_photo(message):
    try:
        s.user_id = message.from_user.id
        s.msg = message.text
        # print(s.msg)
        msg = bot.reply_to(message, 'Отправьте первое фото')
        bot.register_next_step_handler(msg, process_second_photo)
    except:
        bot.reply_to(message, 'oooops from process_first_photo', reply_markup=gen_start_markup())


def process_second_photo(message):
    try:
        if message.content_type == 'photo':
            # print(message.json['photo'][-1]['file_id'])
            photo_1 = message.json['photo'][-1]['file_id']
            file_path = bot.get_file(message.photo[-1].file_id).file_path
            file = bot.download_file(file_path)
            with open("static/images/" + photo_1 + ".jpg", "wb") as code:
                code.write(file)
            s.photo_1 = "static/images/" + photo_1 + ".jpg"
            msg = bot.reply_to(message, 'Отправьте второе фото')
            bot.register_next_step_handler(msg, process_third_photo)
        else:
            bot.reply_to(message, 'Ошибка. Похоже вы отправили не фото. Просьба заполнить анкету заново',
                         reply_markup=gen_start_markup())
    except:
        bot.reply_to(message, 'oooops from process_second_photo', reply_markup=gen_start_markup())


def process_third_photo(message):
    try:
        if message.content_type == 'photo':
            photo_2 = message.json['photo'][-1]['file_id']
            file_path = bot.get_file(message.photo[-1].file_id).file_path
            file = bot.download_file(file_path)
            with open("static/images/" + photo_2 + ".jpg", "wb") as code:
                code.write(file)
            s.photo_2 = "static/images/" + photo_2 + ".jpg"
            msg = bot.reply_to(message, 'Отправьте третье фото')
            bot.register_next_step_handler(msg, process_finish)
        else:
            bot.reply_to(message, 'Ошибка. Похоже вы отправили не фото. Просьба заполнить анкету заново',
                         reply_markup=gen_start_markup())
    except:
        bot.reply_to(message, 'oooops from process_third_photo')


def process_finish(message):
    if message.content_type == 'photo':

        photo_3 = message.json['photo'][-1]['file_id']
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        with open("static/images/" + photo_3 + ".jpg", "wb") as code:
            code.write(file)
        s.photo_3 = "static/images/" + photo_3 + ".jpg"
        img_1 = open(s.photo_1, "rb")
        img_2 = open(s.photo_2, "rb")
        img_3 = open(s.photo_3, "rb")
        bot.send_message(message.chat.id, 'Ваша анкета выглядит следующим образом: ')
        bot.send_media_group(message.chat.id, media=[InputMediaPhoto(media=img_1),
                                                     InputMediaPhoto(media=img_2),
                                                     InputMediaPhoto(media=img_3)])
        bot.send_message(message.chat.id, s.msg)
        img_1.close()
        img_2.close()
        img_3.close()
        bot.send_message(message.chat.id, 'Опубликовать?', reply_markup=gen_yes_no_markup())
    else:
        bot.reply_to(message, 'Ошибка. Похоже вы отправили не фото. Просьба заполнить анкету заново',
                     reply_markup=gen_start_markup())


@bot.callback_query_handler(func=lambda call: True)
def subscription_btn_handler(call):
    if call.data == "cb_yes":
        try:
            connection = sql.connect('../slivki_data_base.sqlite3')
            cursor = connection.cursor()
            message_insert_param = """INSERT INTO messages (msg_id, user_name, msg_text, photo_1, photo_2, photo_3, payment, 
            exp_date, user_id_id, comment) VALUES (?,?,?,?,?,?,?,?,?,?)"""
            try:
                cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (? );', (s.user_id,))
            except:
                print('Error INSERT INTO users. User has already been inserted')

            message_data_tuple = (call.message.id,
                                  '@'+call.message.chat.username,
                                  s.msg,
                                  s.photo_1,
                                  s.photo_2,
                                  s.photo_3,
                                  0,
                                  date_now,
                                  s.user_id,
                                  ' ')
            try:
                print(message_data_tuple)
                print(type(call.message.id),
                      type('@'+call.message.chat.username),
                      type(s.msg),
                      type(s.photo_1),
                      type(s.photo_2),
                      type(s.photo_3),
                      type(0),
                      type(date_now),
                      type(s.user_id))
                cursor.execute(message_insert_param, message_data_tuple)
            except:
                print("message_data_tuple_failed")
            connection.commit()
            bot.send_message(call.message.chat.id, 'Спасибо! Ваша анкета направлена на модерацию 📌',
                             reply_markup=gen_start_markup())
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.delete_message(call.message.chat.id, call.message.id - 1)
            bot.delete_message(call.message.chat.id, call.message.id - 2)
            bot.delete_message(call.message.chat.id, call.message.id - 3)
            bot.delete_message(call.message.chat.id, call.message.id - 4)
            bot.delete_message(call.message.chat.id, call.message.id - 5)
            bot.delete_message(call.message.chat.id, call.message.id - 6)
            bot.delete_message(call.message.chat.id, call.message.id - 7)
            bot.delete_message(call.message.chat.id, call.message.id - 8)
            bot.delete_message(call.message.chat.id, call.message.id - 9)
            bot.delete_message(call.message.chat.id, call.message.id - 10)
            bot.delete_message(call.message.chat.id, call.message.id - 11)
            bot.delete_message(call.message.chat.id, call.message.id - 12)
            bot.delete_message(call.message.chat.id, call.message.id - 13)
            bot.delete_message(call.message.chat.id, call.message.id - 14)
            bot.answer_callback_query(call.id)
        except sql.OperationalError:
            bot.send_message(call.message.chat.id, 'Ошибка базы данных')
    if call.data == "cb_no":
        bot.send_message(call.message.chat.id, 'Возвращайтесь к нам ещё', reply_markup=gen_start_markup())
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.delete_message(call.message.chat.id, call.message.id - 2)
        bot.delete_message(call.message.chat.id, call.message.id - 3)
        bot.delete_message(call.message.chat.id, call.message.id - 4)
        bot.delete_message(call.message.chat.id, call.message.id - 5)
        bot.delete_message(call.message.chat.id, call.message.id - 6)
        bot.delete_message(call.message.chat.id, call.message.id - 7)
        bot.delete_message(call.message.chat.id, call.message.id - 8)
        bot.delete_message(call.message.chat.id, call.message.id - 9)
        bot.delete_message(call.message.chat.id, call.message.id - 10)
        bot.delete_message(call.message.chat.id, call.message.id - 11)
        bot.delete_message(call.message.chat.id, call.message.id - 12)
        bot.delete_message(call.message.chat.id, call.message.id - 13)
        bot.delete_message(call.message.chat.id, call.message.id - 14)
        bot.answer_callback_query(call.id)
    if call.data == "cb_edit":
        msg = bot.send_message(call.message.chat.id, 'Нажмите кнопку редактировать',
                               reply_markup=gen_edit_markup())
        bot.register_next_step_handler(msg, create)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.delete_message(call.message.chat.id, call.message.id - 2)
        bot.answer_callback_query(call.id)


@bot.message_handler(regexp='Написать администратору ✍🏼')
def support(message):
    msg = bot.reply_to(message, 'Введите ваше сообщение:')
    bot.register_next_step_handler(msg, process_support)


def process_support(message):
    print(message)
    print(message.from_user.username)
    user = types.ChatMember(message.from_user.id, True)
    print(user)
    bot.send_message(message.chat.id, 'Ваша заявка принята, администратор ответит вам в ближайшее время')
    bot.delete_message(message.chat.id, message.id - 1)
    bot.delete_message(message.chat.id, message.id - 2)
    if message.from_user.username == 'None':
        bot.send_message(message.chat.id, 'Поступило обращение:')
        bot.forward_message(message.chat.id, message.chat.id, message.id)
    else:
        bot.send_message(message.chat.id,
                         'Поступило обращение от @{0}:\n{1}'.format(message.from_user.username, message.text))


@bot.message_handler(regexp='Мои анкеты 🔹')
def my_account(message):
    user_id = message.from_user.id
    try:
        connection = sql.connect('../slivki_data_base.sqlite3')
        cursor = connection.cursor()
        cur = cursor.execute('SELECT * FROM messages WHERE user_id_id=?', (user_id,)).fetchall()
        bot.send_message(message.chat.id, "У вас найдено анкет: {0}".format(len(cur)))
        connection.commit()
    except:
        print('Ошибка в Мои анкеты')


@bot.message_handler(commands=['test'])
def cancel(message):
    try:
        bot.send_message(message.chat.id, 'DATABASE TESTING')
        connection = sql.connect('../slivki_data_base.sqlite3')
        cursor = connection.cursor()
        data = cursor.execute('SELECT * FROM messages').fetchall()
        print(data)
        data = cursor.execute('SELECT * FROM users').fetchall()
        print(data)
        data = cursor.execute('SELECT user_id FROM messages').fetchall()
        print(data)
        data = cursor.execute('SELECT msg_text FROM messages WHERE user_id=753169055').fetchall()
        print(data)
        connection.commit()
        print(message.chat.username)
    except:
        print('error from DB test')


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
