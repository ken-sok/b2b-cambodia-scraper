r'''
File: scraper-b2b-docker.py
Project: b2b-scraper
File Created: Tuesday, 9th June 2020 4:59:39 pm
Author: Chhaikheang Sok (chhaikheang.sok@gmail.com)
-----
Modified By: Chhaikheang Sok (chhaikheang.sok@gmail.com>)
-----
Copyright © 2020
'''

#library for webscraping
import requests

#method to download image of email 
import urllib.request

#library to parse site
from bs4 import BeautifulSoup

#library to dynamically scroll page 
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#libary to import to excel
import csv


#info source
catalogue_URL = input('add URL: ')

def get_full_catalog(catalogue_URL): 
    
    '''this function uses the browser driver in incognito mode, and without 
    opening a browser window to get full catalogue of yellow page companies(URL) according to
    area of business'''

    #copied from 
    #https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    #linux and windows have different local host addresses
    localhost = (input("please select localhost address of your computer:\nType '1' for 192.168.99.100\n" +
    "Type '2' for 127.0.0.1\nInput: "))

    while True: 
        if localhost == '1': 
            localhost = '192.168.99.100'
            driver = webdriver.Remote("http://"+localhost+":4444/wd/hub", DesiredCapabilities.CHROME)
            driver.get(catalogue_URL)
            break
        elif localhost == '2':
            localhost = '127.0.0.1'
            driver = webdriver.Remote("http://"+localhost+":4444/wd/hub", DesiredCapabilities.CHROME)
            driver.get(catalogue_URL)
            break
        else: 
            localhost = (input("please select localhost address of your computer:\nType '1' for 192.168.99.100\n" +
    "Type '2' for 127.0.0.1\nInput: "))

    
    #copied from 
    #https://stackoverflow.com/questions/51092362/selenium-clicking-to-next-page-until-on-last-page
    
    page_sources=[]
    print('scraping pages...\n')
    while True:
        
        #sometimes next is found inside pagination, sometimes not => use two xpath, one full, one shortened
        next_page_btn = driver.find_elements_by_xpath("/html/body/div[6]/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/div/div[3]/ul/li[@class = 'w2dc-inactive next']/a") 
        next_page_btn2 = driver.find_elements_by_xpath("//li[@class = 'w2dc-inactive next']/a") 
        page_sources.append(driver.page_source)
        if (len(next_page_btn2) < 1 and len(next_page_btn) < 1):
            print("No more pages left")
            break
        else:
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, '>'))).click()
            time.sleep(5)
            print(len(page_sources))
    
    driver.quit()
    
    return page_sources
            
def get_link(page, catalogue_links):

    '''this function takes in the downloaded page and 
    return the list of links to each company in the URL'''
    
    soup = BeautifulSoup(page, 'lxml')
    
    link_headers = soup.find_all("header", class_ = "w2dc-listing-header") 
    for link in link_headers: 
        
        link = link.find('a')['href']
        
        #to avoid duplicates
        if link not in catalogue_links: 

            catalogue_links.append(link) 
    


def check_one_company(URL, companies): 
    
    '''modify this to take in one page URL and collect all data on the company'''
    #return data from website
    page = requests.get(URL)
    

    #parse the page
    soup = BeautifulSoup(page.content, 'html.parser')

    #dictionary to store 1 company's details
    company = dict()
    
    #get company name
    name = soup.find("header", class_= "w2dc-listing-header").find("h1", itemprop= "name")
    company['name'] = name.get_text(strip=True)

    
    #location
    loc = soup.find("address", class_="w2dc-location")
    if loc != None: 
        loc = loc.get_text(strip=True)
        company['location'] = loc
        
    else: 
        company['location'] = ''

    
    
    #phone numbers
    numbers = soup.select("div.w2dc-field-output-block-6 > span.w2dc-field-content")
    company['phone_numbers'] = list()
    for number in numbers: 
        number = number.get_text(strip=True)
        company['phone_numbers'].append(number)
    
    #emails
    emails = soup.find_all("meta", itemprop="email")
    company['emails'] = list()
    for email in emails: 
        email = email['content']
        #remove spaces
        email = email.replace(" ", "")
        company['emails'].append(email)

    #website
    site = soup.find('a', itemprop="url")
    #print(site)
    if site != None: 
        company['website'] = site['href']
    else: 
        company['website'] = ''
    
    
    #append company dict to list 
    companies.append(company)

def get_info_all_comp(catalogue_URL): 

    '''main function to gather all information needed on companies in URL
    and export to excel'''

    #list of dictionaries to store all details of each company
    companies = list(dict())

    #get full catalogue from website
    catalogue = get_full_catalog(catalogue_URL)

    #get category name 
    category = get_cat(catalogue_URL)

    #list to store all individual yp of each companies
    catalogue_links = list()

    #add all links of companies to 'catalogue_links'
    for page in catalogue: 
        get_link(page, catalogue_links)
    
    print('getting details on page...\n')
    #browse each link of companies and note all details in 'companies'
    for link in catalogue_links:
        check_one_company(link, companies)

    #export to csv
    print("exporting to excel...")
    export_to_csv(companies, category)
    print("exported to excel")
    
    return companies

def get_cat(catalogue_URL):
    '''this function takes in the downloaded page and 
    return the category of the company on the URL'''
    #return data from website
    page = requests.get(catalogue_URL)
    
    #for later version
    #page.set_secure_cookie('key', value, secure=True, httponly=True)
    
    #parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    categories = soup.select("header.w2dc-page-header > h2")
    for category in categories:
        category = category.get_text()
        category = category.strip()
        print('Category: ' + category)
    return category

def export_to_csv(companies, category):
    
    export_path = r"/src/app/b2b-page-excel/"
  
    with open(export_path+category+".csv", "w", newline="", encoding="utf-8") as csv_file:
        cols = ["name","location","phone_numbers","emails","website"] 
        writer = csv.DictWriter(csv_file, fieldnames=cols)
        writer.writeheader()
        writer.writerows(companies)
    



#call main function
companies = get_info_all_comp(catalogue_URL)

