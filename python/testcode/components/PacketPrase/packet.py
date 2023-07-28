import struct

# 计算校验
def get_sum(pload,len):
    sum = 0
    for i in range(len):
        sum += pload[i]
    sum %= 256
    # print("cal sum:%02x" % (sum))
    return sum

def get_packet(cmd,pload,l):
    frame_header = 0x013352a3 #帧头
    min_frame_len = 13  # 最小帧长度(帧头+命令+保留位+数据长度+校验=13
    formstr = "<IHHI%ds"%l #帧(帧头+命令+保留位+数据长度+数据+校验

    data = struct.pack(formstr,frame_header,cmd,0x0000,l,pload)
    v = struct.pack('B',get_sum(data, min_frame_len + l - 1))

    data = data +v

    return data

