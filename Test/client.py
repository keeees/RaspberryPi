
import socket
import time
import subprocess

TCP_IP = '192.168.50.34'
TCP_PORT = 60001

BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

clock_start = time.clock()
time_start = time.time()

with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        #print('receiving data...')
        data = s.recv(1024)
        #print('data=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')

bashCommand = "sudo fbi -a -T 1 /home/pi/RaspberryPi/received_file"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

clock_end = time.clock()
time_end = time.time()

duration_clock = clock_end - clock_start
print 'clock:  start = ',clock_start, ' end = ',clock_end
print 'clock:  duration_clock = ', duration_clock

duration_time = time_end - time_start
print 'time:  start = ',time_start, ' end = ',time_end
print 'time:  duration_time = ', duration_time