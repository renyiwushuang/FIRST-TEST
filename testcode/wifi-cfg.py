
from queue import Queue
import binascii
import struct
import time
import os
import sys
import threading

import config

from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.PacketPrase import packet

mq = Queue()
sub_list = list()
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append(config.mqtt_topic_tx_header + sys.argv[i])
else:
    sub_list.append(config.mqtt_topic_tx_header+"#")
print(config.mqtt_broker_ip,config.mqtt_topic_tx_header)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

        
phy_mode_prase = dict()
phy_mode_prase[1] = "11B"
phy_mode_prase[2] = "11G"
phy_mode_prase[3] = "11N"
def Prase_0A80_wifi_hb(data,l,port):
    global phy_mode_prase
    if(l>21):
        bs_id,hw,sw,rssi,sub,mac,ap_mac,phy_mode,mode,seq = struct.unpack("<HIIbB3s6sBBH",data)
        '''if (bs_id in wifi_info.keys()) == False:
            wifi_info[bs_id] = dict()
            wifi_info[bs_id]["cnt"] = 0

        wifi_info[bs_id]["rssi"] = rssi
        wifi_info[bs_id]["ap_mac"] = binascii.hexlify(ap_mac).decode("utf-8")
        wifi_info[bs_id]["info"]
        wifi_info[bs_id]["cnt"]+=1
        '''
        print("id:%04x  rssi:%d  phy_mode:%s  seq:%d"%(bs_id,rssi,phy_mode_prase[phy_mode],seq))
    else:
        bs_id,hw,sw,rssi,sub,mac,ap_mac = struct.unpack("<HIIbB3s6s",data)
        print("id:%04x  rssi:%d "%(bs_id,rssi))

def Prase_0A81_wifi_query_cfg_ack(data,l,port):
    #print(data)
    #print(type(data),len(data))
    tp = struct.unpack("<H20s20s20s",data[:62])
    print("配置查询响应：0x%04x  %s %s %s"%(tp[0],tp[1].decode("utf-8"),tp[2].decode("utf-8"),tp[3].decode("utf-8")))

def Prase_0A83_wifi_connect_cfg_ack(data,l,port):
    global phy_mode_prase
    #print(binascii.hexlify(data),len(data),data)
    tp = struct.unpack("<HB20s20s",data[:43])
    print("WIFI无线配置响应：0x%04x  phy_mode:%s ssid:%s password:%s"%(tp[0],phy_mode_prase[tp[1]],tp[2].decode("utf-8"),tp[3].decode("utf-8")))

def Prase_0A84_wifi_mqtt_cfg_ack(data,l,port):
    tp = struct.unpack("<H20s40sH20s20s",data[:104])
    #print(tp[1],binascii.hexlify(tp[2]),len(tp[2]))
    print("WIFI MQTT配置响应：0x%04x  TopicHeader:%s brokerIP:%s(%d) MQTTuserName:%s MQTTpassword:%s"%(tp[0],tp[1].decode("utf-8"),
                                                                                                  tp[2].decode("utf-8"),tp[3],tp[4].decode("utf-8"),tp[5].decode("utf-8")))

mqtt_prase.add_cmd(0x0A80,Prase_0A80_wifi_hb)
mqtt_prase.add_cmd(0x0A81,Prase_0A81_wifi_query_cfg_ack)
mqtt_prase.add_cmd(0x0A83,Prase_0A83_wifi_connect_cfg_ack)
mqtt_prase.add_cmd(0x0A84,Prase_0A84_wifi_mqtt_cfg_ack)


def wifi_reset(bs_id):
    global mqtt
    reset_data = struct.pack("<HH",bs_id,0x0000)
    reset_packet = packet.get_packet(0x0B83, reset_data, len(reset_data))

    bs_rx_topic = config.mqtt_topic_rx_header
    if bs_id == 0xffff:
        bs_rx_topic +=  "brd"
    else:
        bs_rx_topic += "%04x"%(bs_id)
    mqtt.mqtt_pub(bs_rx_topic,reset_packet)
    print(bs_rx_topic,binascii.hexlify(reset_packet))
    print("重启wifi：%x"%(bs_id))

def wifi_con_cfg(bs_id,phy_mode,ssid,password):
    global mqtt,phy_mode_prase
    con_data = struct.pack("<HB20s20sB",bs_id,phy_mode,ssid.encode("utf-8"),password.encode("utf-8"),1)
    con_packet = packet.get_packet(0x0B84, con_data, len(con_data))

    bs_rx_topic = config.mqtt_topic_rx_header
    if bs_id == 0xffff:
        bs_rx_topic +=  "brd"
    else:
        bs_rx_topic += "%04x"%(bs_id)
    mqtt.mqtt_pub(bs_rx_topic,con_packet)
    #print(bs_rx_topic,binascii.hexlify(con_packet),'\n',con_packet)
    print("配置WIFI无线 %04x 无线模式:%s 配置SSID:%s Password：%s"%(bs_id,phy_mode_prase[phy_mode],ssid,password))

def wifi_mqtt_cfg(bs_id,ip,port,username,password):
    global mqtt
    mqtt_data = struct.pack("<H20s40sH20s20sB",bs_id,"/EH100602/".encode("utf-8"),ip.encode("utf-8"),port,username.encode("utf-8"),password.encode("utf-8"),1)
    mqtt_packet = packet.get_packet(0x0B85, mqtt_data, len(mqtt_data))

    bs_rx_topic = config.mqtt_topic_rx_header
    if bs_id == 0xffff:
        bs_rx_topic +=  "brd"
    else:
        bs_rx_topic += "%04x"%(bs_id)
    mqtt.mqtt_pub(bs_rx_topic,mqtt_packet)
    #print(bs_rx_topic,binascii.hexlify(mqtt_packet),'\n',mqtt_packet)
    print("配置WIFI-MQTT %04x ip:%s(%d) 用户名:%s 密码:%s"%(bs_id,ip,port,username,password))

def wifi_ack_rqst(bs_id,cmd):
    global mqtt
    mqtt_data = struct.pack("<HHB",bs_id,cmd,1)
    mqtt_packet = packet.get_packet(0x0B82, mqtt_data, len(mqtt_data))
    
    bs_rx_topic = config.mqtt_topic_rx_header
    if bs_id == 0xffff:
        bs_rx_topic +=  "brd"
    else:
        bs_rx_topic += "%04x"%(bs_id)
    mqtt.mqtt_pub(bs_rx_topic,mqtt_packet)
    #print(bs_rx_topic,binascii.hexlify(mqtt_packet),'\n',mqtt_packet)
    print("查询基站:%04x 配置:%04x"%(bs_id,cmd))
    
'''
#解包线程类
class input_class(threading.Thread):
    def __init__(self,t_name,):
        threading.Thread.__init__(self, name=t_name)
    def run(self):
        while(True):
            str = input()
            print("input:",str)
            if("r" == str):
                wifi_reset(0x5069)
            
time.sleep(2)
input_instance = input_class("input")
input_instance.start()
'''
time.sleep(2)

bs_id = 0x2135
while(True):
    #time.sleep(2)
    str = input()
    print("input:",str)
    if("rst" == str):
        wifi_reset(bs_id)
    elif("cc" == str):
        wifi_con_cfg(bs_id,3,"HGK","HGKJ2014")
    elif("mc" == str):
        wifi_mqtt_cfg(bs_id,"192.168.0.65",1884,"admin","Abc123")#ehigh2014.oicp.net
    elif("rq" == str):
        wifi_ack_rqst(bs_id,0x0b84)
        time.sleep(0.5)
        wifi_ack_rqst(bs_id,0x0b85)
    
        
