#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import time

# CoinMarketCap API key
api_key = '0f609342-3d73-4628-8a59-b120a87a2f74'

# Define the headers
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# URL for the latest listings
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Parameters for the API request
parameters = {
    'start': '1',  # Starting point
    'limit': '15',  # Limit the number of results
    'convert': 'USD'  # Convert the price data to USD
}

# error handeling
try:
    response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()  # Raises an error for bad status codes
    data = response.json()

except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")
    # Optionally, log the error


# Make the API request
response = requests.get(url, headers=headers, params=parameters)

# Convert the response to JSON
data = response.json()


# In[2]:


type(data)


# In[3]:


#This allows you to see all the columns, not just like 15
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[4]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.Timestamp('now')


# In[5]:


# Extract listings data
listings = data['data']

df.head()


# In[6]:


# function to append data into the dataframe
def api_runner():
    global df
        # CoinMarketCap API key
    api_key = '0f609342-3d73-4628-8a59-b120a87a2f74'

    # Define the headers
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # URL for the latest listings
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    # Parameters for the API request
    parameters = {
        'start': '1',  # Starting point
        'limit': '15',  # Limit the number of results
        'convert': 'USD'  # Convert the price data to USD
    }

    # error handeling
    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        # Optionally, log the error


    # Make the API request
    response = requests.get(url, headers=headers, params=parameters)

    # Convert the response to JSON
    data = response.json()
    
        # Extract listings data
    listings = data['data']

    # Convert to a pandas DataFrame for easy manipulation
    
   #This normalizes the data and makes it all pretty in a dataframe
    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.Timestamp('now')
    df = pd.concat([df, df2], ignore_index=True)
    
    if not os.path.isfile(r'C:\Users\HP\OneDrive\Desktop\DA Project with Alex\Python Projects\API.csv'):
        df.to_csv(r'C:\Users\HP\OneDrive\Desktop\DA Project with Alex\Python Projects\API.csv', header ='columns_name')
    else:
        df.to_csv(r'C:\Users\HP\OneDrive\Desktop\DA Project with Alex\Python Projects\API.csv', mode='a', header=False)
        


# In[7]:


# automating append process
import os 
from time import time
from time import sleep

for i in range(333): #333 number of api run for day as range
    api_runner()
    print('API runner completed')
    sleep(5) #sleep for 5secs
exit()


# In[9]:


df3 = pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\DA Project with Alex\Python Projects\API.csv')
df3.head()


# In[10]:


# getting rid of expo numbers, 1.000000e+09
pd.set_option('display.float_format',lambda x: '%.5f' % x)


# In[11]:


df4 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d',
                                     'quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df4


# In[12]:


df5 = df4.stack()
df5


# In[13]:


type(df5)


# In[14]:


df5.to_frame(name = 'values')


# In[15]:


df5.count()


# In[16]:


# setting index for the rows
index = pd.Index(range(90))

df5 = df5.reset_index()
df5


# In[19]:


df5 = df5.rename(columns={'level_1':'percent_change'})
df5 = df5.rename(columns={0:'values'})

df5


# ### EDA

# In[22]:


df5['percent_change'] = df5['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df5


# In[23]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x='percent_change', y='values', hue='name', data=df5, kind='point')


# In[25]:


# Now to do something much simpler
# we are going to create a dataframe with the columns we want

df6 = df[['name','quote.USD.price','timestamp']]
df6 = df6.query("name == 'Bitcoin'")
df6


# In[26]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df6);


# In[ ]:




