# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:53:56 2019

@author: Administrator
"""

import wx
import MyFrame
import os
import io
from PyPDF2 import PdfFileReader,PdfFileWriter
from wand.image import Image 

def _run_convert(pdfile,savefilename,page_index,res=500):
    
    pageobj = pdfile.getPage(page_index)
    dst_pdf = PdfFileWriter()
    dst_pdf.addPage(pageobj)
    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)
    img = Image(file=pdf_bytes,resolution=res)
    img.format = 'jpg' 
    img.save(filename=savefilename+'-'+str(page_index)+'.jpg')
    img.destroy() 

def dealpdf(file):
    portion = os.path.splitext(file)
    savefilename = portion[0].split('\\')[-1]
    pdfile = PdfFileReader(file)
    page_num = pdfile.getNumPages()
    for page_index in range(page_num):
        _run_convert(pdfile,savefilename,page_index)
    
    
   
   
class MyFrame(MyFrame.MyFrame):
    
    def getOutpath( self, event ):
        dlg = wx.DirDialog(self,'output',os.getcwd())
        if dlg.ShowModal() == wx.ID_OK :
               
               self.m_textCtrl3.write(dlg.GetPath()+'\n')
               
               
               os.chdir(dlg.GetPath())
        dlg.Destroy()
    
    def gochange( self, event ):
        
       
        dlg = wx.FileDialog(self,'Change',os.getcwd(),style=wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK :
            
            print(dlg.GetPaths())
            for file in dlg.GetPaths():
                dealpdf(file)
           
            
        dlg.Destroy()
        self.m_textCtrl3.write('done\n')
        
   
         
  
     
     
if __name__== '__main__' :
    
        app = wx.App()
        
        main_win = MyFrame(None)
        main_win.Show()

        app.MainLoop()