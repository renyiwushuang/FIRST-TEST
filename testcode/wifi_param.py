
from queue import Queue
import binascii
import struct
import time
import os
import sys

from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.PacketPrase import packet

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")

#sub_list.append("/EH100602/rx/#")
mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


def Prase_0A81_wifi_query_cfg_ack(data,l,port):
    #print(data)
    #print(type(data),len(data))
    tp = struct.unpack("<H20s20s20s",data[:-3])
    print("0x%04x  %s %s %s"%(tp[0],tp[1].decode("utf-8"),tp[2].decode("utf-8"),tp[3].decode("utf-8")))
mqtt_prase.add_cmd(0x0A81,Prase_0A81_wifi_query_cfg_ack)

time.sleep(2)
query_data = b''
query_paket=packet.get_packet(0x0B81, query_data, len(query_data))
#print(binascii.hexlify(query_paket))
mqtt.mqtt_pub("/EH100602/rx/ff01",query_paket)
while(True):
    #input_context = input("input :s(suspend figure),r(resume figure)")
    #if(input_context == "s"):
        #show_instance.suspend()
    #mqtt.mqtt_pub("/EH100602/rx/ff01",query_paket)
    time.sleep(5)
    


        
        




        
