import telebot
from telebot import types
from json import loads

from managment_bd import take_all_competitions, check_person_in_competition, insert_person, take_all_persons

token = ''
bot = telebot.TeleBot(token)
competition_name = ''


@bot.message_handler(commands=['start'])
def send_welcome(message):
    is_registration = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Да я хочу записаться", callback_data='{"st":"rt"}')
    button2 = types.InlineKeyboardButton('Нет, я уже записан', callback_data='{"st":"rf"}')
    is_registration.add(button1, button2)
    bot.send_message(message.chat.id,
                     'Привет, это бот для записи на соревнования, вы хотели бы записаться на соревнование?',
                     reply_markup=is_registration)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     'Привет, это бот для записи на соревнования. Все возможные команды можно просмотреть написав /')


@bot.message_handler(commands=['lk'])
def lk(message):
    lk_menu = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton("Мой напарник", callback_data='{"st":"pp"}')
    button2 = types.InlineKeyboardButton('Соперники', callback_data='{"st":"pc"}')
    button3 = types.InlineKeyboardButton('Записаться на игру', callback_data='{"st":"tg"}')
    button4 = types.InlineKeyboardButton('Записать очки за игру', callback_data='{"st":"ts"}')
    button5 = types.InlineKeyboardButton('Прекратить участие в соревновании', callback_data='{"st":"ex"}')
    lk_menu.add(button1, button2, button3)
    lk_menu.add(button4, button5)
    if competition_name:
        bot.send_message(message.chat.id,
                         f'Добро пожаловать на соревнование {competition_name}', reply_markup=lk_menu)
    else:
        bot.send_message(message.chat.id,
                         'Пока вы не учавствуете ни в одном соревновании, напишите команду /start для регистрации участия в соревновании или подключению к существующему соревнованию')


@bot.callback_query_handler(func=lambda call: loads(call.data)['st'] in ('cic', 'rt', 'rf'))
def callback_inline(call):
    try:
        data = loads(call.data)
        if call.message:
            all_competitions = take_all_competitions()
            choose_competition = types.InlineKeyboardMarkup()
            for competition in all_competitions:
                choose_competition.add(types.InlineKeyboardButton(f'{competition}',
                                                                  callback_data='{"ost":"' + data[
                                                                      'st'] + '","st":"cic","cn":"' + competition + '"}'))
            if data['st'] == "rt":
                bot.send_message(call.message.chat.id, 'Круто, на какое соревнование тебе хочеться попасть?',
                                 reply_markup=choose_competition)
            if data['st'] == "rf":
                bot.send_message(call.message.chat.id, 'В каком соревновании вы уже учавствуете?',
                                 reply_markup=choose_competition)
            if data['st'] == "cic":
                check_person = check_person_in_competition(data['cn'], call.message.chat.username)
                if check_person:
                    if data['ost'] == 'rt':
                        bot.send_message(call.message.chat.id,
                                         'Вы уже были зарегестрированы в этом соревновании.\nЧтобы зайти в личный кабинет напишите /lk')
                    elif data['ost'] == 'rf':
                        bot.send_message(call.message.chat.id,
                                         'Вы учавствуете в соревновании\nЧтобы зайти в личный кабинет напишите /lk')
                    global competition_name
                    competition_name = data['cn']
                elif not check_person:
                    if data['ost'] == 'rf':
                        bot.send_message(call.message.chat.id,
                                         'Вы не зарегистрированы на данном соревновании\nЧтобы зарегистрироваться напишите /start')
                    elif data['ost'] == 'rt':
                        bot.send_message(call.message.chat.id, 'Надо пройти регистрацию')
                        bot.send_message(call.message.chat.id, "Введите имя и фамилию: ")
                        user_data = []

                        @bot.message_handler(content_types='text')
                        def take_company_name(message):
                            user_data.append(message.text)
                            bot.send_message(call.message.chat.id, "Введите компанию: ")
                            bot.register_next_step_handler(message, registration_sucsess)

                        def registration_sucsess(message):
                            user_data.append(message.text)
                            insert_person(data['cn'],
                                          [(f'{user_data[0]}', user_data[1], message.chat.username)])
                            bot.send_message(call.message.chat.id,
                                             f"{user_data[0]} вы успешно прошли регистрацию на соревнование {data['cn']}\nЧтобы зайти в личный кабинет набирите команду /lk")
                            global competition_name
                            competition_name = data['cn']

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
