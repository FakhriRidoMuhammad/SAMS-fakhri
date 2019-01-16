from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from config.sensor_config import SensorConfig
from api_plugin.sams_science import Api
from main.dataset import Dataset
from main.log import Log
import time


class Application:
    def __init__(self):
        self.sensor_config = SensorConfig("/home/pi/config/config.ini")
        self.dht22_pin = self.sensor_config.dht22
        self.is_data_posted = False
        self.is_data_saved = False
        self.scale = Scale()
        self.log = Log()
        self.dht22_sensor = DHT22(self.dht22_pin["sensor_1"])
        self.api = Api()

        self.data = Dataset()
        self.dataset = dict()

    def take_dataset(self):
        self.dataset = self.data.get_dataset()

    def start(self):
        while True:
            time.sleep(60 * 30)


