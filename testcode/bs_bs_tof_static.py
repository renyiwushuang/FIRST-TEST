
from queue import Queue
import binascii
import struct
import time
import os
import sys

#from components.MQTT import MqttThread
from components.PacketPrase import prase
from components.SerialCom import SerialThread
from components.FileSave import FileSave


com = "COM4"
interal = 50
count = 100
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


while(True):
    msg = mqSerial.get()
    print("rcv",msg)
    mqFileSave.put(msg)
    mqPacket.put((msg,com))
        
        




        
