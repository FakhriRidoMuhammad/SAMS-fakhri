import configparser
config_file = '/home/pi/config/config.ini'


class IntervalConfig:
    def __init__(self):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)
        self.section_name = "INTERVAL"
        self.median_key = "median"
        self.wait_key = "wait_time_seconds"

    def get_median_interval(self):
        self.config.read(self.config_file)

        return int(self.config[self.section_name][self.median_key])

    def get_wait_time(self):
        self.config.read(self.config_file)

        return int(self.config[self.section_name][self.wait_key])
