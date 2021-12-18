#Light class creates a light object, and sends True or false if enough is detected by light sensor on Pin 36
from machine import *
#from driver import OLED
from time import sleep, sleep_ms

class Light:
        
    def __init__(self, pin = 36, rolling_avg_n = 5):
        self.light= Pin(pin, Pin.IN)
        self.light_sensor= ADC(self.light)
        self.rolling_avg_n = rolling_avg_n
        self.threshold = 200 #change this depending on season and preference
        self.already_moved_up = False
        self.already_moved_down = False
        #self.oled = OLED()
        
    def rolling_avg(self):
        #returns avg light in (rolling_avg_n * 0.8) seconds
        temp = self.rolling_avg_n
        avg_light = 0
        while(temp > 0):
            #print(" reading ", self.light_sensor.read())
            avg_light = avg_light + self.light_sensor.read()
            #print("light is ... ", self.light_sensor.read())
            temp = temp - 1
            
            sleep_ms(800)
        return round( avg_light/self.rolling_avg_n )


    def phototransistor(self):
        #returns True if rolling avg light > Threshold
        #else returns false
        current_light = self.rolling_avg()
        #print(" amount of light is ", current_light)
        if(current_light >= self.threshold ) :
            return True
        else: 
            return False