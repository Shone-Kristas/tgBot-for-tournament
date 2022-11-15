import telebot
from telebot import types
import gspread
import random
import requests
from bs4 import BeautifulSoup

bot_token = ''
googlesheet_id = ''
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account()

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Первый этап: Внести имя персонажа (слитно или через пробел)")


@bot.message_handler(commands=['player'])
def send_players(message):
    Battle_file = open('Battle.txt', 'r')
    list_battle = [heroes.strip() for heroes in Battle_file]
    Battle_file.close()
    global list_hero_player1
    global list_hero_player2
    global list_hero_player3
    global list_hero_player4
    list_hero_player1 = list_battle.copy()
    list_hero_player2 = list_battle.copy()
    list_hero_player3 = list_battle.copy()
    list_hero_player4 = list_battle.copy()
    player_all = types.InlineKeyboardMarkup(row_width=1)
    player_1 = types.InlineKeyboardButton(text='Первый', callback_data='Первый')
    player_2 = types.InlineKeyboardButton(text='Второй', callback_data='Второй')
    player_3 = types.InlineKeyboardButton(text='Третий', callback_data='Третий')
    player_4 = types.InlineKeyboardButton(text='Четверый', callback_data='Четвертый')
    player_all.add(player_1, player_2, player_3, player_4)
    bot.send_message(message.chat.id, 'Номер игрока', reply_markup=player_all)


@bot.callback_query_handler(lambda call: call.data=='Первый' or call.data=='Второй' or call.data=='Третий' or call.data=='Четвертый')
def callback_query_players(call):
    global tittle
    if call.data == 'Первый':
        tittle = 1
        bot.send_message(call.message.chat.id, "Оценивает первый игрок")
        bot.send_message(call.message.chat.id, "Используйте /point")
    elif call.data == 'Второй':
        tittle = 2
        bot.send_message(call.message.chat.id, "Оценивает второй игрок")
        bot.send_message(call.message.chat.id, "Используйте /point")
    elif call.data == 'Третий':
        tittle = 3
        bot.send_message(call.message.chat.id, "Оценивает третий игрок")
        bot.send_message(call.message.chat.id, "Используйте /point")
    elif call.data == 'Четвертый':
        tittle = 4
        bot.send_message(call.message.chat.id, "Оценивает четвертый игрок")
        bot.send_message(call.message.chat.id, "Используйте /point")

@bot.message_handler(commands=['point'])
def send_point(message):
    global heroes_first

    picture = types.InlineKeyboardButton(text='Напомнить кто это?', callback_data='picture')
    button_photo = types.InlineKeyboardMarkup(row_width=4).add(picture)
    one = types.InlineKeyboardButton(text='1', callback_data='one')
    two = types.InlineKeyboardButton(text='2', callback_data='two')
    thre = types.InlineKeyboardButton(text='3', callback_data='three')
    four = types.InlineKeyboardButton(text='4', callback_data='four')
    five = types.InlineKeyboardButton(text='5', callback_data='five')
    six = types.InlineKeyboardButton(text='6', callback_data='six')
    seven = types.InlineKeyboardButton(text='7', callback_data='seven')
    eight = types.InlineKeyboardButton(text='8', callback_data='eight')
    nine = types.InlineKeyboardButton(text='9', callback_data='nine')
    ten = types.InlineKeyboardButton(text='10', callback_data='ten')
    button_photo.add(one, two, thre, four, five, six, seven, eight, nine, ten)
    if tittle == 1 and len(list_hero_player1) != 0:
        heroes_first = list_hero_player1.pop(0)
        bot.send_message(message.chat.id, heroes_first, reply_markup=button_photo)
    elif tittle == 2 and len(list_hero_player2) != 0:
        heroes_first = list_hero_player2.pop(0)
        bot.send_message(message.chat.id, heroes_first, reply_markup=button_photo)
    elif tittle == 3 and len(list_hero_player3) != 0:
        heroes_first = list_hero_player3.pop(0)
        bot.send_message(message.chat.id, heroes_first, reply_markup=button_photo)
    elif tittle == 4 and len(list_hero_player4) != 0:
        heroes_first = list_hero_player4.pop(0)
        bot.send_message(message.chat.id, heroes_first, reply_markup=button_photo)
    elif len(list_hero_player1) == 0 or len(list_hero_player2) == 0 or len(list_hero_player3) == 0 or len(list_hero_player4) == 0:
        bot.send_message(message.chat.id, 'Выберите следующего игрока /player')

global total_one
total_one = []
global total_two
total_two = []
global total_three
total_three = []
global total_four
total_four = []
global total_five
total_five = []
global total_six
total_six = []
global total_seven
total_seven = []
global total_eight
total_eight = []
global total_nine
total_nine = []
global total_ten
total_ten = []

@bot.callback_query_handler(lambda call: call.data=='picture' or call.data=='one' or call.data=='two' or call.data=='three' or call.data=='four' or call.data=='five' or call.data=='six' or call.data=='seven' or call.data=='eight' or call.data=='nine' or call.data=='ten')
def callback_query_picture(call):
    points = []
    if call.data == 'picture':
        url = (f"https://yandex.ru/images/search?text={heroes_first}&from=tabbar")

        r = requests.get(url)
        t = r.text

        soup = BeautifulSoup(t, 'lxml')
        photo_url = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        list_photo = [image['src'] for image in photo_url]
        random.shuffle(list_photo)
        bot.send_photo(call.message.chat.id, f'https:{list_photo[0]}')
    elif call.data == 'one':
        point = '1'
        total_one.append(point)
        if 10 >= len(total_one):
            bot.send_message(call.message.chat.id, f"1 - осталось {10 - len(total_one)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_one) > 10:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'two':
        point = '2'
        total_two.append(point)
        if 10 >= len(total_two):
            bot.send_message(call.message.chat.id, f"2 - осталось {10 - len(total_two)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_two) > 10:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'three':
        point = '3'
        total_three.append(point)
        if 8 >= len(total_three):
            bot.send_message(call.message.chat.id, f"3 - осталось {8 - len(total_three)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_three) > 8:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'four':
        point = '4'
        total_four.append(point)
        if 8 >= len(total_four):
            bot.send_message(call.message.chat.id, f"4 - осталось {8 - len(total_four)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_four) > 8:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'five':
        point = '5'
        total_five.append(point)
        if 6 >= len(total_five):
            bot.send_message(call.message.chat.id, f"5 - осталось {6 - len(total_five)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_five) > 6:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'six':
        point = '6'
        total_six.append(point)
        if 6 >= len(total_six):
            bot.send_message(call.message.chat.id, f"6 - осталось {6 - len(total_six)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_six) > 6:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'seven':
        point = '7'
        total_seven.append(point)
        if 6 >= len(total_seven):
            bot.send_message(call.message.chat.id, f"7 - осталось {6 - len(total_seven)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_seven) > 6:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'eight':
        point = '8'
        total_eight.append(point)
        if 4 >= len(total_eight):
            bot.send_message(call.message.chat.id, f"8 - осталось {4 - len(total_eight)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_eight) > 4:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'nine':
        point = '9'
        total_nine.append(point)
        if 4 >= len(total_nine):
            bot.send_message(call.message.chat.id, f"9 - осталось {4 - len(total_nine)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_nine) > 4:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")
    elif call.data == 'ten':
        point = '10'
        total_ten.append(point)
        if 2 >= len(total_ten):
            bot.send_message(call.message.chat.id, f"10 - осталось {2 - len(total_ten)}")
            points.append(point)
            points.append(heroes_first)
            sh = gc.open_by_key(googlesheet_id)
            sh.get_worksheet(tittle).append_row(points)
        elif len(total_ten) > 2:
            bot.send_message(call.message.chat.id, "Лимит очков исчерпан")


list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64]
global heroes
heroes = []


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        random.shuffle(list)
        hero_first_number = list.pop(0)
        hero_number = hero_first_number
        global hero_name
        hero_name = message.text.title()
        
        text_message = f'В таблицу добавлена запись: {hero_name}, {hero_number}'
        bot.send_message(message.chat.id, text_message)

        heroes.append(hero_name)
        if len(heroes) == 64:
            Battle_file = open('Battle.txt', 'w')
            for index in heroes:
                Battle_file.write(index + '\n')
            Battle_file.close()
        kaneki = []
        kaneki.append(hero_number)
        kaneki.append(hero_name)
        
        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row(kaneki)
        return heroes
    except:
        bot.send_message(message.chat.id, "Выберите игрока, кто начнёт расставлять оценки: с помощью команды /player)")
    


if __name__ == '__main__':
    bot.polling(none_stop=True)
