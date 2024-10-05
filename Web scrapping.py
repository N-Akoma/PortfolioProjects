#!/usr/bin/env python
# coding: utf-8

# ### Scrapping data from a real website

# In[11]:


from bs4 import BeautifulSoup
import requests


# In[43]:


# getting the url of the web
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

# loading the html
soup = BeautifulSoup(page.text,'html')


# In[77]:


table = soup.find('table', class_='wikitable sortable')

print(table)


# In[78]:


table_headers = table.find_all('th')

print(table_headers)


# In[79]:


# extracting the html text from tags
table_headers_title = [title.text.strip() for title in table_headers]

print(table_headers_title)


# In[80]:


# creating a pandas dataframe 
import pandas as pd


# In[81]:


df = pd.DataFrame(columns = table_headers_title)

df


# In[97]:


cols_data = table.find_all('tr')
cols_data


# In[108]:


for row in cols_data[1:]:
    # Find all 'td' elements (columns in each row)
    row_data = row.find_all('td')
    
    # Extract the text from each 'td' element and strip whitespace
    individual_row_data = [data.text.strip() for data in row_data]
    
    # Append this row to the existing DataFrame
    df.loc[len(df)] = individual_row_data


# In[110]:


df.head()


# In[111]:


# Save the DataFrame as a CSV file
df.to_csv(r'C:\Users\HP\OneDrive\Desktop\DA Project with Alex\Python Projects/companies.csv', index=False)


# In[ ]:




