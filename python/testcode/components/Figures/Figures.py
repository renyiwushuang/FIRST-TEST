import matplotlib.pyplot as plt
import time
import threading


show_state = True

signal_bs_list=list()

'''
show_data = {
"figuren":{
        "show":{"id":{
                        "data":list(data),#must
                        "x_data":list(data),#Optional
                        "colour":xxx,     #Optional
                        "flag":xxx,#Optional,fill by show_thread_entry
                     }
            }
        "xmax":xxx,          #Optional
        "x_vlaue":xxx        #fill by show_thread_entry
        "colours_cnt":xxx,   #fill by show_thread_entry
        "figure_flag":xxx,   #fill by show_thread_entry
        "xlabel":xxx,        #Optional 
        "ylabel":xxx,        #Optional
        }
}
'''
class show_thread_entry(threading.Thread):
    def __init__(self, t_name,user_dict):
        threading.Thread.__init__(self, name=t_name)
        
        self.user_dict = user_dict
        self.dflt_xmax = 250
        self.dflt_xlabel = "x"
        self.dflt_ylabel = "y"

        self.show_data = user_dict

        self.colours = ['red','blue', 'orange','magenta', 'yellow','green',  'cyan',  'black','gray']
        self.colours_cnt = 0

        self.suspend_flag = False
    def suspend(self):
        self.suspend_flag = True
        
    def resume(self):
        self.suspend_flag = False
        
    def run(self):

        
        
        while(True):

            if (self.suspend_flag == False):
                for figure in self.show_data.keys():
                    #figure 参数设置
                    if ("figure_flag" in self.show_data[figure].keys()) == False:
                        self.show_data[figure]["figure_flag"] = 1
                        if ("xmax" in self.show_data[figure].keys()) == False:
                            self.show_data[figure]["xmax"] = self.dflt_xmax
                            
                        if ("xlabel" in self.show_data[figure].keys()) == False:
                            self.show_data[figure]["xlabel"] = "x"
                            
                        if ("ylabel" in self.show_data[figure].keys()) == False:
                            self.show_data[figure]["ylabel"] = "y"
                            
                        self.show_data[figure]["colours_cnt"] = 0
                        self.show_data[figure]["x_vlaue"]     = 0
                    #figure 更新数据
                    plt.figure(figure)
                    plt.cla()
                    plt.grid(True)

                    id_list = list(self.show_data[figure]["show"].keys())
                    id_list.sort()
                    for id in id_list:
                        #曲线参数设置
                        if ("flag" in self.show_data[figure]["show"][id].keys()) == False:
                            self.show_data[figure]["show"][id]["flag"] = 1
                            if ("colour" in self.show_data[figure]["show"][id].keys()) == False:
                                self.show_data[figure]["show"][id]["colour"] = self.colours[self.show_data[figure]["colours_cnt"]]
                                self.show_data[figure]["colours_cnt"] += 1
                                self.show_data[figure]["colours_cnt"] %= len(self.colours)
                        #曲线数据更新
                        self.show_data[figure]["x_vlaue"] = max(self.show_data[figure]["x_vlaue"],len(self.show_data[figure]["show"][id]["data"]))#figure最长X轴

                        if len(self.show_data[figure]["show"][id]["data"]) > self.show_data[figure]["xmax"]:
                            if("x_data" in self.show_data[figure]["show"][id].keys()):
                                plt.plot(self.show_data[figure]["show"][id]["x_data"][len(self.show_data[figure]["show"][id]) - self.show_data[figure]["xmax"]:],self.show_data[figure]["show"][id]["data"][len(self.show_data[figure]["show"][id]) - self.show_data[figure]["xmax"]:], label=id, color=self.show_data[figure]["show"][id]["colour"])  # "#%06x"%(int(0xffffff/int(key,16)))#                  
                            else:
                                plt.plot(self.show_data[figure]["show"][id]["data"][len(self.show_data[figure]["show"][id]) - self.show_data[figure]["xmax"]:], label=id, color=self.show_data[figure]["show"][id]["colour"])  # "#%06x"%(int(0xffffff/int(key,16)))#
                        else:
                            if("x_data" in self.show_data[figure]["show"][id].keys()):
                                plt.plot(self.show_data[figure]["show"][id]["x_data"],self.user_dict[figure]["show"][id]["data"],label=id, color=self.show_data[figure]["show"][id]["colour"])
                            else:
                                plt.plot(self.user_dict[figure]["show"][id]["data"],label=id, color=self.show_data[figure]["show"][id]["colour"])

                    #figure x/y label、legend 显示            
                    plt.xlabel(self.show_data[figure]["xlabel"])
                    plt.ylabel(self.show_data[figure]["ylabel"])
                    plt.legend(loc='upper left')
                
            plt.pause(1)

            

def FiguresInit (name,user_dict):
    show = show_thread_entry(name,user_dict)
    show.start()
    return show
