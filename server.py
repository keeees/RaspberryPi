import socket
import os
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = ''
TCP_PORT = 60001
BUFFER_SIZE = 1024

print 'TCP_IP=',TCP_IP
print 'TCP_PORT=',TCP_PORT

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        Path = "/home/pi/Downloads/"
        filelist = os.listdir(Path)
        for i in filelist:
            if i.endswith(".jpg"):  # You could also add "and i.startswith('f')
                with open(Path + i, 'r') as f:
                    while True:
                        l = f.read(BUFFER_SIZE)
                        while (l):
                            self.sock.send(l)
                            l = f.read(BUFFER_SIZE)
                        if not l:
                            f.close()
                            self.sock.close()
                            break
        #filename='/home/pi/Downloads/cloud-formation-clouds-cloudy-247478.jpg'
        #f = open(filename,'rb')
        #while True:
         #   l = f.read(BUFFER_SIZE)
          #  while (l):
           #     self.sock.send(l)
            #    #print('Sent ',repr(l))
            #    l = f.read(BUFFER_SIZE)
            #if not l:
             #   f.close()
              #  self.sock.close()
               # break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()