from ftplib import FTP
import time

ftp = FTP('')
ftp.connect('192.168.50.34',1026)
ftp.login()
ftp.cwd('/RaspberryPi/')
ftp.retrlines('LIST')
#clock_start = time.clock()
time_start = time.time()

def uploadFile():
 filename = 'ray.pdf'
 ftp.storbinary('STOR '+filename, open(filename, 'rb'))
 ftp.quit()

def downloadFile():
    clock_start = time.clock()
    for i in range(1):
        #clock_start = time.clock()
        filename = 'test.jpg'
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        #ftp.quit()
        localfile.close()
    clock_end = time.clock()
    time_end = time.time()
    ftp.quit()
    duration_clock = clock_end - clock_start
    print ('clock:  start = ',clock_start, ' end = ',clock_end)
    print ('clock:  duration_clock = ', duration_clock)

    #duration_time = time_end - time_start
    #print ('time:  start = ',time_start, ' end = ',time_end)
    #print ('time:  duration_time = ', duration_time)

#uploadFile()
downloadFile()
