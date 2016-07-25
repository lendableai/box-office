from selenium import webdriver
import pandas as pd
import numpy as np
import urllib2
from bs4 import BeautifulSoup
# import logging
# logging.basicConfig(level=logging.DEBUG)
import string
import cPickle as pickle
from fake_useragent import UserAgent
from pyvirtualdisplay import Display
from unidecode import unidecode
from xvfbwrapper import Xvfb
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

# vdisplay = Xvfb
# vdisplay.start()

# Use PhantomJS and set window
# driver = webdriver.PhantomJS()
# driver.set_window_size(1120, 550)
# Run initially to keep display from opening up
def extract_links(movie_name):
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    path_to_chromedriver = '/Users/rodrigogonzalez/Dropbox/Galvanize/box-office/selenium/chromedriver'

    # Set option for chromebrowser
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("user-agent={}".format(UserAgent().random))


    # change path as needed to where web driver lives
    browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=chrome_options)

    # Go to page
    url = 'https://www.rottentomatoes.com/'
    browser.get(url)

    # For rottentomatoes
    # name = 'search'
    # id = 'search-term'
    try:
        # Clear the search field, and input the search term
        browser.find_element_by_id('search-term').clear()
        browser.find_element_by_id('search-term').send_keys(movie_name)

        # Click search
        browser.find_element_by_xpath('//*[@id="header_brand_column"]/div[1]/form/div/div/div[1]/button').click()

        # First Link
        # //*[@id="movie_results_ul"]/li[1]/div/div/a
        # or //*[@id="movie_results_ul"]/li/div/div/a
        # Figure out how to use contains term
        # dyn_frame = browser.find_element_by_xpath('//*[contains(@id, "movie_results_ul")]')

        # Find the first search result (default)


        dyn_frame = browser.find_element_by_xpath('//*[@id="movie_results_ul"]/li/div/div/a')

        linkname = dyn_frame.get_attribute('href')

        # Go to the movie URL
        browser.get(linkname)
        dyn_frame2 = browser.find_element_by_xpath('//*[@id="criticHeaders"]/a[2]').click()

        # Get all reviews links in id = "content"

        dyn_frame3 = browser.find_elements_by_xpath('//*[contains(@rel, "nofollow")]')

        links = []

        for link in dyn_frame3:
            links.append(unidecode(link.get_attribute('href')))
            print unidecode(link.get_attribute('href'))

        pd.DataFrame(links).to_csv('../critic_links/'+  +'.txt', sep='\t', index=False)

    except Exception, e:
        empty_keys.append(movie_name)
        logging.exception(e)# look at critic names later

    browser.quit() #closes browser

if __name__ == '__main__':
    empty_keys = []
    df = pd.read_csv('../html_postgres/movie_revs.csv')
    for title in df['title2']:
        extract_links(title)
        # empty_keys.append(title)
    np.savetxt("empty_keys.csv", empty_keys, delimiter=",", fmt='%s')
