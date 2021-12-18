from machine import Pin
from machine import PWM

class Servo_obj:
    def __init__(self, pin = 14, min_pw = 1280, max_pw = 1720, freq = 50):

        self.Pin = Pin(pin)
        self.freq = freq
        self.min_pw = min_pw
        self.max_pw = max_pw
        self.pwm = PWM(self.Pin)
        self.pwm.freq(self.freq)
       
    def set_pw(self, pulse_width):
        self.pwm.duty(pulse_width)

    def move_right(self):
        self.set_pw(73)

    def move_left(self):
        self.set_pw(79)

    def stop(self):
        self.set_pw(76)

