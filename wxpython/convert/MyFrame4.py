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

class MyFrame2 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 424,307 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button6 = wx.Button( self, wx.ID_ANY, u"ERP", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button6, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"calibration", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"OUTPUT", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_button9 = wx.Button( self, wx.ID_ANY, u"CONVERT", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button9, 0, wx.ALL, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer5.Add( self.m_textCtrl5, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button6.Bind( wx.EVT_BUTTON, self.erpget )
		self.m_button7.Bind( wx.EVT_BUTTON, self.calibrationget )
		self.m_button8.Bind( wx.EVT_BUTTON, self.outpathget )
		self.m_button9.Bind( wx.EVT_BUTTON, self.convert )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def erpget( self, event ):
		event.Skip()
	
	def calibrationget( self, event ):
		event.Skip()
	
	def outpathget( self, event ):
		event.Skip()
	
	def convert( self, event ):
		event.Skip()
	

