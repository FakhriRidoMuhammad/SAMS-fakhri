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
        self.dataset = ""
        self.dataset = self.data.get_dataset()

    def start(self):
        while True:
            print("take dataset...")
            self.take_dataset()

            if self.log.has_log_files():
                print("has log files...")
                self.log.post_log_files(self.dataset)
            else:
                response = self.api.post_dataset(self.dataset)
                if response:
                    print("Dataset posted!")
                else:
                    print ("Dataset posting failed. Statuscode: {0}".format(response))
                    self.is_data_posted = False  # reset is data posted
                    print("log dataset")
                    self.log.insert(self.dataset)  # log dataset
                    while not self.is_data_posted:
                        print("try to post dataset...")
                        self.is_data_posted = self.api.post_dataset(self.dataset)
                        time.sleep(5)
            print("wait 10 seconds...")
            time.sleep(10)


