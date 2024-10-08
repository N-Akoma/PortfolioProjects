#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries

from bs4 import BeautifulSoup
import requests
import time
import datetime

import smtplib #for getting emial to myslef


# In[2]:


URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_4?crid=1WUG9W28Q321U&dib=eyJ2IjoiMSJ9.E-H5Z9cAvFvKSM510n9CcAQS0RFsUzX6p0rqnNeAYOA_-QGne7A5Yj_2ogulbviCvSe3so7agGx81O32gZtYDUmHbFEl7hTNRwULsdHQkaDBiRJ_eL3Ga0JRQB_0AK0su-UMGb56RqMAk_usj_3a_dgvNjH0VwZqaLlL2OeTJ3LSc3uxF1snhIMZz6sSMfiFHi6GSX6NjO11L9bqAiU0IDYHjGu_zO13vMipG0KPlr7a-TMRK55mvyNRrQoK2fz7QinRqL9p7W7a5SWH4Qaf9ktB0l9Ffkc-qgUJ6qvjh78.KARkjCIo1vKExvZKHgVTWRxU1qSeV2wdyittknxtadQ&dib_tag=se&keywords=data%2Banalyst%2Btshirt&qid=1728298182&sprefix=data%2Bana%2Caps%2C302&sr=8-4&customId=B0752XJYNL&customizationToken=MC_Assembly_1%23B0752XJYNL&th=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Make the request
page = requests.get(URL, headers=headers)

# Parse the content
soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')


# In[4]:


title = soup2.find(id='productTitle').get_text().strip()

price = soup2.find(class_="aok-offscreen").get_text().strip()[1:]

rating = soup2.find(class_="a-size-base a-color-base").get_text().strip()

date = datetime.date.today()
print(date)


# Output the parsed content
print(title)
print(price)
print(rating)


# In[17]:


# saving to csv file
import csv

header = ['Product_Title', 'Price', 'Rating', 'Date']
data = [title,price,rating,date]

# with open('AmazonWebScrapperDataset.csv','w',newline='',encoding='UTF8') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)
#     writer.writerow(data)


# appending date into the csv file
with open('AmazonWebScrapperDataset.csv','a+',newline='',encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)


# In[18]:


import pandas as pd

df = pd.read_csv(r'C:\Users\HP\AmazonWebScrapperDataset.csv')

df.head()


# In[11]:





# In[13]:


# auto update price

def checkPrice():
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_4?crid=1WUG9W28Q321U&dib=eyJ2IjoiMSJ9.E-H5Z9cAvFvKSM510n9CcAQS0RFsUzX6p0rqnNeAYOA_-QGne7A5Yj_2ogulbviCvSe3so7agGx81O32gZtYDUmHbFEl7hTNRwULsdHQkaDBiRJ_eL3Ga0JRQB_0AK0su-UMGb56RqMAk_usj_3a_dgvNjH0VwZqaLlL2OeTJ3LSc3uxF1snhIMZz6sSMfiFHi6GSX6NjO11L9bqAiU0IDYHjGu_zO13vMipG0KPlr7a-TMRK55mvyNRrQoK2fz7QinRqL9p7W7a5SWH4Qaf9ktB0l9Ffkc-qgUJ6qvjh78.KARkjCIo1vKExvZKHgVTWRxU1qSeV2wdyittknxtadQ&dib_tag=se&keywords=data%2Banalyst%2Btshirt&qid=1728298182&sprefix=data%2Bana%2Caps%2C302&sr=8-4&customId=B0752XJYNL&customizationToken=MC_Assembly_1%23B0752XJYNL&th=1'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    # Make the request
    page = requests.get(URL, headers=headers)

    # Parse the content
    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
    
    title = soup2.find(id='productTitle').get_text().strip()

    price = soup2.find(class_="aok-offscreen").get_text().strip()[1:]

    rating = soup2.find(class_="a-size-base a-color-base").get_text().strip()

    date = datetime.date.today()
    
    import csv

    header = ['Product_Title', 'Price', 'Rating', 'Date']
    data = [title,price,rating,date]

    #auto append data in csv file
    with open('AmazonWebScrapperDataset.csv','a+',newline='',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
    if price < 14:
        send_mail()


# In[14]:


while(True):
    checkPrice()
    time.sleep(5) ## checks time in secs


# In[ ]:


import ssl

# To send mail
def send_mail():
    subject = "Price Drop Alert!"
    body = "The price is now $13!"
    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login('nmesomaakoma@gamil.com', 'xxxxxxxxxx')
        server.sendmail('nmesomaakoma@gamil.com', message)
        print("Email sent!")


# In[ ]:




