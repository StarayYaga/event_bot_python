import telebot
from read_configs import ctrl
from config import path_to_database, chatId, timeOut, tg_bot_token, masterAdmin
import datetime 
from threading import Timer
from threading import Thread
from valid import Valid


sql = ctrl(path=path_to_database)
sql.sql_init()
bot = telebot.TeleBot(tg_bot_token)
validation = Valid(bot, sql, masterAdmin)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    text=f"""
1) /add - позволяет добавить событие для отслеживания. (Команда доступна только админам)
2) /set_admin - позволяет добавить админов. (Команда доступна только Главному админу)
3) /id - вернёт ваш id. Он нужен админу. (Команда доступна всем)
4) /check - покажет ближайшие события в радиусе 3, 1 и нынешнего дня. (Доступно всем) 

По вопросам кривой работы бота или совместной работы обращаться @yagistdotcom. (Осторожно, агрессивный админ) 

Ваш id - {message.from_user.id}
"""
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['id'])
def getId(message):
    bot.send_message(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['set_admin'])
def add_admin(message):
    if message.from_user.id != masterAdmin:
        bot.send_message(message.chat.id, "У тебя нет прав. Ты феминистка!") 
        return
    bot.send_message(message.chat.id, 'Введите id')
    bot.register_next_step_handler(message, add)
def add(message):
    id_tg = message.text
    sql.setAdmin(id_tg)
    print(f"Добавлен новый админ - {id_tg}.Его добавил {message.from_user.full_name} - {message.from_user.id}")
    bot.send_message(message.chat.id, "Добавлено!")


@bot.message_handler(commands=['add'])
@validation.official
def edit(message):
    bot.send_message(message.chat.id, 'Введите название праздника!')
    bot.register_next_step_handler(message, get_name_event)
def get_name_event(message):
    name = message.text
    bot.send_message(message.chat.id, 'Введите текст поздарвления')
    bot.register_next_step_handler(message, get_text_event, name)
def get_text_event(message, name):
    text = message.text
    bot.send_message(message.chat.id, "Введите дату праздника")
    bot.register_next_step_handler(message, get_date_create_event, name, text)
def get_date_create_event(message, name, text):
    date = message.text
    dto ={
        "name": name,
        "text": text,
        "date": date
    }
    tr = str(date).split('.')
    try:
        for item in tr:
            int(item)
            
        sql.setEvent(dto)
        print(f"Давблено новое событие - {dto}")
        bot.send_message(message.chat.id, "Добавлено!")
    except:
        bot.send_message(message.chat.id, "Чёто ты хуйню написал. Давай переделывай!")


@bot.message_handler(commands=['check'])
def check(message):
    today = str(datetime.date.today()).split("-")
    events = sql.getEvents()
    for event in events:
        date = event["date"].split(".")
        if (date[1] != today[1]): continue
        if (int(date[0])-int(today[2]) == 3):
            bot.send_message(message.chat.id, f"Скоро {event['name']}!\nОсталось 3 дня!")
            continue
        if (int(date[0])-int(today[2]) == 1):
            bot.send_message(message.chat.id, f"Завтра {event['name']}!!!")
            continue
        if (int(date[0])-int(today[2]) == 0):
            bot.send_message(message.chat.id, event["text"])
        Timer(timeOut, check_event).start()


def check_event():
    today = str(datetime.date.today()).split("-")
    events = sql.getEvents()
    for event in events:
        date = event["date"].split(".")
        if (date[1] != today[1]): continue
        if (int(date[0])-int(today[2]) == 3):
            bot.send_message(chatId, f"Скоро {event['name']}!\nОсталось 3 дня!")
            continue
        if (int(date[0])-int(today[2]) == 1):
            bot.send_message(chatId, f"Завтра {event['name']}!!!")
            continue
        if (int(date[0])-int(today[2]) == 0):
            bot.send_message(chatId, event["text"])
        Timer(timeOut, check_event).start()



def main():
    thread_bot = Thread(target=bot.infinity_polling)
    thread_bot.start()
    print("Bot start")
    check_event()
    print("Timer start")
    

if __name__ == '__main__':
    main()