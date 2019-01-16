import configparser


class SensorConfig:
    def __init__(self, config_file):
        # READ CONFIG
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        self.dht22 = dict()
        self.ds1820 = dict()

        if "DHT22" in self.config:
            for key in self.config['DHT22']:
                self.dht22[key] = int(self.config['DHT22'][key])

        if "DS1820" in self.config:
            for key in self.config['DS1820']:
                self.ds1820[key] = self.config['DS1820'][key]
