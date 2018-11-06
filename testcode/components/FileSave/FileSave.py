import threading
from queue import Queue
import serial


# serial thread entry
class file_save_thread_entry(threading.Thread):
    
    def __init__(self,t_name,file_dir,file_name,data_queue):
        #parent class init
        threading.Thread.__init__(self)
        self.name = t_name
        self.in_mq = data_queue
        
        self.file = open(file_dir+file_name,"wb")
        print(file_dir+file_name)
    def save_file_timer(self):#每秒保存一次数据
        save_timer = threading.Timer(1,self.save_file_timer)
        save_timer.start()
        self.file.flush()

    def save(self):#手动保存数据
        self.file.flush()
        
    def run(self):
        save_timer = threading.Timer(1,self.save_file_timer)
        save_timer.start()
        while(True):
            msg = self.in_mq.get()
            self.file.write(msg)


def File_Save_Init (t_name,file_dir,file_name,data_queue):
    file_t = file_save_thread_entry(t_name,file_dir,file_name,data_queue)
    file_t.start()
    return file_t




