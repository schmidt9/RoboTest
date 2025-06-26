from utils.settings import settings
import i2c_master


def send_settings_to_i2c_slave():
    i2c_master.send_str_command(settings.speed_left)
    i2c_master.send_str_command(settings.speed_right)
    i2c_master.send_str_command(settings.speed_turn)


send_settings_to_i2c_slave()
