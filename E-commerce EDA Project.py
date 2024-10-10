#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import warnings

warnings.filterwarnings("ignore")

# Define the path to your Excel file
excel_file_path = './e-commerce-dataNNew.xlsx'

# Create an ExcelFile object
excel_file = pd.ExcelFile(excel_file_path)

# Access a specific sheet
sales_data = excel_file.parse(sheet_name='Sales-fact-table')
customer_data = excel_file.parse(sheet_name='Customer')
inventory_data = excel_file.parse(sheet_name='Inventory')
date_data = excel_file.parse(sheet_name='Date')
promotions_data = excel_file.parse(sheet_name='Promotions')
reviews_data = excel_file.parse(sheet_name='Reviews')
suppliers_data = excel_file.parse(sheet_name='Suppliers')
economic_data = excel_file.parse(sheet_name='Economic-Indicators')
market_data = excel_file.parse(sheet_name='Market-Data')
weather_data = excel_file.parse(sheet_name='Weather')
website_traffic_data = excel_file.parse(sheet_name='Website-Traffic')


# In[2]:


# Define a function to remove spaces from column names
def remove_spaces(df):
    df.columns = df.columns.str.replace(' ', '')

# Apply the function to each dataframe
for df in [sales_data, customer_data, inventory_data, date_data, promotions_data,
           reviews_data, suppliers_data, economic_data, market_data, weather_data,
           website_traffic_data]:
    remove_spaces(df)


# In[3]:


# Define relevant columns for each dataframe
sales_columns = ['product_id', 'customer_id', 'quantity_sold', 'sale_date','promo_id','supplier_id', 'revenue']
customer_columns = ['id', 'gender', 'age']
inventory_columns = ['product_id', 'quantity', 'inventory_level']
date_columns = ['date', 'day_of_week', 'day_of_month', 'month', 'year', 'quarter',
                'week_of_year', 'is_weekend', 'is_holiday', 'season']  # Add relevant date features
promotions_columns = ['promo_id', 'discounts', 'impact_on_demand','marketingcampaign']
suppliers_columns = ['supplier_id', 'performance_rating']
economic_columns = ['date', 'economic_indicator_name','economic_indicator_value']
market_columns = ['date','external_factors', 'competitor_revenue', 'competitor_market_share',
       'competitor_customer_satisfaction']
weather_columns = ['date','temperature', 'precipitation', 'humidity']
website_traffic_columns = ['date', 'page_views', 'bounce_rate', 'conversion_rate', 'clicks']


# In[4]:


# Select relevant columns from each dataframe
sales_data = sales_data[sales_columns]
customer_data = customer_data[customer_columns]
inventory_data = inventory_data[inventory_columns]
date_data = date_data[date_columns]
promotions_data = promotions_data[promotions_columns]
suppliers_data = suppliers_data[suppliers_columns]
economic_data = economic_data[economic_columns]
market_data = market_data[market_columns]
weather_data = weather_data[weather_columns]
website_traffic_data = website_traffic_data[website_traffic_columns]


# In[5]:


# Rename columns in sales_data
sales_data = sales_data.rename(columns={'sale_date': 'date'})

# Rename columns in customer_data
customer_data = customer_data.rename(columns={'id': 'customer_id'})

# Rename columns in supplier_data
inventory_data = inventory_data.rename(columns={'location': 'supplier_state'})


# In[6]:


# datatype conversion
sales_data['date'] = pd.to_datetime(sales_data['date'], format='%d/%m/%Y')
sales_data['quantity_sold'] = sales_data['quantity_sold'].astype(int)
sales_data['revenue'] = sales_data['revenue'].astype(float)
economic_data['date'] = pd.to_datetime(economic_data['date'],format='%d/%m/%Y')
market_data['date'] = pd.to_datetime(economic_data['date'],format='%d/%m/%Y')
weather_data['date'] = pd.to_datetime(weather_data['date'],format='%d/%m/%Y')
website_traffic_data['date'] = pd.to_datetime(website_traffic_data['date'],format='%d/%m/%Y')


# In[7]:


# Merge dataframes based on common columns
merged_data = pd.merge(sales_data, customer_data, on='customer_id', how='inner')
merged_data = pd.merge(merged_data, inventory_data, on='product_id', how='inner')
merged_data = pd.merge(merged_data, date_data, on='date', how='inner')
merged_data = pd.merge(merged_data, promotions_data, on='promo_id', how='left')  # Use left join if promotions are not available for all sales
merged_data = pd.merge(merged_data, suppliers_data, on=['supplier_id'], how='left')  # Use left join if supplier information is not available for all products
merged_data = pd.merge(merged_data, economic_data, on='date', how='left')  # Use left join if economic data is not available for all dates
merged_data = pd.merge(merged_data, market_data, on='date', how='left')  # Use left join if market data is not available for all dates
merged_data = pd.merge(merged_data, weather_data, on='date', how='left')  # Use left join if weather data is not available for all dates
merged_data = pd.merge(merged_data, website_traffic_data, on='date', how='left')  # Use left join if website traffic data is not available for all dates


# In[8]:


merged_data.head()


# In[9]:


merged_data.duplicated().sum()


# In[10]:


merged_data.describe()


# In[11]:


merged_data.info()


# In[12]:


merged_data.isna().sum()


# In[13]:


merged_data.shape


# In[14]:


# Drop duplicate rows
merged_data.drop_duplicates(inplace=True)

# Handling missing values in temperature, precipitation, and humidity using linear interpolation
weather_columns = ['temperature', 'precipitation', 'humidity']

for column in weather_columns:
    merged_data[column].interpolate(method='linear', inplace=True)

# Handling missing values in other numerical columns using the mean
numerical_columns = ['performance_rating', 'competitor_revenue', 'competitor_market_share',
                      'competitor_customer_satisfaction', 'page_views', 'bounce_rate', 'conversion_rate', 'clicks', 'economic_indicator_value']

for column in numerical_columns:
    merged_data[column].fillna(merged_data[column].mean(), inplace=True)

# Handling missing values in categorical columns using the mode
categorical_columns = ['economic_indicator_name', 'external_factors']

for column in categorical_columns:
    if merged_data[column].dtype == 'object':
        merged_data[column].fillna(merged_data[column].mode()[0], inplace=True)


# Verify that there are no remaining missing values
missing_values = merged_data.isnull().sum()
print("Remaining Missing Values:")
print(missing_values)


# In[15]:


merged_data.head()


# In[16]:


merged_data.duplicated().sum()


# ***Trend Analysis***

# In[17]:


import matplotlib.pyplot as plt

# Convert 'date' column to datetime if it's not already in datetime format
sales_data['date'] = pd.to_datetime(sales_data['date'])

# Set 'date' column as index
sales_data.set_index('date', inplace=True)

# Resample the data to monthly frequency and calculate the rolling mean for trend analysis
monthly_sales = sales_data['quantity_sold'].resample('M').mean()
rolling_mean = monthly_sales.rolling(window=12).mean()  # 12-month rolling mean for yearly trend

# Plot the original data and the rolling mean for trend analysis
plt.figure(figsize=(8, 4))
plt.plot(monthly_sales, label='Monthly Sales')
plt.plot(rolling_mean, label='12-Month Rolling Mean', color='red')
plt.title('Trend Analysis - Sales Over Time')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Quantity Sold')
plt.show()


# - Long-term Sales Direction: sales are increasing and decreasing no cyclical Patterns i.e. any recurring patterns that might not be seasonal but occur over longer periods (e.g., multi-year cycles).

# ***Time Series Decomposition***

# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Assuming you have a DataFrame named sales_data

# Create a copy of the original DataFrame
sales_data_copy = sales_data.copy()

# Reset the index of the DataFrame
sales_data_copy.reset_index(inplace=True)

# Convert 'sale_date' to a datetime object and set it as the index
sales_data_copy['date'] = pd.to_datetime(sales_data_copy['date'])
sales_data_copy.set_index('date', inplace=True)

# Resample the data to daily frequency (assuming you have daily data)
sales_data_copy = sales_data_copy.resample('D').sum()

# Decompose the time series using the additive model
decomposition = seasonal_decompose(sales_data_copy['quantity_sold'], model='additive')

# Get the components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plot the components of the decomposition
plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(sales_data_copy['quantity_sold'], label='Original', color='blue')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend', color='red')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality', color='green')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals', color='purple')
plt.legend(loc='best')
plt.tight_layout()

plt.show()


# - Trend Component: The overall direction of sales, excluding seasonal and irregular fluctuations.
# - Seasonal Component: Isolating the recurring patterns that occur with a fixed frequency.
# - Residual Component: Captures variations that cannot be attributed to trend or seasonality, indicating irregular or random fluctuations.

# ***Customer Behaviour Analysis***

# In[19]:


import seaborn as sns

# Calculate CLV per customer
clv_data = sales_data.groupby('customer_id')['revenue'].sum().reset_index()
clv_data.columns = ['customer_id', 'total_revenue']

# Plot Customer Lifetime Value distribution
plt.figure(figsize=(6, 4))
sns.histplot(clv_data['total_revenue'], bins=20, kde=True)
plt.title('Distribution of Customer Lifetime Value')
plt.xlabel('Total Revenue per Customer')
plt.ylabel('Count')
plt.show()


# - This histogram displays the distribution of total revenue per customer, offering insights into the spread and concentration of customer lifetime values.
# - These visualizations aid in understanding customer segments based on demographics and behavior, as well as the distribution of customer lifetime values, empowering businesses to tailor marketing strategies, product offerings, and customer retention initiatives effectively. 

# ***Reorder-point Analysis***

# In[20]:


# Reset the index of the DataFrame
sales_data.reset_index(inplace=True)

# Calculate average daily sales per product
daily_sales = sales_data.groupby('product_id').resample('D', on='date').size().mean(level=0)
daily_sales.name = 'avg_daily_sales'  # Assign a name to the Series

# Merge inventory_data with daily sales
merged_inventory = pd.merge(inventory_data, daily_sales, on='product_id', how='left')

# Calculate reorder point (assuming lead time = 1 day for simplicity)
merged_inventory['reorder_point'] = merged_inventory['avg_daily_sales'] * 3  # Adjust lead time accordingly

# Plot Reorder Point Analysis
plt.figure(figsize=(6, 4))
plt.scatter(merged_inventory['quantity'], merged_inventory['reorder_point'])
plt.title('Reorder Point Analysis')
plt.xlabel('Current Inventory Level')
plt.ylabel('Reorder Point')
plt.axline([0, 0], [1, 1], linestyle='--', color='red', label='Ideal Reorder Level')  # Example threshold for reorder
plt.legend()
plt.show()



# - Points below the diagonal line indicate products where the current inventory is below the reorder point, suggesting the need for restocking.
# - Points above the line indicate sufficient inventory levels relative to the calculated reorder point.
# - This analysis provides a simplistic view of the reorder point based on average daily sales and current inventory levels.

# ***Promotion Impact Analysis***

# In[21]:


# Assuming promotions_data has 'promo_id', 'discounts', 'impact_on_sales' columns

# Plotting Promotion Impact on Sales
plt.figure(figsize=(6, 4))
plt.scatter(promotions_data['discounts'], promotions_data['impact_on_demand'])
plt.title('Promotion Impact on Sales')
plt.xlabel('Discounts')
plt.ylabel('Impact on Sales')
plt.show()


# - Each plot indicate a promotion and the plot shows sales which had positive, excellence and average impact on sales based on promotion.

# ***Determine the Effectiveness of Different Marketing Channels:***

# In[22]:


# Assuming market_channels_data has 'channel_id', 'campaign', 'sales' columns

# Group by marketing channels and calculate total sales per channel
total_sales_per_channel = merged_data.groupby('marketingcampaign')['quantity_sold'].sum()

# Plotting Attribution of Sales to Marketing Channels
plt.figure(figsize=(6, 4))
total_sales_per_channel.plot(kind='bar')
plt.title('Attribution of Sales to Marketing Channels')
plt.xlabel('Marketing Campaign')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()


# - Higher bars indicate campaigns that generated more sales.
# - campaigns with taller bars are comparatively more effective in driving sales than those with shorter bars.

# In[23]:


# Assuming economic_data has 'date', 'GDP_growth', 'inflation_rate' columns and sales_data has 'sale_date', 'revenue' columns

# Plotting Correlation between GDP Growth and Sales
plt.figure(figsize=(6, 4))
plt.scatter(merged_data['economic_indicator_name'], merged_data['revenue'])
plt.title('Correlation between Economic Indicator and Sales')
plt.xlabel('Economic Indicator')
plt.ylabel('Sales Revenue')
plt.xticks(rotation=90)
plt.show()


# - here, each point represent date
# - this plot indicates that as economic indicator increase, sales revenue tends to increase (positive correlation).

# In[24]:


# Plotting Correlation between Inflation Rate and Sales
plt.figure(figsize=(6, 4))
plt.scatter(merged_data['economic_indicator_value'], merged_data['revenue'])
plt.title('Correlation between Economic Indicator Value and Sales')
plt.xlabel('Economic Indicator Value')
plt.ylabel('Sales Revenue')
plt.show()


# - the points cluster tightly around a line, it indicates a strong correlation, while a more scattered distribution implies a weaker correlation.

# ***Seasonal Analysis

# In[25]:


import seaborn as sns

# Seasonal analysis
plt.figure(figsize=(6, 4))
sns.boxplot(x='season', y='quantity_sold', data=merged_data)
plt.title('Seasonal Analysis of Sales')
plt.xlabel('Season')
plt.ylabel('Sales')
plt.show()


# - The seasonal analysis shows that the all seasons makes good sales but the Spring season has the higher percentage

# In[26]:


# caculating unit cost of goods sold to customers
merged_data['price_sold'] = merged_data['revenue'] / merged_data['quantity_sold']


# Assuming 'cost' is a relevant column
merged_data['profit'] = merged_data['revenue'] - (merged_data['price_sold'] * merged_data['quantity_sold'])


# ***Customer Segmentation Analysis***

# In[27]:


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Assuming 'numeric_features' contains relevant numerical features for clustering
numeric_features = merged_data[['revenue', 'quantity_sold', 'profit']]

# Standardize numerical features
scaler = StandardScaler()
numeric_features_scaled = scaler.fit_transform(numeric_features)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
merged_data['cluster'] = kmeans.fit_predict(numeric_features_scaled)

# Visualize clusters
plt.figure(figsize=(6, 4))
sns.scatterplot(x='revenue', y='quantity_sold', hue='cluster', data=merged_data)
plt.title('Customer Segmentation')
plt.xlabel('Revenue')
plt.ylabel('Quantity')
plt.show()


# - this pattern identified different cluster of customers who share similar characteristics like purchasing behaviour in terms of sales and quantity. this would help in marketing behaviour, personalized promotions and understing distinct needs of different customers

# In[ ]:




