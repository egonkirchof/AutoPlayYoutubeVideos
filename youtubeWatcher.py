# Automatically watches a list of youtube videos for a random amount of time
# Use threads and Tor to emulate views from different users

from selenium import webdriver
import time
import random

#-------------- basic browser functions
browser=None

        
def newBrowser(mute=True,proxy_port=None,proxy_type="network.proxy.socks"):
    profile = webdriver.FirefoxProfile()
    if proxy_port is not None:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference(proxy_type, "127.0.0.1")
        profile.set_preference("network.proxy.socks_port", proxy_port)
    if mute: 
        profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile)
    
def loadPage(page,browser=browser):
    browser.get(page)
    return browser.page_source

# list of videos to play    
videos = [ "BnMyRl1-FHw",        "8PEI8vl-AAQ",     "foR27m9-8xY",
        "mHQQYBqRHFk", "DnKKeztGHwU", "9aliKzvbOoY","1VO8VFc0GDs","PeknEnjnDnc"  ]
    
def pageFormat(video):
    return "https://www.youtube.com/watch?v="+video+"&autoplay=1"

#----------------- play video function

def playVideo(video,browser,t,max_time_in_minutes,mute=False):    
    """ 
    Play video in browser for at most max_time_in_minutes minutes.
    Check to see if thread (t) is interrupted while playing.
    Set mute to True if you don't want to listen to the video."""
    
    try:
        loadPage(pageFormat(video),browser)
    except:
        print("Error loading video ",video)
        return False  
    try:
        if mute:           
            browser.execute_script("return document.getElementById('movie_player').mute()")
            browser.execute_script("return document.getElementById('movie_player').playVideo()")
        else:
            browser.find_element_by_id("movie_player").click()
        
        # decide for how long to play the video    
        video_duration = browser.execute_script("return document.getElementById('movie_player').getDuration()")
    except:
        print("Error in video page:",video)
        return False
    
    watch_for = random.randint(1,max_time_in_minutes)
    print("Playing ",video," for ",watch_for," minutes.")    
    watch_for = watch_for * 60
    if watch_for>video_duration: watch_for = video_duration
    
    while keepGoing(t) and watch_for>0: # wait for watch_for minutes, unless thread is interrupted
        time.sleep(1)
        watch_for -= 1
    return True
            
#--------------------- play videos in loop function
    
def doIt(max_time_in_minutes=20,max_times=None,max_errors=10):
    """
    Plays videos from "videos" until it is interrupted or max_times is reached
    Set max_time_in_minutes for the maximun amount of minutes to play the video
    """
    errors = 0
    t = currentThread()
    if tor_thread:
        print("Creating browser with Tor")
        browser = newBrowser(proxy_port=tor_port)
    else:
        print("Creating browser")
        browser = newBrowser()
    n_videos = len(videos)
    if max_times is None: max_times = n_videos
    repeat_allowed = max_times>len(videos)
    times = 0
    chosen = []
    start = time.time()
    # main loop
    while keepGoing(t) and times<max_times:
        times += 1
        while keepGoing(t): #choose next video to play
            r = random.randint(0,n_videos-1)
            if repeat_allowed or r not in chosen: break
        chosen.append(r)
        if playVideo(videos[r],browser,t,max_time_in_minutes): # play it
            pass
        else:
            errors += 1
            if errors==max_errors: break    
        # if using Tor, pause threads to change IP
        t.paused = False
        while keepGoing(t) and threadPaused(t):
            if not t.paused: print("Thread ",t," paused.")
            t.paused = True
            time.sleep(1)
        if t.paused: print("Thread ",t," resumed.")
        t.paused = False
            
    if not keepGoing(t): print("Thread interrupted: ",t) 
    if errors == max_errors: print("Too many errors.")       
    print("Execution time thread",t,":", time.time() - start)
    browser.close()


#-------------------- Threads and Tor
from threading import Thread,currentThread
from stem import Signal
from stem.control import Controller

tor_thread = None
tor_port = 9090 # default is 9050
tor_ctrl_port = 9091 # default is 9051 I qm uwint 9091

def renew_connection(port=tor_ctrl_port): # for use with Tor
    with Controller.from_port(port = port) as controller:
        controller.authenticate(password = 'my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()
        
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
                if (tr is not this and getattr(tr,"paused",False)
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
        
def createThreads(n_threads=10,use_tor=True):
    global tor_thread
    if tor_thread is None and use_tor: #only creates Tor thread once
        print("Creating Tor controller thread.")
        tor_thread = Thread(target=changeTorIp)
        t.append(tor_thread)
        tor_thread.start()
        time.sleep(10) # wait for IP to change before opening threads
        
    for i in range(n_threads):
        tr = Thread(target=doIt)
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
        



            
    


