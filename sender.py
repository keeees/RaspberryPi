import sys
import time
import os
import socket
import struct
from threading import Thread
from socketserver import ThreadingMixIn
from picamera import PiCamera
import io
from PIL import Image
from PIL import ImageChops

hostname = ''
hostport = 30002
MAXBUFLEN = 1024
ack = 33


class SenderThread(Thread):

    def __init__(self, ip,port,sock):
        ''' Constructor. '''
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started")

    def run(self):
        f = self.sock.makefile('rwb')
        camera = PiCamera()
        camera.resolution = (1280,720)
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()
        camera.capture('foo.jpg')
        stream = io.BytesIO()
        count = 0
        print('start sending image')
        
        try:
            
            for frame in camera.capture_continuous(stream,'jpeg'):
                #check whether image has changed
                prev_image = Image.open('foo.jpg')
                curr_image = Image.open(stream)
                diff = ImageChops.difference(prev_image,curr_image)
                if True:#diff.getbbox(): #if images are different, send size of file
                    print("images are different")
                    f.write(struct.pack('<L',stream.tell())) #get size in little endian unsigned long
                    f.flush()
                    stream.seek(0)
                    
                    #waiting for request from receiver
                    request = f.read(struct.calcsize('<L'))

                    if(request == struct.pack('<L',ack)): #get request
                        f.write(stream.read()) #send simage data
                        curr_image.save('foo.jpg')
                        print('sending image ',count)
                        stream.seek(0)
                        stream.truncate()
                        count+=1
                        
                    else: #no request, buffer file
                        print('no request received, buffer file')
                        
                else:
                    print("images are the same")
        except:
            print('Oops!',sys.exc_info()[0],'occured')
            f.close()
            self.sock.close()

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockfd.bind((hostname,hostport))
threads = []

while True:
    sockfd.listen(5)
    print('Listening ....')
    conn, (ip,port) = sockfd.accept()
    print('Connected by', (ip,port))
    newthread = SenderThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)
    break

for t in threads:
    t.join()
