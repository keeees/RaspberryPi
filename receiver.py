import os
import sys
import socket
import subprocess


TCP_IP = '192.168.50.142'
TCP_PORT = 30002
MAXBUFLEN = 1024


sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((TCP_IP, TCP_PORT))

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
