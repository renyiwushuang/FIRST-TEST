import Figures
import time
import math
import threading

show = dict()
show["figure1"] = dict()
show["figure1"]["xmax"] = 500

show["figure1"]["show"] = dict()
show["figure1"]["show"]["ff01"] = dict()
show["figure1"]["show"]["ff01"]["data"] = [0]
show["figure1"]["show"]["ff02"] = dict()
show["figure1"]["show"]["ff02"]["data"] = [0]


show["figure2"] = dict()
show["figure2"]["xmax"] = 1000

show["figure2"]["show"] = dict()
show["figure2"]["show"]["ff01"] = dict()
show["figure2"]["show"]["ff01"]["data"] = [0]
show["figure2"]["show"]["ff02"] = dict()
show["figure2"]["show"]["ff02"]["data"] = [0]

show_instance = Figures.FiguresInit("show",show)



cnt=0
def calc_rate():
    global cnt
    show["figure1"]["show"]["ff01"]["data"].append(math.sin(cnt))
    show["figure1"]["show"]["ff02"]["data"].append(math.cos(cnt))
    
    show["figure2"]["show"]["ff01"]["data"].append(math.cos(cnt))
    show["figure2"]["show"]["ff02"]["data"].append(math.sin(cnt))
    cnt += 0.02
    #print("*")
    rate_timer = threading.Timer(0.02, calc_rate)
    rate_timer.start()

rate_timer = threading.Timer(1,calc_rate)
rate_timer.start()

time.sleep(0.5)#iput must    
while True:
    #input_context = input("input :")
    input_context = input("input :s(suspend figure),r(resume figure)")
    if(input_context == "s"):
        show_instance.suspend()
    elif (input_context == "r"):
        show_instance.resume()
    #print(input_context)
    #time.sleep(1)

