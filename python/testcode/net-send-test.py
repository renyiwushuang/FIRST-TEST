
from queue import Queue
import binascii
import struct
import time
import os
import sys
import threading
import ctypes

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
    #sub_list.append("/EH100602/tx/#")
    pass

show = dict()

show["figure_wifi_delay"] = dict()
show["figure_wifi_delay"]["xmax"] = 1000
show["figure_wifi_delay"]["show"] = dict()
show["figure_wifi_delay"]["ylabel"] = "s"
        
show["figure_wifi_delay"]["show"]["send"] = dict()
show["figure_wifi_delay"]["show"]["send"]["data"] = list()

sub_list = list()
#mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)


sub_topic_header = "/EH100602/tx/"
average_period = 0.01 #1s




time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)

mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)

average_rate_dict = dict()

prebuffer = ctypes.create_string_buffer(40)
send_dat = bytes(prebuffer)

old_time=0

def calc_rate():
    global old_time,show,calc_rate

    #print("calc_rate")
    rate_timer = threading.Timer(average_period, calc_rate)
    rate_timer.start()
    
    frame=packet.get_packet(0xab12,send_dat,len(send_dat))
    mqtt.mqtt_pub("/NetTest/tx/test",frame)
    t = time.time()

    if old_time != 0 :
        show["figure_wifi_delay"]["show"]["send"]["data"].append(t-old_time)

    old_time = t


rate_timer = threading.Timer(average_period,calc_rate)
rate_timer.start()





while(True):
    time.sleep(10)
    
    #print(time.time())


        
        




        
