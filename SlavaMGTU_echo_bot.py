
from random import choice
import telebot

token = '5092579027:AAEiaQ7lfOYURUyDo0Yjx2Qn2MuvH5-1yVA'
bot = telebot.TeleBot(token)
RANDOM_TASKS = ['помыть посуду', 'Выучить Python', 'Сделать уроки', 'Посмотреть сериальчик']
todos = {"сегодня": ["учиться"],"31.12.21":["готовиться"], "8 марта":["выкинуть ёлку"]}

HELP = '''
Список доступных команд:
/print "дата" - напечать все задачи на заданную дату
/print_all - напечать ВСЕ задачи
/add "дата" "задача"- добавить задачу на опред.дату
/random - добавить на сегодня случайную задачу
/help - Напечатать help
'''

def add_todo(date, task):# добавить задачу в словарь
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача:" {task} " добавлена на сегодня')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    if len(tail)< 3:
        er='Error: Задачи меньше 3х символов не бывает'
        bot.send_message(message.chat.id, f'{er}')
    else:
        task = ' '.join([tail])
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача:" {task} "добавлена на дату:" {date} "')


@bot.message_handler(commands=['print', 'show'])
def print_(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = date.upper()+":\n"
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)

@bot.message_handler(commands=['print_all'])
def print_all(message):
    if len(todos)!=0:
        tasks =''
        for date in todos.keys():
            tasks +=  date.upper()+":\n"
            for task in todos.get(date):
                tasks +=  f'[ ] {task}\n'
    else:
        tasks = 'органайзер пуст'
    bot.send_message(message.chat.id, tasks)

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)

