from machine import *
from driver import OLED

from time import *

import main_ada_sub 

import Servo
from feedback360 import *
import Light


up_button = Pin(26, Pin.IN)
down_button = Pin(25, Pin.IN)
setup_button = Pin(4,Pin.IN)
switch_mode = Pin(39,Pin.IN)

control_mode = 0

turns = 0
starting_ang = feedback360()

last_val = 0
oled = OLED()

servo = Servo.Servo_obj()

light = Light.Light()

position = 0
    
counted_turn = False

set_up_max_turns_top = 0
set_up_max_turns_bot = 0
SHADE_LIMITS_SETUP = False #debugging, so setting to true

#updates position, by diving turns over max turns
# position is a percentage
def update_position():
    global set_up_max_turns_top, turns, position,control_mode
    oled.clear()
    try:
        position = ( turns / set_up_max_turns_top) * 100
    except:
        position = 0
    
    position = round(position, 1)
    display_position = "Position: " +str(position) + "% \n Mode: " + str(control_mode)
    oled.write_text(display_position)


#returns position
def get_position():
    global position
    return position

#checks if motor is within bounds
def in_bounds(x):
    # x is a direction
    global set_up_max_turns_top, set_up_max_turns_bot, turns, position
    if x == 1:
        #check if max number of turns has been reached
        return turns <= set_up_max_turns_top
    return (turns > set_up_max_turns_bot)
    

#checks if up, down, or switch mode buttons were pressed
def button_pressed(pin):
    global set_up_state, starting_ang, counted_turn, turns
    global set_up_max_turns_top
    global SHADE_LIMITS_SETUP
    sleep_us(10)
    
    #while in set up state, we dont check if we are in bounds as we let the user
    #define max turns to reach top
    if(up_button.value() ==0 and set_up_state == 2 ):
        #print("UP button ", up_button.value(), "set state ", set_up_state, " start time ")
        
        if (feedback360() > starting_ang and counted_turn == False):
            #we check if we have passed the starting angle and we count turn only if we haven't seen this turn yet
            turns = turns + 1
            counted_turn = True
        elif (feedback360() <= starting_ang):
            counted_turn = False
        #sets up max turns
        set_up_max_turns_top = turns

        servo.move_right()
    
    #we check if we are within bounds to move up or in set_up_state 1
    elif(up_button.value() ==0 and (set_up_state == 1 or in_bounds(1) ) ):
        if (feedback360() > starting_ang and counted_turn == False):
            turns = turns + 1
            counted_turn = True
        elif (feedback360() <= starting_ang):
            counted_turn = False
        #print("turns ", turns, " btw SUP ", set_up_state)
        servo.move_right()
        if set_up_state != 1:
            update_position()

    #when moving down, we care if we are within the bounds
    if(down_button.value() == 0 and (set_up_state == 1 or in_bounds(0)) ):
        if (feedback360() < starting_ang and counted_turn == False):
            turns = turns - 1
            counted_turn = True
        elif (feedback360() >= starting_ang):
            counted_turn = False
        #print("turns ", turns)
        servo.move_left()
        
        if set_up_state != 1:
            update_position()
    
    elif(switch_mode.value()==0):
       # switch between 4 modes: 1 manual, 2 light mode, 3 mqtt mode
        global control_mode
        control_mode = (control_mode +1 )%4
        sleep_us(15)
    sleep_us(10)

def move_shade_down():
    #moving shade all the way down slowly
    global turns, counted_turn, starting_ang
    servo.move_left()
    sleep_ms(30) 
    servo.stop()
    if (feedback360() < starting_ang and counted_turn == False):
            turns = turns - 1
            counted_turn = True
    elif (feedback360() >= starting_ang):
        counted_turn = False
 

def move_shade_up():
    #moving shade all the way up slowly
    global turns, counted_turn, starting_ang

    servo.move_right()
    sleep_ms(30) 
    servo.stop()
    if (feedback360() > starting_ang and counted_turn == False):
        turns = turns + 1
        counted_turn = True
    elif (feedback360() <= starting_ang):
        counted_turn = False
        

def up_button_released(pin):
    global set_up_state, turns, SHADE_LIMITS_SETUP
    global set_up_max_turns_top
    
    servo.stop()
    #print("up button ", up_button.value(), "set state ", set_up_state)
    if(up_button.value() ==1 and set_up_state == 2 and SHADE_LIMITS_SETUP == False ): 

        set_up_max_turns_top = turns
        print("so the final number of turns is ... ", set_up_max_turns_top)
        SHADE_LIMITS_SETUP = True
        set_up_state = 3
        set_up()
        #turns = 0
    elif(up_button.value() ==1 and SHADE_LIMITS_SETUP and set_up_state > 3):
        update_position()
        sleep(2)

    elif(up_button.value() ==1 and SHADE_LIMITS_SETUP):
        update_position()
    
    sleep_us(20)

def down_button_released(pin):    
    global SHADE_LIMITS_SETUP
    #only for up and down rising
    sleep_us(10)
    servo.stop()
    #update position
    if(down_button.value() ==1 and SHADE_LIMITS_SETUP):
        update_position()

switch_mode.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

set_up_state = 0


def set_up():
    global set_up_state, starting_ang
    global time_to_top, mqtt
    global time_to_bot, turns, control_mode
    global SHADE_LIMITS_SETUP

    global set_up_max_turns_top, set_up_max_turns_bot, turns

    servo.stop()
    if set_up_state == 0:
        SHADE_LIMITS_SETUP = False
        #calculate time to top
        oled.write_text("1. Move Curtain All the way to the bottom to initialize set up. \n Press White Button to start Set up")
        sleep(1)

    elif set_up_state == 1:
        #curtaion is at bottom
        oled.clear()
        starting_ang = feedback360()
        oled.write_text("2. Press Up button and release At your top position.\n Press White Button to Complete Set up")
        turns = 0
        #
        sleep(1)

    elif set_up_state >= 3 :
        print("turns to top ", set_up_max_turns_top )
        oled.clear()
        SHADE_LIMITS_SETUP = True
        control_mode = 0 #after set up, we move to manual mode
        #set_up_state =(set_up_state + 1) %5
        print("Setup State completed")
        
        sleep(1)
        update_position()
  
    
    print("Setup State ",set_up_state," completed")
    
    set_up_state= (set_up_state + 1) %5
    
def set_to_position(desiredPosition):
    #we tell the motor to move to a desired position
    if desiredPosition == None:
        #if mqtt returns None, we stop
        servo.stop()
        return

    global up_button, down_button
    direction_to_move = desiredPosition - get_position()

    dir = 0 #move down
    if (direction_to_move > 0): #positive, move Up
        dir = 1
    while (in_bounds(dir)):
        #move until we reach the position
        if dir == 1 and get_position() < desiredPosition :

            move_shade_up()
        elif dir == 0 and desiredPosition < get_position() :
            move_shade_down()
        
        update_position() #update position on OLED
        sleep_ms(10)


def set_up_pressed(pin):
    #calls set_up
    set_up()
    sleep_ms(20) #debounce makes sure we only call it once


previousTenthSecondMillis = ticks_ms()

up_was_pressed, down_was_pressed = False , False
entered_light_mode = False

set_up_state = 0

oled.write_text("Welcome. Press blue button to begin.")
#print("init everything")

mqtt = main_ada_sub.MQTT_Subscribe()
mqtt.run_client()

control_mode = 0
#update_position()

while(1):
    millis = ticks_ms()
    if (millis - previousTenthSecondMillis  >= 10): #checking every 10 ms
        #print("starting mode ... ", control_mode)
        #print(feedback360())
        if (up_button.value() == 0): 
            button_pressed(up_button)
            if (control_mode == 2 or control_mode == 3):
                #if buttons pressed, go back to manual mode
                control_mode = 0
            up_was_pressed = True
        elif (down_button.value()== 0):
            button_pressed(down_button)
            if (control_mode == 2 or control_mode == 3):
                control_mode = 0
            down_was_pressed = True
        elif (up_was_pressed and up_button.value() == 1):
            up_button_released(up_button)
            #up_was_pressed = False
        elif (down_was_pressed and down_button.value() == 1):
            down_button_released(down_button)
            #down_was_pressed = False
        
        if control_mode == 1 :
            #mode 1 = set up
            #print("Set up", set_up_max_turns_top)
            if set_up_state == 0:
                oled.write_text("Press White Button to CONTINUE with Set Up. Otherwise Press blue button to exit set up mode.")
            
            if setup_button.value() == 0 :
                set_up_pressed(setup_button) #calling set up func
            

        elif control_mode == 2:
            #mqtt mode is only available after uset has set up positions
            if (SHADE_LIMITS_SETUP == False ):
                oled.write_text("Cannot use Modes until you set up. Please set up your shade")
                sleep(2)
                control_mode = 1
            else: 
                print("MQTTTT")
                print("ran client")
                received = mqtt.get_message()
                #print("printing desired position ",  received, " type ", type(received) )
                sleep_ms(500)
                try:
                    #print("setting position ... ", received )
                    set_to_position(received) #sending MQTT position and setting it
                    sleep(1)
                except:
                    print("an exception occurred ")
                    sleep(1) #wait 1 sec before trying again
                update_position()
            

        elif control_mode == 3:
            #light mode only available after user completes sets up
            if (SHADE_LIMITS_SETUP == False ):
                oled.write_text("Cannot use Modes until you set up. Please set up your shade")
                sleep(2)
                control_mode = 1
            else:
                if entered_light_mode == False:
                    oled.write_text("light mode, shade will move depending on the amount of light")
                    sleep(2)
                enough_light = light.phototransistor()
                sleep(2)
                if enough_light:
                    set_to_position(100)
                    update_position()
                elif (enough_light == False) :
                    set_to_position(0)
                entered_light_mode = True
                sleep_us(10)
                continue

    else:
        continue

    previousTenthSecondMillis += 10 #we check every 10 ms
    