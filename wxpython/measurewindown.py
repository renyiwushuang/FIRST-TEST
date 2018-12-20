# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 17:09:40 2018

@author: Administrator
"""

import wx
import wx.xrc

###########################################################################
## Class MyFrame4
###########################################################################

class MyFrame4 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 489,229 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer11 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer11.AddGrowableRow( 1 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer39 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl19 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.m_textCtrl19, 4, wx.ALL, 5 )
		
		self.m_button44 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.m_button44, 1, wx.ALL, 5 )
		
		self.m_button45 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.m_button45, 1, wx.ALL, 5 )
		
		
		fgSizer11.Add( bSizer39, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrl20 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer41.Add( self.m_textCtrl20, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer11.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer11 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

app = wx.App()
  
main_win = MyFrame4(None)
main_win.Show()

app.MainLoop()