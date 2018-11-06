
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
#sub_list.append("/EH100602/tx/"+"fefc")
#sub_list.append("/EH100602/tx/"+sys.argv[1])
#sub_list.append("/EH100602/tx/#")
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")

print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)




def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

def pver(ver):
    return "%d.%d.%d.%d"%((ver&0xff000000)>>24,(ver&0x00ff0000)>>16,(ver&0x0000ff00)>>8,ver&0x000000ff)

'''
{
"bs_id":{
         "wifi":xxx
         "uwb",xxx
         "mb",xxx
        } 
}
'''
bs_hb = dict()

'''
{
"bs_id":{
         "uwb_sw":x.x.x.x;
         "cnt",xxx
        } 
}
'''
bs_uwb_hb=dict()
def Prase_2A00_uwb_hb(data,l,port):
    global bs_hb
    try:
        tp = struct.unpack("<HIBBBBHH10sB",data[0:25])
        uwb_log_level = 0xff
        cir_mode = 0xff
        if(len(data)>25):
            uwb_log_level = data[25]
        if(len(data)>26):
            cir_mode = data[26]
        bs_id = tp[0]
        if (bs_id in bs_hb.keys()) == False:
            bs_hb[bs_id] = dict()
        if("uwb" in bs_hb[bs_id].keys())== False:
            bs_hb[bs_id]["uwb"] = ""
            bs_hb[bs_id]["uwb_cnt"] = 0
        bs_hb[bs_id]["uwb"] = "%d.%d.%d.%d SN:%s 固件码:%d log:%d cir:%d"%(tp[2],tp[3],tp[4],tp[5],tp[8].decode("utf-8"),tp[9],uwb_log_level,cir_mode)
        bs_hb[bs_id]["uwb_cnt"] += 1
    except Exception as err:  
        print(err,port)  

bs_mb_hb=dict()
def Prase_0BA0_mb_hb(data,l,port):
    global bs_hb
    bs_id,hw,sw,bs_mac,net_mode,ptp,reserva,wifi_mac,rssi,sub_dev,reset_reason,cpu_h,cpu_l,sn,fw_code = struct.unpack("<HII3sBBH3sbBBBB10sB",data[0:36])
    lan_speed = 0
    if len(data)>36:
        lan_speed = data[36]
    if (bs_id in bs_hb.keys()) == False:
        bs_hb[bs_id] = dict()
    if ("mb" in bs_hb[bs_id].keys()) == False:
        bs_hb[bs_id]["mb"] = ""
        bs_hb[bs_id]["mb_cnt"] = 0
    bs_hb[bs_id]["mb"] = "HW:%s SW:%s 网络:%d CPU:%d.%d%% lan速率:%dM"%(pver(hw),pver(sw),net_mode,cpu_h,cpu_l,lan_speed*10)
    bs_hb[bs_id]["mb_cnt"] += 1
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
    global bs_hb
    bs_id,hw,sw,rssi,sub,mac,ap_mac = struct.unpack("<HIIbB3s6s",data[0:21])
    if (bs_id in bs_hb.keys()) == False:
        bs_hb[bs_id] = dict()
    if ("wifi" in bs_hb[bs_id].keys()) == False:
        bs_hb[bs_id]["wifi"] = ""
        bs_hb[bs_id]["wifi_cnt"] = 0
    #print("sw:%x"%sw)
    sw_s = "%u.%u.%u"%(((sw&0x00ff0000)>>16) | ((sw&0xff000000)>>24),(sw&0x0000ff00)>>8,sw&0x000000ff)
    bs_hb[bs_id]["wifi"] = "SW:%s RSSI:%d AP:%s"%(sw_s, rssi, binascii.hexlify(ap_mac).decode("utf-8"))
    bs_hb[bs_id]["wifi_cnt"] += 1

'''
{
"bs_id":{
         "ch":xxx;
         "prf",xxx
         "prfcode",xxx
         "pac",xxx
         "len",xxx
         "rate",xxx
         "sfd",xxx
         "sfdto",xxx
          "ntm1",xxx
         "ntm2",xxx
         "cnt",xxx
        } 
}
'''
prb_len = dict()
prb_len[0x04] = 64
prb_len[0x14] = 128
prb_len[0x24] = 256
prb_len[0x34] = 512
prb_len[0x08] = 1024
prb_len[0x18] = 1536
prb_len[0x28] = 2048
prb_len[0x0c] = 4096
bs_uwb_ch_param = dict()
def Prase_2A02_uwb_ch_param(data,len,port):
    prf=["Error","16M","64M"]
    pac=["PAC8","PAC16","PAC32","PAC64"]
    rate = ["110Kbps","850Kbps","6.8Mbps"]
    tp = struct.unpack("<HBBBBBBBHBH",data[0:14])
    bs_id = tp[0]
    if (bs_id in bs_uwb_ch_param.keys()) == False:
        bs_uwb_ch_param[bs_id] = dict()
        bs_uwb_ch_param[bs_id]["cnt"] = 0
        
    bs_uwb_ch_param[bs_id]["ch"] = tp[1]
    bs_uwb_ch_param[bs_id]["prf"] = prf[tp[2]]
    bs_uwb_ch_param[bs_id]["prfcode"] = tp[3]
    bs_uwb_ch_param[bs_id]["pac"] = pac[tp[4]]
    bs_uwb_ch_param[bs_id]["len"] = prb_len[tp[5]]
    bs_uwb_ch_param[bs_id]["rate"] = rate[tp[6]]
    bs_uwb_ch_param[bs_id]["sfd"] = tp[7]
    bs_uwb_ch_param[bs_id]["sfdto"] = tp[8]
    bs_uwb_ch_param[bs_id]["ntm1"] = tp[9]
    bs_uwb_ch_param[bs_id]["ntm2"] = tp[10]
    
    bs_uwb_ch_param[bs_id]["cnt"] += 1
    

'''
{
"bs_id":{
         "ex_pa_en":xxx;
         "man_power_en",xxx
         "power_value",xxx
         "cnt",xxx
        } 
}
'''
bs_power = dict()
def Prase_2A04_power_param(data,len,port):
    global bs_power
    ex_pa_en = ["ByPass","EN"]
    man_power_en = ["Smart","Man"]
    tp = struct.unpack("<HBBI",data[0:10])
    bs_id = tp[0]
    if (bs_id in bs_power.keys()) == False:
        bs_power[bs_id] = dict()
        bs_power[bs_id]["cnt"] = 0
    bs_power[bs_id]["ex_pa_en"] = ex_pa_en[tp[1]]
    bs_power[bs_id]["man_power_en"] = man_power_en[tp[2]]
    bs_power[bs_id]["power_value"] = tp[3]
    bs_power[bs_id]["cnt"] += 1
    

'''
{
"bs_id":{
         "work_mode":xxx,
         "lct_way":xxx,
         "syn_period":xxx,
         "rand_period",xxx
         "cnt",xxx
        } 
}
'''
bs_lct_param =dict()
def Prase_2A06_lct_param(data,l,port):
    global bs_lct_param
    work_mode = ["PowerOFF","Receive","TPSN","RBS"]
    lct_way = ["Error","TDOA","AOA","TOF"]
    tp = struct.unpack("<HBBHHI",data[0:])
    bs_id = tp[0]
    if (bs_id in bs_lct_param.keys()) == False:
        bs_lct_param[bs_id] = dict()
        bs_lct_param[bs_id]["cnt"] = 0

    bs_lct_param[bs_id]["work_mode"] = work_mode[tp[1]]
    bs_lct_param[bs_id]["lct_way"] = str(tp[2])
    bs_lct_param[bs_id]["syn_period"] = tp[3]
    bs_lct_param[bs_id]["rand_period"] = tp[4]
    bs_lct_param[bs_id]["cnt"] += 1 
    #print("bs_id:%x\t work_mode:%d\t lct_mode:%d\t syn_t:%d\t rand_t:%d"%(bs_id,tp[1],tp[2],tp[3],tp[4]))
        


mqtt_prase.add_cmd(0x2A00,Prase_2A00_uwb_hb)
mqtt_prase.add_cmd(0x2A02,Prase_2A02_uwb_ch_param)
mqtt_prase.add_cmd(0x2A04,Prase_2A04_power_param)
mqtt_prase.add_cmd(0x2A06,Prase_2A06_lct_param)
mqtt_prase.add_cmd(0x0A80,Prase_0A80_wifi_rssi)
mqtt_prase.add_cmd(0x0BA0,Prase_0BA0_mb_hb)

while(True):
    time.sleep(2)

    os.system('cls')
    print(time.time())
    if bs_lct_param :
        bs_list = list(bs_lct_param.keys())
        bs_list.sort()
        print("location param:")
        for bs_id in bs_list:
            dd = bs_lct_param[bs_id]
            print("bs_id:%04x work_mode:%s lct_way:%s  syn_t:%dms rand_t:%dms  cnt:%d"%(bs_id,dd["work_mode"],dd["lct_way"],dd["syn_period"],dd["rand_period"],dd["cnt"]))

    if bs_uwb_hb:
        bs_list = list(bs_uwb_hb.keys())
        bs_list.sort()
        print("\nbs uwb hb:")
        for bs_id in bs_list:
            dd = bs_uwb_hb[bs_id]
            print("bs_id:%04x uwb_sw:%s  cnt:%d"%(bs_id,dd["uwb_sw"],dd["cnt"]))
            
    if bs_mb_hb:
        bs_list = list(bs_mb_hb.keys())
        bs_list.sort()
        print("\nbs mb hb:")
        for bs_id in bs_list:
            dd = bs_mb_hb[bs_id]
            print("bs_id:%04x mb_info:%s  cnt:%d"%(bs_id,dd["mb_info"],dd["cnt"]))
    if bs_power:
        bs_list = list(bs_power.keys())
        bs_list.sort()
        print("\nbs uwb power param:")
        for bs_id in bs_list:
            dd = bs_power[bs_id]
            print("bs_id:%04x ex_pa:%s man_pa_en:%s power:%08x  cnt:%d"%(bs_id,dd["ex_pa_en"],dd["man_power_en"],dd["power_value"],dd["cnt"]))
        


    if bs_uwb_ch_param:
        bs_list = list(bs_uwb_ch_param.keys())
        bs_list.sort()
        print("\nbs uwb power param:")
        for bs_id in bs_list:
            dd = bs_uwb_ch_param[bs_id]
            print("bs_id:%04x ch:%d prf:%s code:%d pac:%s len:%d rate:%s sfd:%d sftd:%d ntm1:%x ntm2:%x cnt:%d"%(bs_id,dd["ch"],dd["prf"],dd["prfcode"],dd["pac"],\
                                                                                    dd["len"],dd["rate"],dd["sfd"],dd["sfdto"],dd["ntm1"],dd["ntm2"],dd["cnt"]))

    if wifi_info:
        bs_list = list(wifi_info.keys())
        bs_list.sort()
        
        print("\nwifi info:")
        for bs_id in bs_list:
            print("bs_id:%04x SW:%s rssi:%d ap_mac:%s cnt:%d"%(bs_id,wifi_info[bs_id]["sw"],wifi_info[bs_id]["rssi"],wifi_info[bs_id]["ap_mac"],wifi_info[bs_id]["cnt"]))
            
    if bs_hb:
        bs_list = list(bs_hb.keys())
        bs_list.sort()
        print("\n基站心跳:")
        for bs_id in bs_list:
            dd = bs_hb[bs_id]
            print(" 基站:%04x(%d): "%(bs_id,bs_id))
            str_show = ""
            if("uwb" in dd):
                str_show += "\tUWB:%s 计数:%d"%(dd["uwb"],dd["uwb_cnt"])
            if("mb" in dd):
                str_show += ("\t主控:%s 计数:%d"%(dd["mb"],dd["mb_cnt"]))
            if("wifi" in dd):
                str_show += "\tWIFI:%s 计数:%d"%(dd["wifi"],dd["wifi_cnt"])
            
            print(str_show)
            #print("bs_id:%04x mb_info:%s  cnt:%d"%(bs_id,dd["mb_info"],dd["cnt"]))
        
