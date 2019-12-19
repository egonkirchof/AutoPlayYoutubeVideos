# Automatically watches a list of youtube videos for a random amount of time
# Use threads and Tor to emulate views from different users

import time
import random
from threading import currentThread

from browserFunctions import newBrowser,loadPage,pageFormat 
from threadFunctions import getListOfThreads,keepGoing,threadPaused,createThreads,killThreads,pauseThreads,checkThreads
from torFunctions import use_tor,tor_port

#----------------- play video function

# list of videos to play    
videos = [ "BnMyRl1-FHw", "8PEI8vl-AAQ", "foR27m9-8xY",
        "mHQQYBqRHFk", "DnKKeztGHwU", "9aliKzvbOoY","1VO8VFc0GDs",
        "PeknEnjnDnc"  ]
    

def playVideo(video,browser,t,max_time_in_minutes,mute=False):    
    """ 
    Play youtube video in browser for at most max_time_in_minutes minutes.
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
        video_duration = browser.execute_script("return document.getElementById('movie_player').getDuration()")
    except:
        print("Error in video page:",video)
        return False
    
    watch_for = random.randint(1,max_time_in_minutes)*60
    if watch_for>video_duration: watch_for = video_duration
    print("Playing ",video," for ",watch_for//60," minutes. (",t.name,")")    
    
    while keepGoing(t) and not threadPaused(t) and watch_for>0: # wait for watch_for minutes, unless thread is interrupted
        time.sleep(1)
        watch_for -= 1
    return True
            
#--------------------- play videos in loop, thread function
def doIt(max_time_in_minutes=20,max_times=None,max_errors=10):
    """
    Plays videos from "videos" until it is interrupted or max_times is reached
    Set max_time_in_minutes for the maximun amount of minutes to play the video
    """
    errors = 0
    tr = currentThread()
    if use_tor:
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
    while keepGoing(tr) and times<max_times:
        
        while keepGoing(tr): #choose next video to play
            r = random.randint(0,n_videos-1)
            if repeat_allowed or r not in chosen: break
        chosen.append(r)
        
        if playVideo(videos[r],browser,tr,max_time_in_minutes): # play it
            times += 1
        else:
            errors += 1
            if errors==max_errors: break    
        
        # if using Tor, pause threads to change IP when necessary
        # I am not using this anymore
        tr.paused = False
        while keepGoing(tr) and threadPaused(tr):
            if not tr.paused: print("Thread ",tr.name," paused.")
            tr.paused = True
            time.sleep(1)
        if tr.paused: print("Thread ",tr.name," resumed.")
        tr.paused = False
            
    if not keepGoing(tr): print("Thread interrupted: ",tr.name) 
    if errors == max_errors: print("Too many errors, thread ", tr.name,".")       
    print("Execution time thread",tr.name,":", time.time() - start)
    browser.close()
    
if __name__ == "__main__":
    # createThread is the function you have to call
    #to do: allow passing parameters to doIt
    #createThreads(doIt,10,False)
    threads = getListOfThreads()
    pass

#



            
    


