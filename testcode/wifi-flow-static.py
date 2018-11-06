
from queue import Queue
import binascii
import struct
import time
import os
import sys
import threading

import config

from components.MQTT import MqttThread
from components.PacketPrase import prase

from components.Figures import Figures

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")

#mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)


sub_topic_header = "/EH100602/tx/"
average_period = 1 #1s

show = dict()

show["figure_wifi_tx"] = dict()
show["figure_wifi_tx"]["xmax"] = 1000
show["figure_wifi_tx"]["show"] = dict()
show["figure_wifi_tx"]["ylabel"] = "Bytes"
        
show["figure_wifi_rx"] = dict()
show["figure_wifi_rx"]["xmax"] = 1000
show["figure_wifi_rx"]["show"] = dict()


time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)


print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)

average_rate_dict = dict()

def calc_rate():
    global average_dict,show

    #print("calc_rate")
    rate_timer = threading.Timer(average_period, calc_rate)
    rate_timer.start()
    
    for rate_id in average_rate_dict.keys():
        
        if((rate_id in show["figure_wifi_tx"]["show"].keys()) == False):
            show["figure_wifi_tx"]["show"][rate_id] = dict()
            show["figure_wifi_tx"]["show"][rate_id]["data"] = list()
            
        show["figure_wifi_tx"]["show"][rate_id]["data"].append(average_rate_dict[rate_id])
        average_rate_dict[rate_id] = 0


rate_timer = threading.Timer(average_period,calc_rate)
rate_timer.start()

while(True):
    msg=mq.get()
    bs_id_str = msg[1][len(sub_topic_header):]
    #print(msg[1][len(sub_topic_header):],len(msg[0]))

    if (bs_id_str in average_rate_dict.keys()) == False:
        average_rate_dict[bs_id_str] = len(msg[0])
    else:
        average_rate_dict[bs_id_str] += len(msg[0])



        
        




        
