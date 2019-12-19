#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:28:58 2019

@author: egon
"""

from stem import Signal
from stem.control import Controller
from threading import currentThread
from threadFunctions import t,keepGoing,threadPaused
import time

tor_thread = None
tor_port = 9090 # default is 9050
tor_ctrl_port = 9091 # default is 9051 I qm uwint 9091
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
    while keepGoing(this):
        print("Changing Tor IP...")
        # pause all threads
        for tr in t:
            if tr is not this: tr.pause = True
        n_threads = len(t)-1 # tor thread is included in t
        paused_threads = 0
        print("Waiting for threads to pause...")
        while keepGoing(this) and (paused_threads < n_threads):
            paused_threads = 0
            for tr in t:
                if (tr is not this and threadPaused(tr)
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
        print(this,keepGoing(this))
        while keepGoing(this) and (time_to_wait>0):
            time_to_wait -= 1
    print("Tor thread killed.")
        