# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:11:27 2021

@author: fdezdayan
"""

import os
import time
import csv
import shutil
import random
import urllib
import getpass
import unittest
import pandas as pd
from datetime import datetime
from selenium import webdriver
from time import gmtime, strftime
from collections import OrderedDict
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setUp():#open your website for you
   
    global driver
    while True:
        try:
            driver.quit()
            print('closed old browser')
        except:
            pass
       
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('disable-infobars')
       
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.get('https://bls.mind-over-data.com/index.cfm/external/SearchResults?regionID=&companyTypeID=1&q=&search=speciesRegionCompanyType&bookName=Handbook')
        print('driver ready')
        break
                 
finalList = []  
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
# below is for type 1 listings
def parseName(form):# driver.find_elements_by_xpath('//div[@class="form-actions well"]')[2]
                    #driver.find_elements_by_xpath('//div[@class="form-actions well nonAdResult"]')[1]
    try:
        companyName = form.find_element_by_xpath('.//h2[@class="gray company-name"]').text
        print('company name - '+str(companyName))
        return companyName
    except:
        return 'NA'

    
def parseStreet(form):
    companyStreet = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n') 
    for index, item in enumerate(companyInfo): 
        addressSecond = item.split()
        for x in addressSecond:   
            if len(x) == 2 and x.isupper() and not containsInt(x) and not containsDot(x):
                print('company Street  - '+str(companyInfo[index - 1]))
                companyStreet = str(companyInfo[index - 1])
    return companyStreet 
         
            
def removeZip(data):
    for char in data:
        # print(char)
        if char.isdigit():
            data  = data.replace(char,'')
    return data


def parseCity(form):
    city = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        addressSecond = x.split(',')
        # print(addressSecond)
        for index, state in enumerate(addressSecond):
            state = removeZip(state).strip()
            if len(state) == 2 and state.isupper() and not containsInt(state) and not containsDot(state):
                print('city  - '+str(addressSecond[index - 1]))
                city = str(addressSecond[index - 1])        
    return city
            # print('----------------------')
        
    
    # companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    # for x in companyInfo:
    #     addressSecond = x.split(',')
    #     for index, state in enumerate(addressSecond):
    #         state = state.strip()
    #         if len(state) == 2 and state.isupper() and not containsInt(state) and not containsDot(state):
    #             print('city  - '+str(addressSecond[index - 1]))
    #             return addressSecond[index - 1].replace(',', '')
    
   
def containsInt(var):# this func return true if str var contains a int and false if not
    for char in var:
        if char.isdigit():
            return True
        
    return False
        

def containsDot(var):
    for char in var:
        if char == ('.'):
            return True
    return False
    

def parseState(form):
    companyState = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyState:
        addressSecond = x.split()
        for state in addressSecond:
            if len(state) == 2 and state.isupper() and not containsInt(state) and not containsDot(state):
                print('state - '+str(state))
                state = str(state)
                return state
    state = 'NA'
    return state


def isInt(var):
    try:
        int(var)
        return True
    except:
        return False
    
    
def parseZip(form):
    zipCode = 'NA'
    companyZip = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyZip:
        addressSecond = x.split()
        for areaCode in addressSecond:
            if len(areaCode) == 5 and isInt(areaCode):
                print('area code - '+str(areaCode))
                zipCode = str(areaCode)
    return zipCode
    
       
def parsePhone(form):
    phone = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        if 'phone' in x.lower():
            print('phone - '+str(x))
            phoneNumber = str(x).replace('Phone: ', '')
    return phoneNumber

    
def parsePhone2(form):
    phoneNumber = []
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        if 'phone' in x.lower():
            phoneNumber.append(x)
    try:
        print('phone2 - '+str(phoneNumber[1]))
        return str(phoneNumber[1].replace('Phone: ', ''))
    except: 
        print('phone2 - NA')    
        return 'NA'
    
    return x
    

def parseEmail(form):
    email = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for item in companyInfo:
        if '@' in item:
            email = item
    print('email - '+str(email))
    return email
    

#----------------------------
def parse(form):
    name = parseName(form)
    address = parseStreet(form)
    city = parseCity(form)
    state = parseState(form)
    zipcode = parseZip(form)
    phone = parsePhone(form)
    phone2 = parsePhone2(form)
    email = parseEmail(form)
    print('-----------------------')
    companyList = [name,address, city,state,zipcode, phone, phone2,email]
    return companyList

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#below is for type 2 listings

def parseName2(form):# driver.find_elements_by_xpath('//div[@class="form-actions well"]')[2]
    try:
        companyName = form.find_element_by_xpath('.//h3[@class="gray company-name"]').text
        print('company name: '+str(companyName))
        return companyName
    except:
        return 'NA'
    
    
def parseStreet2(form):
    # companyStreet = driver.find_elements_by_xpath('//div[@class="form-actions well nonAdResult"]')[0].find_element_by_xpath('.//address').text.split('\n')
    # for index, item in enumerate(companyStreet): 
    #     addressSecond = item.split()
    #     for x in addressSecond:   
    #         if len(x) == 2 and x.isupper() and not containsInt(x) and not containsDot(x):
    print('company Street  - NA')
    return 'NA'
               
def parseCity2(form):
    cityType2 = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        addressSecond = x.split(',')
        # print(addressSecond)
        for index, state in enumerate(addressSecond):
            state = state.strip()
            if len(state) == 2 and state.isupper() and not containsInt(state) and not containsDot(state):
                print('city  - '+str(addressSecond[index - 1]))
                cityType2 = str(addressSecond[index - 1])
    return cityType2
    

def parseState2(form):
    stateType2 = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        addressSecond = x.split()
        for state in addressSecond:
            if len(state) == 2 and state.isupper() and not containsInt(state) and not containsDot(state):
                print('state - '+str(state))
                stateType2 = str(state)
    return stateType2

    
def parseZip2(form):
    # companyZip = driver.find_elements_by_xpath('//div[@class="form-actions well nonAdResult"]')[0].find_element_by_xpath('.//address').text.split('\n')
    # for x in companyZip:
    #     addressSecond = x.split()
    #     for areaCode in addressSecond:
    #         if len(areaCode) == 5 and isInt(areaCode):
    print('area code - NA')
    return 'NA' 
    
       
def parsePhoneType2(form):
    phoneType2 = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        if 'phone' in x.lower():
            print('phone - '+str(x))
            phoneType2 = str(x).replace('Phone: ', '')
            break 
    return phoneType2

    
def parsePhone2Type2(form):
    phoneNumber = []
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for x in companyInfo:
        if 'phone' in x.lower():
            phoneNumber.append(x)
    try:
        print('phone2 - '+str(phoneNumber[1]))
        return str(phoneNumber[1].replace('Phone: ', ''))
    except: 
        print('phone2 - NA')    
        return 'NA'
    
    return x


def parseEmail2(form):
    email = 'NA'
    companyInfo = form.find_element_by_xpath('.//address').text.split('\n')
    for item in companyInfo:
        if '@' in item:
            email = item
    print('email - '+str(email))
    return email   




def parse2(form):
    name = parseName2(form)
    address = parseStreet2(form)
    city = parseCity2(form)
    state = parseState2(form)
    zipcode = parseZip2(form)
    phone = parsePhoneType2(form)
    phone2 = parsePhone2Type2(form)
    email = parseEmail2(form)
    print('-----------------------------')
    companyList = [name,address, city,state,zipcode, phone, phone2,email]
    return companyList


#-----------------------------------------------------------------------------------
def pageAction():
    type1 = driver.find_elements_by_xpath('//div[@class="form-actions well"]')
    type2 = driver.find_elements_by_xpath('//div[@class="form-actions well nonAdResult"]')
#    adLen = len(fromAction)
#    noLen = len(fromActionNoAd)
    for form in type1:
        result = parse(form)#companyList
        
        finalList.append(result)
   
    for form in type2:
        result = parse2(form)#companyList
        finalList.append(result)

setUp()
for pageNum in range(1, 12):
    driver.get('https://bls.mind-over-data.com/index.cfm/external/SearchResults/Handbook/{}/%20/speciesRegionCompanyType/-1/1'.format(pageNum))
    pageAction()
    

def save():  
    row0=["Company Name","Street Address","City","State","Zip Code","Phone","Phone 2","Email"]
    fileName = ("lumbermanufacturers.csv")
 
    with open(fileName, 'w', encoding='utf-8', newline='') as csvfile:
        lineWriter= csv.writer(csvfile)
        lineWriter.writerow(row0)
        
        for item in finalList:
            lineWriter.writerow(item)
            print(item)

    print("csv file saved")























   
   
