import RPi.GPIO as GPIO
from sensorlib.hx711 import HX711
from config.scale_config import ScaleConfig


class Scale:
    def __init__(self):
        self.config = ScaleConfig()  # config init
        self.hx = HX711(dout_pin=5, pd_sck_pin=6, gain_channel_A=64, select_channel='A')  # initialize scale
        self.is_calibrated = self.config.is_calibrated()  # check config if scale is calibrated
        self.ratio = 0  # scale ratio for calibration
        self.value = 0
        self.measure_weight = 0
        self.result = 0
        self.data = 0
        if self.is_calibrated:
            self.hx._offset_A_64 = float(self.config.get_offset())
            self.config_ratio = self.config.get_ratio()  # get scale ratio of config
            self.hx.set_scale_ratio(scale_ratio=float(self.config_ratio))

    def setup(self):
        self.data = self.hx.get_raw_data_mean(times=1)
        self.result = self.hx.zero(times=10)
        self.data = self.hx.get_data_mean(times=10)

    def calibrate(self, weight):
        self.data = self.hx.get_data_mean(times=10)
        try:
            self.value = float(weight)
            self.ratio = self.data / self.value
            self.hx.set_scale_ratio(scale_ratio=self.ratio)
            self.config.insert_ratio(self.ratio, self.hx._offset_A_64)
        except ValueError:
            print('Expected integer or float and I have got: '
                  + str(weight))

    def get_data(self):
        val = self.hx.get_weight_mean(6)
        self.measure_weight = round((val / 1000), 1)

        return self.measure_weight

    def calibrated(self):
        self.is_calibrated = self.config.is_calibrated()

        return self.is_calibrated

    def reset(self):
        self.config.reset_scale()

    @staticmethod
    def clean():
        GPIO.cleanup()
