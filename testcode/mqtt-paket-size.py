
from queue import Queue
import binascii
import struct
import time
import os
import sys

import config

from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.FileSave import FileSave

mq = Queue()
sub_list = list()
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


file_mq = Queue()
FileSave.File_Save_Init("file_save","./","mqtt-packet-size.txt",file_mq)




max_size = 0
min_size = 0xffffffff
while(True):
    msg=mq.get()
    #print(len(msg[0]))

    max_size = max(max_size,len(msg[0]))
    min_size = min(min_size,len(msg[0]))
    str_context = "max:\t%d\t min:\t%d\t 当前值:\t%d\n"%(max_size,min_size,len(msg[0]))
    print(str_context)
    #str_context += "\n"
    file_mq.put(str_context.encode("utf-8"))

    #time.sleep(0.1)
