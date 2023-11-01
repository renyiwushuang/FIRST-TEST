# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 12:54:39 2018

@author: Administrator
"""

import wx


class SketchWindow(wx.Window):
    def __init__(self,parent,ID):
        wx.Window.__init__(self,parent,ID)
        self.SetBackgroundColour('White')
        self.colour = 'Black'
        self.thickness = 1
        self.pen = wx.Pen(self.colour,self.thickness,wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0,0)
        self.InitBuffer()
        
        self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)
        self.Bind(wx.EVT_MOTION,self.OnMotion)
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.Bind(wx.EVT_IDLE,self.OnIdle)
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        
        
    def InitBuffer(self):
            size = self.GetClientSize()
            self.buffer = wx.EmptyBitmap(size.width,size.height)
            dc = wx.BufferedDC(None,self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DrawLines(dc)
            
            self.reInitBuffer = False
            
    def GetLinesData(self):
            return self.lines[:]
        
        
    def SetLinesData(self,lines):
            self.lines = lines[:]
            self.InitBuffer()
            self.Refresh()
            
    def OnLeftDown(self,event):
        self.curLine =[]
        self.pos = event.GetPosition()
        self.CaptureMouse()
    
    def OnLeftUp(self,event):
        if self.HasCapture():
            self.lines.append((self.colour,
                               self.thickness,
                               self.curLine))
            self.curLine = []
            self.ReleaseMouse()
            
            
    def OnMotion(self,event):
        if event.Dragging() and event.LeftIsDown():
          dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
          self.drawMotion(dc,event)
        event.Skip()
        
    def drawMotion(self,dc,event):
        dc.SetPen(self.pen)
        newPos = event.GetPosition()
        coords = self.pos+newPos
        
        self.curLine.append(coords)
        dc.DrawLine(self.pos,newPos)
        self.pos = newPos
        
    def OnSize(self,event):
        self.reInitBuffer = True
        
    def OnIdle(self,event):
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)
            
    def OnPaint(self,event):
        dc = wx.BufferedPaintDC(self,self.buffer)
    
    def DrawLines(self,dc):
        for colour,thickness,line in self.lines:
            pen = wx.Pen(colour,thickness,wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)
                
    def SetColor(self,color):
        self.color = color
        self.pen = wx.Pen(self.color,self.thickness,wx.SOLID)
    def SetThickness(self,num):
        self.thickness = num
        self.pen = wx.Pen(self.color,self.thickness,wx.SOLID)
    
    
class SketchFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,-1,'Sketch Frame',size=(800,600))
        self.sketch = SketchWindow(self,-1)
        
        
if __name__ == '__main__' :
    app = wx.App()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()
                
         
       