import RPi.GPIO as GPIO
from sensorlib.hx711 import HX711
from config.config import Config


class Scale:
    def __init__(self):
        self.config = Config()  # config init
        self.config_data = self.config.get_config_data()
        self.hx = HX711(dout_pin=5, pd_sck_pin=6, gain_channel_A=64, select_channel='A')  # initialize scale
        self.is_calibrated = self.config_data['SCALE'].getboolean("calibrated")  # check config if scale is calibrated
        self.ratio = 0  # scale ratio for calibration
        self.offset = 0
        self.value = 0
        self.result = 0
        self.data = 0
        if self.is_calibrated:
            self.hx._offset_A_64 = float(self.config_data["SCALE"]['offset'])
            self.config_ratio = self.config_data["SCALE"]['ratio']  # get scale ratio of config
            self.hx.set_scale_ratio(scale_ratio=float(self.config_ratio))

    def setup(self):
        try:
            self.data = self.hx.get_raw_data_mean(times=10)
            self.result = self.hx.zero(times=10)
            self.data = self.hx.get_data_mean(times=10)
        except Exception as e:
            print("Scale or HX711 connected? : {0}".format(e))

    def calibrate(self, weight):
        self.data = self.hx.get_data_mean(times=10)
        try:
            self.value = float(weight)
            self.ratio = self.data / self.value
            self.hx.set_scale_ratio(scale_ratio=self.ratio)
            self.config.set_scale(ratio=self.ratio, offset=self.hx.get_current_offset(), calibrated=1)
        except ValueError:
            print('Expected integer or float and I have got: '
                  + str(weight))

    def get_data(self):
        try:
            self.hx.power_up()
            val = self.hx.get_weight_mean(5)
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
        new_offset = self.hx.get_raw_data_mean(times=10)
        self.config.set_offset(new_offset)
        self.hx.zero()

    @staticmethod
    def clean():
        GPIO.cleanup()
