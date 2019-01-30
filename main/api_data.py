from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS18B20
from config.config import Config


class ApiData:
    def __init__(self):
        self.config = Config()
        self.config_data = self.config.get_config_data()
        self.dht22 = DHT22(self.config_data['DHT22']['pin'])
        self.DS18B20 = DS18B20()

        self.ds18b20_temp = []
        self.dht22_data = []

    @staticmethod
    def error_message(device, exception_msg):
        return "something went wrong by collecting the {0} dataset! Error: {1}".format(device, exception_msg)

    def get_ds18b20_data(self):
        sensor_counter = self.DS18B20.device_count()
        try:
            if sensor_counter != 0:
                for x in range(sensor_counter):
                    self.ds18b20_temp.append(self.DS18B20.tempC(x))

                if len(self.ds18b20_temp) != 0:
                    return self.ds18b20_temp

        except Exception as e:
            print(self.error_message("ds18b20", e))

    def get_dht22_data(self):
        return self.dht22.get_data()
