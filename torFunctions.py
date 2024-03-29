#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:28:58 2019

@author: egon
"""

from stem import Signal
from stem.control import Controller
from threading import currentThread
import threadFunctions 
import time

tor_thread = None
tor_port = 9050 # default port. 
tor_ctrl_port = 9051 # 
use_tor = False

def renew_connection(port=tor_ctrl_port): # for use with Tor
    with Controller.from_port(port = port) as controller:
        controller.authenticate(password = 'my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()
    
# I won't be using this function because 
# Tor changes the IP from time to time automatically
# This function adds too much complexity to the Threads
def changeTorIp(interval=30):
    this = currentThread()
    t = threadFunctions.getListOfThreads()
    while threadFunctions.keepGoing(this):
        print("Changing Tor IP...")
        # pause all threads
        for tr in t:
            if tr is not this: tr.pause = True
        n_threads = len(t)-1 # tor thread is included in t
        paused_threads = 0
        print("Waiting for threads to pause...")
        while threadFunctions.keepGoing(this) and (paused_threads < n_threads):
            paused_threads = 0
            for tr in t:
                if (tr is not this and threadFunctions.threadPaused(tr)
                   ) or not tr.is_alive():
                    paused_threads += 1
            time.sleep(1)
        print("Threads paused.")
        # change IP        
        renew_connection(tor_ctrl_port) # I am using 9091, default is 9051
        time.sleep(10) # time for new connection to be ready 
        # unpause all threads
        for tr in t:
            if tr is not this: tr.pause = False
        # sleep 
        print("Done changing Tor Ip.")
        time_to_wait = interval*60
        print("Next Tor IP in ",time_to_wait," seconds.")
        print(this,threadFunctions.keepGoing(this))
        while threadFunctions.keepGoing(this) and (time_to_wait>0):
            time_to_wait -= 1
    print("Tor thread killed.")
        