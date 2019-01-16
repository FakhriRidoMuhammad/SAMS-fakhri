import configparser


class AudioConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)
        self.section_name = "AUDIO"
        self.duration_key = "duration"
        self.fs_key = "fs"
        self.nWindow_key = "nWindow"

    def get_duration(self):
        self.config.read(self.config_file)

        return int(self.config[self.section_name][self.duration_key])

    def get_fs(self):
        self.config.read(self.config_file)

        return int(self.config[self.section_name][self.fs_key])

    def get_nWindow(self):
        self.config.read(self.config_file)

        return self.config[self.section_name][self.nWindow_key]
