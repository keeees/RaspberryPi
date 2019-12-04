import os
import time
import sys
import socket
import subprocess
import struct
import io
from PIL import Image
import numpy as np
import cv2


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
#count = 0

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow('img',cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('img',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
try:
    while True:
        t1 = cv2.getTickCount()

        #waiting for signal from sender
        image_size = struct.unpack('<L',f.read(struct.calcsize('<L')))[0]
 
         #received signal from sender, send request for the file
        f.write(struct.pack('<L',ack)) #get size in little endian unsigned long

        f.flush()

        #start receiving file
        stream = io.BytesIO()
        stream.write(f.read(image_size))
        stream.seek(0)

        img = cv2.imdecode(np.fromstring(stream.read(),np.uint8),1)
        cv2.putText(img,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        cv2.imshow("img",img)
        
         
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        if cv2.waitKey(1) == ord('q'):
            break
        #save image
        #image = Image.open(stream)
        #print('receive image'+str(count))
        #image.save('image.jpg')
        #count+=1
        #image.show()
        
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
