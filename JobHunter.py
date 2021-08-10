# -*- coding: utf-8 -*-
"""
Web Scraping Automation Project : 
    
In this project I grab all the job posts from the last 24 hours from linkedin using selenium library
by inserting job location and job title, and saves the data in excel using panda library 

Created on Tue Jul 20 21:53:02 2021
@author: Ido Kadosh
"""
from datetime import date
from pynput.keyboard import Key, Controller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager



#Insert my credentials in order to login             
def loginLinkedin():
    file = open('Credentials.txt')
    fileContent = file.readlines()
    username = fileContent[0]
    password = fileContent[1]
    elementID = driver.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = driver.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

#Insert the job title and the job location in order to get results     
def findJobs(jobTitle, jobLocation):
    try:
        driver.find_element_by_xpath('//html//body//div[6]//header//div//nav//ul//li[3]//a').click()
        sleep(1)
        elementID = driver.find_element_by_xpath("/html/body/div[6]/header/div/div/div/div[2]/div[1]/div/div[2]/input[1]")
        elementID.clear()
        sleep(1)
        elementID.send_keys(jobTitle)
        elementID1 = driver.find_element_by_xpath("/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div[2]/input[1]")
        elementID1.clear()
        elementID1.send_keys(jobLocation)
        sleep(1)
        keyboard = Controller()
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    except:
        print("page not found")#incase there was a problem while loading the linkedin page 
        
#Brute Force solution in order to set search prefrences using tabs and space keys.
def setSearchPrefrences ():
    keyboard = Controller()
    driver.find_element_by_xpath("/html/body/div[6]/header/div/div/div/div[2]/button[1]").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/section/div/div/div/div/div/button").click()
    sleep(1)
    for i in range(0,8):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        if i == 7: 
            keyboard.press(Key.space)
            keyboard.release(Key.space)
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/div/button[2]/span").click()
            
    
    
def JobHunterMain(driver,Title,Location):    
    url = "https://www.linkedin.com/uas/login"
    driver.get(url)
    loginLinkedin()
    findJobs(Title, Location)
    sleep(1)
    setSearchPrefrences()
    action = ActionChains(driver)
    sleep(1)
    no_of_jobs = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div/div/section[1]/div/header/div[1]/small").get_attribute('innerText')
    num = [int(s) for s in no_of_jobs.split() if s.isdigit()]
    numOfJobs = num[0]
    
    job_title = []
    company_name = []
    location = []
    datePosted = []
    jodDescription = []
    job_link = []


    #Get the job posts necessary data from linkedin
    for i in range(0,numOfJobs):    
        #Display full data about the jobs             
        job_click_path = '/html/body/div[6]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[' + str(i+1) +']'
        try:
            job_click = driver.find_element_by_xpath(job_click_path).click()
        except: 
            continue
        
        #Get job title 
        try: 
            jobTitle = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/a/h2").get_attribute('innerText')
            job_title.append(jobTitle)
        except:
            job_title.append("N/A")
        
        #Get company name
        try:     
            companyName = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]/a").get_attribute('innerText')
            company_name.append(companyName)
        except:
            company_name.append("N/A")
            
        #Get job location
        try:
            jobLocation = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]").get_attribute('innerText')
            location.append(jobLocation)
        except:
            location.append("N/A")
            
        #Update today's date 
        myDate = date.today()
        datePosted.append(myDate)
        
        #Get job description 
        try:
            jd = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div[3]/div/div/section[2]/div/div/div[1]/div/div[2]").get_attribute('innerText')
            jodDescription.append(jd)
        except:
            jodDescription.append("N/A")
        #Get job link 
        try:
            jobLink = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[' + str(i+1) +']/div/div/div[1]/div[1]/a').get_attribute('href')
            job_link.append(jobLink) 
        except:
            job_link.append("N/A")
    ############ End Loop ############
    
    
    #### Create DataFrame using panda #### 
    job_data = pd.DataFrame({
    'Date': datePosted,
    'Company': company_name,
    'Title': job_title,
    'Location': location,
    'Description': jodDescription,
    'Link': job_link
    })
    # cleaning description column
    job_data['Description'] = job_data['Description'].str.replace('\n',' ')
    
    #Export data frame into excel file    
    job_data.to_excel('Jobs.xlsx') 
    
    driver.close()
    

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
# driver.implicitly_wait(5)
JobHunterMain(driver,'Junior','Israel')#update job title and job location 




    
