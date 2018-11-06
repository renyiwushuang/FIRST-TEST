
from queue import Queue
import binascii
import struct
import time
import os
import sys

import threading

from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.Figures import Figures

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/NetTest/tx/"+sys.argv[i])
else:
    sub_list.append("/NetTest/tx/#")
#sub_list.append("/EH100602/rx/#")



show = dict()

show["figure_wifi_delay"] = dict()
show["figure_wifi_delay"]["xmax"] = 1000
show["figure_wifi_delay"]["show"] = dict()
show["figure_wifi_delay"]["ylabel"] = "s"
        
show["figure_wifi_delay"]["show"]["rcv"] = dict()
show["figure_wifi_delay"]["show"]["rcv"]["data"] = list()

time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)

mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)


MAX_WAIT_DELAY = 10# 2s

def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)




#p_2a0a_set = dict()
old_time=0
def Prase_ab12_Test(data,len,port):
    global old_time
    global show

    t = time.time()

    if old_time != 0 :
        show["figure_wifi_delay"]["show"]["rcv"]["data"].append(t-old_time)

    old_time = t
        




mqtt_prase.add_cmd(0xab12,Prase_ab12_Test)


while(True):
    time.sleep(2)



                    
                
            

        



        
