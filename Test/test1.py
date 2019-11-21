import wget
import time
from ftplib import FTP
clock_start = time.clock()
time_start = time.time()
for i in range(1):

    url = 'http://192.168.50.142:8000/test.jpg'
    filename = wget.download(url)
    clock_end = time.clock()
    time_end = time.time()
   # time.sleep(0.25)

duration_clock = clock_end - clock_start
print ('clock:  start = ',clock_start, ' end = ',clock_end)
print ('clock:  duration_clock = ', duration_clock)

duration_time = time_end - time_start
print ('time:  start = ',time_start, ' end = ',time_end)
print ('time:  duration_time = ', duration_time)
