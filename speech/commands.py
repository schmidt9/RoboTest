import datetime
import fuzzywuzzy.fuzz
import num2t4ru
import speak
import pytz

command_dic = {
    "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'),
    "about": ('расскажи о себе', 'что ты такое', 'ты кто', 'о себе'),
    "ctime": ('время', 'текущее время', 'сейчас времени', 'который час', 'сколько время', 'скажи время')
}


def recognize_command(input_command: str):
    similarity_percent = 50
    found_command = 'no_data'

    for command_id, command_texts in command_dic.items():
        for command_text in command_texts:
            similarity = fuzzywuzzy.fuzz.ratio(input_command, command_text)

        print(f"Совпадение команды: {similarity}% | Ключ: {command_id}")

        if similarity >= similarity_percent:
            found_command = command_id
            process_command(command_id)

    return found_command


def process_command(key: str):
    match key:
        case 'help':
            f_help()
        case 'about':
            f_about()
        case 'ctime':
            f_ctime()
        case _:
            print('Нет данных')


def f_help():
    print("HELP")


def f_about():
    print("ABOUT")


def f_ctime():
    timezone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now().astimezone(timezone)
    text = "Сейчас "
    text += num2t4ru.num2text(int(now.hour)) + '.'

    if now.minute < 10:
        text += "ноль "

    text += num2t4ru.num2text(int(now.minute)) + '.'
    speak.speak(text)
