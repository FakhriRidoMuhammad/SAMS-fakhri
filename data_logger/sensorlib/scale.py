import RPi.GPIO as GPIO
from data_logger.sensorlib.hx711 import HX711
from data_logger.config.config import Config


class Scale:
    def __init__(self):
        self.config = Config()  # config init
        self.config_data = self.config.get_config_data()
        self.hx = HX711(5, 6)  # initialize scale
        self.is_calibrated = self.config_data['SCALE'].getboolean("calibrated")  # check config if scale is calibrated
        self.ratio = 0  # scale ratio for calibration
        self.offset = 0
        self.value = 0
        self.result = 0
        self.data = 0
        if self.is_calibrated:
            self.hx.set_offset(float(self.config_data["SCALE"]['offset']))
            self.config_ratio = self.config_data["SCALE"]['ratio']  # get scale ratio of config
            self.hx.set_scale(float(self.config_ratio))

    def setup(self):
        try:
            self.offset = self.hx.read_average()
            self.hx.set_offset(self.offset)
            print("offset: {}".format(self.offset))
        except Exception as e:
            print("Scale or HX711 connected? : {0}".format(e))

    def read(self):
        if self.hx.read_average < 1:
            return False
        else:
            return True

    def calibrate(self, weight):
        try:
            self.value = int(weight)
            measured_weight = (self.hx.read_average() - self.hx.get_offset())
            print("measured weight: {}".format(measured_weight))
            self.ratio = int(measured_weight) / self.value
            print("offset: {}".format(self.offset))
            print("ratio: {}".format(self.ratio))
            self.hx.set_scale(self.ratio)
            self.config.set_scale(ratio=self.ratio, offset=self.hx.get_offset(), calibrated=1)
        except ValueError:
            print('Expected integer or float and I have got: '
                  + str(weight))

    def get_data(self):
        try:
            self.hx.power_up()
            val = self.hx.get_grams()
            measure_weight = round((val / 1000), 2)
            self.hx.power_down()
            return measure_weight
        except Exception as e:
            print("Scale or HX711 connected? : {0}".format(e))

    def calibrated(self):
        self.is_calibrated = self.config_data['SCALE'].getboolean("calibrated")

        return self.is_calibrated

    def reset(self):
        self.config.set_scale()

    def tare(self):
        pass

    @staticmethod
    def clean():
        GPIO.cleanup()
