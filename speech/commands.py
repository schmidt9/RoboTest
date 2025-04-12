import fuzzywuzzy.fuzz

command_dic = {
    "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'),
    "about": ('расскажи о себе', 'что ты такое', 'ты кто', 'о себе'),
    "ctime": ('время', 'текущее время', 'сейчас времени', 'который час', 'сколько время')
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
    print("ВРЕМЯ")
