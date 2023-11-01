
from queue import Queue
import binascii
import struct
import time
import os
import sys
import threading


from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.PacketPrase import packet

from components.Figures import Figures

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")

sub_list = list()
#mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)


sub_topic_header = "/EH100602/tx/"
average_period = 0.1 #1s

show = dict()

show["figure_wifi_tx"] = dict()
show["figure_wifi_tx"]["xmax"] = 1000
show["figure_wifi_tx"]["show"] = dict()
show["figure_wifi_tx"]["ylabel"] = "Bytes"
        
show["figure_wifi_rx"] = dict()
show["figure_wifi_rx"]["xmax"] = 1000
show["figure_wifi_rx"]["show"] = dict()


time.sleep(1)
#show_instance = Figures.FiguresInit("show",show)
time.sleep(1)

mqtt = MqttThread.mqtt_thread_init("192.168.100.139",sub_list,mq)

average_rate_dict = dict()

'''
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

'''

while(True):
    time.sleep(0.01)
    frame=packet.get_packet(0xab12,b'1234567890',len(b'1234567890'))
    mqtt.mqtt_pub("/EH100602/tx/ab12",frame)



        
        




        
