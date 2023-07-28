
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




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


'''
#{"bs_id":
         {
           "card":
                   {
                     "_card_id":
                           {
                           "max":xxx,
                           "min":xxx,
                           "cnt":xxx
                           }
                    }
            "card_num":set()
          }
 }
'''
p_2a0a_dict = dict()

#p_2a0a_set = dict()
def Prase_2A0A_Test(data,len,port):
    
    global p_2a0a_dict
    global p_2a0a_set
    index = 0


    #print(binascii.hexlify(data))

    tp = struct.unpack("<HBB",data[index:4])
    index += 4
    
    bs_addr_r = tp[0]
    mode = tp[1]
    num = tp[2]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))
    if (bs_addr_r in p_2a0a_dict.keys()) == False:
         p_2a0a_dict[bs_addr_r] = dict()
         p_2a0a_dict[bs_addr_r]["card"] = dict()
         p_2a0a_dict[bs_addr_r]["card_num"] = set()
         
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<IBHBHBIb",data[index:16+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 16
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        if (card_addr in p_2a0a_dict[bs_addr_r]["card"].keys()) == False:
            p_2a0a_dict[bs_addr_r]["card"][card_addr] = dict()
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = 0x00000000
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = 0xffffffff
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = 0x00000000

            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]+1
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"] = tp[7]
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cl"] = 101

        else:
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]+1
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"] = tp[7]
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cl"] = 101
        p_2a0a_dict[bs_addr_r]["card_num"].add(card_addr)

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
    if (bs_addr_r in p_2a0a_dict.keys()) == False:
         p_2a0a_dict[bs_addr_r] = dict()
         p_2a0a_dict[bs_addr_r]["card"] = dict()
         p_2a0a_dict[bs_addr_r]["card_num"] = set()
         
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<IBHBHBIbB",data[index:17+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 17
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        if (card_addr in p_2a0a_dict[bs_addr_r]["card"].keys()) == False:
            p_2a0a_dict[bs_addr_r]["card"][card_addr] = dict()
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = 0x00000000
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = 0xffffffff
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = 0x00000000

        p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"],unix_ts)
        p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"],unix_ts)
        p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]+1
        p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"] = tp[7]
        p_2a0a_dict[bs_addr_r]["card"][card_addr]["cl"] = tp[8]


        p_2a0a_dict[bs_addr_r]["card_num"].add(card_addr)
        if 667==card_addr and 0x2cb7 == bs_addr_r:
            print(unix_ts)
            #print(unix_ts)
            #if(tp[7] > -50):
            #print("rssi:%d",tp[7])


#mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)
mqtt_prase.add_cmd(0x2A16,Prase_2A16_Test)

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

card_sc_sum = 0        
while(True):
    time.sleep(2)
    if p_2a0a_dict :

        bs_list = list(p_2a0a_dict.keys())
        bs_list.sort()

        
        os.system('cls')
        
        for bs_addr_r in bs_list:
            card_list = list(p_2a0a_dict[bs_addr_r]["card"].keys())
            card_list.sort()
            card_sc_sum = 0
            for card_addr in card_list:
                max_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"]
                min_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"]
                cnt_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]
                card_sc_sum += cnt_v/(max_v-min_v+1)
            print("bs addr:%x(%d)card num:%d %0.1f %%"%(bs_addr_r,bs_addr_r,len( p_2a0a_dict[bs_addr_r]["card_num"]),card_sc_sum/len( p_2a0a_dict[bs_addr_r]["card_num"])*100))
            
            for card_addr in card_list:
                max_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"]
                min_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"]
                cnt_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]
                rssi_v = p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"]
                cl = 101
                try:
                    cl  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cl"]
                except e:
                    pass
                print("\t%05d(%04x)\tcnt:%05d\t%0.1f %%\trssi:%d\tCL:%d"%(card_addr,card_addr,cnt_v, cnt_v/(max_v-min_v+1)*100,rssi_v,cl))

        
        




        
