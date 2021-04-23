import datetime
import random
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from requests import get

TOKEN = '1720450815:AAFwgom5PsIguFBYTFvsEJnok0IejNpAC_E'
state = 1


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("end", end))
    dp.add_handler(CommandHandler("rename", rename))
    dp.add_handler(CommandHandler("add_joke", add_joke))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(MessageHandler(Filters.text, text))
    updater.start_polling()
    updater.idle()


def first_choice(update, context):
    global state
    if update.message.text == 'давай':
        site(update, context)
        close_keyboard(update, context)
    elif update.message.text == 'нехочу':
        persuade(update, context)
    elif update.message.text == 'Нет!':
        dialog(update, context)
    elif update.message.text == 'Мне надоел этот разговор.':
        end(update, context)
    elif update.message.text == 'Что ты умеешь делать?':
        state = 4
        skills(update, context)
    elif update.message.text == 'Расскажи о сайте.':
        state = 5
        about_site(update, context)


def function_choice(update, context):
    global state
    if update.message.text == 'Время':
        datetime_today(update, context)
    elif update.message.text == 'Игры':
        games(update, context)
    elif update.message.text == 'Не хочу играть!':
        skills_again(update, context)
    elif update.message.text == 'Камень, ножницы, бумага':
        state = 's_p_s'
        reply_keyboard = [['камень'], ['ножницы'], ['бумага'], ['мне надоело']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text("Игра начинается!", reply_markup=markup)
    elif update.message.text == 'Угадай число':
        state = 'g_num'
        generate_num(update, context)
        reply_keyboard = [['мне надоело']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text("Игра начинается!", reply_markup=markup)
    elif update.message.text == 'Шутки':
        jokes(update, context)
    elif update.message.text == 'Расскажи о сайте.':
        state = 5
        about_site(update, context)
    elif update.message.text == 'Что ты умеешь делать?':
        skills(update, context)


def site_choice(update, context):
    global state
    if update.message.text == 'Расскажи о товарах':
        goods(update, context)
    elif update.message.text == 'Расскажи о посетителях':
        users(update, context)
    elif update.message.text == 'Что ты умеешь делать?':
        state = 4
        skills(update, context)


def site(update, context):
    update.message.reply_text(
        "Сайт: http://store-model.herokuapp.com/")


def end(update, context):
    global state
    update.message.reply_text('Диалог окончен!')
    state = 3
    close_keyboard(update, context)


def text(update, context):
    global state
    if state == 1:
        return greeting(update, context)
    if state == 2:
        return first_choice(update, context)
    if state == 3:
        return end(update, context)
    if state == 4:
        function_choice(update, context)
    if state == 5:
        site_choice(update, context)
    if state == 's_p_s':
        s_p_s(update, context)
    if state == 'g_num':
        guess_number(update, context)
    if state == 'jokes':
        add_joke(update, state)


def add_joke(update, context):
    global state
    state = 'jokes'
    joke = update.message.text
    print(joke)
    if joke != '/add_joke':
        con = sqlite3.connect("db/jokes.db")
        cur = con.cursor()
        result = cur.execute("""SELECT jokes FROM jokes """).fetchall()
        id_sum = len(result) + 1
        print(joke)
        cur.execute("""INSERT INTO jokes(id, jokes) VALUES(?, ?)""", (id_sum, joke))
        con.commit()
        con.close()
        state = 4


def rename(update, context):
    global name
    update.message.reply_text("введите свое имя по которому я буду к вам обращаться.")
    name = update.message.text


def start(update, context):
    global state
    state = 1
    greeting(update, context)


def help(update, context):
    update.message.reply_text("Я владею некоторыми функциями:")
    update.message.reply_text("/start - запускает или перезапускает программу")
    update.message.reply_text("/site - ссылка на сайт")
    update.message.reply_text("/end - заканчивает программу")
    update.message.reply_text("/add_joke - добавляет шутку, которую будет рассказывать бот")
    update.message.reply_text('/rename - позволяет смнеить имя по'
                              ' которому я буду обращаться к вам в будущем.'
                              ' P.S. Кроме как вначале моей работы,'
                              ' я к вам по имене не обращаюсь')


def greeting(update, context):
    global state
    state = 2
    reply_keyboard = [['давай', 'нехочу']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Приветствую вас! Я бот консультант магазина pepeShop!')
    update.message.reply_text(f'Вас зовут update.message.chat.first_name, не так ли?')
    update.message.reply_text('Рекомендую посетить наш сайт!', reply_markup=markup)


def persuade(update, context):
    reply_keyboard = [['Нет!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('И все же, я рекомендую пройти на сайт вот по этой ссылке:',
                              reply_markup=markup)
    site(update, context)


def dialog(update, context):
    reply_keyboard = [['Расскажи о сайте.'], ['Что ты умеешь делать?'],
                      ['Мне надоел этот разговор.']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Хорошо. Тогда что ты хочешь от меня?',
                              reply_markup=markup)


def datetime_today(update, context):
    update.message.reply_text(str(datetime.datetime.now()))


def games(update, context):
    reply_keyboard = [['Камень, ножницы, бумага'], ['Угадай число'], ['Не хочу играть!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Во что вы хотите поиграть?', reply_markup=markup)
    update.message.reply_text('Камень, ножницы, бумага.')
    update.message.reply_text('Угадай число')


def s_p_s(update, context):
    global state
    game_list = ['камень', 'ножницы', 'бумага', 'мне надоело']
    bot_list = ['камень', 'ножницы', 'бумага']
    player = update.message.text
    if not (player in game_list):
        return
    if update.message.text == 'мне надоело':
        state = 4
        update.message.reply_text('Ок')
        skills_again(update, context)
        return
    bot = random.choice(bot_list)
    update.message.reply_text(bot)
    if player == bot:
        update.message.reply_text('ничья')
    elif player == 'камень' and bot == 'ножницы':
        update.message.reply_text('Ты победил')
    elif player == 'ножницы' and bot == 'бумага':
        update.message.reply_text('Ты победил')
    elif player == 'бумага' and bot == 'камень':
        update.message.reply_text('Ты победил')
    elif player == 'камень' and bot == 'бумага':
        update.message.reply_text('Ты проиграл')
    elif player == 'бумага' and bot == 'ножницы':
        update.message.reply_text('Ты проиграл')
    elif player == 'ножницы' and bot == 'камень':
        update.message.reply_text('Ты проиграл')


def generate_num(update, context):
    global number
    number = random.randint(1, 100)
    update.message.reply_text('Угадай число от 1 до 100')


def guess_number(update, context):
    global state
    try:
        if update.message.text == 'мне надоело':
            state = 4
            update.message.reply_text('Ок')
            skills_again(update, context)
            return
        user = int(update.message.text)
        if user > number:
            update.message.reply_text("Число должно быть меньше!")
        elif user < number:
            update.message.reply_text("Число должно быть больше!")
        else:
            update.message.reply_text("Вы угадали, это число = " + str(number))
            state = 4
            update.message.reply_text('Ок')
            skills_again(update, context)
            return
    except ValueError:
        return


def skills(update, context):
    reply_keyboard = [['Игры'], ['Время'], ['Шутки'], ['/help'],
                      ['Расскажи о сайте.'], ['/end']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Я умею...', reply_markup=markup)
    update.message.reply_text('Я могу предложить тебе поиграть в пару игр.')
    update.message.reply_text('Еще я могу назвать точное время.')
    update.message.reply_text('Также я могу рассказывать веселые шутки,'
                              ' а если ты хочешь научить меня, тобы я рассказывал твою шутку,'
                              ' то используй команду /add_joke')
    update.message.reply_text('Ну и могу тебе рассказать о коммандах, если ты напишешь /help')


def jokes(update, context):
    con = sqlite3.connect("db/jokes.db")
    cur = con.cursor()
    result = cur.execute("""SELECT jokes FROM jokes """).fetchall()
    id_sum = len(result)
    jokes_num = random.randint(1, id_sum)
    result = cur.execute("""SELECT jokes FROM jokes WHERE id = ? """, (jokes_num,)).fetchall()
    update.message.reply_text(*result[0])
    con.close()


def skills_again(update, context):
    reply_keyboard = [['Игры'], ['Время'], ['Шутки'], ['/help'],
                      ['Расскажи о сайте.'], ['/end']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Чего ты хочешь сейчас?', reply_markup=markup)


def about_site(update, context):
    reply_keyboard = [['Расскажи о товарах'], ['Расскажи о посетителях'],
                      ['Что ты умеешь делать?'], ['/help'], ['/end']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Этот сайт представляет собой'
                              ' самую лучшую торговую площадку в мире!', reply_markup=markup)
    update.message.reply_text('Здесь ты можешь приобрести самые крутые вещи!')
    update.message.reply_text('Этот сайт сделали три гениальных программиста.')
    update.message.reply_text('Ну и лови ссылочку на сайт.')
    site(update, context)


def goods(update, context):
    goods = get('http://store-model.herokuapp.com/api/goods').json()
    if not goods['goods']:
        update.message.reply_text('К сожалению на данный момент на торговой площадке нет'
                                  ' товаров, но вы все еще можете перейти туда и'
                                  ' выставить на продажу свой товар.')
        site(update, context)
        return
    for i in range(len(goods['goods'])):
        good_price = goods['goods'][i]['price']
        good_name = goods['goods'][i]['name']
        update.message.reply_text(f'предмет: {good_name}, цена: {good_price}')
        goods_num = i + 1
    if goods_num >= 3:
        update.message.reply_text(f'Кстати, в последние времятовар:'
                                  f' {goods["goods"][random.randint(0, goods_num)]["name"]}'
                                  f'очень популярен. Рекомендую купить')
    update.message.reply_text('Более подробную информацию о товарах ты найдешь на сайте.')
    site(update, context)


def users(update, context):
    update.message.reply_text('Неужели ты думаешь что я буду распростронять'
                              ' информацию о наших клиянтах. Никогда!')


def close_keyboard(update, context):
    update.message.reply_text('Пока', reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    main()










