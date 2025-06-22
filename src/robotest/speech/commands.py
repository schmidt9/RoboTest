import datetime
import fuzzywuzzy.fuzz
import speak
import pytz

command_dic = {
    "help": ("список команд", "команды", "что ты умеешь", "твои навыки", "навыки"),
    "about": ("расскажи о себе", "что ты такое", "ты кто", "о себе"),
    "ctime": (
        "время",
        "текущее время",
        "сейчас времени",
        "который час",
        "сколько время",
        "скажи время",
    ),
}

name_alias = ["привет"]


def recognize_command(input_command: str):
    similarity_percent = 50
    result = False

    for command_id, command_texts in command_dic.items():
        for command_text in command_texts:
            similarity = fuzzywuzzy.fuzz.ratio(input_command, command_text)

        print(f"Command recognized: {similarity}% | key: {command_id}")

        if similarity >= similarity_percent:
            result = process_command(command_id)

            if result is False:
                speak.speak(f"Для команды {input_command} не назначено действие")

    return result


def recognize_name(name: str):
    similarity_percent = 70
    stat = False

    print(f"Recognizing {name}:")

    for item in name_alias:
        similarity = fuzzywuzzy.fuzz.ratio(name, item)

        print(f"Sililarity to {item}: {similarity}%")

        if similarity > similarity_percent:
            stat = True
            print(f"Name recognized: '{name}'")
            break

    if stat is False:
        print(f"Name not recognized: '{name}'")

    return stat


def process_command(key: str):
    result = True

    match key:
        case "help":
            f_help()
        case "about":
            f_about()
        case "ctime":
            f_ctime()
        case _:
            print(f"Unknown command key '{key}'")
            result = False

    return result


def f_help():
    print("HELP")


def f_about():
    print("ABOUT")


def f_ctime():
    timezone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now().astimezone(timezone)
    text = "Сейчас "
    text += f"{now.hour} "

    if now.minute < 10:
        text += "ноль "

    text += f"{now.minute}"
    speak.speak(text)


if __name__ == "__main__":
    recognize_name("привет")
