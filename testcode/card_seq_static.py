
from queue import Queue
import binascii
import struct
import time
import os
import sys

import threading

from components.MQTT import MqttThread
from components.PacketPrase import prase

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/0079")
#sub_list.append("/EH100602/rx/#")
mqtt = MqttThread.mqtt_thread_init("192.168.0.139",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


'''
#{"card_id":
         {
         
               "seq":
                       {
                               {
                               "max":xxx,
                               "min":xxx,
                               }
                        }
          }
 }
'''
p_2a0a_dict = dict()

#p_2a0a_set = dict()
last_sqe = 0;
last_time = 0;
def Prase_2A0A_Test(data,len,port):
    
    global p_2a0a_dict
    global p_2a0a_set
    global last_seq,last_time
    index = 0


    #print(binascii.hexlify(data))

    tp = struct.unpack("<HBB",data[index:4])
    index += 4
    
    bs_addr_r = tp[0]
    mode = tp[1]
    num = tp[2]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))
    '''if (bs_addr_r in p_2a0a_dict.keys()) == False:
         p_2a0a_dict[bs_addr_r] = dict()
         p_2a0a_dict[bs_addr_r]["card"] = dict()
         p_2a0a_dict[bs_addr_r]["card_num"] = set()'''
         
    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<IBHBHBIb",data[index:16+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 16
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        '''
        if (card_addr in p_2a0a_dict[bs_addr_r]["card"].keys()) == False:
            p_2a0a_dict[bs_addr_r]["card"][card_addr] = dict()
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = 0x00000000
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = 0xffffffff
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = 0x00000000

            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]+1
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"] = tp[7]

        else:
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"] = max(p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"] = min(p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"],unix_ts)
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"] = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]+1
            p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"] = tp[7]
        p_2a0a_dict[bs_addr_r]["card_num"].add(card_addr)
        '''

        '''
        if 279==card_addr:
            print("bs:%x t:%0.3f s:%d"%(bs_addr_r,time.time(),unix_ts))
            #print(unix_ts)
        '''
        if 279 == card_addr:
            if (last_time == 0) == True:
                last_time = time.time()
                last_seq = unix_ts
            else:
                new_time = time.time()

                dt = new_time-last_time
                ds = unix_ts-last_seq
                dt_ds = (dt)/(ds)
                
                if dt_ds > 0.750:
                    print("seq:%5d \tt:%0.3f \tdt/ds:%0.3f**********************************"%(unix_ts,new_time,dt_ds))
                else:
                    print("seq:%5d \tt:%0.3f \tdt/ds:%0.3f"%(unix_ts,new_time,dt_ds))
                last_seq = unix_ts
                last_time = new_time

mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)


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
        
while(True):
    time.sleep(2)
    if False:#p_2a0a_dict :

        bs_list = list(p_2a0a_dict.keys())
        bs_list.sort()

        
        os.system('cls')
        for bs_addr_r in bs_list:
            card_list = list(p_2a0a_dict[bs_addr_r]["card"].keys())
            card_list.sort()
           
            print("bs addr:%x(%d)card num:%d "%(bs_addr_r,bs_addr_r,len( p_2a0a_dict[bs_addr_r]["card_num"])))
            for card_addr in card_list:
                max_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["max"]
                min_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["min"]
                cnt_v  = p_2a0a_dict[bs_addr_r]["card"][card_addr]["cnt"]
                rssi_v = p_2a0a_dict[bs_addr_r]["card"][card_addr]["rssi"]
                print("\t%05d(%04x)   cnt:%05d   %0.1f %%  rssi:%d"%(card_addr,card_addr,cnt_v, cnt_v/(max_v-min_v+1)*100,rssi_v))

        
        




        
