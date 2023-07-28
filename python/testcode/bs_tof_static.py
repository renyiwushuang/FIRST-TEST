
from queue import Queue
import binascii
import struct
import time
import os
import sys

#from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.PacketPrase import packet
from components.SerialCom import SerialThread
from components.FileSave import FileSave


com = "COM15"
interal = 50
count = 2000

#com interal count
if(len(sys.argv ) == 4):
    com = sys.argv[1]
    interal = int(sys.argv[2])
    count = int(sys.argv[3])
    #print(type(com),type(interal),type(count))
    print("input config",com,interal,count)
else:
    print("default config",com,interal,count)


file_name = "interval_%d__times_%d"%(interal,count)+".txt"

    
mqSerial = Queue()   
mqPacket = Queue()
mqFileSave = Queue()

serial_instance = SerialThread.SC_thread_init(mqSerial,com,460800)
FileSave.File_Save_Init("file_save",os.getcwd()+"\\",file_name,mqFileSave)



def un_register(cmd,data,port):
    print(port,hex(cmd),binascii.hexlify(data))
    pass
serial_prase = prase.prase_class_init("serial_prase",mqPacket,un_register)



#mqtt_prase.add_cmd(0x2A0A,Prase_2A0A_Test)


_uwb_msg = struct.pack('<BBBBHH',0x00,0x05,0x87,0x01,0xff01,0xfeff)
_uwb_msg_test = struct.pack('<BBBBHHH',0x00,0x05,0x50,0x01,interal,count,0xfeff)

time.sleep(1)
uwb_msg = packet.get_packet(0x0022,_uwb_msg,len(_uwb_msg))
serial_instance.send(uwb_msg,len(uwb_msg))
time.sleep(0.5)
uwb_msg_test = packet.get_packet(0x0022,_uwb_msg_test,len(_uwb_msg_test))
serial_instance.send(uwb_msg_test,len(uwb_msg_test))
time.sleep(1)

cnt = 0
while(True):
    msg = mqSerial.get()
    print("rcv %d:%s"%(cnt,msg))
    cnt += 1
    mqFileSave.put(msg)
    mqPacket.put((msg,com))
        
        




        
