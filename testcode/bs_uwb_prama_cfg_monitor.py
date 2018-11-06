
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
#sub_list.append("/EH100602/tx/"+sys.argv[1])
#sub_list.append("/EH100602/tx/#")
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
        sub_list.append("/EH100602/rx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")
    sub_list.append("/EH100602/rx/#")

mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

'''
{
"bs_id":{
         "uwb_sw":x.x.x.x;
         "cnt",xxx
        } 
}
'''
bs_uwb_hb=dict()
def Prase_2A00_uwb_hb(data,len,port):
    global bs_uwb_hb
    tp = struct.unpack("<HIBBBB",data[0:10])
    bs_id = tp[0]
    if (bs_id in bs_uwb_hb.keys()) == False:
        bs_uwb_hb[bs_id] = dict()
        bs_uwb_hb[bs_id]["cnt"] = 0
    bs_uwb_hb[bs_id]["uwb_sw"] = "%d.%d.%d.%d"%(tp[2],tp[3],tp[4],tp[5])
    bs_uwb_hb[bs_id]["cnt"] += 1


def Prase_2A01_uwb_ch_param(data,len,port):
    print("bs_id:%s\t定位信道配置 %f\t "%(port[13:],time.time()))

def Prase_2A02_uwb_ch_parama_ack(data,len,port):
    tp = struct.unpack("<HBBBBBBBHBH",data[0:14])
    bs_id = tp[0]
    print("bs_id:0x%x 定位信道配置响应或定时回传 %f\t "%(bs_id,time.time()))
    

def Prase_2A03_power_param(data,len,port):  
    print("bs_id:%s\t定位功率配置 %f\t "%(port[13:],time.time()))
    
def Prase_2A04_power_param_ack(data,len,port):  
    tp = struct.unpack("<HBBI",data[0:10])
    bs_id = tp[0]
    print("bs_id:0x%x 定位功率配置响应或定时回传 %f\t "%(bs_id,time.time()))
    

def Prase_2A05_lct_param(data,l,port):
    print("bs_id:%s\t定位参数配置 %f\t "%(port[13:],time.time()))
    #print("bs_id:%x\t work_mode:%d\t lct_mode:%d\t syn_t:%d\t rand_t:%d"%(bs_id,tp[1],tp[2],tp[3],tp[4]))
def Prase_2A06_lct_param_ack(data,l,port):
    tp = struct.unpack("<HBBHHI",data[0:])
    bs_id = tp[0]
    print("bs_id:0x%x 定位参数配置响应或定时回传 %f\t "%(bs_id,time.time()))
    #print("bs_id:%x\t work_mode:%d\t lct_mode:%d\t syn_t:%d\t rand_t:%d"%(bs_id,tp[1],tp[2],tp[3],tp[4]))
        
    

mqtt_prase.add_cmd(0x2A00,Prase_2A00_uwb_hb)

mqtt_prase.add_cmd(0x2A01,Prase_2A01_uwb_ch_param)
mqtt_prase.add_cmd(0x2A02,Prase_2A02_uwb_ch_parama_ack)

mqtt_prase.add_cmd(0x2A03,Prase_2A03_power_param)
mqtt_prase.add_cmd(0x2A04,Prase_2A04_power_param_ack)

mqtt_prase.add_cmd(0x2A05,Prase_2A05_lct_param)
mqtt_prase.add_cmd(0x2A06,Prase_2A06_lct_param_ack)



while(True):
    time.sleep(2)



        
