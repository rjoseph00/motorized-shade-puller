from machine import *

pinFeedback = Pin(27, Pin.IN)


def feedback360():                            # Cog keeps angle variable updated
    unitsFC = 360                          # Units in a full circle
    dutyScale = 1000                       # Scale duty cycle to 1/1000ths
    dcMin = 29                             # Minimum duty cycle
    dcMax = 971                            # Maximum duty cycle
    q2min = unitsFC/4                      # For checking if in 1st quadrant
    q3max = q2min * 3                      # For checking if in 4th quadrant
    turns = 0                              # For tracking turns
  # dc is duty cycle, theta is 0 to 359 angle, thetaP is theta from previous
  # loop repetition, tHigh and tLow are the high and low signal times for 
  # duty cycle calculations.

  # Measure feedback signal high/low times.
    tLow = time_pulse_us(pinFeedback, 0)            # Measure low time 
    tHigh = time_pulse_us(pinFeedback, 1)           # Measure high time

  # Calculate initial duty cycle and angle.
    dc = (dutyScale * tHigh) / (tHigh + tLow)
    theta = (unitsFC - 1) - ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1)
    thetaP = theta

    for x in range(1):                                    # Main loop for this cog
  
    # Measure high and low times, making sure to only take valid cycle
    # times (a high and a low on opposite sides of the 0/359 boundary
    # will not be valid.
        tCycle = 0                           # Clear cycle time
        while(1):                                 # Keep checking
            tHigh = time_pulse_us(pinFeedback, 1)       # Measure time high
            tLow = time_pulse_us(pinFeedback, 0)        # Measure time low
            tCycle = tHigh + tLow
            if((tCycle > 1000) and (tCycle < 1200)):  # If cycle time valid
                break                                # break from loop
     
        dc = (dutyScale * tHigh) / tCycle        # Calculate duty cycle
    
    # This gives a theta increasing  the
    # counterclockwise direction.
        theta = (unitsFC - 1) - ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1)

        if(theta < 0):                             # Keep theta valid
            theta = 0
        elif(theta > (unitsFC - 1)):
            theta = unitsFC - 1

    # If transition from quadrant 4 to  
    # quadrant 1, increase turns count. 
        if((theta < q2min) and (thetaP > q3max)):
            turns= turns+1
    # If transition from quadrant 1 to  
    # quadrant 4, decrease turns count. 
        elif((thetaP < q2min) and (theta > q3max)):
            turns=turns-1
    # Construct the angle measurement from the turns count and
    # current theta value.
        if(turns >= 0):
            angle = (turns * unitsFC) + theta
        elif(turns <  0):
            angle = ((turns + 1) * unitsFC) - (unitsFC - theta)

        #print("theta ", theta)
        #print("thetaP ", thetaP)
        thetaP = theta                           # Theta previous for next rep
        #print(" turns ", all_turns)
        #print(" angles ", angle)
        return round(angle)

