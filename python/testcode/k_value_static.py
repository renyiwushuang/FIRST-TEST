
from queue import Queue
import binascii
import struct
import time
import os
import sys

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
mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)



show = dict()

show["figure_bs_unix_ts"] = dict()
show["figure_bs_uwb_ts"] = dict()

def Prase_2A07_Test(data,len,port):
    
    index = 0
    #print(binascii.hexlify(data))

    tp = struct.unpack("<HBBHBI",data[index:11])

    bs_id = tp[0]
    bs_id_str = "%04x"%bs_id

    bs_unix_ts = tp[2]+tp[3]*256
    bs_uwb_ts = tp[4] + tp[5]*256

    #print(tp[5]&0xff000000)
    #if (bs_id_str in show["figure_bs_unix_ts"].keys()) == False:
        #show["figure_bs_unix_ts"][bs_id_str] = dict()
        #show["figure_bs_unix_ts"][bs_id_str]["xmax"] = 1000
        #show["figure_bs_unix_ts"][bs_id_str]["data"] = list()
        #show["figure_bs_unix_ts"][bs_id_str]["data"].append(bs_unix_ts)
    #else:
         #show["figure_bs_unix_ts"][bs_id_str]["data"].append(bs_unix_ts)
         
    if (bs_id_str in show["figure_bs_uwb_ts"].keys()) == False:
        show["figure_bs_uwb_ts"][bs_id_str] = dict()
        show["figure_bs_uwb_ts"][bs_id_str]["xmax"] = 1000
        show["figure_bs_uwb_ts"][bs_id_str]["data"] = list()
        show["figure_bs_uwb_ts"][bs_id_str]["data"].append(bs_uwb_ts)
    else:
        show["figure_bs_uwb_ts"][bs_id_str]["data"].append(bs_uwb_ts)
        

#show["figure_bs_brd_rcv_unix_ts"] = dict()
#show["figure_bs_brd_rcv_uwb_ts"] = dict()
#基站广播接收
def Prase_2A08_Test(data,len,port):
    global show
    index = 0

    #print(binascii.hexlify(data))

    tp = struct.unpack("<HBB",data[index:4])
    index += 4
    
    bs_addr_r = tp[0]
    mode = tp[1]
    num = tp[2]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))

    rcv_bs_id = "figure_bs_brd_rcv_unix_ts_%04x"%(bs_addr_r)
    if (rcv_bs_id in show.keys()) == False:
        show[rcv_bs_id] = dict()
    for i in range(0,num):
        tp = struct.unpack("<HBHBHBIB",data[index:14+index])
        index += 14
        snd_bs_id = "%04x"%tp[0]
        rcv_uwb_ts = tp[5] + tp[6]*256
        if (snd_bs_id in show[rcv_bs_id].keys()) == False:
            show[rcv_bs_id][snd_bs_id] = dict()
            show[rcv_bs_id][snd_bs_id]["xmax"] = 1000
            show[rcv_bs_id][snd_bs_id]["data"] = list()
            show[rcv_bs_id][snd_bs_id]["data"].append(rcv_uwb_ts)
        else:
            show[rcv_bs_id][snd_bs_id]["data"].append(rcv_uwb_ts)
  
#mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)

mqtt_prase.add_cmd(0x2A07,Prase_2A07_Test)
mqtt_prase.add_cmd(0x2A08,Prase_2A08_Test)

time.sleep(3)
show_instance = Figures.FiguresInit("show",show)
while(True):
    #input_context = input("input :s(suspend figure),r(resume figure)")
    #if(input_context == "s"):
        #show_instance.suspend()
    #elif (input_context == "r"):
        #show_instance.resume()
    time.sleep(2)


        
        




        
