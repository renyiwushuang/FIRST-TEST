
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

import json

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")
#sub_list.append("/EH100602/rx/#")
print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)

xyz_mq = Queue()
xyz_mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,["/LocXYZ/#"],xyz_mq)


def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)



p_2a0a_dict = dict()
def Prase_2A16_Test(data,l,port):
    
    global p_2a0a_dict
    global p_2a0a_set
    index = 0

    #print(binascii.hexlify(data))

    tp = struct.unpack("<BHHBB",data[index:7])
    index += 7
    
    bs_addr_r = tp[1]
    mode = tp[3]
    num = tp[4]
    #print(tp)
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))
         
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<IBHBHBIbb",data[index:17+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 17
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        if (tp[-1] & 0x80) == 0x80:
            if (card_addr in p_2a0a_dict.keys()) == False:
                p_2a0a_dict[card_addr] = dict()
                p_2a0a_dict[card_addr][unix_ts] = dict()
                p_2a0a_dict[card_addr][unix_ts]["bs_list"] = list()
                p_2a0a_dict[card_addr][unix_ts]["dis_list"] = list()
            p_2a0a_dict[card_addr][unix_ts]["bs_list"].append(bs_addr_r)
            





#mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)
mqtt_prase.add_cmd(0x2A16,Prase_2A16_Test)




#解包线程类
class xyz_class(threading.Thread):
    def __init__(self,t_name,mq):
        threading.Thread.__init__(self, name=t_name)
        self.handler_mq = mq
    def run(self):
        global p_2a0a_dict
        
        while(True):
            data = self.handler_mq.get()
            data_str = data[0].decode("utf-8")
            json_data = json_loads(data_str)
            for card_info in json_data:
                if card_info["card_id"] in p_2a0a_dict.keys():
                    if card_info["seq_num"] in p_2a0a_dict[card_info["card_id"]].keys():
                        p_2a0a_dict[card_info["card_id"]][card_info["seq_num"]][dis_list].append(card_info["card_x"])
                        p_2a0a_dict[card_info["card_id"]][card_info["seq_num"]][dis_list].append(card_info["card_y"])
                        p_2a0a_dict[card_info["card_id"]][card_info["seq_num"]][dis_list].append(card_info["card_z"])
                    

xyz_instance = input_class("xyz",xyz_mq)
xyz_instance.start()

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
            if str == "clear":
                #print(self.d)
                p_2a0a_dict = dict()
                #print(self.d)
            if str == "save":
                pass
            

input_instance = input_class("input",p_2a0a_dict)
input_instance.start()

card_sc_sum = 0        
while(True):
    time.sleep(2)
    print(p_2a0a_dict)

        
        




        
