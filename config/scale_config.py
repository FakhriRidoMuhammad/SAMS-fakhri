import configparser


class ScaleConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)
        self.section_name = "SCALE"
        self.ratio_key = "ratio"
        self.offset_key = "offset"
        self.calibrated_key = "calibrated"

    def insert_ratio(self, ratio, offset):
        try:
            self.config.set(self.section_name, self.ratio_key, ratio)
            self.config.set(self.section_name, self.offset_key, offset)
            self.config.set(self.section_name, self.calibrated_key, '1')
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(e)

    def get_ratio(self):
        self.config.read(self.config_file)
        return self.config[self.section_name][self.ratio_key]

    def get_offset(self):
        self.config.read(self.config_file)
        return self.config[self.section_name][self.offset_key]

    def is_calibrated(self):
        self.config.read(self.config_file)
        return self.config[self.section_name].getboolean(self.calibrated_key)

    def reset_scale(self):
        try:
            self.config.set(self.section_name, self.ratio_key, "0")
            self.config.set(self.section_name, self.offset_key, "0")
            self.config.set(self.section_name, self.calibrated_key, '0')
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(e)
