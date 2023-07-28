
from queue import Queue
import binascii
import struct
import time
import os
import sys

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
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)



p_2a0a_dict = dict()#{"id":{"max":xxx,"min":xxx,"cnt":xxx}}
p_2a0a_set=set()
#基站接收基站广播
def Prase_2A08_Test(data,len,port):
    
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
    #print(num)
    if (bs_addr_r in p_2a0a_dict.keys()) == False:
         p_2a0a_dict[bs_addr_r] = dict()
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<HBHBHBIbH",data[index:16+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 16
        card_addr = tp[0]
        unix_ts = tp[3] + tp[4]*256

        if (card_addr in p_2a0a_dict[bs_addr_r].keys()) == False:
            p_2a0a_dict[bs_addr_r][card_addr] = dict()
            p_2a0a_dict[bs_addr_r][card_addr]["max"] = 0x00000000
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = 0xffffffff
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = 0x00000000

            p_2a0a_dict[bs_addr_r][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r][card_addr]["max"],time.time())#max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r][card_addr]["min"],time.time())#min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r][card_addr]["cnt"]+1

        else:
            p_2a0a_dict[bs_addr_r][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r][card_addr]["max"],time.time())#max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r][card_addr]["min"],time.time())#min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r][card_addr]["cnt"]+1
        p_2a0a_dict[bs_addr_r][card_addr]["rssi"] = tp[7]
           # p_2a0a_dict[card_addr]["list"].append(unix_ts)
        #print(hex(card_addr))
    #p_2a0a_set.add(bs_addr_r)

#基站接收基站广播
def Prase_2A15_Test(data,l,port):
    
    global p_2a0a_dict
    global p_2a0a_set
    index = 0


    #print(binascii.hexlify(data))

    tp = struct.unpack("<BHHBB",data[index:7])
    index += 7
    
    bs_addr_r = tp[1]
    mode = tp[3]
    num = tp[4]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))
    #print(num)
    if (bs_addr_r in p_2a0a_dict.keys()) == False:
         p_2a0a_dict[bs_addr_r] = dict()
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<HBHBHBIbHB",data[index:17+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 17
        card_addr = tp[0]
        unix_ts = tp[3] + tp[4]*256

        if(bs_addr_r == 0x2cb0):
            print(unix_ts,tp[1]+tp[2]*256)
        
        if (card_addr in p_2a0a_dict[bs_addr_r].keys()) == False:
            p_2a0a_dict[bs_addr_r][card_addr] = dict()
            p_2a0a_dict[bs_addr_r][card_addr]["max"] = 0x00000000
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = 0xffffffff
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = 0x00000000

            p_2a0a_dict[bs_addr_r][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r][card_addr]["max"],time.time())#max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r][card_addr]["min"],time.time())#min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r][card_addr]["cnt"]+1

        else:
            p_2a0a_dict[bs_addr_r][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r][card_addr]["max"],time.time())#max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r][card_addr]["min"],time.time())#min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r][card_addr]["cnt"]+1
        p_2a0a_dict[bs_addr_r][card_addr]["rssi"] = tp[7]

p_2a07_dict = dict()
def Prase_2A07_Test(data,len,port):
    global p_2a07_dict
    #print(binascii.hexlify(data))
    index = 0
    tp = struct.unpack("<HBBHBI",data[index:11])

    bs_id = tp[0]
    #bs_id_str = "%04x"%bs_id
    #bs_unix_ts = tp[2]+tp[3]*256
    #bs_uwb_ts = tp[4] + tp[5]*256

    if (bs_id in p_2a07_dict.keys()) == False:
        p_2a07_dict[bs_id] = dict()
        p_2a07_dict[bs_id]["max"] = 0x00000000
        p_2a07_dict[bs_id]["min"] = 0xffffffff
        p_2a07_dict[bs_id]["cnt"] = 0x00000000

    p_2a07_dict[bs_id]["max"] = max(p_2a07_dict[bs_id]["max"],time.time())
    p_2a07_dict[bs_id]["min"] = min(p_2a07_dict[bs_id]["min"],time.time())
    p_2a07_dict[bs_id]["cnt"] += 1

mqtt_prase.add_cmd(0x2A08,Prase_2A08_Test)
mqtt_prase.add_cmd(0x2A15,Prase_2A15_Test)
mqtt_prase.add_cmd(0x2A07,Prase_2A07_Test)

while(True):
    time.sleep(200)

    if p_2a0a_dict:
        bs_rx_list = list(p_2a0a_dict.keys())
        bs_rx_list.sort()
        os.system('cls')
        print("bs_rx_sucess_static_by_time:")
        for bs_addr_r in bs_rx_list:
            print("%d(0x%x):"%(bs_addr_r,bs_addr_r))
            bs_tx_list = list(p_2a0a_dict[bs_addr_r].keys())
            bs_tx_list.sort()
            for bs_addr_t in bs_tx_list:
                print("\t%05d(0x%04x)   计数:%05d   成功率:%0.1f %% RSSI:%d"%(bs_addr_t,bs_addr_t,p_2a0a_dict[bs_addr_r][bs_addr_t]["cnt"],
                                                              p_2a0a_dict[bs_addr_r][bs_addr_t]["cnt"]/(p_2a0a_dict[bs_addr_r][bs_addr_t]["max"]-p_2a0a_dict[bs_addr_r][bs_addr_t]["min"]+1)*10,
                                                              p_2a0a_dict[bs_addr_r][bs_addr_t]["rssi"]))
        
    if p_2a07_dict:
        bs_tx_list = list(p_2a07_dict.keys())
        bs_tx_list.sort()
        print("\nbs_tx_sucess_static_by_time:")
        for bs_addr_t_ in bs_tx_list:
            print("\t%05d(0x%04x)   cnt:%05d   %0.1f %% "%(bs_addr_t_,bs_addr_t_,p_2a07_dict[bs_addr_t_]["cnt"],\
                                                              p_2a07_dict[bs_addr_t_]["cnt"]/(p_2a07_dict[bs_addr_t_]["max"]-p_2a07_dict[bs_addr_t_]["min"])*10))            
