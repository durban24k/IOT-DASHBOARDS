#simulator.py
"""A connected thermostat simulator that publishes JSON data messages to dweet.io"""

import dweepy
import sys
import time
import random

MIN_CELSIUS_TEMP=-25
MAX_CELSIUS_TEMP=45
MAX_TEMP_CHANGE=2

#get the number of messages to simulate and delay between them
NUM_OF_MESSAGES=int(sys.argv[1])
MESSAGE_DELAY=int(sys.argv[2])

dweeter="durban24k-temp-simulator" #unique name
thermostat={
     'Location':'KASARANI, KAS, KIM, KENYA',
     'Temperature':20,
     'LowTempWarning':False,
     'HighTempWarning':False
}
print('Temperature Simulator is starting')

for message in range(NUM_OF_MESSAGES):
     # generate a random number in the range of MAX_TEMP_CHANGE
     # through MAX_TEMP_CHANGE and add it to the current temperature
     thermostat['Temperature']+=random.randrange(-MAX_TEMP_CHANGE,MAX_TEMP_CHANGE+1) 

     #ensure that the temperature is within range
     if thermostat['Temperature']<MIN_CELSIUS_TEMP:
          thermostat['Temperature']=MIN_CELSIUS_TEMP
     
     if thermostat['Temperature']>MAX_CELSIUS_TEMP:
          thermostat['Temperature']=MAX_CELSIUS_TEMP

     #check for low temperature warning
     if thermostat['Temperature']<3:
          thermostat['LowTempWarning']=True
     else:
          thermostat['LowTempWarning']=False
     
     #check for high temperature warning
     if thermostat['Temperature']>35:
          thermostat['HighTempWarning']=True
     else:
          thermostat['HighTempWarning']=False

     #send the dweet to dweet.io via dweepy
     print(f'Message sent: {message +1}\r', end='')
     dweepy.dweet_for(dweeter,thermostat)
     time.sleep(MESSAGE_DELAY)

print('Temperature Simulator finished')