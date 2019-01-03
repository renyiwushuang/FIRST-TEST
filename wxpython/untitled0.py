# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 01:19:36 2019

@author: 21524
"""

a=('&File',(
                ('&New','New Sketch file','self.OnNew'),
                ('&Open','Open sketch file','self.OnOpen'),
                ('&Save','Save sketch file','self.OnSave'),
                ('','',''),
                ('&Color',(('&Black','','self.OnColor,wx.ITEM_RADIO'),
                ('&Red','','self.OnColor,wx.ITEM_RADIO'),
                ('&Green','','self.OnColor,wx.ITEM_RADIO'),
                ('&Blue','','self.OnColor,wx.ITEM_RADIO'),
                )),
                ('','',''),
                ('&Quit','Quit','self.OnCloseWindow')))