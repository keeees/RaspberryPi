import os
import time
import sys
import socket
import subprocess
import struct
import io
from PIL import Image



TCP_IP = '192.168.50.34' #ip address of sender
TCP_PORT = 30002
MAXBUFLEN = 1024
ack = 33
#size_buff = b''
def readn(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if packet == '':
            return ''
        data += packet
    #size_buff = data
    return data
    
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((TCP_IP, TCP_PORT))
#time_start = time.clock()
print('Connection established')


f = sockfd.makefile('rwb')
count = 0
try:
    while True:
        #waiting for signal from sender
        image_size = struct.unpack('<L',f.read(struct.calcsize('<L')))[0]
 
         #received signal from sender, send request for the file
        f.write(struct.pack('<L',ack)) #get size in little endian unsigned long

        f.flush()

        #start receiving file
        stream = io.BytesIO()
        stream.write(f.read(image_size))
        stream.seek(0)
        image = Image.open(stream)
        print('receive image'+str(count))
        image.save('image%d.jpg'%count)
        count+=1
        #bashCommand = 'sudo fbi -a -T 1 -t 1 -1  /home/pi/RaspberryPi/received_file_%i.jpg' %i
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        #time.sleep(1)
except:
    print('Oops!',sys.exc_info()[0],'occured')
    f.close()
    sockfd.close()
#sockfd.close()
#time_end = time.clock()
print('Success, connection closed')
#print('time duration_time = ',time_end-time_start )
#bashCommand = "sudo fbi -a -T 1 /home/pi/RaspberryPi/received_file"
#bashCommand = "sudo fbi -a -T 1 -t 1 -1  /home/pi/RaspberryPi/*.jpg"
#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#output, error = process.communicate()
