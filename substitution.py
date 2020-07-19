#!/usr/bin/env python3

import struct
import math
import dpkt
import socket
import random
import numpy
from collections import Counter
from frequency import *

def substitute(attack_payload, substitution_table):
    # Using the substitution table you generated to encrypt attack payload
    # Note that you also need to generate a xor_table which will be used to decrypt
    # the attack_payload
    # i.e. (encrypted attack payload) XOR (xor_table) = (original attack payload)
    b_attack_payload = bytearray(attack_payload, "utf8")
    result = []
    xor_table = []
    # print(b_attack_payload)

    result = []

    for untouched_char_unicode in b_attack_payload:
        # print(chr(current_byte))
        sub_frequencies = substitution_table[chr(untouched_char_unicode)]
        total_frequencies = 0
        sub_frequencies_probabilities = []
        for current_frequency in sub_frequencies:
            total_frequencies += current_frequency[1]
        for current_frequency in sub_frequencies:
            # print('Total frequencies and current frequency divided is... ')
            # print(current_frequency[1]/total_frequencies)
            # print('Current frequency is... ')
            # print(current_frequency)
            # print('Total frequency is... ')
            # print(total_frequencies)
            # print('All frequencies are... ')
            # print(sub_frequencies)
            sub_frequencies_probabilities.append(current_frequency[1]/total_frequencies)
            # print(sub_frequencies_probabilities)
        # print(list(map(mapProbabilities, sub_frequencies)))
        listOfLetterNames = list(map(mapLetterNames, sub_frequencies))
        # selected_char = numpy.random.choice(listOfLetterNames, sub_frequencies_probabilities)
        selected_char = random.choices(population = listOfLetterNames, weights = sub_frequencies_probabilities)[0]
        # print('Found the char!')
        # print(selected_char)
        substituted_char_unicode = ord(selected_char)
        xor_char_unicode = untouched_char_unicode ^ substituted_char_unicode
        xor_char = chr(xor_char_unicode)

        xor_table.append(xor_char)
        result.append(selected_char)
    
    # print('Printing random choices')
    
    # print(numpy.random.choice([5, 3, 2], p = [0.8, 0.1, 0.1]))

    # Based on your implementattion of substitution table, please prepare result
    # and xor_table as output

    return (xor_table, result)

def getSubstitutionTable(artificial_payload, attack_payload):
    substitution_table = {}
    # You will need to generate a substitution table which can be used to encrypt the attack
    # body by replacing the most frequent byte in attack body by the most frequent byte in
    # artificial profile one by one

    # Note that the frequency for each byte is provided below in dictionay format.
    # Please check frequency.py for more details
    # print("in here")
    artificial_frequency = frequency(artificial_payload)
    attack_frequency = frequency(attack_payload)

    sorted_artificial_frequency = sorting(artificial_frequency)
    sorted_attack_frequency = sorting(attack_frequency)
    # print(sorted_artificial_frequency)
    # print(sorted_attack_frequency)

    # for x in sorted_attack_frequency:
        # print (x)
        # substitution_table[x] = 
    for i in range(len(sorted_attack_frequency)):
        # print (sorted_attack_frequency)
        substitution_table[sorted_attack_frequency[i][0]] = [sorted_artificial_frequency[i]]
    

    # count = 0
    for item in sorted_artificial_frequency[len(sorted_attack_frequency):]:
        max_ratio_frequency = calculateFrequencyWithMaxRatio(sorted_attack_frequency, substitution_table)
        substitution_table[max_ratio_frequency[0]].append(item)
        # print(max_ratio_frequency)
        # print('Adding a new item to the dictionary')
        # print(item)

        # print('doing stuff')
        # count = count + 1
    # print('Count for times sorted artificial was run through')
    # print(count)
    # print('Length of artifical sorted array is... ')
    # print(len(sorted_artificial_frequency))
    # print('Length of attack sorted array is... ')
    # print(len(sorted_attack_frequency))
    # print(substitution_table)
    # Your code here ...

    
    # Make sure your substitution table can be used in
    # substitute(attack_payload, subsitution_table)
    # print(substitution_table)
    return substitution_table

def mapLetterNames(x):
    return x[0]

def calculateFrequencyWithMaxRatio(sorted_attack_frequency, substitution_table):
    # Find m char with max ratio of g(y_j)/t^f(y_j)
    max_ratio = 0
    max_ratio_attack_frequency = None
    for single_attack_frequency in sorted_attack_frequency:
        sub_frequencies_total = 0
        # print(substitution_table)
        for sub_frequency in substitution_table[single_attack_frequency[0]]:
            sub_frequencies_total += sub_frequency[1]
            # print(sub_frequency)
        # print(sub_frequencies_total)
        # print(substitution_table[single_attack_frequency])
        current_ratio = single_attack_frequency[1] / sub_frequencies_total
        # print(current_ratio)
        if current_ratio > max_ratio:
            max_ratio = current_ratio
            max_ratio_attack_frequency = single_attack_frequency
    return max_ratio_attack_frequency

def getAttackBodyPayload(path):
    f = open(path, 'rb')
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        if socket.inet_ntoa(ip.dst) == "192.150.11.111": 
            tcp = ip.data
            if tcp.data == "":
                continue
            return tcp.data.rstrip()

def getArtificialPayload(path):
    f = open(path, 'rb')
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        if tcp.sport == 80 and len(tcp.data) > 0:
            return tcp.data
