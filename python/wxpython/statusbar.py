
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
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1,-2,-3])
        
        
        
    def OnSketchMotion(self,event):
        self.statusbar.SetStatusText('Pos:%s'%str(event.GetPosition()),0)
        self.statusbar.SetStatusText('Currren Pts:%s'%len(self.sketchwindow.curLine),1)
        self.statusbar.SetStatusText('Line Count:%s'%len(self.sketchwindow.lines),2)
        event.Skip()


if __name__ == '__main__' :
    app = wx.App()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()
    