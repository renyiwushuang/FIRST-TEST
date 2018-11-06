
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
        sub_list.append(config.mqtt_topic_tx_header + sys.argv[i])
else:
    sub_list.append(config.mqtt_topic_tx_header+"#")
print(config.mqtt_broker_ip,config.mqtt_topic_tx_header)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


mq_tx = Queue()
sub_tx_list = list()
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_tx_list.append("/EH100602/rx/"+sys.argv[i])
else:
    sub_tx_list.append("/EH100602/rx/#")

mqtt_tx = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_tx_list,mq_tx)





def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

mqtt_tx_prase = prase.prase_class_init("mqtt_prase-tx",mq_tx,un_register)
        
'''
{
"bs_id":{
         "rssi":xxx,
         "cnt",xxx
        } 
}
'''
wifi_info = dict()
def Prase_0A80_wifi_rssi(data,l,port):
    global wifi_info
    bs_id,hw,sw,rssi,sub,mac,ap_mac = struct.unpack("<HIIbB3s6s",data)
    if (bs_id in wifi_info.keys()) == False:
        wifi_info[bs_id] = dict()
        wifi_info[bs_id]["cnt"] = 0

    wifi_info[bs_id]["rssi"] = rssi
    wifi_info[bs_id]["ap_mac"] = binascii.hexlify(ap_mac).decode("utf-8")
    wifi_info[bs_id]["cnt"]+=1

def Prase_0A81_wifi_query_cfg_ack(data,l,port):
    #print(data)
    #print(type(data),len(data))
    tp = struct.unpack("<H20s20s20s",data[:62])
    print("配置查询响应：0x%04x  %s %s %s"%(tp[0],tp[1].decode("utf-8"),tp[2].decode("utf-8"),tp[3].decode("utf-8")))
    
def Prase_0B80_wifi_cfg(data,l,port):
    tp = struct.unpack("<H20s20s20s",data[:62])
    print("配置：0x%04x  %s %s %s"%(tp[0],tp[1].decode("utf-8"),tp[2].decode("utf-8"),tp[3].decode("utf-8")))
    
def Prase_0B81_wifi_query(data,l,port):
    print("查询WIFI配置")

def Prase_0B84_wifi_cfg(data,l,port):
    bs_id,phy_mode,ssid,password,d = struct.unpack("<HB20s20sB",data[:44])
    print("WIFI高级配置:基站:%x WIFI模式:%d SSID:%s 密码:%s "%(bs_id,phy_mode,ssid.decode("utf-8"),password.decode("utf-8")))
def Prase_0B85_wifi_cfg(data,l,port):
    print("NQTT高级配置")
def Prase_0B84_wifi_cfg_ack(data,l,port):
    bs_id,phy_mode,ssid,password,d = struct.unpack("<HB20s20sB",data[:44])
    print("WIFI高级配置响应:基站:%x WIFI模式:%d SSID:%s 密码:%s "%(bs_id,phy_mode,ssid.decode("utf-8"),password.decode("utf-8")))
def Prase_0B85_wifi_cfg_ack(data,l,port):
    print("NQTT高级配置响应")  
    
#mqtt_prase.add_cmd(0x0A80,Prase_0A80_wifi_rssi)
mqtt_prase.add_cmd(0x0A81,Prase_0A81_wifi_query_cfg_ack)
mqtt_prase.add_cmd(0x0A83,Prase_0B84_wifi_cfg_ack)

mqtt_tx_prase.add_cmd(0x0B80,Prase_0B80_wifi_cfg)
mqtt_tx_prase.add_cmd(0x0B81,Prase_0B81_wifi_query)
mqtt_tx_prase.add_cmd(0x0B84,Prase_0B84_wifi_cfg)
while(True):
    time.sleep(2)

    #os.system('cls')
    #print(time.time())
    if wifi_info:
        bs_list = list(wifi_info.keys())
        bs_list.sort()
        
        print("\nwifi info:")
        for bs_id in bs_list:
            print("bs_id:%04x rssi:%d ap_mac:%s cnt:%d"%(bs_id,wifi_info[bs_id]["rssi"],wifi_info[bs_id]["ap_mac"].upper()[0:6]+"-"+wifi_info[bs_id]["ap_mac"].upper()[6:12],wifi_info[bs_id]["cnt"]))
        
