from umqtt.robust import MQTTClient
import sys
import os
from time import sleep_us, sleep_ms

class MQTT_Subscribe:
    
    def __init__(self):
        #initialize to none
        self.client = None
        self.message = None

    def run_client(self):
        def cb(topic, msg):
            #print('Topic = {}, Msg = {}'.format(topic, msg))
            self.message = int(msg)
            #servo_pwm.freq(50)
            #servo_pwm.duty(position)
            #print (self.message)
        #global client
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

        # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
        #
        # To use a secure connection (encrypted) with TLS:
        #   set MQTTClient initializer parameter to "ssl=True"
        #   Caveat: a secure connection uses about 9k bytes of the heap
        #         (about 1/4 of the micropython heap on the ESP8266 platform)
        ADAFRUIT_IO_URL = b'io.adafruit.com'
        ADAFRUIT_USERNAME = b'jarodriguez'
        ADAFRUIT_IO_KEY = b'aio_HHAG19l0a5s082cvRANdoB8ajwJh'
        ADAFRUIT_IO_FEEDNAME_SUB = b'Shade-pub'

        self.client = MQTTClient(client_id=mqtt_client_id,
                            server=ADAFRUIT_IO_URL,
                            user=ADAFRUIT_USERNAME,
                            password=ADAFRUIT_IO_KEY,
                            ssl=True)

        try:
            self.client.connect()
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            sys.exit()

        # Subscrie to feed
        mqtt_feedname_sub = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME_SUB), 'utf-8')
        self.client.set_callback(cb)
        self.client.subscribe(mqtt_feedname_sub)


    def get_message(self):
        #checks if a message was sent to feed. sets up self.message in callback function
        try:
            self.client.check_msg()  
            sleep(1)
            return self.message
        except:
            #self.client.disconnect()
            print("Error w mqtt")
            return None