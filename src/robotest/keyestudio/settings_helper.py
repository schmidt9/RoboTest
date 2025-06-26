from utils.settings import settings
import i2c_master


def send_settings_to_i2c_slave():
    speed_left = f"u{settings.speed_left}#"
    i2c_master.send_str_command(speed_left)

    speed_right = f"v{settings.speed_right}#"
    i2c_master.send_str_command(speed_right)

    speed_turn = f"t{settings.speed_right}#"
    i2c_master.send_str_command(speed_turn)


send_settings_to_i2c_slave()
