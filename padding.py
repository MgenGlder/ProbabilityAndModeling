#!/usr/bin/env python3

import struct
import math
import random
from frequency import *
from collections import Counter

def padding(artificial_payload, raw_payload):
    padding = ""
    
    # Get frequency of raw_payload and artificial profile payload
    artificial_frequency = frequency(artificial_payload)
    raw_payload_frequency = frequency(raw_payload)
    letterOfChoice = ''
    # print(artificial_frequency)
    max_difference = 0
    for normal_letter, normal_frequency in artificial_frequency.items():
        attack_frequency = 0
        # print(normal_letter)
        # print(normal_frequency)
        if normal_letter in raw_payload_frequency:
            attack_frequency = raw_payload_frequency[normal_letter]
        difference = normal_frequency - attack_frequency
        if (difference > max_difference):
            max_difference = difference
            print(difference)
            letterOfChoice = normal_letter
        
    print('Adding the letter...')
    print(letterOfChoice)
    raw_payload.append(letterOfChoice)

        # if (max_difference > )
    # To simplify padding, you only need to find the maximum frequency difference for each
    # byte in raw_payload and artificial_payload, and pad that byte at the end of the
    # raw_payload. 
    # Note: only consider the differences when artificial profile has higher frequency.


    # Depending upon the difference, call raw_payload.append


    # Your code here ... 
