from config.information_config import InformationConfig
from config.config import Config

config = Config()

val = config.get_config_data()

print(val['SCALE'].getboolean("calibrated"))


