import sys
import serial
import os
import argparse
from datetime import datetime

taimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="seria port name (etc COM3 or /dev/ttyUSB0)", default = 'COM18')
parser.add_argument("--out", help="output file name", default = 'stopwatch_{}.txt'.format(taimestamp))
parser.add_argument("--date", help="start date", default = '12.10.2001')
parser.add_argument("--verbose", help="increase output verbosity",action="store_true")

args = parser.parse_args()
#print args
serialport = serial.Serial(args.port, 9600, timeout=0.5)
fname = args.out
fout = open(fname,"w+")
bogus = args.date

print 'Press A button to upload results...'

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

while 1:
	response = serialport.readlines(None)
	if len(response) >= 2:
		indata = response[1].encode("hex") 		
		break

line = 'STARTOFEVENT,{} 00:00:00,junsd_stopwatch\n0,{} 00:00:00\n'.format(bogus,bogus) 
if args.verbose:
    print line

fout.write(line)

chunks = wrap(indata[6:], 16)

for chunk in chunks:

    if chunk[:4] == 'abc3':    
        pla = int(chunk[5:8])
        hour = int(chunk[8:10])
        min = int(chunk[10:12])
        sec = int(chunk[12:14])
        dsec = int(chunk[14:16])

        if dsec > 50 : 
            sec += 1

        if sec == 60 : 
            min += 1
            sec = 0 

        if min == 60 : 
            hour += 1
            min = 0 
        line = '{},{},{}:{}:{},{}:{}:{}\n'.format(pla,bogus,hour,min,sec,hour,min,sec)
        if args.verbose:
            print line
        fout.write(line) 

line = 'ENDOFEVENT,{}:{}:{}\n'.format(bogus,hour,min,sec)

if args.verbose:
    print line

fout.write(line)
fout.close() 

print 'Done, saved to {}'.format(fname)git
