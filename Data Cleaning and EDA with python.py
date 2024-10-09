#!/usr/bin/env python
# coding: utf-8

# # Exploratory data analysis (EDA)

# ## Problem Context
# With 79 explanatory variables describing (almost) every aspect of residential homes in Ames, Iowa,  you have been contacted as a data scientist to explore and identify key markers in determining the final price of homes
# 
# 
# ## Business Goal (Objective)
# You are now familiar with how to use Pandas, NumPy, and Matplotlib in your data analysis process, and you've seen and conquered a variety of data issues.
# 
# In this EDA session, we will :
# 
# Manipulated data and fixed common data issues
# Visualized data using data visualization techniques
# communicate results in the Jupyter notebook
# 
# Make sure to address the following areas.
# carry out your univariate, Multivariate and Bivariate analysis of the dataset
# - focus point: identify the features are good predictors for House Sale Price
# 
# 
# >Best Practices for EDA
# The final notebook should be well-documented, with inline comments explaining the functionality of code and markdown cells containing comments on the observations and insights.
# 
# 

# ## Preparations

# For the preparations lets first import the necessary libraries and load the files needed for our EDA

# In[89]:


import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


plt.style.use('bmh')


# ### ASSESING DATA 

# In[90]:


#reading in dataset
df = pd.read_csv('house-prices-eda/train.csv')
df.head()


# In[91]:


#data summary
df.info()


# In[92]:


#checking for missing features
df.isna().sum()


# In[93]:


#checking for duplicate features
df.duplicated().sum()


# In[94]:


#statistical description of catergorical features
df.describe(exclude=np.number)


# In[95]:


#statistical describtion of numerical features
df.describe()


# **observations**
# From the Data Summary, we can identify some features that won't be relevant in our exploratory analysis. as there are too much missing values
# - Alley
# - PoolQC
# -  Being a multidimension dataset, we can ibserve we have some redundant features, we will remove `Id` and the features with 30% or less `NaN` values.

# ### DATA CLEANING
# from our observations above, we will be cleanig the data by
# - Dropping off redundant features like the id column
# - dropping off any feature that has more than 30% data points missing

# In[96]:


#identifying features that have atleast 30% of data points
df.isnull().mean() <= (1 - 0.3)


# In[97]:


#data cleaning
# checks for columns having 30% of data points missing
df2 = df.loc[:, df.isnull().mean() <= (1 - 0.3)]

#dropping of redundant id feature
df2 = df2.drop('Id',axis=1)


# In[98]:


for c in df.columns:
    if c not in df2.columns:
        print(f"Dropped Column:{c}")


# ### EXPLORATORY DATA ANALAYSIS
# - use visualization techniques to explore data
# - carry out Univariate, Biariate and Multivariate  Visusalization analysis

# **UNIVARIATE ANALYSIS**

# In[99]:


#univariate distribution of the dependent feature (price of house)
plt.figure(figsize=(10,7))
sb.histplot(df['SalePrice'],bins=100);


# **observations**
# - from the distribution of the proce feature above, we can see that the prices are positively skewed
# - we can easilyt detect some outliers prices, (price of house above 500,000)

# In[ ]:





# In[100]:


#creating categorical fatures and numerical ones for easy analysis
num_feat = df.select_dtypes(include = ['float64', 'int64'])
cat_feat = df.select_dtypes(include='object')
cat_feat.head()


# #### Numerical data distribution 
# For sake of time, this part we take a look at the distribution of all of the features by ploting them

# In[111]:


#uniariate distribuions of the nmerical featues in the data
num_feat.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8);


# In[ ]:





# In[110]:


#univariate distribution of the neigborhood feature
plt.figure(figsize=(15,7))
sb.countplot(x='Neighborhood',data=cat_feat)
fig.tight_layout();


# In[103]:


#unnivariate plots of the other categorical features
fig, axes = plt.subplots(round(len(cat_feat.columns) / 3), 3, figsize=(12, 30))

for i, ax in enumerate(fig.axes):
    if i < len(cat_feat.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sb.countplot(x=cat_feat.columns[i], alpha=0.7, data=cat_feat, ax=ax)

fig.tight_layout();


# In[ ]:





# In[ ]:





# ### BIVARIATE ANALYSIS

# In[104]:


#relationship bwtn horsepower and price
plt.figure(figsize=(9,5))
sb.jointplot(x='YearBuilt',y='SalePrice',data=num_feat)


# **observation**
# - there appears to be a positive linear relationship between the year a house was built and the sale price of the house, this is often a good indication that the year built feature is an important feature in determing the price of a house

# In[105]:


#bivariate plots for the other numerical features, plotting out hte relationship between the features
#and the sale price feature
for i in range(0, len(num_feat.columns), 5):
    sns.pairplot(data=num_feat,
                x_vars=num_feat.columns[i:i+5],
                y_vars=['SalePrice'])


# #### Correlation
# Now we'll try to find which features are strongly correlated with sale price feature, as these features may be good indicators
# in determing the price of a house

# In[106]:


#creating im_feat(important features) to investigate correlation between numerical features and target variable
im_feat = num_feat.corr()['SalePrice']
im_feat = im_feat[im_feat > 0.5]
#im_feat


# **observations**
# - We have identify some relationships. Most of them seems to have a linear relationship with the target feature

# In[ ]:





# In[107]:


#bivariate distribution of the BsmtExposure vs SalePrice
plt.figure(figsize = (9, 6))
ax = sb.boxplot(x='BsmtExposure', y='SalePrice', data=df)
plt.xticks(rotation=45);


# In[108]:


plt.figure(figsize = (9, 6))
ax = sb.boxplot(x='SaleCondition', y='SalePrice', data=df)
plt.xticks(rotation=45);


# ### MULTIVARIATE ANALYSIS

# In[109]:


corr = num_feat.drop('SalePrice', axis=1).corr() 
plt.figure(figsize=(12, 10))

sns.heatmap(corr[(corr >= 0.5) | (corr <= -0.4)], 
            cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 8}, square=True);


# **observations**
# - A lot of features seems to be correlated between each other but some of them such as YearBuild and the GarageYrBlt
# 
# - There is a strong negative correlation between `BsmtUnfSF` (Unfinished square feet of basement area) and `BsmtFinSF2` (Type 2 finished square feet).

# In[ ]:




