'''
解包数据包类
'''
import threading
from queue import Queue
import queue
import struct
import binascii

# 计算校验
def get_sum(pload,len):
    sum = 0
    for i in range(len):
        sum += pload[i]
    sum %= 256
    # print("cal sum:%02x" % (sum))
    return sum

#对比校验
def get_check(data,len):
    rt = 0
    sum = data[len-1]
    # print("get sum:%02x"%(sum))
    if(sum == get_sum(data,len-1)):
        rt = True
    else:
        rt = False
    return rt

#解包线程类
class prase_class(threading.Thread):
    def __init__(self, t_name,user_queue,unregisterfun):
        threading.Thread.__init__(self, name=t_name)
        self.handler_mq = user_queue
        self.handler_cmd = dict()#{'cmd':handler}
        self.unregisterfun = unregisterfun
    def add_cmd(self,cmd,cmd_handler):
        self.handler_cmd[cmd] = cmd_handler

    def run(self):
        remain_data = b''#解包剩余长度
        min_frame_len = 13#最小帧长度
        max_frame_len = 1024#最小帧长度
        frame_header = 0x013352a3
        frame_header_len = 4
        while(True):
            data = self.handler_mq.get()
            remain_data = remain_data + data[0]
            pos = 0

            while (min_frame_len <= len(remain_data[pos:])):  # 保证最小帧长度(帧头+命令+保留位+数据长度+校验 = min_frame_len Byte
                # print('frame:',binascii.hexlify(remain_data[pos:]))
                header, command, reserve, datalenght = struct.unpack("<IHHI", remain_data[pos:(pos + min_frame_len-1)])
                if (header == frame_header):  # 帧头对比
                    if (datalenght + min_frame_len <= len(remain_data[pos:])):  # 长度检查
                        if (get_check(remain_data[pos:], datalenght + min_frame_len) == True):
                            if ((command in self.handler_cmd.keys()) == True):
                                self.handler_cmd[command](remain_data[pos+min_frame_len-1:pos+min_frame_len+datalenght-1],datalenght,data[1])#执行命令处理函数
                            else:
                                if self.unregisterfun == None:
                                    print("cmd:%04x no register handler"%command)
                                else:
                                    self.unregisterfun(command,remain_data[pos+min_frame_len-1:pos+min_frame_len+datalenght-1],data[1])
                                pass
                            pos += datalenght + min_frame_len
                        else: # 校验失败移动一个帧头
                            print("frame crc error,cmd:0x%04x"%command)
                            pos += 4
                    else:#长度过短，等待下一帧数据拼包后解析
                        if (datalenght + min_frame_len) > max_frame_len :
                            print("frame length to long")
                            pos += 4
                        else:
                            print("frame length to short %d<%d,cmd:0x%04x"%(datalenght + min_frame_len,len(remain_data[pos:]),command))
                            break
                else:# 帧头错误移动一个字节
                    #print("frame header error:%08x"%header)
                    pos += 1

            remain_data = remain_data[pos:]#保存剩余未能被够被解析数据
        # try:
        #     pass
        # except queue.Empty:
        #     pass

def prase_class_init(name,input_queue,unregisterfun):
    prase_instance = prase_class(name,input_queue,unregisterfun)
    prase_instance.start()
    return prase_instance
