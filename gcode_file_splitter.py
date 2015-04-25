
"""
Run this program in the directory containing the gcode files
you would like to split into 2 files for inserting nuts, etc.
You will be prompted for the file name and the z-height to
stop the print at.
"""

import sys
import re
import time

while True:    
    filename = raw_input('\nEnter filename: ')
    try:
        f = open(filename,'r')
        text = f.read()
        f.close()
    except Exception:
        print filename, "doesn't exist.."
        time.sleep(1)
        continue
    break
    

while True:
    zpos = raw_input('\nEnter z-height to break file at: ')
    m = re.search(r'G.*Z' + zpos, text)
    if m:
        break
    print 'Invalid z-height!'
    time.sleep(1)
    
i = m.start()

g1 = text[:i]
g2 = text[i:]

endText = """
******************End of file 1of2 code******************
G1 X190.000 Y190.000	; move away to edge of bed
M104 S0 ; turn off nozzle temperature
M140 S0 ; turn off bed temperature
"""

g1 += endText

startText = """
******************Start of file 2of2 code******************

;resume with the rest of the print after nuts have been inserted

M190 S110 ; wait for bed temperature to be reached
M104 S230 ; set temperature
M109 S230 ; wait for temperature to be reached

"""

g2 = startText + g2
filename1 = filename.split('.')[0] + '(1of2)' + '.gcode'
filename2 = filename.split('.')[0] + '(2of2)' + '.gcode'

with open(filename1,'w') as f:
    f.write(g1)
    f.close()

with open(filename2,'w') as f:
    f.write(g2)
    f.close()

print '\nGCode file conversion complete!'

time.sleep(1)



