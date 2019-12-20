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

def threadPaused(tr):
    # check if thread was paused ( pause = True ) 
    return getattr(tr,"pause",False) if tr else False
        
    
# Create multiple threads of execution
# It is a very basic thread pool 
# I am creating my own functions to stop and pause the threads
    
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
    
def pauseThreads(threads_to_pause,pause_it=True):
    for tr in threads_to_pause:
        t.pause = pause_it
        
def checkThreads(t):
    for i,tr in enumerate(t):
        if not tr.isAlive():
            del(t[i])
        else:
            print(tr)
 
    