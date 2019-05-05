# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 355,256 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.OUT = wx.Button( self, wx.ID_ANY, u"输出路径", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.OUT, 0, wx.ALL, 5 )
		
		self.change = wx.Button( self, wx.ID_ANY, u"转换文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.change, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE )
		bSizer6.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND|wx.SHAPED, 5 )
		
		
		bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.OUT.Bind( wx.EVT_BUTTON, self.getOutpath )
		self.change.Bind( wx.EVT_BUTTON, self.gochange )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def getOutpath( self, event ):
		event.Skip()
	
	def gochange( self, event ):
		event.Skip()
	

