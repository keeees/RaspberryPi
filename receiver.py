import os
import sys
import socket
import subprocess
import struct

#each file transmission start with sender sending file size, receiver will get the size of file first.
#Then receiver will receive all packets and waiting for next packet

TCP_IP = '192.168.50.34' #ip address of sender
TCP_PORT = 30002
MAXBUFLEN = 1024

def readn(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if packet == '':
            return ''
        data += packet
    return data
    
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((TCP_IP, TCP_PORT))

print('Connection established')
count = sockfd.recv(MAXBUFLEN)
num_files = int.from_bytes(count, byteorder='big')
print('Number of files to be received', int.from_bytes(count, byteorder='big'))
for i in range(num_files):
    size_buff = readn(sockfd, 4)
    if size_buff == '':
        print('Failed to receive file size.', file=sys.stderr)
        sockfd.close()
        sys.exit(3)

    size_unpacked = struct.unpack('!I', size_buff)
    file_size = size_unpacked[0]
    print('Will receive file of size', file_size, 'bytes.')

    with open('received_file_%i.jpg' %i, 'wb') as f:
        BUFFER = MAXBUFLEN
        while file_size > 0:
            if(file_size<BUFFER):
                BUFFER=file_size
            data = sockfd.recv(BUFFER)
            #print(len(data), 'bytes received.')
            if not data:
                print('End of  file.',i)
                break
            f.write(data)
            file_size -= len(data)


sockfd.close()
print('Success, connection closed')
#bashCommand = "sudo fbi -a -T 1 /home/pi/RaspberryPi/received_file"
bashCommand = "sudo fbi -a -T 1 -t 1 -1 --readahead /home/pi/RaspberryPi/*.jpg"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
