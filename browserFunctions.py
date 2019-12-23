#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:26:44 2019

@author: egon
"""

#-------------- basic browser functions
from selenium import webdriver
import random

def newBrowser(browser_type="random",mute=True,proxy_port=None,proxy_type="network.proxy.socks"):
    choices = ["firefox","chrome"] # since I am using Linux I didn't add Edge
    if browser_type =="random":
        choice = choices[random.randint(0,len(choices)-1)]
    elif browser_type in choices:
        choice = browser_type
    else:
        choice = "firefox"
    
    print(choice)
    if choice == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        if mute: chrome_options.add_argument("--mute-audio")
        if proxy_port:
            chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:' + str(proxy_port))
        return webdriver.Chrome(chrome_options=chrome_options)
    
    if choice == "Edge": # I don't use it, I am not running Windows
        return webdriver.Edge() # must have MicrosoftWebDriver.exe in path
        
    # Firefox
    profile = webdriver.FirefoxProfile()
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
 
    if proxy_port is not None:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference(proxy_type, "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", proxy_port)
    if mute: 
        profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile,firefox_options=options)
    
def loadPage(page,browser):
    if browser is None: return None
    browser.get(page)
    return browser.page_source

def pageFormat(video):
    return "https://www.youtube.com/watch?v="+video

