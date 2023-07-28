
import SerialThread
import binascii
from queue import Queue

mq = Queue()

com_test = SerialThread.SC_thread_init(mq,"COM4",115200)

while True:
   com_rcv_data = mq.get()
   if len(com_rcv_data[0]):
       print(binascii.hexlify(com_rcv_data[0]))
       print(com_rcv_data[0])
       com_test.send(com_rcv_data[0],len(com_rcv_data[0]))

