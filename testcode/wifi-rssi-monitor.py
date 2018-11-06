
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
else:
    sub_list.append("/EH100602/tx/#")

mqtt = MqttThread.mqtt_thread_init("192.168.4.44",sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)
        
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


mqtt_prase.add_cmd(0x0A80,Prase_0A80_wifi_rssi)


while(True):
    time.sleep(2)

    os.system('cls')
    print(time.time())
    if wifi_info:
        bs_list = list(wifi_info.keys())
        bs_list.sort()
        
        print("\nwifi info:")
        for bs_id in bs_list:
            print("bs_id:%04x rssi:%d ap_mac:%s cnt:%d"%(bs_id,wifi_info[bs_id]["rssi"],wifi_info[bs_id]["ap_mac"].upper()[0:6]+"-"+wifi_info[bs_id]["ap_mac"].upper()[6:12],wifi_info[bs_id]["cnt"]))
        
