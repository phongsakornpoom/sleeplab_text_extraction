#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 22:41:47 2022

@author: pongsakorntanupatrasakul
"""
import PyPDF2
import cv2
import matplotlib.pyplot as plt
import pypdfium2 as pdfium
import numpy as np
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract'

def text_extracter(pdfpath):
    pdf = pdfium.PdfDocument(pdfpath)
    page1 = pdf.get_page(0)
    pil_image1 = page1.render_topil()
    greyimg1 = greyscale(pil_image1)
#   thes1, otsu1 = cv2.threshold(greyimg1, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    final1 = cv2.resize(greyimg1, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    page2 = pdf.get_page(1)
    pil_image2 = page2.render_topil()
    greyimg2 = greyscale(pil_image2)
    thes2, otsu2 = cv2.threshold(greyimg2, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text1 = pytesseract.image_to_string(final1)
    text2 = pytesseract.image_to_string(otsu2)
    return text1,text2

def greyscale(pil_img):
    img = cv2.cvtColor(np.array(pil_img),cv2.COLOR_RGB2BGR)
    greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    borderremoved = remove_borders(greyimg)
    return borderremoved

#AHI returner
def AHI_returner(text):
    splited_text = text.split()
    try:
        if '(AHI)' in splited_text:
            return float(splited_text[splited_text.index('(AHI)')+2][:-1])
        elif 'INDEX' in splited_text:
            return float(splited_text[splited_text.index('INDEX')+3][:-1])
        else:
            pass
    except:
        pass
    
#HN finder
def HN_returner(text):
    splited_text = text.split()
    try:
        if 'HN:' in splited_text:
            return splited_text[splited_text.index('HN:')+1]
        elif 'SN' in splited_text:
            return splited_text[splited_text.index('SN')-1]
        else:
            try:
                return int(splited_text[13])
            except:
                pass
    except:
        pass
    

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

#testing part 
test_pdf = '2021/2021.pdf'
text1, text2 = text_extracter(test_pdf)
AHI = AHI_returner(text1)
HN = HN_returner(text1)

#full optimum HN and AHI dataframe generator
