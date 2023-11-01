
from queue import Queue
import binascii
import struct
import time
import os
import sys

from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.FileSave import FileSave
from components.Figures import Figures

mq = Queue()
sub_list = list()
#sub_list.append("/EH100602/tx/"+"fefc")
#sub_list.append("/EH100602/tx/"+sys.argv[1])
#sub_list.append("/EH100602/rx/#")
sub_list.append("/EH100602/tx/ff03")
sub_list.append("/EH100602/tx/ff05")
sub_list.append("/EH100602/tx/ff06")
mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

mqFileSave = Queue()
file_name = "prb_cnt" + ".txt"
FileSave.File_Save_Init("file_save",os.getcwd()+"\\","prb_cnt.txt",mqFileSave)


show = dict()
show["prb_cnt_figure"] = dict()
show["prb_cnt_figure"]["xmax"] = 500
show["prb_cnt_figure"]["show"] = dict()

#show = dict()
show["rssi"] = dict()
show["rssi"]["xmax"] = 500
show["rssi"]["show"] = dict()

'''
rcv_bs_id :
         {
            show:
         }
'''
def Prase_2A08_Test(data,l,port):
    
    global show
    index = 0

    #print(binascii.hexlify(data),len(data),l)

    tp = struct.unpack("<HBB",data[index:4])
    index += 4
    
    bs_addr_r = tp[0]
    mode = tp[1]
    num = tp[2]
    #print("bs_addr:%x mode:%d num:%d"%(bs_addr,mode,num))

    for i in range(0,num):
        #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
        #print(binascii.hexlify(data[index:16+index]),len(data[index:16+index]))
        tp = struct.unpack("<HBHBHBIbH",data[index:16+index])
        index += 16
        send_bs_addr = tp[0]
        send_unix_ts = tp[1] + tp[2]*256
        rcv_unix_ts = tp[3] + tp[4]*256
        rssi = tp[7]
        prb_cnt = tp[8]

        bs_addr_r_str = "%04x(%d)"%(bs_addr_r,bs_addr_r)
        if (bs_addr_r_str in show["prb_cnt_figure"]["show"]) == False:
            show["prb_cnt_figure"]["show"][bs_addr_r_str] = dict()
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"] = list()
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"].append(prb_cnt)
        else:
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"].append(prb_cnt)

        bs_addr_r_str += "rssi"  
        if (bs_addr_r_str in show["prb_cnt_figure"]["show"]) == False:
            show["prb_cnt_figure"]["show"][bs_addr_r_str] = dict()
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"] = list()
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"].append(rssi*2+300)
        else:
            show["prb_cnt_figure"]["show"][bs_addr_r_str]["data"].append(rssi*2+300)
        #print("sned:%d\trcv:%d\tprb_cnt:%d"(bs_addr_r,send_bs_addr,prb_cnt))
        data_str = "%x\t%x\t%d\t%d\t%d\t%d\n"%(send_bs_addr,bs_addr_r,send_unix_ts,rcv_unix_ts,rssi,prb_cnt)
        print(data_str)
        mqFileSave.put(data_str.encode("utf-8"))


        


mqtt_prase.add_cmd(0x2A08,Prase_2A08_Test)

time.sleep(2)
show_instance = Figures.FiguresInit("show",show)
while(True):
    time.sleep(2)
        
        




        
