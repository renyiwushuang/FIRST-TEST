import Figures
import time
import math

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

show["figure3"] = dict()
show["figure3"]["xmax"] = 1000

show["figure3"]["show"] = dict()
show["figure3"]["show"]["ff01"] = dict()
show["figure3"]["show"]["ff01"]["data"] = [0]
show["figure3"]["show"]["ff01"]["x_data"] = [0]

show_instance = Figures.FiguresInit("show",show)

cnt=0
_cnt=0
while True:
    time.sleep(0.02)
    show["figure1"]["show"]["ff01"]["data"].append(math.sin(cnt))
    show["figure1"]["show"]["ff02"]["data"].append(math.cos(cnt))
    
    show["figure2"]["show"]["ff01"]["data"].append(math.cos(cnt))
    show["figure2"]["show"]["ff02"]["data"].append(math.sin(cnt))

    show["figure3"]["show"]["ff01"]["data"].append(math.cos(_cnt))
    show["figure3"]["show"]["ff01"]["x_data"].append(_cnt)
    _cnt += 1
    
    cnt += 0.02

    if (cnt > 10) and (cnt < 20):
        show_instance.suspend()
        print("suspend")
