#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import machine
import math
import network
import os
import time
import utime
import gc
import binascii
import socket
import pycom
from machine import RTC
from L76GNSS import L76GNSS
from pycoproc_1 import Pycoproc
from network import LoRa

#   These value are used for identifying states
#   0   UNLOCKED
#   1   LOCKING
#   2   LOCKED
#   3   DANGER 

state = 0
time.sleep(2)
gc.enable()

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5

# connection key
dev_eui = binascii.unhexlify('70B3D5499C89CC8F')
app_eui = binascii.unhexlify('0000000000000000')
app_key = binascii.unhexlify('7C47AF78F8A226FE740FBB6BFFD07B62')


lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# remove all the default channels for EU868
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency (must be before sending the join request)
lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=5)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(6)
    print('Attempting to join lora network...')

print('Network joined!')

#LoRa socket init
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, LORA_NODE_DR)
s.setblocking(False)

py = Pycoproc(Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)
lockcoord = None
time.sleep(5.0)

# state machine -> UNLOCKED, LOCKING, LOCKED, DANGER
    
    if state == 1:
        pycom.rgbled(0xFFFF00) # yellow
        coord = l76.coordinates()
        lockcoord = coord
        state = 2
        state = set_state(state, coord, s, "Locking system at {}", 30)        

    elif state == 2:
        pycom.rgbled(0xFF0F00) # orange
        coord = l76.coordinates()
        if isMoving(coord, lockcoord):
            state = 3
            state = set_state(state, coord, s, "Locked system is moving at {}", 30)
            
        else:
            state = set_state(state, coord, s, "Locked system at {}", 300)
            
    elif state == 3:
        pycom.rgbled(0xFF0000) # red
        coord = l76.coordinates()
        state = set_state(state, coord, s, "Locked system might be in danger at {}", 30)

    else:
        pycom.rgbled(0x00FF00) # green
        coord = l76.coordinates()        
        state = set_state(state, coord, s, "System is Idle at {}", 300)

# Sets new state if any alarm on/off message is received
# and sends position data each 5 minutes or 30 seconds depending on sleeptime

def set_state(state, coord, s, msg, sleeptime):
    print(msg.format(coord))
    if coord[0] == None: 
        b = "NoSignal".encode('utf-8')
        s.send(b)           

    else :
        b = str(coord[0]).encode('utf-8') + str(coord[1]).encode('utf-8')
        s.send(b)
    time.sleep(sleeptime) 
    rx, port = s.recv(256)

    if rx:
        data = rx.decode('utf-8')
        print('Received: ' data)
        if data.lower() == "on": 
            state = 1
            return state

        elif data.lower() == "off":
            state = 0
            return state

    else
        return state

def isMoving(coord, lockcoord):
    if sqrt(pow(coord[0]-lockcoord[0],2) + pow(coord[1]-lockcoord[1],2)) > 0.0003:
        return True
    else return False
    
