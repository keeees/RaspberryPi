
import time
from bluetooth import *
MAXBUFLEN = 1024
def readn(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if packet == '':
            return ''
        data += packet
    #size_buff = data
    return data
    
server_sock=BluetoothSocket( RFCOMM )
#server_sock.setblocking(False)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        count = server_sock.recv(MAXBUFLEN)
        num_files = int.from_bytes(count, byteorder='big')
        print('Number of files to be received', int.from_bytes(count, byteorder='big'))
        #time_start = time.clock()
        for i in range(num_files):
            #while(readn(server_sock,4)!=''):
            size_buff = readn(server_sock, 4)
            if size_buff == '':
                print('Failed to receive file size.')
                server_sock.close()
                sys.exit(3)

            size_unpacked = struct.unpack('!I', size_buff)
            file_size = size_unpacked[0]
            print('Will receive file of size', file_size, 'bytes.')

            with open('received_file_%i.jpg' %i, 'wb') as f:
                BUFFER = MAXBUFLEN
                while file_size > 0:
                    if(file_size<BUFFER):
                        BUFFER=file_size
                    data = server_sock.recv(BUFFER)
                    #print(len(data), 'bytes received.')
                    if not data:
                        print('End of  file.',i)
                        break
                    f.write(data)
                    file_size -= len(data)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
