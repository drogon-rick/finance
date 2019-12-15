# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 21:54:11 2019

@author: JOE
"""
import sys

for x in sys.path:
    ix=x.find('site-packages')
    if( ix>=0 and x[ix:]=='site-packages'):
      sitepath=x;
      break;
sitepath=sitepath+"\\WindPy.pth"
pathfile=open(sitepath)
dllpath=pathfile.readlines();
pathfile.close();