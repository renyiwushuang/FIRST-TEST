from queue import Queue
import Prase
import Packet
import time
import binascii
import struct


def fun(data,len,port):
    print("fun test !\t",binascii.hexlify(data).upper())

def unregisterfun(cmd,data,port):
    print(hex(cmd),':',binascii.hexlify(data).upper())
    pass

mq = Queue()

prase_test = Prase.prase_class_init("test",mq,unregisterfun)

prase_test.add_cmd(0xaaaa,fun)
# prase.join()
# print(binascii.hexlify(packet.get_packet(0xaa55,b'\x00\x11\x22\x33',4)))

cnt = 0
while True:
    cnt += 1
    v = struct.pack('>H', cnt%0xffff)
    data = Packet.get_packet(0xaaa2,v,len(v))
    # mq.put(binascii.unhexlify("A3523301A20A000004000000FFFF02FFD8"))
    mq.put((data,0))

    data = Packet.get_packet(0xaaaa,v,len(v))
    # mq.put(binascii.unhexlify("A3523301A20A000004000000FFFF02FFD8"))
    mq.put((data,0))
    # print(binascii.hexlify(data))
    time.sleep(1)
    # print("main")
