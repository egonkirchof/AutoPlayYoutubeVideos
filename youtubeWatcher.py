# Automatically watches a list of youtube videos for a random amount of time
# Use threads and Tor to emulate views from different users

from selenium import webdriver

def newBrowser():
    return webdriver.Firefox()
         
browser=None


from lxml import html
from lxml.cssselect import CSSSelector
import time
import random

def loadPage(page,browser=browser):
    browser.get(page)
    return browser.page_source

def loadPageTree(page_source):
    tree = html.document_fromstring(page_source)
    return tree


def pause():
    time.sleep(random.randint(30,59)+8*random.random())
    
videos = [ "BnMyRl1-FHw",        "8PEI8vl-AAQ",     "foR27m9-8xY",
        "mHQQYBqRHFk", "DnKKeztGHwU", "9aliKzvbOoY","1VO8VFc0GDs","PeknEnjnDnc"  ]
    
def pageFormat(video):
    return "https://www.youtube.com/watch?v="+video+"&autoplay=1"
import json
from urllib.request import urlopen

from threading import Thread,currentThread
t=[]

def keepGoing(t):
    return not getattr(t,"kill",False) if t else True
    
def doIt(max_time_in_minutes=20,max_times=None,max_errors=10):
    errors = 0
    t = currentThread()
    browser = newBrowser()
    n_videos = len(videos)
    if max_times is None: max_times = n_videos
    repeat_allowed = max_times>len(videos)
    times = 0
    chosen = []
    start = time.time()
    while keepGoing(t) and times<max_times:
        times += 1
        while keepGoing(t):
            r = random.randint(0,n_videos-1)
            if repeat_allowed or r not in chosen: break
        chosen.append(r)
        try:
            loadPage(pageFormat(videos[r]),browser)
        except:
            print("Error loading video ",videos[r])
            errors += 1
            if errors==max_errors: break
            continue
            
        browser.execute_script("return document.getElementById('movie_player').mute()")
        browser.execute_script("return document.getElementById('movie_player').playVideo()")
        watch_for = random.randint(1,max_time_in_minutes)
        print("Playing ",videos[r]," for ",watch_for," minutes.")
        watch_for = watch_for * 60
        while keepGoing(t) and watch_for>0:
            time.sleep(1)
            watch_for -= 1
    if not keepGoing(t): print("Thread interrupted: ",t) 
    if errors == max_errors: print("Too many errors.")       
    print("Execution time thread",t,":", time.time() - start)
    browser.close()


# In[37]:

def main(n_threads=10):
    for i in range(n_threads):
        tr = Thread(target=doIt)
        t.append(tr)
        tr.start()
        time.sleep(1)

# In[38]:

def checkThreads():
    for i,tr in enumerate(t):
        if not tr.isAlive():
            del(t[i])
        else:
            print(tr)



            
    


