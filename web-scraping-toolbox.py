###############################################################################
###############################################################################
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:06:22 2019

@author: Timo Schnepf
"""

### This code provides building blocks for a web-scraping script in python3.
### It is organized in three parts:

### I) Getting the inner HTML code of a webpage
### Ia) where innerHTML = frontEnd
### Ib) where innerHTML != frontEnd, i.e. JavaScript, with Selenium

### II) Navigating within pages with Selenium

### III) Getting data from 
### IIIa) tables or 
### IIIb) by class names


###############################################################################
### Required libraries

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import requests
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###############################################################################

###############################################################################
#### Ia) Getting the inner HTML code of a webpage where innerHTML = frontEnd
###############################################################################

url = 'MYURLHERE'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')


###############################################################################
#### Ib) Getting the inner HTML code of a webpage where innerHTML != frontEnd, 
### 	 i.e. JavaScript with Selenium
###############################################################################

# next two lines for headless mode (script runs in background)
options = Options() 
options.headless = True

driver = webdriver.Firefox(options=options) #replace with .Firefox() for automated screen mode; with the driver/browser of your choice
driver.get('MYURLHERE') #navigate to the page

innerHTML = driver.execute_script("return document.body.innerHTML")

soup = BeautifulSoup(innerHTML, 'lxml')




###############################################################################
### II) Navigating within pages with Selenium
###############################################################################

# Waiting commands
# webdriver waits 15 seconds
wait = WebDriverWait(driver, 15)
# alternative
time.sleep(15)   # requires time library

# webdriver waits until "X" element is loaded 
wait.until(EC.presence_of_element_located((By.ID, "X")))


# Click on things
# Click on element "X"
nextpage = driver.find_element_by_id("X")
nextpage.click()


# Choose element X from dropdown list Y

el = driver.find_element_by_id('Y')
for option in el.find_elements_by_tag_name('Y'):
    if option.text == 'X':
        option.click()
        break
        
        
# Automated ScrollDown

	# scroll infinite page 60 seconds (e.g. facebook)
timeout = time.time() + 60   #  scrolls 60 seconds from now
SCROLL_PAUSE_TIME = 2   # 2 seconds for reloading content

	# Gets scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height or time.time() > timeout:
        break
    last_height = new_height 
    

###############################################################################
### IIIa) Getting data from tables
###############################################################################

	# find the name of the table within the HTML code, here "tbody"
datatable = []
table = soup.find("tbody", {"id": "posts"})

rows = table.findAll('tr')	# find row elements, usually "tr"
for row in rows:
    cols = row.findAll('td')	# find column elements usually "td"
    cols = [ele.text.strip() for ele in cols]
    datatable.append([ele for ele in cols if ele])
    
helpdf = pd.DataFrame(datatable)
    
	# remove unwanted columns (here: 0, 1 and 3)
df = []
df = helpdf[[0, 1, 3]] 
	# adding information to each cell in column 0, here e.g. "Posted on"
df[0] = 'Posted on ' + df[0].astype(str)    # add "Posted on" in each cell of further information

	# Renames table headers (variable names), here examples "Title", "Deadline" and "Further Information"
df = df.rename(columns={0: 'Title', 1: 'Deadline', 0: 'Further Information'})
	# adds a column with the source
df['Source'] = 'MYURLHERE'

	# export
df.to_excel("MYDATA.xlsx", index=False)   # no Index
driver.close()


###############################################################################
### IIIb) Getting data by class names
###############################################################################


### Getting data from class "A"/"B"/"C" within the "R" elements

titles =[]
deadlines = []
infos = []

for i in soup.findAll("R", {"class": "A"}):
    ttl=i.getText()
    ttl = ttl.replace('this_text_needs_to_be_removed','') # cleans text, e.g. "\n" for return-bars
    titles.append(ttl)
	    
for j in soup.findAll("R", {"class": "B"}):
    deadline=j.getText()
    deadlines.append(deadline)
    
for k in soup.findAll("R", {"class": "C"}):
    info=k.getText()
    infos.append(info)

    # write the data into a dataframe/excel file
    
data={'Title': titles, 'Deadline': deadlines, 'Further Information': infos}
df=pd.DataFrame(data=data)
df.to_excel("MYDATA.xlsx", index=False)   # no index

###############################################################################
###############################################################################