#used starter code provided by Prof. Vaccari

import network
from machine import Pin, PWM

WIFI_SSID = 'Pixel_jeff' #'MiddleburyGuest'
password = '******' 

def ok():
    """ Blink once a second """
    PWM(Pin(13), freq=1, duty=512)

def trying():
    """ Blink 10 times a second """
    PWM(Pin(13), freq=10, duty=512)

def connect():
    """ Setup a connection """
    trying()  # Blink 10 times a second while trying to connect

    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('Connecting to ' + WIFI_SSID)
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, password)
        while not sta_if.isconnected():
            print('.', end='');
    else:
        print('Already connected to ' + sta_if.config('essid'))

    ok()  # Once connected, blink only once a second
    print('network config:', sta_if.ifconfig())

connect()


