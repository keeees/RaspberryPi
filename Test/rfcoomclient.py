import time
from bluetooth import *
import sys
MAXBUFLEN = 1024
if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("no device specified.  Searching all nearby bluetooth devices for")
    print("the SampleServer service")
else:
    addr = sys.argv[1]
    print("Searching for SampleServer on %s" % addr)

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("connected.  type stuff")
while True:
    Path = "/home/pi/Downloads/"
    #Path = "/home/ke/Downloads/"
    filelist = os.listdir(Path)
    count = 0
    for i in filelist:
        if i.endswith(".jpg"):
            count+=1
    print('number of file', count)
    sock.send(struct.pack("B",count))
    for i in filelist:
        if i.endswith(".jpg"):
            file_size = os.path.getsize(Path+i)
            print(file_size)
            buffer = b''
            buffer = struct.pack('!I', file_size)
            print('File size packed into binary format:', buffer)
            sock.sendall(buffer)
            time.sleep(0.5)
            with open(Path + i, 'rb') as f:
                while True:
                    l = f.read(MAXBUFLEN)
                    while (l):
                        sock.send(l)
                        l = f.read(MAXBUFLEN)
                        time.sleep(0.5)
                    if not l:
                        f.close()
                        break
            time.sleep(0.25)
sock.close()
