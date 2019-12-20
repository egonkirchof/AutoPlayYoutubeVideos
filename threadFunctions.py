#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:28:00 2019

@author: egon
"""

#-------------------- Threads 

from threading import Thread
import torFunctions  
import time

t=[] # list of threads

def getListOfThreads():
    return t

def keepGoing(tr):
    # check if thread was interrupted (kill attribute was set to True)
    return not getattr(tr,"kill",False) if tr else True
   
# Create multiple threads of execution
    
def createThreads(target_function,params={},n_threads=10,use_tor=True):

    torFunctions.use_tor = use_tor
    for i in range(n_threads):
        tr = Thread(target=target_function,args=params) #should be doIt
        t.append(tr)
        tr.start()
        time.sleep(1)
            
def killThreads(threads_to_kill=t,kill_tor=True):
    for tr in threads_to_kill:
        tr.kill = True

def checkThreads(t):
    for i,tr in enumerate(t):
        if not tr.isAlive():
            del(t[i])
        else:
            print(tr)
 
    