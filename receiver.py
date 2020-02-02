import os
import time
import sys
import socket
import subprocess
import struct
import io
from PIL import Image
import numpy as np
import cv2
import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "AePl_v_n50PFiqXjjbuErv_4ccb2ztWZqnGDleVsaNFS" # eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_RESOURCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/6e9a4df7db9b40d5828c209deb0f57d7:41ce9f26-dbbc-49ff-9e8d-42a0b6dbb7b1::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_RESOURCE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
    )

def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))
get_buckets()
multi_part_upload('my-bucket-webgallery', 'item.jpg', '/home/pi/RaspberryPi/foo.jpg')
TCP_IP = '10.182.138.200' #ip address of sender
TCP_PORT = 30002
MAXBUFLEN = 1024
ack = 33
#size_buff = b''
def readn(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if packet == '':
            return ''
        data += packet
    #size_buff = data
    return data
    
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((TCP_IP, TCP_PORT))
#time_start = time.clock()
print('Connection established')

f = sockfd.makefile('rwb')
#count = 0

# Initialize frame rate calculation
frame_rate_calc = 1
#freq = cv2.getTickFrequency()
#font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.namedWindow('img',cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty('img',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
try:
    while True:
        #t1 = cv2.getTickCount()

        #waiting for signal from sender
        image_size = struct.unpack('<L',f.read(struct.calcsize('<L')))[0]
 
         #received signal from sender, send request for the file
        f.write(struct.pack('<L',ack)) #get size in little endian unsigned long

        f.flush()

        #start receiving file
        stream = io.BytesIO()
        stream.write(f.read(image_size))
        stream.seek(0)

        img = cv2.imdecode(np.fromstring(stream.read(),np.uint8),1)
        #cv2.putText(img,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        #cv2.imshow("img",img)
        
         
        #t2 = cv2.getTickCount()
        #time1 = (t2-t1)/freq
        #frame_rate_calc = 1/time1
        #if cv2.waitKey(1) == ord('q'):
        #    break
        
        status = cv2.imwrite('/home/pi/RaspberryPi/image.jpg',img)
        print(status)
        multi_part_upload('my-bucket-webgallery','item.jpg','/home/pi/RaspberryPi/image.jpg')
        #save image
        #image = Image.open(stream)
        #print('receive image'+str(count))
        #image.save('~/ibmcloud/image.jpg')
        #count+=1
        #image.show()
        
except:
    print('Oops!',sys.exc_info()[0],'occured')
    f.close()
    sockfd.close()
#sockfd.close()
#time_end = time.clock()
print('Success, connection closed')
#print('time duration_time = ',time_end-time_start )
#bashCommand = "sudo fbi -a -T 1 /home/pi/RaspberryPi/received_file"
#bashCommand = "sudo fbi -a -T 1 -t 1 -1  /home/pi/RaspberryPi/*.jpg"
#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#output, error = process.communicate()

#sudo LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 receiver.py
