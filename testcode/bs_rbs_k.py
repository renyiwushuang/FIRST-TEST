
from queue import Queue
import binascii
import struct
import time
import os
import sys

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
    sub_list.append("/EH100602/tx/#")

show = dict()
figure_header = "RBS_K_Value"+str(sub_list)
show[figure_header] = dict()
show[figure_header]["xmax"] = 1000
show[figure_header]["show"] = dict()
show[figure_header]["ylabel"] = "k"

time.sleep(1)
show_instance = Figures.FiguresInit("show",show)
time.sleep(1)

print("broker_ip:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)

MAX_WAIT_TIME = 5

'''
{
id:
    {
     seq_r:
        {
            tx_ts:ts
            tx_ts_time:pc_ts
            rx_ts:
               {
              id_r:rx_ts
               }
         }
    }
}
'''
rbs_k_dict = dict()

def Prase_2A07_BS_Snd(data,l,port):
    global rbs_k_dict
    bs_id,uwb_mode,seq_l,seq_h,snd_ts_l,snd_ts_h = struct.unpack("<HBBHBI",data[0:11])

    if uwb_mode == 3:#RSB MODE
        seq = seq_l + seq_h*256
        snd_ts = snd_ts_l + snd_ts_h*256
        if (bs_id in rbs_k_dict.keys()) == False:
            rbs_k_dict[bs_id] = dict()
        if (seq in rbs_k_dict[bs_id].keys()) == False:
            rbs_k_dict[bs_id][seq] = dict()
            rbs_k_dict[bs_id][seq]['tx_ts'] = snd_ts
            rbs_k_dict[bs_id][seq]['tx_ts_time'] = time.time()
            rbs_k_dict[bs_id][seq]['rx_ts'] = dict()
        else:
            print(" uwb send seq overflow")


def Prase_2A08_BS_Rcv(data,l,port):
    global rbs_k_dict
    
    index = 0
    
    #print(binascii.hexlify(data))

    bs_id,uwb_mode,bs_num = struct.unpack("<HBB",data[index:4])
    index += 4
    
    #print("bs_id:%x mode:%d num:%d"%(bs_id,uwb_mode,bs_num))

    if uwb_mode == 1:# Receive mode
        for i in range(0,bs_num):
            #addr(2B) + UNIX_TS_S(3B) + UNIX_TS_R(3B) + TS(5B)
            rcv_bs_id,snd_seq_l,snd_seq_h,rcv_seq_l,rcv_seq_h,rcv_ts_l,rcv_ts_h,rssi,prb = struct.unpack("<HBHBHBIBH",data[index:16+index])
            #print(binascii.hexlify(data[index:16+index]))
            snd_seq = snd_seq_l + snd_seq_h*256
            snd_ts = rcv_ts_l + rcv_ts_h*256

            if (rcv_bs_id in rbs_k_dict.keys()) == True:
                
                if(snd_seq in rbs_k_dict[rcv_bs_id].keys()) == True:
                    #print(snd_seq)
                    rbs_k_dict[rcv_bs_id][snd_seq]['rx_ts'][bs_id] = snd_ts
        

mqtt_prase.add_cmd(0x2A07,Prase_2A07_BS_Snd)
mqtt_prase.add_cmd(0x2A08,Prase_2A08_BS_Rcv)

time.sleep(2)

while(True):
    time.sleep(0.5)
    if rbs_k_dict:
        #RBS基站分类处理
        bs_id_list = list(rbs_k_dict.keys())
        bs_id_list.sort()
        for bs_id in bs_id_list:
            #发送序号处理
            bs_snd_seq_list = list(rbs_k_dict[bs_id].keys())
            bs_snd_seq_list.sort()
            for seq in bs_snd_seq_list[1:]:
                if(rbs_k_dict[bs_id][seq]['tx_ts_time']+MAX_WAIT_TIME > time.time() ):
                    bs_rcv_id_list = list(rbs_k_dict[bs_id][seq]['rx_ts'].keys())
                    bs_rcv_id_list.sort()

                    seq_1 = bs_snd_seq_list[bs_snd_seq_list.index(seq)-1]#下一序号的值
                    
                    #发送间隔
                    if rbs_k_dict[bs_id][seq]['tx_ts'] > rbs_k_dict[bs_id][seq_1]['tx_ts'] :
                        ds = rbs_k_dict[bs_id][seq]['tx_ts'] - rbs_k_dict[bs_id][seq_1]['tx_ts']
                    else:
                        ds = 0xffffffffff + rbs_k_dict[bs_id][seq]['tx_ts'] - rbs_k_dict[bs_id][seq_1]['tx_ts']

                    for bs_rcv_id in bs_rcv_id_list:
                        #print("snd_bs_id:%04x\trcv_bs_id:%04x\tseq:%d\t tx_ts:%d rx_ts:%d"%(bs_id,bs_rcv_id,seq,rbs_k_dict[bs_id][seq]['tx_ts'],rbs_k_dict[bs_id][seq]['rx_ts'][bs_rcv_id]))
                        #print(seq,seq_add_1,bs_rcv_id)
                        #接收间隔
                        if(bs_rcv_id in rbs_k_dict[bs_id][seq]['rx_ts'].keys() and (bs_rcv_id in rbs_k_dict[bs_id][seq_1]['rx_ts'].keys())):
                            if rbs_k_dict[bs_id][seq]['rx_ts'][bs_rcv_id] > rbs_k_dict[bs_id][seq_1]['rx_ts'][bs_rcv_id] :
                                dr = rbs_k_dict[bs_id][seq]['rx_ts'][bs_rcv_id] - rbs_k_dict[bs_id][seq_1]['rx_ts'][bs_rcv_id]
                            else:
                                dr = 0xffffffffff + rbs_k_dict[bs_id][seq]['rx_ts'][bs_rcv_id] - rbs_k_dict[bs_id][seq_1]['rx_ts'][bs_rcv_id]

                            k = ds/dr-1
                            print("snd_bs_id:%04x\trcv_bs_id:%04x\tk:\t%s"%(bs_id,bs_rcv_id,format(k,'.2e')))

                            id_str = "%x->%x"%(bs_id,bs_rcv_id)
                            if (id_str in show[figure_header]["show"].keys()) == False:
                                show[figure_header]["show"][id_str] = dict()
                                show[figure_header]["show"][id_str]["data"] = list()

                            show[figure_header]["show"][id_str]["data"].append(k)
                                
                    del rbs_k_dict[bs_id][seq_1]
                    #bs_snd_seq_list.remove(seq_1)
