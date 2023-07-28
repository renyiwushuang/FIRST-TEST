
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

mq = Queue()
sub_list = list()

default_id = "1131"#0x5069
if(len(sys.argv ) > 1):
    #for i in range(1,len(sys.argv)):
        #sub_list.append("/EH100602/tx/"+sys.argv[i])
    default_id = sys.argv[1].lower()
else:
    #sub_list.append("/EH100602/tx/"+default_id)
    pass
sub_list.append("/EH100602/tx/"+default_id)
print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)

show = dict()
show["CIR"] = dict()
show["CIR"]["xmax"] = 1016

show["CIR"]["show"] = dict()
show["CIR"]["show"]["Amplitude"] = dict()
show["CIR"]["show"]["Amplitude"]["data"] = list()

show["CIR"]["show"]["Noise"] = dict()
show["CIR"]["show"]["Noise"]["data"] = list()
show["CIR"]["show"]["Noise"]["x_data"] = list()

show["CIR"]["show"]["FP-Index"] = dict()
show["CIR"]["show"]["FP-Index"]["data"] = list()
show["CIR"]["show"]["FP-Index"]["x_data"] = list()

show["CIR"]["show"]["PP-Index"] = dict()
show["CIR"]["show"]["PP-Index"]["data"] = list()
show["CIR"]["show"]["PP-Index"]["x_data"] = list()

show_instance = Figures.FiguresInit("show",show)


def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

noise = 0
fp = 0
pp = 0
cir_buff = list()
filter_len=0
filter_context=0
def Prase_2A12_Test(data,l,port):
    global show,show_instance,cir_buff
    global fp,pp,noise,filter_len,filter_context
    #print(l,binascii.hexlify(data))
    bs_id,seq,cir_size,offset,cir_len=struct.unpack("<HHHHB",data[0:9])
    #print("%04x  序号:%d CIR总大小:%d 偏移:%d 当前长度:%d"%(bs_id,seq,cir_size,offset,cir_len))
    if offset == 0:
        cir_buff = list()
        filter_len,filter_context,rssi,fp,pp,noise=struct.unpack("<B16sbHHH",data[9:33])
        tp=struct.unpack("<%dH"%((cir_len-23)/2),data[33:])
    else:
        tp=struct.unpack("<%dH"%(cir_len/2),data[9:])

    #print(list(tp))
    cir_buff += list(tp)
    if len(cir_buff) > 1000:

        #show["CIR"]["show"] = dict()
        #show["CIR"]["show"]["Amplitude"] = dict()
        #show["CIR"]["show"]["Amplitude"]["data"] = list()
        show["CIR"]["show"]["Amplitude"]["data"] = cir_buff
                                       
        show["CIR"]["show"]["Noise"]["data"] = [noise,noise]
        show["CIR"]["show"]["Noise"]["x_data"] = [0,1015]

        show["CIR"]["show"]["FP-Index"]["data"] = [0,max(cir_buff)+max(cir_buff)*0.3]
        show["CIR"]["show"]["FP-Index"]["x_data"] = [fp,fp]

        show["CIR"]["show"]["PP-Index"]["data"] = [0,max(cir_buff)+max(cir_buff)*0.3]
        show["CIR"]["show"]["PP-Index"]["x_data"] = [pp,pp]
        print("%s 首达-索引:%d 峰值-索引:%d 噪声幅度:%d 最大幅度：%d \tPP-FP:%d"%(binascii.hexlify(filter_context[0:filter_len]),fp,pp,noise,max(cir_buff)+100,pp-fp))    
    #show["figure1"]["show"]["ff01"]["data"] +=  list(tp)

def Prase_2AFF_Ack(data,l,port):
    global need_repeat
    bs_id,cmd,seq,data_check,result=struct.unpack("<HHHBB",data[0:8])
    print("基站:0x%04x  命令:%x  下发序号:%d  数据校验:%d  结果:%d"%(bs_id,cmd,seq,data_check,result))

    if cmd == 0x2a11:
        need_repeat = 0
    
mqtt_prase.add_cmd(0x2A12,Prase_2A12_Test)
mqtt_prase.add_cmd(0x2AFF,Prase_2AFF_Ack)

'''
#解包线程类
class input_class(threading.Thread):
    def __init__(self,t_name,d):
        threading.Thread.__init__(self, name=t_name)
        self.d = d
    def run(self):
        global p_2a0a_dict
        while(True):
            str = input()
            #print("input:",str)
            if str == "c":
                #print(self.d)
                p_2a0a_dict = dict()
                #print(self.d)
            

input_instance = input_class("input",p_2a0a_dict)
input_instance.start()
'''

def uwb_cir_cfg(bs_id,cir_en,filter_len,filter_buff):
    global mqtt
    cfg_pload = struct.pack("<HHBB16s",11,0xffff,cir_en,filter_len,filter_buff)
    cfg_packet = packet.get_packet(0x2a11, cfg_pload, len(cfg_pload))

    bs_rx_topic = config.mqtt_topic_rx_header
    if bs_id == 0xffff:
        bs_rx_topic +=  "brd"
    else:
        bs_rx_topic += "%04x"%(bs_id)
    mqtt.mqtt_pub(bs_rx_topic,cfg_packet)
    #print(bs_rx_topic)

need_repeat = True
while(True):
    if need_repeat:
        uwb_cir_cfg(int(default_id,16),1,len(b'\xc0\xbe\x2c'),b'\xc0\x30\x11')
    time.sleep(2)
    

        
        




        
