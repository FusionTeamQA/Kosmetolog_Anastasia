# -*- coding: utf-8 -*-
import telebot
from telebot import types
import setting
import logging
import sqlite3
from datetime import datetime
import os, sys
import time
from requests.exceptions import ConnectionError, ReadTimeout

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log'
                    )
bot = telebot.TeleBot(setting.token)

user_dict = {}
user_chats = 0

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")


class User:

    def __init__(self, name):
        self.name = None
        self.age = None
        self.nums = None
        self.location = None
        self.experience = None
        self.format_work = None

        keys = ['name', 'age', 'nums', 'location', 'experience', 'format_work']
        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])  # стартовая команда
def start(message):
    conn = sqlite3.connect('bd/database2.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER, 
            user_first_name TEXT, 
            user_last_name TEXT, 
            username TEXT,
            data_time varchar(50)
            )''')
    conn.commit()
    people_id = message.from_user.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        USER_ID = [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                   message.from_user.username, dt_string]
        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?);", USER_ID)
        print("Новый юзер добавлен в базу данных")
        conn.commit()
    else:
        print(message.from_user.username)
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Записаться на услугу📆")
    btn2 = types.KeyboardButton('Посмотреть прайс💰')
    btn3 = types.KeyboardButton('Подробнее о программах 🌱')
    btn4 = types.KeyboardButton('Как подготовиться к визиту 📄')
    btn5 = types.KeyboardButton('Противопоказания🙅🏻‍')
    btn6 = types.KeyboardButton('Рекомендации после процедур🙋🏻')
    btn7 = types.KeyboardButton('Контактная информация☎️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.from_user.id, "👋Привет, я бот косметолога и мастера лазерной эпиляции Анастасии",
                     reply_markup=markup)
    bot.send_message(message.from_user.id, 'Помогу тебе:👇')
    bot.send_message(message.from_user.id, '-Записаться на услугу\n'
                                           '-Узнать стоимость услуг\n'
                                           '-Подробнее ознакомиться с уходовыми программами\n'
                                           '-Узнать как подготовиться к процедуре\n'
                                           '-Ознакомиться с противопоказаниями\n'
                                           '-Дам рекомендации после процедур\n'
                                           'А так же напомню адрес кабинета и номер телефона\n')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Записаться на услугу📆':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Я знаю какую услугу выбрать')
        btn2 = types.KeyboardButton('Я не знаю какую услугу выбрать, нужна консультация')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'В этом разделе ты можешь выбрать удобную опцию для записи:',
                         reply_markup=markup, parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         '✔️если ты знаешь на какую процедуру хочешь записаться, жми соответствующую кнопку, '
                         'и я переведу тебя на страницу онлайн записи и ты сама сможешь подобрать удобное время.',
                         reply_markup=markup, parse_mode='HTML')
        bot.send_message(message.from_user.id, '✔️если ты ещё не определилась с услугой и тебе нужна консультация, '
                                               'или если в онлайн записи нет подходящего времени жми вторую кнопку, '
                                               'и я переведу тебя в  личный чат с Анастасией»', reply_markup=markup,
                         parse_mode='HTML')

    elif message.text == 'Я знаю какую услугу выбрать':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Выбрать услугу и записаться", setting.DIKIDI))
        bot.send_message(message.from_user.id,
                         'Перейдите по ссылке или нажмите на кнопку чтобы записаться на прием \n'
                         + setting.DIKIDI,
                         reply_markup=markup2, parse_mode='HTML')

    elif message.text == 'Я не знаю какую услугу выбрать, нужна консультация':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Получить консультацию", setting.telegram_anastasia))
        bot.send_message(message.from_user.id,
                         'Нажмите на кнопку "Получить консультацию"\n'
                         'для связи с Анастасией',
                         reply_markup=markup2, parse_mode='HTML')

    elif message.text == 'Посмотреть прайс💰':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Эстетическая косметология')
        btn2 = types.KeyboardButton('Лазерная эпиляция')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '⬇ В этом разделе ты можешь ознакомиться с '
                                               'актуальными ценами на услуги, для того что бы тебе удобнее было '
                                               'искать нужную услугу прайс разделён по категориям,'
                                               'выбирай нужную и я пришлю тебе информацию', reply_markup=markup, parse_mode='HTML')

    elif message.text == 'Эстетическая косметология':
        bot.send_photo(message.from_user.id, open('File/Estetic/photo_2023-03-06 11.39.09.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Estetic/photo_2023-03-06 11.39.11.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Estetic/photo_2023-03-06 11.39.12.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Estetic/photo_2023-03-06 11.39.14.jpeg', 'rb'))

    elif message.text == 'Лазерная эпиляция':
        bot.send_photo(message.from_user.id, open('File/Laser/photo_2023-03-06 11.22.37.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Laser/photo_2023-03-06 11.22.40.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Laser/photo_2023-03-06 11.22.42.jpeg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/Laser/photo_2023-03-06 11.22.44.jpeg', 'rb'))


    elif message.text == 'Разработчик Fullstack':
        logging.info('Открыт раздел Разработчик, юзер - ' + message.chat.username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🔙 Главное меню')
        markup.add(btn1)
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton("Открыть вакансию", setting.DEV_FULL))
        bot.send_message(message.from_user.id,
                         'Разработчик Fullstack -->>> Перейти к разделу можно по ссылке ' + setting.DEV_FULL,
                         reply_markup=markup2, parse_mode='HTML')

    elif message.text == 'Подробнее о программах 🌱':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Чистка')
        btn2 = types.KeyboardButton('Микронидлинг')
        btn3 = types.KeyboardButton('Пилинг программы')
        btn4 = types.KeyboardButton('Комплексные уходовые программы')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id,
                         '⬇ В этом разделе дана краткая справка по каждой из услуг эстетической косметологии, '
                         'переходи в нужный раздел и выбирай программу, а я расскажу тебе о ней все что знаю. ',
                         reply_markup=markup, parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Если у тебя останутся вопросы, ты можешь вернуться в предыдущий раздел, '
                         'и нажав кнопку «Контактная информация» перейти в диалог с Анастасией, и она ответит все твои вопросы',
                         reply_markup=markup, parse_mode='HTML')

    elif message.text == 'Чистка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Ультразвуковая чистка лица')
        btn2 = types.KeyboardButton('Мануальная чистка')
        btn3 = types.KeyboardButton('Комбинированная чистка')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, 'Какая чистка тебя интересует? ⬇', reply_markup=markup,
                         parse_mode='HTML')

    elif message.text == 'Ультразвуковая чистка лица':
        bot.send_message(message.from_user.id, 'Самая востребованная процедура круглый год.', parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Это обусловлено тем, что применение ультразвука помогает эффективно очистить кожу, не травмируя ее.',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Ультразвуковая чистка может проводиться в любое время года, показана любому типу кожи, даже чувствительной.',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Ультразвуковая чистка позволяет: 💁‍♀️\n'
                                               '✅Очистить кожу от внешних загрязнений \n'
                                               '✅Удалить омертвевшие клетки эпидермиса \n'
                                               '✅Открыть протоки сальных желёз \n'
                                               '✅Улучшить кровоснабжение\n', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Что ты получишь после процедуры: 💁‍♀️\n'
                                               '✅Уменьшится отечность\n'
                                               '✅Выровняется цвет лица а кожа станет свежей и мягкой\n',
                         parse_mode='HTML')

    elif message.text == 'Мануальная чистка':
        bot.send_message(message.from_user.id,
                         'Мануальная чистка лица  направлена на очищение кожи от ороговевшего эпителия, '
                         'излишков жира, угревой сыпи, чёрных точек. '
                         'Процедура проводится с строгим соблюдением специальных техник выполнения манипуляций.',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Общая продолжительность сеанса составляет в среднем 1,5 – 2 часа. '
                                               'Все зависит от состояния кожного покрова а так же степени выраженности косметических ньюансов.',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Сразу после сеанса на коже, подвергшейся обработке, могут появиться покраснения, небольшая отечность, раздражение поэтому важно помнить, '
                         'что процедура чистки требует определенного периода реабилитации. '
                         'Не стоит планировать чистку, перед важными мероприятиями. ', parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Эти симптомы считаются вариантом нормы и исчезают через 12 – 24 часа без специального лечения. '
                         'Если же дерма тонкая, чувствительная, склонна к воспалениям, побочные эффекты в виде гиперемии и отека могут сохраняться в течение 2 – 3 суток. '
                         'В этот период важно строго соблюдать рекомендации косметолога, касающиеся реабилитационного восстановления',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Так же Важно помнить, что после чистки в первые 3-5 дней не рекомендуется использовать декоративную косметику, '
                         'а помагать коже восстанавливаться индивидуально подобранными уходовыми средствами.',
                         parse_mode='HTML')
        bot.send_message(message.from_user.id,
                         'Через несколько дней после процедуры поверхностные слои эпидермиса начинают отмирать и слущиваться. Внешне это проявляется незначительным шелушением, '
                         'которое быстро проходит при условии регулярного использования увлажняющих косметических средств. '
                         'В это же время запускаются естественные процессы регенерации клеток дермы, что способствует не только очищению, '
                         'но и эффективному омоложению кожного покрова.', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Показания к мануальной чистке: ℹ️\n'
                                               'Ручная чистка лица подходит для любого типа кожи, но наиболее выраженный эффект будут наблюдать обладатели жирной, '
                                               'пористой, склонной к воспалениям дермы. Основные показания к процедуре такие:\n'
                                               'ℹ️расширенные поры \n'
                                               'ℹ️повышенная активность сальных желез \n'
                                               'ℹ️склонность к многочисленным высыпаниям, акне \n'
                                               'ℹ️пониженный тонус кожи \n'
                                               'ℹ️жировики, милиумы и другие дерматологические дефекты \n'
                                               'ℹ️черные угри, склонные к воспалениям \n'
                                               'ℹ️неровня поверхность кожного покрова \n'
                                               'ℹ️фурункулы \n', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Что ты получишь после процедуры: 💁‍♀️\n'
                                               'Первые дни после процедуры может усилиться салоотделение и шелушение. Эффект чистки можно оценить спустя 5 – 7 суток:\n'
                                               '✅очищенные поры суживаются\n'
                                               '✅кожа становится гладкой, упругой, сияющей, матовой\n'
                                               '✅выравнивается микрорельеф\n'
                                               '✅исчезает жирный блеск\n'
                                               '✅лицо выглядит посвежевшим, помолодевшим\n'
                                               '✅нормализуется работа сальных желез\n', parse_mode='HTML')

    elif message.text == 'Комбинированная чистка':
        bot.send_message(message.from_user.id, 'Комбинированная чистка лица – процедура, подразумевающая совмещение '
                                               'сразу двух методик очищения кожи: '
                                               'аппаратную (ультразвуковую) и мануальную (ручную). '
                                               'На сегодняшний день это один из самых эффективных способов глубокого '
                                               'очищения '
                                               'способствующий борьбе с дефектами на лице.', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Что ты получишь после процедуры: 💁‍♀️\n'
                                               '✅Очищение кожи от поверхностных и глубоких загрязнений\n'
                                               '✅Ровные тон\n'
                                               '✅Гладкий рельеф \n'
                                               '✅Здоровый вид лица \n', parse_mode='HTML')

    elif message.text == 'Микронидлинг':
        bot.send_photo(message.from_user.id, open('File/Programms/Micronidling/IMG_7564.jpg', 'rb'))

    elif message.text == 'Пилинг программы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Гидрореставрация кожи')
        btn2 = types.KeyboardButton('Атравматичная пилинг-чистка')
        btn3 = types.KeyboardButton('Ретиноловая DERMA-реконструкция')
        btn4 = types.KeyboardButton('Комплексный фитиновый пилинг')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, 'Выбери интересующую программу пилинга🍀', reply_markup=markup,
                         parse_mode='HTML')

    elif message.text == 'Гидрореставрация кожи':
        bot.send_photo(message.from_user.id, open('File/Programms/Piling/1.jpg', 'rb'))

    elif message.text == 'Атравматичная пилинг-чистка':
        bot.send_photo(message.from_user.id, open('File/Programms/Piling/2.jpg', 'rb'))

    elif message.text == 'Ретиноловая DERMA-реконструкция':
        bot.send_photo(message.from_user.id, open('File/Programms/Piling/3.jpg', 'rb'))

    elif message.text == 'Комплексный фитиновый пилинг':
        bot.send_photo(message.from_user.id, open('File/Programms/Piling/4.jpg', 'rb'))

    elif message.text == 'Комплексные уходовые программы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Экспресс-программа HYDRA SPA THERAPY')
        btn2 = types.KeyboardButton('Программа «Классика омоложения»')
        # btn3 = types.KeyboardButton('Программа активного увлажняющего детокс-ухода')
        btn4 = types.KeyboardButton('Экспресс-уход за жирной, комбинированной, проблемной кожей')
        markup.add(btn1, btn2, btn4)
        bot.send_message(message.from_user.id,
                         'Комплексные программы направлены на заботу и поддержание здорового и ухоженного вида твоей кожи🌸. '
                         'Во время проведения комплекса не используются травмирующие методики работы,'
                         'а это значит, что ты сможешь расслабиться и насладиться процессом ухода за твоей кожей.'
                         'Помни, при желании, к каждой программе мы можем добавить 30 минут массажа либо дополнительную маску',
                         reply_markup=markup, parse_mode='HTML')


    elif message.text == 'Экспресс-программа HYDRA SPA THERAPY':
        bot.send_photo(message.from_user.id, open('File/Programms/Kompleks/1.jpg', 'rb'))

    elif message.text == 'Программа «Классика омоложения»':
        bot.send_photo(message.from_user.id, open('File/Programms/Kompleks/2.jpg', 'rb'))

    # elif message.text == 'Программа активного увлажняющего детокс-ухода':
    #     bot.send_photo(message.from_user.id, open('File/Programms/Kompleks/3.jpg', 'rb'))

    elif message.text == 'Экспресс-уход за жирной, комбинированной, проблемной кожей':
        bot.send_photo(message.from_user.id, open('File/Programms/Kompleks/4.jpg', 'rb'))

    elif message.text == 'Как подготовиться к визиту 📄':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Подготовка - Лазерная эпиляция')
        btn2 = types.KeyboardButton('Подготовка - Эстетическая косметология')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id,
                         'Как подготовиться к визиту?',
                         reply_markup=markup, parse_mode='HTML')

    elif message.text == 'Подготовка - Лазерная эпиляция':
        bot.send_photo(message.from_user.id, open('File/Helps/1.jpg', 'rb'))

    elif message.text == 'Подготовка - Эстетическая косметология':
        bot.send_message(message.from_user.id, 'Комплексные эстетические программы не требуют определённой подготовки, '
                                               'все что вам нужно это взять хорошее настроение 😉', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Рекомендации перед чисткой лица: \n'
                                               '❕Помните, процедура чистки требует некоторого реабилитационного периода, '
                                               'поэтому не стоит делать ее перед важным событием или мероприятием.\n '
                                               '❕Старайтесь не делать чистку в период менструации,'
                                               'это позволит снизить вероятность возникновения воспалительных элементов после процедуры.\n',
                         parse_mode='HTML')


    elif message.text == 'Контактная информация☎️':
        bot.send_location(message.from_user.id, 61.077953, 72.611660)
        bot.send_message(message.from_user.id, '📍г. Нефтеюганск, ул. Южная 1, лестница слева, 3 этаж, 309 кабинет \n'
                                               'Контактный номер: 89505061150', parse_mode='HTML')
        bot.send_contact(message.from_user.id, '89505061150', 'Anastasia', 'Prusak')

    elif message.text == 'Рекомендации после процедур🙋🏻':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Рекомендации "Лазерная эпиляция"')
        btn2 = types.KeyboardButton('Рекомендации "Чистка"')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Помни, что некоторые процедуры требуют соблюдения рекомендаций в '
                                               'период реабилитации, в этом разделе ты найдёшь всю необходимую информацию',
                         reply_markup=markup, parse_mode='HTML')

    elif message.text == 'Рекомендации "Лазерная эпиляция"':
        bot.send_photo(message.from_user.id, open('File/Helps/2.jpg', 'rb'))

    elif message.text == 'Рекомендации "Чистка"':
        bot.send_message(message.from_user.id, '❗️В первые сутки после процедуры не принимайте ванную и горячий душ.\n'
                                               '❗️Откажитесь от посещения сауны, бани, бассейна и тренажерного зала на 1-2 суток.\n'
                                               '❗️Избегайте загара (в том числе в солярии) 5-7 дней после чистки.\n'
                                               '❗️По возможности откажитесь от декоративной косметики в первые 1-2 суток.\n'
                                               '❗️В день после процедуры обязательно смените наволочку на подушке на чистую! '
                                               'А так же замените обычное полотенце для лица на бумажные. \n'
                                               '❗️Вы должны быть готова к тому, что после процедуры, особенно первичной, возможно появление единичных воспалительных элементов, '
                                               'помните давить их ни в коем случае нельзя! '
                                               'Используйте водный раствор хлоргексидина, протирайте им лицо минимум 2 раза в день и '
                                               'воспаления пройдут самостоятельно.\n'
                                               '❗️Так же возможно шелушение-это нормальный процесс обновления кожи. '
                                               'Не стоит травмировать чешуйки использованием скарба или пилинга без рекомендации специалиста.\n'
                                               '❗️Соблюдайте рекомендации специалиста по уходу после процедуры\n',
                         parse_mode='HTML')

    elif message.text == 'Противопоказания🙅🏻‍':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Противопоказания "Лазерная эпиляция"')
        btn2 = types.KeyboardButton('Противопоказания "Микронидлинг"')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Помни, что некоторые процедуры имеют свои противопоказания. \n'
                                               'Изучи внимательно каждый из разделов.', reply_markup=markup,
                         parse_mode='HTML')


    elif message.text == 'Противопоказания "Лазерная эпиляция"':
        bot.send_photo(message.from_user.id, open('File/NoN/1.jpg', 'rb'))
        time.sleep(2)
        bot.send_photo(message.from_user.id, open('File/NoN/2.jpg', 'rb'))

    elif message.text == 'Противопоказания "Микронидлинг"':
        bot.send_photo(message.from_user.id, open('File/NoN/3.jpg', 'rb'))


# elif message.text == '🅱️ Мы на Behance':
#     logging.info('Открыт раздел Behance, юзер - ' + message.chat.username)
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     btn1 = types.KeyboardButton('🔙 Главное меню')
#     markup.add(btn1)
#     markup2 = types.InlineKeyboardMarkup()
#     markup2.add(types.InlineKeyboardButton("Перейти к нам на страницу", setting.BEHANCE))
#     bot.send_message(message.from_user.id,
#                      'With our expertise,we can suggest the best solutions for your project to make it as good as possible.'
#                      '\n Перейти к разделу можно по ссылке ' + setting.BEHANCE,
#                      reply_markup=markup2, parse_mode='HTML')

# elif message.text == '📝 Оставить заявку':
#     logging.info('Старт заявки' + message.chat.username)
#     chat_id = message.chat.id
#     msg = bot.send_message(chat_id, "Добрый день, представьтесь пожалуйста.")
#     bot.register_next_step_handler(msg, name_step)


# def name_step(message, user=None):
#     try:
#         chat_id = message.chat.id
#         name = message.text
#         user = User(name)
#         user_dict[chat_id] = user
#         msg = bot.send_message(chat_id, "Укажите ваш возраст")
#         bot.register_next_step_handler(msg, process_age_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
#
#
# def process_age_step(message):
#     try:
#         chat_id = message.chat.id
#         age = message.text
#         if not age.isdigit():
#             msg = bot.send_message(chat_id, 'Возраст должен быть числом, введи его повторно: ')
#             bot.register_next_step_handler(msg, process_age_step)
#             return
#         user = user_dict[chat_id]
#         user.age = age
#         msg = bot.send_message(chat_id, 'К какой специализации вы относитесь?', )
#
#         bot.register_next_step_handler(msg, process_spec_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
#
#
# def process_spec_step(message):
#     try:
#         chat_id = message.chat.id
#         language = message.text
#         user = user_dict[chat_id]
#         user.languages = language
#         msg = bot.send_message(chat_id, 'Локация')
#         bot.register_next_step_handler(msg, process_location_step)
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def process_location_step(message):
#     try:
#         chat_id = message.chat.id
#         location = message.text
#         user = user_dict[chat_id]
#         user.location = location
#         msg = bot.send_message(chat_id, 'Формат работы (удаленно/офис)')
#         bot.register_next_step_handler(msg, process_format_work_step)
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def process_format_work_step(message):
#     try:
#         chat_id = message.chat.id
#         format_work = message.text
#         user = user_dict[chat_id]
#         user.format_work = format_work
#         msg = bot.send_message(chat_id, 'Опыт работы?')
#         bot.register_next_step_handler(msg, process_experience_step)
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def process_experience_step(message):
#     try:
#         chat_id = message.chat.id
#         experience = message.text
#         user = user_dict[chat_id]
#         user.experience = experience
#         msg = bot.send_message(chat_id,
#                                'Вставьте ссылку на ваш профиль(GitHub,Behance,Dribbble,Figma,VK) если нет - напишите нет: ')
#         bot.register_next_step_handler(msg, process_git_acc_step)
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def process_git_acc_step(message):
#     try:
#         chat_id = message.chat.id
#         git_acc1 = message.text
#         user = user_dict[chat_id]
#         user.git_acc = git_acc1
#         msg = bot.send_message(chat_id, "Контактные данные")
#         bot.register_next_step_handler(msg, contnums)
#
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def contnums(message):
#     try:
#         chat_id = message.chat.id
#         nums = message.text
#         user = user_dict[chat_id]
#         user.nums = nums
#         chat_id = message.chat.id
#         msg = bot.send_message(chat_id, "Основные навыки")
#         bot.register_next_step_handler(msg, send_z)
#     except Exception as e:
#         bot.reply_to(message, 'Непредвиденная ошибка')
#
#
# def send_z(message):
#     chat_id = message.chat.id
#     first_name = message.chat.first_name
#     last_name = message.chat.last_name
#     user_name = message.chat.username
#     z = message.text  # text user
#     app_text = []
#     app_name_first = []
#     app_name_last = []
#     app_username = []
#     app_name_first.append(first_name)
#     app_name_last.append(last_name)
#     app_username.append(user_name)
#     app_text.append(z)
#     user = user_dict[chat_id]
#     user_chats = message.from_user.id
#     bot.send_message(setting.admin_id_ugraswim, f'Поступил новый отклик от {app_name_first[0]} {app_name_last[0]} !\n'
#                      + f'username в тг = @{app_username[0]} \n'
#                      + f'Возраст  -  {user.age} \n'
#                      + f'Локация  -  {user.location} \n'
#                      + f'Опыт работы  -  {user.experience} \n'
#                      + f'Специализация: {user.languages} \n'
#                      + f'Основные навыки: - {app_text[0]} \n'
#                      + f'Профиль github/социальная сеть  -  {user.git_acc} \n'
#                      + f'Формат работы  -  {user.format_work} \n'
#                      + f'Контактные данные: {user.nums} \n'
#
#                      + f'ID юзера: {user_chats}')
# bot.send_message(setting.admin_hr_id, f'Поступил новый отклик от {app_name_first[0]} {app_name_last[0]} !\n'
#                  + f'username в тг = @{app_username[0]} \n'
#                  + f'Возраст  -  {user.age} \n'
#                  + f'Локация  -  {user.location} \n'
#                  + f'Опыт работы  -  {user.experience} \n'
#                  + f'Специализация: {user.languages} \n'
#                  + f'Основные навыки: - {app_text[0]} \n'
#                  + f'Профиль github/социальная сеть  -  {user.git_acc} \n'
#                  + f'Формат работы  -  {user.format_work} \n'
#                  + f'Контактные данные: {user.nums} \n'
#
# #                  + f'ID юзера: {user_chats}')
# app_name_first.clear()
# app_name_last.clear()
# app_username.clear()
# app_text.clear()
# logging.info('Заявка успешно отправлена от - ' + message.chat.username)
# bot.send_message(chat_id, "Заявка отправлена, мы свяжемся с Вами в ближайшее время")


try:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=90, long_polling_timeout=5)
