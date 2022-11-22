import telebot
from telebot import types

from managment_bd import take_all_competitions

token = '5879973344:AAFTZ6RU-reeZqdzTE2NOQvNA9Cl3KEUbb4'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    is_registration = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Да я хочу записаться", callback_data='registration_true')
    button2 = types.InlineKeyboardButton('Нет, я уже записан', callback_data='registration_false')
    is_registration.add(button1, button2)
    bot.send_message(message.chat.id,
                     'Привет, это бот для записи на соревнования, вы хотели бы записаться на соревнование?',
                     reply_markup=is_registration)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     'Привет, это бот для записи на соревнования. Все возможные команды можно просмотреть написав /')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            all_competitions = take_all_competitions()
            choose_competition = types.InlineKeyboardMarkup()
            for competition in all_competitions:
                choose_competition.add(types.InlineKeyboardButton(f'{competition}', callback_data=str(competition)))
            if call.data == "registration_true":
                bot.send_message(call.message.chat.id, 'Круто, на какое соревнование тебе хочеться попасть?',
                                 reply_markup=choose_competition)
            if call.data == "registration_false":
                bot.send_message(call.message.chat.id, 'В каком соревновании вы уже учавствуете?',
                                 reply_markup=choose_competition)
    except Exception as e:
        print(repr(e))

    @bot.callback_query_handler(func=lambda call: True)
    @bot.message_handler(commands=['my_competition'])
    def callback_inline_2(call):
        try:
            if call.message:
                bot.send_message(call.message.chat.id, f' соревнование  {call.data}')
        except Exception as e:
            print(repr(e))


bot.infinity_polling()
