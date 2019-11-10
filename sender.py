import sys
import os
import socket
import struct
from threading import Thread
from socketserver import ThreadingMixIn

hostname = 'localhost'
hostport = 30002
MAXBUFLEN = 1024



class SenderThread(Thread):

    def __init__(self, ip,port,sock):
        ''' Constructor. '''
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New thread started")

    def run(self):

        #Path = "/home/pi/Downloads/"
        Path = "/home/ke/Downloads/"
        filelist = os.listdir(Path)
        count = 0
        for i in filelist:
            if i.endswith(".jpg"):
                count+=1
        print('number of file', count)
        self.sock.send(struct.pack("B",count))
        for i in filelist:
            if i.endswith(".jpg"):
                with open(Path + i, 'rb') as f:
                    while True:
                        l = f.read(MAXBUFLEN)
                        while (l):
                            self.sock.send(l)
                            l = f.read(MAXBUFLEN)
                        if not l:
                            f.close()
                            break
        self.sock.close()


sockfd = None
for res in socket.getaddrinfo(hostname, hostport, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        sockfd = socket.socket(af, socktype, proto)
    except OSError as msg:
        sockfd = None
        continue
    try:
        sockfd.bind(sa)
    except OSError as msg:
        sockfd.close()
        sockfd = None
        continue
    break
if sockfd is None:
    print('could not open socket')
    sys.exit(1)
#sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#socket.bind((hostname,hostport))
threads = []

while True:
    sockfd.listen()
    print('Listening on',(hostname, hostport))
    conn, (ip,port) = sockfd.accept()
    print('Connected by', (ip,port))
    newthread = SenderThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)
    break

for t in threads:
    t.join()
