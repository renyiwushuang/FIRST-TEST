
from queue import Queue
import binascii
import struct
import time
import os
import sys
import numpy as np
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
    sub_list.append("/EH100602/tx/a00a")
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


show = dict()

show["dw1000s"] = dict()
show["dw1000s"]["xmax"] = 1000
show["dw1000s"]["show"] = dict()
show["dw1000s"]["ylabel"] = "cnt"
show["dw1000s"]["show"]["dw1000_cnt"] = dict()
show["dw1000s"]["show"]["dw1000_cnt"]["data"] = list()

show["dw1000s-dist"] = dict()
show["dw1000s-dist"]["xmax"] = 1000
show["dw1000s-dist"]["show"] = dict()
show["dw1000s-dist"]["show"]["distance"] = dict()
show["dw1000s-dist"]["show"]["distance"]["data"] = list()

show["dw1000s-cnt"] = dict()
show["dw1000s-cnt"]["xmax"] = 1000
show["dw1000s-cnt"]["show"] = dict()
show["dw1000s-cnt"]["show"]["counter"] = dict()
show["dw1000s-cnt"]["show"]["counter"]["data"] = list()


time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)



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
    global p_2a07_dict
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
        unix_ts_rx = tp[3] + tp[4]*256
        unix_ts_tx = tp[1] + tp[2]*256
        bs_uwb_ts  = tp[5] + tp[6]*256

        #print(tp)
        #print(card_addr,tp[-1],unix_ts_rx,unix_ts_tx)
        
        if card_addr in p_2a07_dict.keys():
            #print(p_2a07_dict)
            p_2a07_dict[card_addr][unix_ts_tx]['rx_seq'] = unix_ts_rx
            p_2a07_dict[card_addr][unix_ts_tx]['uwb_rx'] = bs_uwb_ts

p_2a07_dict = dict()
def Prase_2A07_Test(data,len,port):
    global p_2a07_dict
    #print(binascii.hexlify(data))
    index = 0
    tp = struct.unpack("<HBBHBI",data[index:11])

    bs_id = tp[0]
    #bs_id_str = "%04x"%bs_id
    bs_unix_ts = tp[2]+tp[3]*256
    bs_uwb_ts = tp[4] + tp[5]*256

    #print(bs_id,bs_unix_ts,bs_uwb_ts)
    
    if (bs_id in p_2a07_dict.keys()) == False:
        p_2a07_dict[bs_id] = dict()
        
    p_2a07_dict[bs_id][bs_unix_ts] = dict()
    p_2a07_dict[bs_id][bs_unix_ts]['uwb_tx'] = bs_uwb_ts

p_2a16_dict = dict()

def Prase_2A16_Test(data,l,port):
    
    global p_2a16_dict
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
        tp = struct.unpack("<IBHBHBIbB",data[index:17+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 17
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        uwb_ts = tp[5] + tp[6]*256
        if card_addr != 3082:
            continue

        print("tag:%d seq:%d cl:%d uwb_ts:%s %x"%(card_addr,unix_ts,tp[8],str(uwb_ts*1.0/499.2e6/128),uwb_ts))

        if (unix_ts in p_2a16_dict.keys()) == False:
            p_2a16_dict[unix_ts] = dict()
            p_2a16_dict[unix_ts][tp[8]] = uwb_ts
        else:
            p_2a16_dict[unix_ts][tp[8]] = uwb_ts
        

#解包线程类
class input_class(threading.Thread):
    def __init__(self,t_name,d):
        threading.Thread.__init__(self, name=t_name)
        self.d = d
    def run(self):
        global p_2a16_dict,of_cnt
        while(True):
            print('input_class')
            time.sleep(5)
            str = input('input any key to pause!')
            #print("input:",str)
            _of_cnt = of_cnt
            while(True):
                 time.sleep(2)
                 if p_2a16_dict :
                    seq_list = list(p_2a16_dict.keys())
                    seq_list.sort()

                    
                    for seq_r in seq_list:
                        #print()
                        if len(p_2a16_dict[seq_r].keys()) == 2:
                            show["dw1000s-cnt"]["show"]["counter"]["data"].append(p_2a16_dict[seq_r][1] - p_2a16_dict[seq_r][3] - _of_cnt)
                            dist = (p_2a16_dict[seq_r][1] - p_2a16_dict[seq_r][3]-_of_cnt)/499.2e6/128.0*299702547
                            #print("ts:%s \t distance:%f"%(str((p_2a16_dict[seq_r][1] - p_2a16_dict[seq_r][3])/499.2e6/128.0),dist))
                            show["dw1000s-dist"]["show"]["distance"]["data"].append(dist)
                            #print(p_2a16_dict[seq_r])
                            del p_2a16_dict[seq_r]
                 

time.sleep(1)
input_instance = input_class("input",p_2a0a_dict)
input_instance.start()
time.sleep(1)

        


#mqtt_prase.add_cmd(0x2A08,Prase_2A08_Test)
mqtt_prase.add_cmd(0x2A15,Prase_2A15_Test)
mqtt_prase.add_cmd(0x2A07,Prase_2A07_Test)
mqtt_prase.add_cmd(0x2A16,Prase_2A16_Test)

_of_list = show["dw1000s"]["show"]["dw1000_cnt"]["data"]
of_list = list()

of_cnt = 0
time.sleep(3)
print('start')
while(True):
    time.sleep(2)
    #print(p_2a0a_dict)
    
    if 1 not in p_2a07_dict.keys():
        continue
    if 3 not in p_2a07_dict.keys():
        continue
    
    t1_list = list(p_2a07_dict[1].keys())
    t3_list = list(p_2a07_dict[3].keys())

    t1_list.sort()
    t3_list.sort()

    for t1_seq in t1_list:
        
        t1 = p_2a07_dict[1][t1_seq]['uwb_tx']
        if 'uwb_rx' not in p_2a07_dict[1][t1_seq].keys():
            continue
        r2 = p_2a07_dict[1][t1_seq]['uwb_rx']

        #print(t1_seq)
        for t3_seq in t3_list:
            #print(t1_seq)
            if p_2a07_dict[1][t1_seq]['rx_seq'] < t3_seq:
                t2 = p_2a07_dict[3][t3_seq]['uwb_tx']
                if 'uwb_rx' not in p_2a07_dict[3][t3_seq].keys():
                    break
                r1 = p_2a07_dict[3][t3_seq]['uwb_rx']

                t = (t1+r1-t2-r2)/2
                of_list.append(t)
                _of_list.append(np.std(of_list))
                of_cnt = np.mean(of_list)
                #show["dw1000s"]["show"]["dw1000_cnt"]["data"] = np.std(of_list)
                tof = (r1-t1-(t2-r2))/2*1.0/499.2e6/128*299702547
                
                print(t1,r2,t2,r1,t,t*1.0/499.2e6/128,tof,np.std(of_list))
                #print()
                del p_2a07_dict[1][t1_seq]
                del p_2a07_dict[3][t3_seq]
                break
            
        #break
    
        
    #print(t1_list)
    #print(p_2a07_dict)
              
