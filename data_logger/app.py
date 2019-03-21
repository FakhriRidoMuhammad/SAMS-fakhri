#!/usr/bin/python3

from data_logger.main.application import Application
from data_logger.config.config import Config

config = Config()
config_data = config.get_config_data()
is_calibrated = config_data['SCALE'].getboolean("calibrated")

app = Application()

if __name__ == '__main__':
    if is_calibrated:
        app.start()
