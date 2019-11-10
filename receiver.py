import os
import sys
import socket
import subprocess


hostname = 'localhost'
hostport = 30002
MAXBUFLEN = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname,hostport))
s.listen(2)
sockfd,addr = s.accept()

print('Connection established')
count = sockfd.recv(MAXBUFLEN)
num_files = int.from_bytes(count, byteorder='big')
print('Number of files to be received', int.from_bytes(count, byteorder='big'))
for i in range(num_files):
    with open('received_file_%i.jpg' %i, 'wb') as f:
        while True:
            data = sockfd.recv(MAXBUFLEN)
            if not data:
                f.close()
                break
            f.write(data)


sockfd.close()
print('Success, connection closed')
#bashCommand = "sudo fbi -a -T 1 /home/pi/RaspberryPi/received_file"
#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#output, error = process.communicate()
