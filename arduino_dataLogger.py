#!/usr/bin/env python

import os
import serial
import sys
import re
import time


try:
    ser = serial.Serial('/dev/tty.usbmodem621',9600)
    print 'Connected to Arduino'

except Exception:
    print 'Could not connect to Arduino!'
    sys.exit(1)
 
while 1: 
    filename = raw_input('\nEnter filename to save data to: ')
    filename = filename.strip()
    if not '.txt' in filename:
        filename += '.txt'
    
    print 'Data will be saved to ', filename
    time.sleep(0.5)
    
    validInput = False
    
    while not validInput:
        var = raw_input("Press 's' to start logging data, 'q' to quit: ")
        
        if var.strip() == 'q':
            ser.close()
            validInput = True
            sys.exit(1)
            
        elif var.strip() == 's':
            validInput = True
            print 'Logging data...'
            with open(filename,'w') as f:
                ser.flushInput()
                ser.write('s')
                while 1:
                    try:
                        data = ser.readline()
                        f.write(data)
                    except KeyboardInterrupt:
                        f.close()
                        ser.write('s')
                        break
        
    
