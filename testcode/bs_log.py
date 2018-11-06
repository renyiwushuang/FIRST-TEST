
from queue import Queue
import binascii
import struct
import time
import os
import sys

import config

from components.MQTT import MqttThread
from components.PacketPrase import prase

mq = Queue()
sub_list = list()
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)




def Prase_2A0B_bs_log(data,l,port):
    
    index = 0

    #print(binascii.hexlify(data))
    
    #bs_id(2B) + log_level(1B)
    bs_id,log_level = struct.unpack("<HB",data[index:3])
    index += 3
    
    log_str, = struct.unpack("<%ds"%(l-index),data[index:])


    print("%04x\t%d\t%s"%(bs_id,log_level,log_str.decode('utf-8')))
        


mqtt_prase.add_cmd(0x2A0B,Prase_2A0B_bs_log)

while(True):
    time.sleep(2)

        
        




        
