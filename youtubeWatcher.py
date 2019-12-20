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

verbose = True

def startVideo(browser,thread,mute=False):
    """ 
        Click on the video (or use playVideo) to start it  
        You can only use playVideo() if the video is muted
        Otherwise, we must emulate a click on the video
        When it is chrome, sometimes it will start automatically.
        So we check if the video is running after we click it and we click it again, if needed.
        """
        
    if mute:           
        browser.execute_script("return document.getElementById('movie_player').mute()")
        browser.execute_script("return document.getElementById('movie_player').playVideo()") # only allowed if video muted
    else: 
        # click the video so it will start playing
        # sometimes the video starts playing automatically (chrome)
        # Todo: check for Ads
        
        initial_time = browser.execute_script("return document.getElementById('movie_player').getCurrentTime()")
        time.sleep(1)
        clicked = False
        while keepGoing(thread) and initial_time ==  browser.execute_script("return document.getElementById('movie_player').getCurrentTime()"):
            if verbose: print("clicking the video - ",thread.name if thread else "")
            clicked = True
            browser.find_element_by_id("movie_player").click()
            time.sleep(2)
        if verbose and not clicked: print("No need to click video - ",thread.name if thread else "")
     
        
def watchVideo(browser,thread,max_time_in_minutes,video_duration):
    video_duration = browser.execute_script("return document.getElementById('movie_player').getDuration()")  
    watch_for = random.randint(1,max_time_in_minutes)*60
    if watch_for>video_duration: watch_for = video_duration
    if verbose: print("Playing ",browser.title," for ",watch_for//60," minutes. (",thread.name if thread else "" ,")")    
    
    while keepGoing(thread) and not threadPaused(thread) and watch_for>0: # wait for watch_for minutes, unless thread is interrupted
        time.sleep(1)
        watch_for -= 1

def playVideo(video,browser,thread,max_time_in_minutes,mute=False):    
    """ 
    Play youtube video in browser for at most max_time_in_minutes minutes.
    Check to see if thread (t) is interrupted while playing.
    Set mute to True if you don't want to listen to the video."""
    
    try:
        loadPage(pageFormat(video),browser)
        time.sleep(10)
    except:
        if verbose: print("Error loading video ",video)
        return False  
    try:  
        startVideo(browser,thread,mute) 
        watchVideo(browser,thread,max_time_in_minutes)
    except:
        if verbose: print("Error in video page:",video)
        return False
    
    return True
        
#--------------------- play videos in loop, thread function
    


def doIt(max_time_in_minutes=20,max_times=None,max_errors=10,browser_type="random"):
    """
    Plays videos from "videos" until it is interrupted or max_times is reached
    Set max_time_in_minutes for the maximun amount of minutes to play the video
    """
    if verbose: print("Do it params:",max_time_in_minutes,max_times,max_errors,browser_type)
    
    #---- create a browser
    if use_tor:
        if verbose: print("Creating browser with Tor")
        browser = newBrowser(browser_type,proxy_port=tor_port)
    else:
        if verbose: print("Creating browser")
        browser = newBrowser()
    time.sleep(5) 
     
    #--- init vars
    thr = currentThread()
    thr.browser = browser
    errors = 0   
    n_videos = len(videos)
    if max_times is None: max_times = n_videos
    repeat_allowed = max_times>len(videos)
    times = 0
    chosen = []
    start = time.time()
    
    #---- main loop
    while keepGoing(thr) and times<max_times:
        #choose next video to play
        while keepGoing(thr): 
            r = random.randint(0,n_videos-1)
            if repeat_allowed or r not in chosen: break
        chosen.append(r)
        # play it
        if playVideo(videos[r],browser,thr,max_time_in_minutes): 
            times += 1
        else:
            errors += 1
            if errors==max_errors: break    
        
    #---exiting thread        
    if verbose and not keepGoing(thr): print("Thread interrupted: ",thr.name) 
    if verbose and errors == max_errors: print("Too many errors, thread ", thr.name,".")       
    if verbose: print("Thread ended. Execution time ",thr.name,":", time.time() - start)
    browser.close()

#·---------------------------
if __name__ == "__main__":
    # createThread is the function you have to call
    #to do: allow passing parameters to doIt
    #createThreads(doIt,10,False)
    threads = getListOfThreads()
    pass

#



            
    


