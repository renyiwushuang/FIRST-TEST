
from queue import Queue
import binascii
import struct
import time
import os
import sys
import config

import threading

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
#sub_list.append("/EH100602/rx/#")



show = dict()

show["figure_wifi_delay"] = dict()
show["figure_wifi_delay"]["xmax"] = 1000
show["figure_wifi_delay"]["show"] = dict()
show["figure_wifi_delay"]["ylabel"] = "s"
        


time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)

print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


MAX_WAIT_DELAY = 10# 2s

def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


'''

         {
           "card_id":
                   {
                     "seq":
                           {
                           "bs1_id":t1,
                           "bs2_id":t2,
                           "bs3_id":t3,
                           "bs4_id":t4
                           }
                    }
          }

'''
p_2a0a_dict = dict()

#p_2a0a_set = dict()
def Prase_2A0A_Test(data,len,port):
    
    global p_2a0a_dict
    index = 0


    #print(binascii.hexlify(data))

    tp = struct.unpack("<HBB",data[index:4])
    index += 4
    
    bs_addr_r = tp[0]
    mode = tp[1]
    num = tp[2]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))
         
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<IBHBHBIb",data[index:16+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 16
        card_addr = tp[0]&0x1ffff
        unix_ts = tp[1] + tp[2]*256

        if (card_addr in p_2a0a_dict.keys()) == False:
            p_2a0a_dict[card_addr] = dict()#序号
        if (unix_ts in p_2a0a_dict[card_addr].keys()) == False:
            p_2a0a_dict[card_addr][unix_ts] = dict()#基站接收时间

        #print(p_2a0a_dict,card_addr,unix_ts,bs_addr_r)
        p_2a0a_dict[card_addr][unix_ts][bs_addr_r] = time.time()
        
def Prase_2A16_Test(data,l,port):
    
    global p_2a0a_dict
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
        tp = struct.unpack("<IBHBHBIbB",data[index:17+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 17
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        if (card_addr in p_2a0a_dict.keys()) == False:
            p_2a0a_dict[card_addr] = dict()#序号
        if (unix_ts in p_2a0a_dict[card_addr].keys()) == False:
            p_2a0a_dict[card_addr][unix_ts] = dict()#基站接收时间

        #print(p_2a0a_dict,card_addr,unix_ts,bs_addr_r)
        p_2a0a_dict[card_addr][unix_ts][bs_addr_r] = time.time()


mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)
mqtt_prase.add_cmd(0x2A16,Prase_2A16_Test)



'''
{
    card_id:{
        "max_seq":xxx;
        "min_seq"xxx;
        "one_bs":xxx;
        "two_bs":xxx;
        "tree_bs":xxx;
        "four_bs":xxx
    }
}

'''
csr_dict = dict()

s_r_s=0
while(True):
    time.sleep(2)
    if p_2a0a_dict :

        
        card_list = list(p_2a0a_dict.keys())
        card_list.sort()
        
        #calculat card sucess_rata 
        for card_addr_r in card_list:#card id
            if (card_addr_r in show["figure_wifi_delay"]["show"].keys()) == False:
                show["figure_wifi_delay"]["show"][card_addr_r] = dict()
                show["figure_wifi_delay"]["show"][card_addr_r]["data"] = list()

            
            card_seq_list = list(p_2a0a_dict[card_addr_r].keys())#序号字典
            card_seq_list.sort()
            
            #print("bs addr:%x(%d)card num:%d "%(bs_addr_r,bs_addr_r,len( p_2a0a_dict[bs_addr_r]["card_num"])))
            for card_sqe_r in card_seq_list:#card seq
                max_t = time.time()
                min_t = min(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                if (max_t - min_t) > MAX_WAIT_DELAY :
                    delay = max(list(p_2a0a_dict[card_addr_r][card_sqe_r].values())) - min(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    show["figure_wifi_delay"]["show"][card_addr_r]["data"].append(delay)
                    del p_2a0a_dict[card_addr_r][card_sqe_r]


                    
                
            

        



        
