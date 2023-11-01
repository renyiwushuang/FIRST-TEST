
from queue import Queue
import binascii
import struct
import time
import os
import sys

from components.MQTT import MqttThread
from components.PacketPrase import prase

mq = Queue()
sub_list = list()
#sub_list.append("/EH100602/tx/"+"fefc")
sub_list.append("/EH100602/tx/"+sys.argv[1])
#sub_list.append("/EH100602/rx/#")
mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)



p_2a0a_dict = dict()#{"id":{"max":xxx,"min":xxx,"cnt":xxx}}
p_2a0a_set=set()
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

    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        tp = struct.unpack("<HBHBHBIB",data[index:14+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 14
        card_addr = tp[0]
        unix_ts = tp[3] + tp[4]*256

        if (card_addr in p_2a0a_dict.keys()) == False:
            p_2a0a_dict[card_addr] = dict()
            p_2a0a_dict[card_addr]["max"] = 0x00000000
            p_2a0a_dict[card_addr]["min"] = 0xffffffff
            p_2a0a_dict[card_addr]["cnt"] = 0x00000000

            p_2a0a_dict[card_addr]["max"] = max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[card_addr]["min"] = min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[card_addr]["cnt"] = p_2a0a_dict[card_addr]["cnt"]+1

            #p_2a0a_dict[card_addr]["list"] = list()
        else:
            p_2a0a_dict[card_addr]["max"] = max(p_2a0a_dict[card_addr]["max"],unix_ts)
            p_2a0a_dict[card_addr]["min"] = min(p_2a0a_dict[card_addr]["min"],unix_ts)
            p_2a0a_dict[card_addr]["cnt"] = p_2a0a_dict[card_addr]["cnt"]+1

           # p_2a0a_dict[card_addr]["list"].append(unix_ts)
        #print(car_addr)
        p_2a0a_set.add(card_addr)

        if 2474 ==  card_addr:
            #print(binascii.hexlify(data))
            pass
        


mqtt_prase.add_cmd(0x2A08,Prase_2A08_Test)

while(True):
    time.sleep(2)
    if p_2a0a_set :
       

        card_list = list(p_2a0a_dict.keys())
        card_list.sort()

        os.system('cls')
        print("card num:%d "%(len(p_2a0a_set)))
        #print(p_2a0a_dict)
        for card_addr in card_list:
            print("%05d(%04x)   cnt:%05d   %0.1f %%"%(card_addr,card_addr,p_2a0a_dict[card_addr]["cnt"],p_2a0a_dict[card_addr]["cnt"]/(p_2a0a_dict[card_addr]["max"]-p_2a0a_dict[card_addr]["min"]+1)*100))
            #print(card_addr,p_2a0a_dict[card_addr]["list"])

            #if 2328 ==  card_addr:
                #print(card_addr,p_2a0a_dict[card_addr]["list"])
        
        




        
