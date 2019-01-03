# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 21:45:36 2018

@author: 21524
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 01:03:43 2018

@author: 21524
"""

import wx
from draw import SketchWindow


class SketchFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,-1,'Sketch Frame',size=(800,600))
        self.sketchwindow=SketchWindow(self,-1)
        self.sketchwindow.Bind(wx.EVT_MOTION,self.OnSketchMotion)
        self.initStatusBar()
        self.createMenuBar()
        
    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1,-2,-3])
        
        
        
    def OnSketchMotion(self,event):
        self.statusbar.SetStatusText('Pos:%s'%str(event.GetPosition()),0)
        self.statusbar.SetStatusText('Currren Pts:%s'%len(self.sketchwindow.curLine),1)
        self.statusbar.SetStatusText('Line Count:%s'%len(self.sketchwindow.lines),2)
        event.Skip()
        
    def menuData(self):
        return[('&File',(
                ('&New','New Sketch file',self.OnNew),
                ('&Open','Open sketch file',self.OnOpen),
                ('&Save','Save sketch file',self.OnSave),
                ('','',''),
                ('&Color',(('&Black','',self.OnColor,wx.ITEM_RADIO),
                ('&Red','',self.OnColor,wx.ITEM_RADIO),
                ('&Green','',self.OnColor,wx.ITEM_RADIO),
                ('&Blue','',self.OnColor,wx.ITEM_RADIO),
                )),
                ('','',''),
                ('&Quit','Quit',self.OnCloseWindow)))]
                
    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel=eachMenuData[0]
            menuItenms = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItenms),menuLabel)
        self.SetMenuBar(menuBar)
       
    def createMenu(self,menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem)==2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewIdRef(),label,subMenu)
            else:
                self.createMenuItem(menu,eachItem[0],eachItem[1],eachItem[2])
        return menu
                
    def createMenuItem(self,menu,label,status,handler,kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1,label,status,kind)
        self.Bind(wx.EVT_MENU,handler,menuItem)
    
    def OnNew(self,event):
        pass
    def OnOpen(self,event):
        pass
    def OnSave(self,event):
        pass
    def OnColor(self,event):
        menubar = self.GetMenuBar()
        itemId = event.GetId()
        item = menubar.FindItemById(itemId)
        color = item.GetLabel()
        self.sketchwindow.SetColor(color)
        
    def OnCloseWindow(self,event):
        self.Destroy()
        
        
    

if __name__ == '__main__' :
    app = wx.App()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()
    