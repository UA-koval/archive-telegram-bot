import telepot
import time
import json
import random
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import gc
gc.enable()

Deck = {}
Hand = {}
Table = {}

with open("AllCards.json", encoding="utf-8", errors="backslashreplace") as json_file:
    data = json.load(json_file)

manaConvert = {
	    '{0}':'0\U000020E3',
	    '{1}':'1\U000020E3',
	    '{2}':'2\U000020E3',
	    '{3}':'3\U000020E3',
	    '{4}':'4\U000020E3',
	    '{5}':'5\U000020E3',
	    '{6}':'6\U000020E3',
	    '{7}':'7\U000020E3',
	    '{8}':'8\U000020E3',
	    '{9}':'9\U000020E3',
	    '{10}':'1\U000020E30\U000020E3',
	    '{13}':'1\U000020E33\U000020E3',
	    '{15}':'1\U000020E35\U000020E3',
        '{X}':'*\U000020E3',
	    '{W}':'\U0001f7e1',
	    '{U}':'\U0001f535',
	    '{B}':'\U0001f7e3',
	    '{R}':'\U0001f534',
	    '{G}':'\U0001f7e2',
        '{T}':'\U00002935',
        '{C}':'\U000023FA'
	        }


def cardInfo(card):
    for key in data:
        try:
            for i in data[key]['foreignData']:
                if i['language'] == 'Russian':
                    if i['name'] == card:
                        card = key
        except KeyError:
            pass
    try: 
        checkCard = data[card]
    except KeyError:
        TelegramBot.sendMessage(chat_id,'Карта не найдена')
        return None
    ## print(data[card]['manaCost'])
    ## print(data[card]['text'])
    manaCost = ''
    cardName = card
    cardText = ''
    cardType = data[card]['type']
##    for key in manaConvert:
##        if data[card]['text'].find(key) !=       
#while current_card[:len(current_card)-1]
#    current_card = current_card[:len(current_card)-1]     
#current_card = current_card.rstrip()
#
    try:
    	cardText = (data[card]['text'])
    except KeyError:
    	data[card]['text'] = ''
    	
    try:
        for i in data[card]['foreignData']:
            if i['language'] == 'Russian':
                print(i)
                cardName = i['name']
                cardText = i['text']
                cardType = i['type']
    except KeyError:
        pass    	
    	
    try:
        manaCostRaw = data[card]['manaCost']
        manaChar = ''
        while manaCostRaw != '':
            manaChar = manaConvert[manaCostRaw[:3]]
            manaCost = manaCost + ' ' + str(manaChar)
            manaCostRaw = manaCostRaw[3:]
    except KeyError:
        manaCost = ''
    try:
        TelegramBot.sendMessage(chat_id, cardName + '   ' + manaCost + '\n\n' + cardType + '\n' + textEdit(cardText) + '\n[' + data[card]['power'] + '/' + data[card]['toughness'] + ']')
    except KeyError:
        try:
            TelegramBot.sendMessage(chat_id, cardName + '   ' + manaCost + '\n\n' + cardType + '\n' + textEdit(cardText) + '\n[' + data[card]['loyalty'] + ']')
        except KeyError:
            TelegramBot.sendMessage(chat_id, cardName + '   ' + manaCost + '\n\n' + cardType + '\n' + textEdit(cardText))

def textEdit(text):
    redactCheck = False
    string = text
    while redactCheck == False:
            redactCheck = True
            for key in manaConvert:
                    if string.find(key) != -1:
                            string = string[:string.find(key)] + manaConvert[key] + string[string.find(key)+3:]
                            redactCheck = False
    return string
# CARDINFO #

            
def Deckbuilding(input):
    print('Deckbuilding')
    line = (input)
    current_card = ''
    deck = []
    end = False
    length = 0
    printCodeFind = False
    while not end:
        i = int(line.partition('\n')[0][:2])
        current_card = line.partition('\n')[0][2:]
        length = len(line.partition('\n')[0]) + 1
        while current_card[len(current_card)-1].isdigit():
            current_card = current_card[:len(current_card)-1]     
        current_card = current_card.rstrip()
        
        if current_card[len(current_card)-1] == ')':
            printCodeFind = True
         
        while printCodeFind:
             current_card = current_card[:len(current_card)-1]
             if current_card[len(current_card)-1] == '(':
                 current_card = current_card[:len(current_card)-1]
                 printCodeFind = False
        current_card = current_card.strip()
        
        while i != 0:
            deck.append(current_card)
            i=i-1
        line = line[length:]
        if line.partition('\n')[0][:2] == '':
            end = True
    return deck
## DEF: DECKBUILDING END ##

def deal(deck, hand, num):
    if record == False:
        if len(deck) != 0:
            for i in range(num):
                card = random.randint(0,len(deck))
                hand.append(deck.pop(card))
                i=i-1
                handStr = ''
                for card in hand:
                    handStr = handStr + card + '\n'
            TelegramBot.sendMessage(chat_id, handStr)
        else:
            TelegramBot.sendMessage(chat_id, 'Колода отсутствует. Создать - /start')
    else:
        TelegramBot.sendMessage(chat_id, 'Колода отсутствует. Создать - /start')

TelegramBot = telepot.Bot(token)
print(TelegramBot.getMe())

markup = ReplyKeyboardRemove()
## 
##                     ['Plain text', KeyboardButton(text='Text only')],
##                     [dict(text='Phone'), KeyboardButton(text='Спрячь эту клаву')],
##                 ])
group_id = -1001488258241     #DEBUG################

update_id = 960658969
text = 0
message = []
chat_id = 0
record = {}
pick_id = 0
pick_card = ''

#Hand[314793167] = []
#Hand[314793167].append('Daretti, Ingenious Iconoclast')
#Hand[314793167].append('Daretti, Ingenious Iconoclast')
#Hand[314793167].append('Daretti, Ingenious Iconoclast')
#Hand[314793167].append('Daretti, Ingenious Iconoclast')

while True:
    try:
        try:
            message = TelegramBot.getUpdates(update_id+1)
            chat_id = message[0]['message']['chat']['id']
            print(message)
            print('\n   ' + message[0]['message']['from']['first_name'] + ' — ' + message[0]['message']['text'])

            if message[0]['message']['text'] == '/card' or message[0]['message']['text'] == '/card@mtgcropupier_bot' :
                TelegramBot.sendMessage(chat_id, '/card Cardname \nВыводит иформацию о карте. Если доступен русский язык - на русском. Писать на английском языке с большими буквами. Пример:\n/card Shock')
                
            elif message[0]['message']['text'].find('/card') != -1:
                print(message[0]['message']['text'][6:])
                cardInfo(message[0]['message']['text'][6:])
            
            elif message[0]['message']['text'] == '/start' or message[0]['message']['text'] == '/start@mtgcropupier_bot' :
                TelegramBot.sendMessage(chat_id, 'Экспортируйте свою колоду в формате MTG Arena, и отправьте в отет на это сообщение. Я принимаю карты толькотна английском языке. Каждая карта с новой строчки в формате "<количество> <название>", а так же с кодом набора (M20) и номером карты в наборе (125).',reply_markup=markup)
                record[message[0]['message']['from']['id']] = True

            elif message[0]['message']['text'] == '/deal' or message[0]['message']['text'] == '/deal@mtgcropupier_bot':
                try:
                    Hand[message[0]['message']['from']['id']] = []
                    deal(Deck[message[0]['message']['from']['id']], Hand[message[0]['message']['from']['id']], 7)
                    TelegramBot.sendMessage(group_id,message[0]['message']['from']['first_name'] + ' взял начальную руку')
                except KeyError:
                    TelegramBot.sendMessage(chat_id, 'Колода отсутствует. Создать - /start')
                    
            elif message[0]['message']['text'] == '/draw' or message[0]['message']['text'] == '/draw@mtgcropupier_bot':
                try:
                    deal(Deck[message[0]['message']['from']['id']], Hand[message[0]['message']['from']['id']], 1)
                    TelegramBot.sendMessage(group_id,message[0]['message']['from']['first_name'] + ' взял карту')
                except KeyError:
                    print('Колода отсутствует. Создать - /start')

            elif message[0]['message']['text'] == '/help' or message[0]['message']['text'] == '/help@mtgcropupier_bot':
                TelegramBot.sendMessage(chat_id, 'Чтобы пользоваться большинством комманд бота, вам нужно собрать колоду. Для этого перейдите в личные сообщения ко мне, или пишите прямо в чате, если, конечно, никого не стесняетесь. \n 1. /start - Записать новую колоду \n 2. Отпраьте колоду одним сообщ.\n 3. /deal - Взять 7 карт\n 4. /pick - Выбрать карту\n 5. /play - Разыграть ее\n\n  Дополнительные Инструменты:\n/play g или /playg - Разыграть карту сразу на кладбище\n/hand - Посмотреть вашу руку\n/view <Зона> <Имя игрока> - показывает стол/кладбище игрока.\n/move <Откуда> <Куда> <Номер> - Переместить карту\n/token [кол-во] <текст> - Создать токены\n/me - Написать текст о вас от имени бота в игровой чат\nНапишите команду без аргументов, чтобы узнать больше. Вче комманды работают как в личных сообщениях, так и в чате. Записаная колода в личных сообщениях будет работать в групповом чате.')
            elif message[0]['message']['text'].find('/pick') != -1:
                print ('/pick')
                if Hand.get(message[0]['message']['from']['id']) != None:
                    pick_id = message[0]['message']['text'][6:]
                    if pick_id.isdigit() == True:
                        pick_card = Hand.get(message[0]['message']['from']['id'])[int(pick_id)-1]
                        TelegramBot.sendMessage(chat_id, 'Выбрано ' + pick_card)         
                        cardInfo(pick_card)
                    else:
                        TelegramBot.sendMessage(chat_id, '/pick Номер карты в руке')
                else:
                    TelegramBot.sendMessage(chat_id, 'Рука Пуста')
            
            ######### /PLAY ##########
            
            elif message[0]['message']['text'].find('/play') != -1 or message[0]['message']['text'].find('/play@mtgcropupier_bot') != -1:
                if pick_card != '':
                    TelegramBot.sendMessage(group_id,message[0]['message']['from']['first_name'] + ' разыгрывает ' + pick_card + '!')
                    #
                    chat_id = group_id
                    cardInfo(pick_card)
                    chat_id = message[0]['message']['chat']['id']
                    Hand[message[0]['message']['from']['id'] ].pop(int(pick_id)-1)
                    if message[0]['message']['text'].find('g') != -1:
                        zone = 'grave'
                    else:
                        zone = 'table'
                    try:
                        Table[message[0]['message']['from']['first_name']][zone].append(pick_card)
                    except KeyError:
                        try:
                            Table[message[0]['message']['from']['first_name']][zone] = []
                            Table[message[0]['message']['from']['first_name']][zone].append(pick_card)
                            print(Table)
                        except KeyError:
                            Table[message[0]['message']['from']['first_name']] = {}
                            Table[message[0]['message']['from']['first_name']][zone] = []
                            Table[message[0]['message']['from']['first_name']][zone].append(pick_card)
                    pick_id = ''
                    pick_card = ''
                else:
                    TelegramBot.sendMessage(chat_id,'Сначала выберите карту (/pick <номер>)')
                    
                    
                    
            elif message[0]['message']['text'] == '/me' or message[0]['message']['text'] == '/me@mtgcropupier_bot':
                TelegramBot.sendMessage(chat_id,'/me <Текст>\nВ игровой чат выводиться текст о вас от имени бота\n/me готов! - выведет в чат "Коваль готов!"') 
            elif message[0]['message']['text'].find('/me') != -1:
                text = message[0]['message']['text'][4:]
                if text == '':
                    text = ' '
                TelegramBot.sendMessage(group_id,message[0]['message']['from']['first_name'] + ' ' + text)
                
            elif message[0]['message']['text'] == ('/view') or message[0]['message']['text'] == ('/view@mtgcropupier_bot'):
                TelegramBot.sendMessage(chat_id,'/view <Зона> <Имя игрока>\nДоступные зоны: Стол, Кладбище, Table, Graveyard\n\nПример: /view Table Коваль')
                
            elif message[0]['message']['text'].find('/view') != -1:
                zone = ''
                if message[0]['message']['text'].find('/view@mtgcropupier_bot') != -1:
                    view = message[0]['message']['text'][23:]
                else:
                    view = message[0]['message']['text'][6:]
                if view.find('Graveyard') != -1 or view.find('Кладбище') != -1:
                    if view.find('Graveyard') != -1:
                        view = view[10:]
                    else:
                        view = view[9:]
                    zone = 'grave'
                    
                
                elif view.find('Table') != -1 or view.find('Стол') != -1:
                    if view.find('Table') != -1:
                        view = view[6:]
                    else:
                        view = view[5:]
                    zone = 'table'
                text = ''
                for card in Table[view][zone]:
                    text = card + '\n' + text
                if text == '':
                    text = '<пусто>'
                TelegramBot.sendMessage(chat_id, text)
             
            elif message[0]['message']['text'].find('/hand') != -1:
                text = ''
                try:
                    for card in Hand[message[0]['message']['from']['id']]:
                        text = card + '\n' + text
                    if text == '' or text == ' ':
                        text = '<не найдено>'
                    TelegramBot.sendMessage(chat_id, text)
                except KeyError:
                     TelegramBot.sendMessage(chat_id,'У вас нет руки. Раздать - /deal')
                     
            elif message[0]['message']['text'] == ('/move') or message[0]['message']['text'] == ('/move@mtgcropupier'):
                TelegramBot.sendMessage(chat_id,'/move <Зона из которой переместить карту> <Зона куда переместить карту> <Номер карты по счету в зоне>\nДоступные зоны: Рука, Стол, Кладбище, Hand, Table, Graveyard\n\nПример: Карта Opt вторая по счету на кладбище. Чтобы вернуть ее в руку, нужно написать\n/move Graveyard Hand 2')
                
                     
                     
            elif message[0]['message']['text'].find('/move') != -1:
                 msg = message[0]['message']['text']
                 if message[0]['message']['text'].find('/move@mtgcropupier_bot') != -1:
                     msg = msg[23:]
                 else:
                     msg = msg[6:]
                     
                 if msg.find('Graveyard') == 0:
                     zoneFrom = 'grave'
                     msg = msg[10:]
                 elif msg.find('Кладбище') == 0:
                     zoneFrom = 'grave'
                     msg = msg[9:]
                 elif msg.find('Table') == 0:
                     zoneFrom = 'table'
                     msg = msg[6:]
                 elif msg.find('Стол') == 0:
                     zoneFrom = 'table'
                     msg = msg[5:]
                 elif msg.find('Hand') == 0:
                     zoneFrom = 'hand'
                     msg = msg[5:]
                 elif msg.find('Рука') == 0:
                     zoneFrom = 'hand'
                     msg = msg[5:]
                 else:
                     zoneFrom = '<not assigned>'
                 
                 if msg.find('Graveyard') == 0:
                     zoneTo = 'grave'
                     msg = msg[10:]
                 elif msg.find('Кладбище') == 0:
                     zoneTo = 'grave'
                     msg = msg[9:]
                 elif msg.find('Table') == 0:
                     zoneTo = 'table'
                     msg = msg[6:]
                 elif msg.find('Стол') == 0:
                     zoneTo = 'table'
                     msg = msg[5:]
                 elif msg.find('Hand') == 0:
                     zoneTo = 'hand'
                     msg = msg[5:]
                 elif msg.find('Рука') == 0:
                     zoneTo = 'hand'
                     msg = msg[5:]
                 else:
                     zoneTo = '<not assigned>'
                     
                 if msg.isdigit():
                     move_id = int(msg)-1
                 else:
                     TelegramBot.sendMessage(chat_id,'Номер карты не найден.')
                 
                 if zoneFrom != 'hand':
                     try:
                         move_card = Table[message[0]['message']['from']['first_name']][zoneFrom].pop(move_id)
                     except IndexError:
                         TelegramBot.sendMessage(chat_id,'Зона из которой вы пытаетесь переместить карту не найдена.')
                 else:
                     try:
                         move_card = Hand[message[0]['message']['from']['id']].pop(move_id)
                     except IndexError:
                         TelegramBot.sendMessage(chat_id,'Такой карты нет.')
                
                 if zoneTo == '<not assigned>':
                     TelegramBot.sendMessage(chat_id,'Зона на которую вы пытаетесь переместить карту не найдена')
                 elif zoneTo != 'hand':
                     try:
                         Table[message[0]['message']['from']['first_name']][zoneTo].append(move_card)
                         TelegramBot.sendMessage(group_id,'Карта ' + move_card + " перемещена с " + zoneFrom + " на " + zoneTo)
                         TelegramBot.sendMessage(chat_id,Table)
                     except KeyError:
                         Table[message[0]['message']['from']['first_name']][zoneTo] = []
                         Table[message[0]['message']['from']['first_name']][zoneTo].append(move_card)
                         TelegramBot.sendMessage(group_id,'Карта ' + move_card + " перемещена с " + zoneFrom + " на " + zoneTo)
                 else:
                     try:
                         Hand[message[0]['message']['from']['id']].append(move_card)
                         TelegramBot.sendMessage(group_id,message[0]['message']['from']['first_name'] + ' забрал карту ' + move_card)
                     except IndexError:
                         TelegramBot.sendMessage(chat_id,'Рука не найдена.')
                     
                     
            elif message[0]['message']['text'].find('/token') != -1:
                 msg = message[0]['message']['text'][7:]
                 if msg != '':
                     try:
                         Table[message[0]['message']['from']['first_name']].get('table')
                     except KeyError:
                         Table[message[0]['message']['from']['first_name']] = {}
                         Table[message[0]['message']['from']['first_name']]['table'] = []
                     if msg[:2].rstrip().isdigit():
                         count = msg[:2].rstrip()
                         msg = msg[2:].lstrip()
                         for i in range(int(count.rstrip())):
                             Table[message[0]['message']['from']['first_name']]['table'].append(msg)
                         TelegramBot.sendMessage(chat_id, message[0]['message']['from']['first_name'] + ' призвал ' + str(count) + ' токенов ' + msg)
                     
                     else:
                         TelegramBot.sendMessage(group_id, message[0]['message']['from']['first_name'] + ' призвал токен ' + msg)
                         Table[message[0]['message']['from']['first_name']]['table'].append(msg)
                 else:
                     TelegramBot.sendMessage(chat_id,'/token [Количество] <Текст> Пример:\n/token 2 Thopter 1/1 Flying')
                     
            elif message[0]['message']['text'].find('/commander') != -1:
                if message[0]['message']['text'].find('/commander@mtgcropupier_bot') != -1:
                    msg = message[0]['message']['text'][28:]
                else:
                    msg = message[0]['message']['text'][11:]
                Hand[message[0]['message']['from']['id']].append(msg)
                TelegramBot.sendMessage(grou_id,message[0]['message']['from']['first_name'] + ' взял себе на руку в качестве коммандера ' + msg)
                     
                    
                    
            elif record[message[0]['message']['from']['id']]:
                try:
                    Deck[message[0]['message']['from']['id']] = Deckbuilding(message[0]['message']['text'])
                    print(Deck)
                    TelegramBot.sendMessage(chat_id, 'Хорошо, я записал вашу колоду.')
                    record = False
                except ValueError:
                    TelegramBot.sendMessage( chat_id, 'Не могу прочитать колоду')
            update_id = message[0]['update_id']
        except KeyError:
            chat_id = message[0]['message']['chat']['id']
            TelegramBot.sendMessage(chat_id, 'Не понял')
            print('Не понял')
            update_id = message[0]['update_id']
        except UnicodeEncodeError:
            chat_id = message[0]['message']['chat']['id']
            TelegramBot.sendMessage(chat_id, 'Не понял')
            print('Не понял')
            update_id = message[0]['update_id']
    except IndexError:
        pass
    time.sleep(1)
##[{
##    'update_id': 960658935,
##     'message':
##    {
##        'message_id': 10, 'from':
##                                                    {
##                                                        'id': 314793167, 'is_bot': False, 'first_name': '\u2060', 'username': 'thinkingt00much', 'language_code': 'ru'
##                                                    }
##        , 'chat':
##        {
##            'id': 314793167, 'first_name': '\u2060', 'username': 'thinkingt00much', 'type': 'private'
##        }
##        , 'date': 1574603750, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}, {'update_id': 960658936, 'message': {'message_id': 11, 'from': {'id': 314793167, 'is_bot': False, 'first_name': '\u2060', 'username': 'thinkingt00much', 'language_code': 'ru'}, 'chat': {'id': 314793167, 'first_name': '\u2060', 'username': 'thinkingt00much', 'type': 'private'}, 'date': 1574604619, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}]

##[
##    {
##        'update_id': 960658951, 'message':
##        {
##            'message_id': 1637, 'from':
##            {
##                'id': 314793167, 'is_bot': False, 'first_name': '\u2060', 'username': 'thinkingt00much', 'language_code': 'ru'
##            }
##            , 'chat':
##            {
##                'id': -1001488258241, 'title': 'Magic: The Gathering', 'type': 'supergroup'
##            }
##            , 'date': 1574606495, 'text': '/start@mtgcropupier_bot', 'entities': [{'offset': 0, 'length': 23, 'type': 'bot_command'}]}}]
