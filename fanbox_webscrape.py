import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SCROLL_PAUSE_TIME = 0.5


# This function scrolls to the very bottom of webpages with "infinite" scroll/posts
# Code from https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
# Author: @Cuong Tran
def full_scroll(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def main():
    # Create the Firefox webdriver
    driver = webdriver.Firefox()
    # Tell the webdriver to access this page
    driver.get("")
    # Print out the title of the webpage to the console
    print(driver.title)

    # TO - UNCOMMENT: Temporarily disable login for now

    # This finds the path to the Login button through a hardcoded XPath and clicks on it
    login_button = driver.find_element_by_xpath("/html/body/div/div[4]/div[4]/button")
    login_button.click()

    # Fill out the login details using an external file
    f = open("./secret/secret.txt", "r")

    # Make sure that the file has the username on the 1st line and password on the 2nd
    username = f.readline().strip()
    password = f.readline().strip()

    f.close()

    # Fill in the login details
    login_username = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[1]/input")
    login_username.send_keys(username)
    login_password = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/div[1]/div[2]/input")
    login_password.send_keys(password)

    # Click "Login"
    login_button = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/form/button")
    login_button.click()

    # Give 5 second for all elements to load
    time.sleep(5)

    full_scroll(driver)

    # Get the html source from the browser driver (content is stored)
    html = driver.page_source

    # Create bs4 object
    soup = BeautifulSoup(html, "html.parser")

    all_urls = []
    post_urls = []

    # Find all 'a' (link) elements inside of a 'div' class
    for div1_tag in soup.find_all('div'):
        a_tag = div1_tag.find('a')
        
        if a_tag != None:
            # Remove all urls that do not contain '/posts'
            if "/posts" in a_tag.attrs['href']:
                all_urls.append(a_tag.attrs['href'])

    # Remove all duplicate urls from all_urls list
    for post in all_urls: 
        if post not in post_urls: 
            post_urls.append(post) 

    # Print out the list of post urls and the number of items in the lists
    # There should be 40 posts for my use case
    print(post_urls)
    print(len(post_urls))


    image_url = []
    clean_image_url = []

    for post in post_urls:
        # Opening a new tab in Firefox may not be possible now
        # https://stackoverflow.com/questions/28431765/open-web-in-new-tab-selenium-python
        driver.get("https://www.fanbox.cc/@izumi000" + post)

        full_scroll(driver)

        # Log the webpage title
        print(driver.title)

        time.sleep(2)

        # Store the newly loaded html to the system and the new temp_soup object
        html = driver.page_source
        temp_soup = BeautifulSoup(html, "html.parser")

        for div1_tag in temp_soup.find_all('div'):
            a_tag = div1_tag.find('a')
            
            if a_tag != None:
                if "download" in a_tag.attrs['href']:
                    print(a_tag.attrs['href'])
                    image_url.append(a_tag.attrs['href'])
   
    
    # Remove all duplicate urls from all_urls list
    for image in image_url: 
        if image not in clean_image_url: 
            clean_image_url.append(image) 

    print(clean_image_url)

    # Store all the urls in a file
    f = open("image_scrape.txt", "w")
    
    for url in clean_image_url:
        f.write(url)
        f.write("\n")
    
    f.close()
    driver.close()

main()

