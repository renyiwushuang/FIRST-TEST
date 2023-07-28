
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

mq = Queue()
sub_list = list()

        
if(len(sys.argv ) > 1):
    for i in range(1,len(sys.argv)):
        sub_list.append("/EH100602/tx/"+sys.argv[i])
else:
    sub_list.append("/EH100602/tx/#")
#sub_list.append("/EH100602/rx/#")
print("服务器IP:",config.mqtt_broker_ip)
mqtt = MqttThread.mqtt_thread_init(config.mqtt_broker_ip,sub_list,mq)


CARD_LCT_T= 2#HZ
MAX_WAIT_DELAY = 0.5# 2s

def un_register(cmd,data,port):
    #print(hex(cmd),binascii.hexlify(data))
    pass

mqtt_prase = prase.prase_class_init("mqtt_prase",mq,un_register)


'''

         {
           "card_id":
                   {
                     "seq":
                           {
                           "bs1_id":t1,
                           "bs2_id":t2,
                           "bs3_id":t3,
                           "bs4_id":t4
                           }
                    }
          }

'''
p_2a0a_dict = dict()

#p_2a0a_set = dict()
def Prase_2A0A_Test(data,len,port):
    
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
        tp = struct.unpack("<IBHBHBIb",data[index:16+index])
        #print(binascii.hexlify(data[index:16+index]))
        index += 16
        card_addr = tp[0]
        unix_ts = tp[1] + tp[2]*256

        if (card_addr in p_2a0a_dict.keys()) == False:
            p_2a0a_dict[card_addr] = dict()#序号
        if (unix_ts in p_2a0a_dict[card_addr].keys()) == False:
            p_2a0a_dict[card_addr][unix_ts] = dict()#基站接收时间

        #print(p_2a0a_dict,card_addr,unix_ts,bs_addr_r)
        p_2a0a_dict[card_addr][unix_ts][bs_addr_r] = time.time()
        




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
            
time.sleep(2)
input_instance = input_class("input",p_2a0a_dict)
#input_instance.start()

'''
{
    card_id:{
        "max_seq":xxx;
        "min_seq"xxx;
        "one_bs":xxx;
        "two_bs":xxx;
        "tree_bs":xxx;
        "four_bs":xxx
    }
}

'''
csr_dict = dict()

s_r_s=0
s_r_three=0
s_r_two=0
s_r_one=0
s_r_zero=0
while(True):
    time.sleep(2)
    if p_2a0a_dict :

        
        card_list = list(p_2a0a_dict.keys())
        card_list.sort()
        
        #calculat card sucess_rata 
        for card_addr_r in card_list:#card id
            if (card_addr_r in csr_dict.keys()) == False:
                csr_dict[card_addr_r] = dict()
                csr_dict[card_addr_r]["max_seq"] = 0x00
                csr_dict[card_addr_r]["min_seq"] = 0xffffffff
                csr_dict[card_addr_r]["one_bs"] = 0x00
                csr_dict[card_addr_r]["two_bs"] = 0x00
                csr_dict[card_addr_r]["tree_bs"] = 0x00
                csr_dict[card_addr_r]["four_bs"] = 0x00
            
            card_seq_list = list(p_2a0a_dict[card_addr_r].keys())#序号字典
            card_seq_list.sort()
            
            #print("bs addr:%x(%d)card num:%d "%(bs_addr_r,bs_addr_r,len( p_2a0a_dict[bs_addr_r]["card_num"])))
            for card_sqe_r in card_seq_list:#card seq
                if(len(p_2a0a_dict[card_addr_r][card_sqe_r]) == 4):#only four bs receive card sucess rate
                    csr_dict[card_addr_r]["max_seq"] = max(csr_dict[card_addr_r]["max_seq"],card_sqe_r)
                    csr_dict[card_addr_r]["min_seq"] = min(csr_dict[card_addr_r]["min_seq"],card_sqe_r)
                    csr_dict[card_addr_r]["four_bs"] += 1
                    del p_2a0a_dict[card_addr_r][card_sqe_r]
                elif(len(p_2a0a_dict[card_addr_r][card_sqe_r]) == 3):#only three bs receive card sucess rate
                    max_t = time.time()#max(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    min_t = min(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    if (max_t - min_t) > MAX_WAIT_DELAY :
                        csr_dict[card_addr_r]["max_seq"] = max(csr_dict[card_addr_r]["max_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["min_seq"] = min(csr_dict[card_addr_r]["min_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["tree_bs"] += 1
                        del p_2a0a_dict[card_addr_r][card_sqe_r]
                elif(len(p_2a0a_dict[card_addr_r][card_sqe_r]) == 2): #only two bs receive card sucess rate
                    max_t = time.time()#max(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    min_t = min(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    if (max_t - min_t) > MAX_WAIT_DELAY :
                        csr_dict[card_addr_r]["max_seq"] = max(csr_dict[card_addr_r]["max_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["min_seq"] = min(csr_dict[card_addr_r]["min_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["two_bs"] += 1
                        del p_2a0a_dict[card_addr_r][card_sqe_r]
                elif(len(p_2a0a_dict[card_addr_r][card_sqe_r]) == 1):#only a bs receive card sucess rate
                    max_t = time.time()#max(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    min_t = min(list(p_2a0a_dict[card_addr_r][card_sqe_r].values()))
                    if (max_t - min_t) > MAX_WAIT_DELAY :
                        csr_dict[card_addr_r]["max_seq"] = max(csr_dict[card_addr_r]["max_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["min_seq"] = min(csr_dict[card_addr_r]["min_seq"],card_sqe_r)
                        csr_dict[card_addr_r]["one_bs"] += 1
                        del p_2a0a_dict[card_addr_r][card_sqe_r]
                else:
                    print('rx over max bs num')
                
             
                
                
               
                

                
                

                
                
                




        #print card sucess
        #os.system('cls')
        #print(csr_dict)
        #print("card num:%d all_sucess_rate:%0.2f%% "%(len(csr_dict.keys()),s_r_s/len(csr_dict.keys())*100))
        print("card num:%d all_sucess_rate:%0.2f%% \t%0.2f%% \t%0.2f%% \t%0.2f%% \t%0.2f%% \t"%(len(csr_dict.keys()),s_r_s/len(csr_dict.keys())*100,s_r_three/len(csr_dict.keys())*100,s_r_two/len(csr_dict.keys())*100,s_r_one/len(csr_dict.keys())*100,s_r_zero/len(csr_dict.keys())*100))
        s_r_s=s_r_three=s_r_two=s_r_one=s_r_zero=0
        csr_dict_key_list = list(csr_dict.keys())
        csr_dict_key_list.sort()
        for card_id_s in csr_dict_key_list:
            max_v = csr_dict[card_id_s]['max_seq']
            min_v = csr_dict[card_id_s]['min_seq']
            send_times = max_v - min_v + 1
            
            f_cnt_v = csr_dict[card_id_s]['four_bs']
            th_cnt_v = csr_dict[card_id_s]['tree_bs']
            tw_cnt_v = csr_dict[card_id_s]['two_bs']
            o_cnt_v = csr_dict[card_id_s]['one_bs']

            s_r_s += f_cnt_v/send_times
            s_r_three += th_cnt_v/send_times
            s_r_two += tw_cnt_v/send_times
            s_r_one += o_cnt_v/send_times
            
            

            scbs4 = f_cnt_v/send_times*100
            scbs3 = th_cnt_v/send_times*100
            scbs2 = tw_cnt_v/send_times*100
            scbs1 = o_cnt_v/send_times*100
            scbs0 = 100-scbs4-scbs3-scbs2-scbs1

            s_r_zero += scbs0/100.0
            print("id:0x%04x(%05d)   \t4-bs:%0.2f%%(%d)   \t3-bs:%0.2f%%(%d)   \t2-bs:%0.2f%%(%d)   \t1-bs:%0.2f%%(%d)   \t0-bs:%0.2f%%"%\
                  (card_id_s,card_id_s,scbs4,f_cnt_v,scbs3,th_cnt_v,\
                   scbs2,tw_cnt_v,scbs1,o_cnt_v,scbs0));
            

        



        
