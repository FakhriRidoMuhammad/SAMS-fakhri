import configparser


class Config:
    def __init__(self):
        self.config_file = '/home/pi/config/config.ini'
        self.config = configparser.ConfigParser()
        self.scale_section = "SCALE"

    def get_config_data(self):
        self.config.read(self.config_file)
        return self.config

    def set_scale(self, ratio=0, offset=0, calibrated=0):
        self.config.set(self.scale_section, "ratio", ratio)
        self.config.set(self.scale_section, "offset", offset)
        self.config.set(self.scale_section, "calibrated", calibrated)
        self.write_config()

    def write_config(self):
        try:
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(e)
