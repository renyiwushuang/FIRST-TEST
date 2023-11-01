# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:05:03 2019

@author: Administrator
"""

import io
from PyPDF2 import PdfFileReader,PdfFileWriter
from wand.image import Image

pdfile = PdfFileReader('E:\\YJZ\work\\化工安全\\M02模块送审\\修改\\904.pdf')
pageobj = pdfile.getPage(0)
dst_pdf = PdfFileWriter()
dst_pdf.addPage(pageobj)
pdf_bytes = io.BytesIO()
dst_pdf.write(pdf_bytes)
pdf_bytes.seek(0)
img = Image(file=pdf_bytes,resolution=500)
img.format = 'jpg' 
img.save(filename='2.jpg')
img.destroy() 
