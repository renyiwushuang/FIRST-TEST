
import FileSave
import binascii
from queue import Queue
import time 

mq = Queue()

FileSave.File_Save_Init("file_save","./","test.txt",mq)

msg = bytes(range(0,255))
while True:
   mq.put(msg)
   time.sleep(1)

