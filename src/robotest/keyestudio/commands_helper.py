from robotest.utils.settings import settings
from robotest.keyestudio import i2c_master


# Using class for constants to be able to use it in match statement
class Prefix:
    SPEED_LEFT = "u"
    SPEED_RIGHT = "v"
    SPEED_TURN = "t"


def send_speed_left():
    command = f"{Prefix.SPEED_LEFT}{settings.speed_left}#"
    i2c_master.send_str_command(command)


def send_speed_right():
    command = f"{Prefix.SPEED_RIGHT}{settings.speed_right}#"
    i2c_master.send_str_command(command)


def send_speed_turn():
    command = f"{Prefix.SPEED_TURN}{settings.speed_turn}#"
    i2c_master.send_str_command(command)


def send_settings_to_i2c_slave():
    send_speed_left()
    send_speed_right()
    send_speed_turn()


def get_speed_value(command: str):
    return int(command[1:-1])


def save_and_send_speed_command(command: str):
    match command[0]:
        case Prefix.SPEED_LEFT:
            settings.speed_left = get_speed_value(command)
        case Prefix.SPEED_RIGHT:
            settings.speed_right = get_speed_value(command)
        case Prefix.SPEED_TURN:
            settings.speed_turn = get_speed_value(command)
        case _:
            print(f"Unknown command {command}")

    settings.write()
    i2c_master.send_str_command(command)


def send_direction_command(command: str):
    match command:
        case "forward":
            i2c_master.send_byte_command(ord("F"))
        case "back":
            i2c_master.send_byte_command(ord("B"))
        case "left":
            i2c_master.send_byte_command(ord("L"))
        case "right":
            i2c_master.send_byte_command(ord("R"))
        case "stop":
            i2c_master.send_byte_command(ord("S"))
        case _:
            print(f"Unknown command {command}")
