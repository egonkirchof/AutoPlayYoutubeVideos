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

def keepGoing(tr):
    # check if thread was interrupted (kill attribute was set to True)
    return not getattr(tr,"kill",False) if tr else True

def threadPaused(tr):
    # check if thread was paused ( pause = True ) 
    return getattr(tr,"pause",False) if tr else False
        
    
# Create multiple threads of execution
# It is a very basic thread pool 
# I am creating my own functions to stop and pause the threads
    
def createThreads(target_function,n_threads=10,use_tor=True):
    
    # Not using chegTorIp anymore. Too much unnecessary complexity
    """
    if torFunctions.tor_thread is None and use_tor: #only creates Tor thread once
        print("Creating Tor controller thread.")
        torFunctions.tor_thread = Thread(target=torFunctions.changeTorIp)
        t.append(torFunctions.tor_thread)
        torFunctions.tor_thread.start()
        time.sleep(10) # wait for IP to change before opening threads
    """
    torFunctions.use_tor = use_tor
    
    for i in range(n_threads):
        tr = Thread(target=target_function) #should be doIt
        t.append(tr)
        tr.start()
        time.sleep(1)
            
def killThreads(t=t,kill_tor=True):
    global tor_thread
    for tr in t:
        tr.kill = True
    if tor_thread and kill_tor:
        while tor_thread.isAlive(): 
            tor_thread.kill = True
            time.sleep(1)
        tor_thread = None
        
def pauseThreads(t,pause_it=True):
    for tr in t:
        t.pause = pause_it
        
def checkThreads():
    global tor_thread
    for i,tr in enumerate(t):
        if not tr.isAlive():
            del(t[i])
        else:
            print(tr)
    if tor_thread and not tor_thread.isAlive():
        tor_thread = None
        