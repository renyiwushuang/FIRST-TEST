 
from queue import Queue
import binascii
import struct
import time
import os
import sys

import config

from components.MQTT import MqttThread
from components.PacketPrase import prase



tag_filter_list = []


mq = Queue()
sub_list = list()
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        tag_filter_list.append(int(sys.argv[i]))
sub_list.append("/EH100602/tx/#")
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)



'''
{
    bs_id:{
          bs:{
                       "max":xxx
                       "min":xxx
                       "cnt":xxx
             }
         card:{
               card_id:{
                       "max":xxx
                       "min":xxx
                       "cnt":xxx
                     }
         }
                      
    }
}
'''
tof_sr = dict()#Success rate

def Prase_2A0D_tof_data_back(data,l,port):
    global tof_sr
    #print(binascii.hexlify(data[0:17]))
    index = 0
    #bs_id(2B) + bs_seq(3B) + data_rx_ts(5B) + card_id(4B) + card_seq(3B) + poll_tx(5B) + data_tx(5B) + bs_num(1B)
    bs_id,brs_l,brs_h,dr_ts_l,dr_ts_h,card_id,cts_l,cts_h,pt_ts_l,pt_ts_h,dt_ts_l,dt_ts_h,cnt = struct.unpack("<HHBIBIHBIBIBB",data[index:28])

    bs_rx_seq = brs_l + brs_h*256
    card_tx_seq = cts_l + cts_h*256

    #print(bs_rx_seq,card_tx_seq)
    #bs 
    if (bs_id in tof_sr.keys()) == False:
        tof_sr[bs_id] = dict()
        tof_sr[bs_id]["bs"] = dict()
        tof_sr[bs_id]["card"] = dict()
        tof_sr[bs_id]["bs"]["max"] = 0x00
        tof_sr[bs_id]["bs"]["min"] = 0xffffffff
        tof_sr[bs_id]["bs"]["cnt"] = 0
        
    tof_sr[bs_id]["bs"]["cnt"] += 1
    tof_sr[bs_id]["bs"]["max"] = max( tof_sr[bs_id]["bs"]["max"],bs_rx_seq)
    tof_sr[bs_id]["bs"]["min"] = min( tof_sr[bs_id]["bs"]["min"],bs_rx_seq)

    #card
    if (card_id in tof_sr[bs_id]["card"].keys()) == False:
        tof_sr[bs_id]["card"][card_id] = dict()
        tof_sr[bs_id]["card"][card_id]["max"] = 0x00
        tof_sr[bs_id]["card"][card_id]["min"] = 0xffffffff
        tof_sr[bs_id]["card"][card_id]["cnt"] = 0
    tof_sr[bs_id]["card"][card_id]["cnt"] += 1
    tof_sr[bs_id]["card"][card_id]["max"] = max( tof_sr[bs_id]["card"][card_id]["max"],card_tx_seq)
    tof_sr[bs_id]["card"][card_id]["min"] = min( tof_sr[bs_id]["card"][card_id]["min"],card_tx_seq)    
    '''
    index = 28
    for i in range(0,cnt):
        card_bs_id,cr_ts_l,cr_ts_h,k_l,k_h=struct.unpack("<HHBIBIHBIBIBB",data[index:index+10])#bs_id(2B) + conf_ts(5B) + k (3B)
        index += 10
        '''
tof_static = {}
def Prase_2A17_tof_data_back(data,l,port):
    global tof_static,tag_filter_list
    #print(binascii.hexlify(data))
    index = 0

    #header
    try:
        bs_id,brs_l,brs_h,dr_ts_l,dr_ts_h,card_id,cmd_ver = struct.unpack("<HHBIBIB",data[index:index+15])
        index += 15
    except Exception as err:  
        print(err,hex(l))
        os.system("pause")

    cts_l,cts_h,pt_ts_l,pt_ts_h,bs_num = struct.unpack("<HBIBB",data[index:index+9])
    index += 9

    card_tx_seq = cts_l + cts_h*256

    if tag_filter_list:
        if (card_id in tag_filter_list) == False:
            return
    if (card_id in tof_static.keys()) == False:
        tof_static[card_id] = dict()
    #plod
    if cmd_ver == 0:#pload 00
        for i in range(bs_num):
            tof_bs_id,conf_ts,k = struct.unpack("<H5s3s",data[index:index+10])
            index += 10

            if (tof_bs_id in tof_static[card_id].keys()) == False:
                tof_static[card_id][tof_bs_id] = set()
            
            tof_static[card_id][tof_bs_id].add(card_tx_seq)
            
    elif cmd_ver == 1:#pload 01
        for i in range(bs_num):
            tof_bs_id,conf_ts,k,cl = struct.unpack("<H5s3sB",data[index:index+11])
            index += 11

            if (tof_bs_id in tof_static[card_id].keys()) == False:
                tof_static[card_id][tof_bs_id] = set()
            tof_static[card_id][tof_bs_id].add(card_tx_seq)

            if card_id == 0:
                print(hex(tof_bs_id),binascii.hexlify(data[24:]))
    else:
        print("cmd_ver:%d",cmd_ver)
        return
    
    
#mqtt_prase.add_cmd(0x2A0D,Prase_2A0D_tof_data_back)
mqtt_prase.add_cmd(0x2A17,Prase_2A17_tof_data_back)

    
while(True):
    time.sleep(2)
    if tof_static:
        tag_list = list(tof_static.keys())
        tag_list.sort()
        os.system('cls')
        print(sub_list)
        for tag_id in tag_list:
            bs_list = list(tof_static[tag_id].keys())
            bs_list.sort()
            bs_sc_info = ""
            for bs_id in bs_list:
                cnt = len(tof_static[tag_id][bs_id])
                cnt_max = (max(tof_static[tag_id][bs_id]) - min(tof_static[tag_id][bs_id])+1)
                bs_sc_info += "bs_id:%x \t成功率:%0.2f \t计数:%u\n\t\t "%(bs_id,100.0*cnt/cnt_max,cnt_max)
            print("tag_id:%d \t%s"%(tag_id,bs_sc_info))




            
           
