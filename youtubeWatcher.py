# Automatically watches a list of youtube videos for a random amount of time
# Use threads and Tor to emulate views from different users

from selenium import webdriver
import time
import random

browser=None

def newBrowser(mute=True):
    profile = webdriver.FirefoxProfile()
    if mute: profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile)
    
def loadPage(page,browser=browser):
    browser.get(page)
    return browser.page_source

# list of videos to play    
videos = [ "BnMyRl1-FHw",        "8PEI8vl-AAQ",     "foR27m9-8xY",
        "mHQQYBqRHFk", "DnKKeztGHwU", "9aliKzvbOoY","1VO8VFc0GDs","PeknEnjnDnc"  ]
    
def pageFormat(video):
    return "https://www.youtube.com/watch?v="+video+"&autoplay=1"

from threading import Thread,currentThread
t=[] # list of threads

def keepGoing(t):
    # check if thread was interrupted (kill attribute was set to True)
    return not getattr(t,"kill",False) if t else True
    

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
    if mute:           
        browser.execute_script("return document.getElementById('movie_player').mute()")
        browser.execute_script("return document.getElementById('movie_player').playVideo()")
    else:
        browser.find_element_by_id("movie_player").click()
        
    # decide for how long to play the video    
    video_duration = browser.execute_script("return document.getElementById('movie_player').getDuration()")
    watch_for = random.randint(1,max_time_in_minutes)
    print("Playing ",video," for ",watch_for," minutes.")
    watch_for = watch_for * 60
    if watch_for>video_duration: watch_for = video_duration
    
    while keepGoing(t) and watch_for>0: # wait for watch_for minutes, unless thread is interrupted
        time.sleep(1)
        watch_for -= 1
    return True
            
def doIt(max_time_in_minutes=20,max_times=None,max_errors=10):
    """
    Plays videos from "videos" until it is interrupted or max_times is reached
    Set max_time_in_minutes for the maximun amount of minutes to play the video
    """

    errors = 0
    t = currentThread()
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
            
    if not keepGoing(t): print("Thread interrupted: ",t) 
    if errors == max_errors: print("Too many errors.")       
    print("Execution time thread",t,":", time.time() - start)
    browser.close()


# Create multiple threads of execution
def main(n_threads=10):
    for i in range(n_threads):
        tr = Thread(target=doIt)
        t.append(tr)
        tr.start()
        time.sleep(1)

def checkThreads():
    for i,tr in enumerate(t):
        if not tr.isAlive():
            del(t[i])
        else:
            print(tr)



            
    


