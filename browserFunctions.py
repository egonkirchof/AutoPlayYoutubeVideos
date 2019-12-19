#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:26:44 2019

@author: egon
"""

#-------------- basic browser functions
from selenium import webdriver
        
def newBrowser(mute=True,proxy_port=None,proxy_type="network.proxy.socks"):
    profile = webdriver.FirefoxProfile()
    if proxy_port is not None:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference(proxy_type, "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", proxy_port)
    if mute: 
        profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile)
    
def loadPage(page,browser):
    if browser is None: return None
    browser.get(page)
    return browser.page_source

def pageFormat(video):
    return "https://www.youtube.com/watch?v="+video+"&autoplay=1"

