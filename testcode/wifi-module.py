
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
from components.PacketPrase import packet
from components.Figures import Figures
from components.SerialCom import SerialThread

'''
参数解析
'''
bs_id = "2cbe"
com_port = "COM19"
if(len(sys.argv ) > 2):
    com_port = sys.argv[1]
    bs_id = sys.argv[2]


'''
串口数据
'''
com_mq = Queue()
com_instance = SerialThread.SC_thread_init(com_mq,com_port,460800)

'''
串口解析
'''
def com_unregisterfun(cmd,data,port):
    #print(hex(cmd),':',binascii.hexlify(data).upper())
    frame=packet.get_packet(cmd,data,len(data))
    mqtt.mqtt_pub(config.mqtt_topic_tx_header+bs_id,frame)
    
com_prase = prase.prase_class_init("com_prase",com_mq,com_unregisterfun)

'''
MQTT数据
'''
mqtt_mq = Queue()
sub_list = list()
sub_list.append(config.mqtt_topic_rx_header+bs_id)  
print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mqtt_mq)

average_period = 3
wifi_seq=0
def wifi_hb_send():
    global wifi_seq
    rate_timer = threading.Timer(average_period, wifi_hb_send)
    rate_timer.start()
    data = struct.pack("<HIIbB3s6sBBH",int(bs_id,16),0x01,0x09,-50,0x03,b'123',b'\1\2\3\4\5\6',0x3,0x1,wifi_seq)
    wifi_seq += 1
    frame = packet.get_packet(0x0A80, data, len(data))
    com_instance.send(frame,len(frame))
    mqtt.mqtt_pub(config.mqtt_topic_tx_header+bs_id,frame)
    
rate_timer = threading.Timer(average_period,wifi_hb_send)
rate_timer.start()

while(True):

    com_rcv_data = mqtt_mq.get()
    if len(com_rcv_data[0]):
       #print(binascii.hexlify(com_rcv_data[0]))
       #print(com_rcv_data[0])
       com_instance.send(com_rcv_data[0],len(com_rcv_data[0]))



        
        




        
