
import time
import MqttThread
import binascii
import queue
from queue import Queue

mq = Queue()
sub_list = list()
sub_list.append("/lct3d/tx/#")
mqtt = MqttThread.mqtt_thread_init("192.168.0.158",sub_list,mq)

f = open("mqtt_record.txt",'w')
while(True):
    try:
        data = mq.get(timeout=2)
        if len(data):
            # f.write(binascii.hexlify(data).decode('utf-8'))
            print(data[1],len(data[0]),binascii.hexlify(data[0]).decode('utf-8'))
        else:
            print("mqtt mq get timeout")
    except queue.Empty:
        f.close()
        f = open("mqtt_record.txt",'a')
        print("mqtt mq get Empty")
    # time.sleep(1)