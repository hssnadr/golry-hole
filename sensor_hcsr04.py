import RPi.GPIO as GPIO
import time

import _UTILITIES.mean_data_point as mdp

class HCSR04:

    def __init__(self, pin_trig_, pin_echo_):
        # init GPIO
        self._pin_trig = pin_trig_
        self._pin_echo = pin_echo_
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_trig,GPIO.OUT)
        GPIO.setup(self._pin_echo,GPIO.IN)
        GPIO.output(self._pin_trig, False)

        # init continuous mean data filter
        self._sensor_data = mdp.MeanDataPoint(5)
        self._distance = 0

    def update(self):
        GPIO.output(self._pin_trig, True)
        time.sleep(0.00001)
        GPIO.output(self._pin_trig, False)

        sens_start_ = 0.0
        while GPIO.input(self._pin_echo)==0:
            sens_start_ = time.time()

        while GPIO.input(self._pin_echo)==1:
            sens_end_ = time.time()

        self._distance = round((sens_end_ - sens_start_) * 340 * 100 / 2, 1)  ## Sound speed = 340 m.s-1
        self._sensor_data.push_raw_data(self._distance)
        self._distance = self._sensor_data.get_filter_value()
    
    def get_distance(self) -> float:
        return self._distance

    def __del__(self):
        print("quitting HCSR04 sensor")
        GPIO.cleanup()