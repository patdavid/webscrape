#!/usr/bin/python

from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import re
import youtube_dl

#urlfile = "Superstore-urls.txt"
#
# print "Setting up text file for logging urls..."
# if not os.path.exists(urlfile):
#     print urlfile, " doesn't exist, creating..."
#     file(urlfile, 'w').close()
#     print "Created."
# else:
#     print urlfile, " already exists."

#success = False

def my_hook(d):
    if d['status'] == 'finished':
        print "Success!"
        print "Done downloading..."
        print "-------------------"
        #global success 
        #success = True

driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
driver.get('http://www.nbc.com/superstore/episodes')
#driver.get('http://www.nbc.com/grimm/video')
#driver.get('http://www.nbc.com/saturday-night-live/video')

#print driver.find_elements(By.XPATH, "//div[@class='video-season']/text()")
#videoseason = driver.find_elements_by_css_selector('div.video-season')

# nextbutton = driver.find_element_by_xpath("//a[@class='button btn_next nmc_btn_next']")
# print "nextbutton class: ", nextbutton.get_attribute("class")
# 
# while True:
#     for test in driver.find_elements_by_xpath("//div[@data-is-full-episode='true']"):
#         anchor = test.find_element_by_class_name('mpx-thumbnail-link')
#         #print anchor.get_attribute('href')
#         seasonep = test.find_element_by_css_selector('div.video-season')
#         #print "Season/Ep: ", seasonep.text
#         if seasonep.text:
#             print "Season/Ep: ", seasonep.text
#             print anchor.get_attribute('href')
# 
#     if "navigation-disabled" in nextbutton.get_attribute("class"):
#         break
#     else:
#         nextbutton.click()
#         time.sleep(2)

#for episode in driver.find_elements_by_css_selector('a.card__watch-episode'):
for show in driver.find_elements_by_css_selector('div.card__meta'):
    #print "show.text: ", show.text
    title_raw = show.find_element_by_css_selector('a.card__title-link')
    title = title_raw.text
    url = title_raw.get_attribute('href')

    seep = show.find_element_by_css_selector('div.card__description > span.card__description__part')

    int_se = [int(s) for s in re.findall(r'\d+', seep.text)]
    season_int = int_se[0]
    episode_int = int_se[1]

    # Offset might be needed - so split out the season/episode
    # into ints so we can offset as needed.
    #print "Season: %d Episode: %d" % (season_int, episode_int)
    if season_int == 2:
        episode_int -= 1
        if episode_int == 0:
            season_int = 0
            episode_int = 1

    #print "## season_int = ", season_int
    parsed_seep = "S%d E%d" % (season_int, episode_int)

    #seasonep = re.sub(r"[Ss](\d{1}) ", "S0\\1", seep.text)
    seasonep = re.sub(r"[Ss](\d{1}) ", "S0\\1", parsed_seep)
    seasonep = re.sub(r"[Ee](\d{1})$", "E0\\1", seasonep)
    seasonep = seasonep.replace(" ", "")

    print "------------------"
    print "title: %s" % title
    print "Season/Episode: %s" % seasonep
    print "url: %s" % url

    filename = "Superstore - "+ seasonep +" - "+ title
    print "filename: %s " % filename

    #inurl = False 

    #print "## Getting ready to pass params to ydl..."
    #print "season: %d, episode: %d" % (season_int, episode_int)
    ydl_opts = {
            'outtmpl': "/home/pat/Downloads/complete/"+filename +".%(ext)s",
            'download_archive': 'ydl-archive-superstore.txt',
            'progress_hooks': [my_hook]
            }
    with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
        result = ydl.extract_info( url )
#    print "Testing success..."
#    if success:
#        print "Success!"
#    else:
#        print "Uh oh. Didn't download?  Already exists?"


#    with open(urlfile, 'a+b') as thefile:
#        for line in thefile:
#            print "Checking if url in line..."
#            if url in line:
#                inurl = True
#                print "url in line: ", inurl
#                break
#            else:
#                print "url in line: ", inurl
#
#        if not inurl:
#            print "## Getting ready to pass params to ydl"
#            print "season: %d, episode: %d" % (season_int, episode_int)
#            ydl_opts = {
#                    'outtmpl': filename +".%(ext)s",
#                    'download_archive': 'ydl-archive.txt',
#                    'progress_hooks': [my_hook]
#                    }
#            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#                result = ydl.extract_info( url )
#            print "Testing success..."
#            if success:
#                print "Success!"
#                print>>thefile, url
#            else:
#                print "Uh oh.  Didn't download?"

