import threading
from queue import Queue
import serial


def serial_send(msg):
    global ser
    ser.write(msg)

# serial thread entry
class srlcom_thread_entry(threading.Thread):
    
    def __init__(self,t_name,user_queue,sc_port,sc_baudrate):
        #parent class init
        threading.Thread.__init__(self)
        self.name = t_name
        self.out_mq = user_queue

        self.srlcom = serial.Serial()
        
        self.srlcom.port = sc_port
        self.srlcom.baudrate = sc_baudrate
        self.srlcom.timeout = 0.01
        
        
    def send(self,data,l):
        self.srlcom.write(data)
    
    def run(self):

        #self.srlcom = serial.Serial()
        #self.srlcom.port = "com4"
        #self.srlcom.baudrate = 115200
        #self.srlcom.timeout = 0.01
        
        self.srlcom.open()
        print(self.srlcom.name,"opend")
        
        while(True):
            msg = self.srlcom.read(64)
            if(len(msg)):
                self.out_mq.put((msg,self.srlcom.port))


def SC_thread_init (user_queue,sc_port,sc_baudrate):
    srlcom_t = srlcom_thread_entry("Serial_"+sc_port,user_queue,sc_port,sc_baudrate)
    srlcom_t.start()
    return srlcom_t




