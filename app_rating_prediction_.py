# -*- coding: utf-8 -*-
"""App Rating Prediction .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pg93Bo2ZN5_YXLPwvRmCqm9saojAvYl-
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""#1.Load the data file using pandas."""

df = pd.read_csv("/content/googleplaystore.csv")

df.shape

df.head(2)

"""## 2.Check for null values in the data. Get the number of null values for each column.

"""

df.isnull().sum()

"""#3.Drop records with nulls in any of the columns."""

df1 = df.dropna()
#the data that has null values in the columns get removed

df1.shape
#the number of elements in each dimensions

print(df1.isna().sum())
#it will return the total number of null values in the dataframe

"""#4.	Variables seem to have incorrect type and inconsistent formatting. You need to fix them:
  1.	Size column has sizes in Kb as well as Mb. To analyze, you’ll need to convert these to numeric:
      
        i).	Extract the numeric value from the column

        ii).	Multiply the value by 1,000, if size is mentioned in Mb

"""

#4.1.i)

def convert_size(size):
  if 'Mb' in size:
        return float(size.replace('Mb', '').strip()) * 1000  # Convert Mb to Kb
  elif 'Kb' in size:
        return float(size.replace('Kb', '').strip())
  else:
        return None
df['Size(Kb)'] = df['Size'].apply(convert_size)
print(df)
print('*'*100)
numeric_sizes = df['Size(Kb)']
print(numeric_sizes)

#4.1.ii)

df1['Size(Kb)'] = df1['Size'].apply(lambda x: float(x.replace('Mb', '').strip()) * 1000 if 'Mb' in x else float(x.replace('Kb', '').strip()) if 'Kb' in x else None)
print(df1)
print('*'*100)
numeric_sizes = df['Size(Kb)']
print(numeric_sizes)

"""2.	Reviews is a numeric field that is loaded as a string field. Convert it to numeric (int/float)."""

#4.2

df1['Reviews'] = pd.to_numeric(df1['Reviews'], errors='coerce').astype('Int64')
print(df1)

"""3.	Installs field is currently stored as string and has values like 1,000,000+.
  1.	Treat 1,000,000+ as 1,000,000
  2.	remove ‘+’, ‘,’ from the field, convert it to integer

"""

df1['Installs'] = df1['Installs'].str.replace('+', '').str.replace(',', '')
df1["Installs"] = pd.to_numeric(df1.Installs)
df1["Installs"].dtype

print(df1)

"""4.	Price field is a string and has $ symbol. Remove $ sign, and convert it to numeric."""

df1['Price'] = df1['Price'].str.replace('$', '')
df1["Price"] = pd.to_numeric(df1.Price)
print(df1)

"""
**5. Sanity checks:**

  i.Average rating should be between 1 and 5 as only these values are allowed on the play store. Drop the rows that have a value outside this range.
"""

df1 = df1[(df1.Rating>=1) & (df1.Rating<=5)]
df1["Rating"]
#here the rating column should be greater than or equal 1 and less thsn 5 '&' operator is used to combine both the values

df1.head(5)
#displays the first 5 rows

len(df1.index)
#number of datasets remaining after removing the ones having ratings not between 1 and 5

"""ii.	Reviews should not be more than installs as only those who installed can review the app. If there are any such records, drop them."""

df1.drop(df1.index[df1.Reviews>df1.Installs],axis=0,inplace=True)
#used to drop rows specified by their indices.

len(df1.index)
#determine the size or length of data structures

#built in python module which ignores warnings
"""
import warnings
warnings.filterwarnings('ignore')
"""

df1[(df1["Type"]=="Free") & (df1["Price"]>0)]  #since there are no such data, hence nothing is dropped

len(df1.index)
 #determine the size or length of data structures

"""#5. Performing univariate analysis:


##•	`Boxplot for Price`

•	Are there any outliers? Think about the price of usual apps on Play Store.

	Boxplot for Reviews #boxplots are used for showing the distribution of data points across a selected measure. In this case "Reviews"
•	Are there any apps with very high number of reviews? Do the values seem right?

	Histogram for Rating #histogram are used to summarize discrete or continuous data that are measured on an interval scale.In this case "Rating"
•	How are the ratings distributed? Is it more toward higher ratings?

	Histogram for Size #histogram are used to summarize discrete or continuous data that are measured on an interval scale.
Note down your observations for the plots made above. Which of these seem to have outliers?

A histogram groups the data into ranges and then plots the frequency that data occurs in each range. A box plot is used to compare multiple groups of data, and it shows the median, interquartile range, and maximum and minimum values of the data

#6. Outlier Treatment
##  1. Boxplot for Price
"""

sns.boxplot(x="Price",data=df1, palette = 'pastel')
sns.set_style(rc = {'axes.facecolor': 'black'})

"""•	Are there any outliers? Think about the price of usual apps on Play Store"""

std = np.std(df1.Price)
mean = np.mean(df1.Price)
outlier_uplimit = mean + 3*std
print(outlier_uplimit)

len(df1[(df1["Price"]>outlier_uplimit)])

df1[(df1["Price"]>outlier_uplimit)]  #list of apps with high prices

"""# `Boxplot for Reviews`

  2. Reviews: Very few apps have very high number of reviews. These are all star apps that don’t help with the analysis and, in fact, will skew it. Drop records having more than 2 million reviews.




"""

std2 = np.std(df1.Reviews)
mean2 = np.mean(df1.Reviews)
outlier_uplimit_2 = mean + 3*std
print(outlier_uplimit_2)

len(df1[(df1["Reviews"]>outlier_uplimit_2)])

df1[(df1["Reviews"]>outlier_uplimit_2)].tail(10)

"""3.	Installs:  There seems to be some outliers in this field
too. Apps having very high number of installs should be dropped from the analysis.
  1.	Find out the different percentiles – 10, 25, 50, 70, 90, 95, 99
  2.	Decide a threshold as cutoff for outlier and drop records having values more than that

"""

sns.boxplot(x="Installs",data=df1)

print(np.percentile(df1["Installs"],10))
print(np.percentile(df1["Installs"],25))
print(np.percentile(df1["Installs"],50))
print(np.percentile(df1["Installs"],70))
print(np.percentile(df1["Installs"],90))
print(np.percentile(df1["Installs"],99))

sns.distplot(df1["Installs"])

len(df1[df1.Installs>=100000000.0])

df1.drop(df1.index[df1.Installs>=100000000.0],inplace=True)
len(df1.index)

"""#7. Bivariate analysis: Let’s look at how the available predictors relate to the variable of interest, i.e., our target variable rating. Make scatter plots (for numeric features) and box plots (for character features) to assess the relations between rating and the other features."""

# Make scatter plot/joinplot for Rating vs. Price
sns.jointplot(x="Price",y="Rating",data=df1)

# Make scatter plot/joinplot for Rating vs Size
sns.jointplot(x="Size",y="Rating",data=df1)
plt.tight_layout()

"""#8. Data preprocessing

 For the steps below, create a copy of the dataframe to make all the edits. Name it inp1.

 Reviews and Install have some values that are still relatively very high. Before building a linear regression model,
 you need to reduce the skew. Apply log transformation (np.log1p) to Reviews and Installs.

 Drop columns App, Last Updated, Current Ver, and Android Ver. These variables are not useful for our task.

 Get dummy columns for Category, Genres, and Content Rating. This needs to be done as the models do not understand categorical
 data, and all data should be numeric. Dummy encoding is one way to convert character fields to numeric. Name of dataframe
 should be inp2.
"""

inp1 = df1.copy()

# Apply log transformation to 'Reviews' and 'Installs'
inp1['Reviews'] = np.log1p(inp1['Reviews'])
inp1['Installs'] = np.log1p(inp1['Installs'])

# Drop unnecessary columns
columns_to_drop = ['App', 'Last Updated', 'Current Ver', 'Android Ver']
inp1.drop(columns=columns_to_drop, inplace=True)

inp1.info()

# Get dummy columns for 'Category', 'Genres', and 'Content Rating' using pd.get_dummies
inp2 = pd.get_dummies(inp1, columns=['Category', 'Genres', 'Content Rating'], drop_first=True)

print(inp2.head())

inp2.head(2)

y = inp2.iloc[:,0] #target

X=inp2.iloc[:,1:] #features

"""# 9. Train test split  and apply 70-30 split. Name the new dataframes df_train and df_test.

"""

# Step 1: Import the necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import seaborn as sns

# You can choose which columns to include in X (features) and y (target variable)
# For this example, let's use 'Rating' as the target variable (y).
X = df.drop(columns=['Rating'])  # Features
y = df['Rating']  # Target variable

# Perform the train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 4: Create new dataframes for training and testing data
df_train = pd.concat([X_train, y_train], axis=1)  # Combine features and target for training
df_test = pd.concat([X_test, y_test], axis=1)  # Combine features and target for testing

# Optional: You can use Seaborn to visualize the data if needed
# For example, to create a heatmap of correlations:
# sns.heatmap(df_train.corr(), annot=True)

# Now you have df_train and df_test containing the training and testing data, respectively.

"""#10. Separate the dataframes into X_train, y_train, X_test, and y_test.

"""

#Import the necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import seaborn as sns

# Load the data


# Data preprocessing and cleaning (if needed)
# For example, you might want to remove or fill missing values, handle categorical data, etc.

# Let's assume you want to predict the 'Rating' column, so set it as the target variable (y)
y = df['Rating']

# Remove the 'Rating' column from the dataframe to create the feature matrix (X)
X = df.drop('Rating', axis=1)

# Split the data into training and testing sets (e.g., 80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Now you have separated dataframes:
# - X_train: Features for training
# - y_train: Target values for training
# - X_test: Features for testing
# - y_test: Target values for testing

"""#11.Model building
Use linear regression as the technique

Report the R2 on the train set

"""

# Import the necessary libraries

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


# Data preprocessing (cleaning and feature selection)
# For this example, let's use 'Reviews' as the feature and 'Rating' as the target variable.
X = df1[['Reviews']]  # Feature
y = df1['Rating']  # Target variable

# Perform the train-test split with a 70-30 ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the training set
y_train_pred = model.predict(X_train)

# Calculate the R2 score on the training set
r2_train = r2_score(y_train, y_train_pred)
print("R-squared (R2) on the training set:", r2_train)
print("\n")

# Optional: Visualize the data and the regression line
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_train['Reviews'], y=y_train, label='Actual Rating')
sns.relplot(x=X_train['Reviews'], y=y_train_pred, color='red', label='Linear Regression Line')
plt.title('Linear Regression Model')
plt.xlabel('Reviews')
plt.ylabel('Rating')
plt.legend()
plt.show()



# In this code:
# We load the dataset into a DataFrame named df.
# We select 'Reviews' as the feature and 'Rating' as the target variable for the linear regression model.
# We perform a train-test split with a 70-30 ratio.
# We create a linear regression model, fit it on the training data, and make predictions on the training set.
# We calculate and print the R-squared (R2) score on the training set, which measures the goodness of fit for the model.
# You can adjust the feature and target variable according to your specific requirements. Additionally, the code includes an optional step to visualize the data and the regression line using Seaborn and Matplotlib.

"""#12.Make predictions on the test set and report R2"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


# Data preprocessing (cleaning and feature selection)
# For this example, let's use 'Reviews' as the feature and 'Rating' as the target variable.
X = df1[['Reviews']]  # Feature
y = df1['Rating']  # Target variable

# Perform the train-test split with a 70-30 ratio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the training set
y_test_pred = model.predict(X_test)

# Calculate the R2 score on the training set
r2_test = r2_score(y_test, y_test_pred)
print("R-squared (R2) on the training set:", r2_test)
print("\n")


plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_test_pred)

sns.relplot(x=X_test['Reviews'], y=y_test_pred, color='#ffdd00', label='Linear Regression Line')

plt.title('Linear Regression Model - Test Set Predictions vs. Actual Ratings')
plt.xlabel('Actual Ratings')
plt.ylabel('Predicted Ratings')
plt.legend()
plt.show()

# We create a linear regression model, fit it on the training data, and make predictions on the test set.
# We calculate and print the R-squared (R2) score on the test set, which measures the goodness of fit for the model.
# Additionally, the code includes an optional step to visualize the predictions on the test set using Seaborn and Matplotlib.

# Make scatter plot/joinplot for Rating vs. Reviews
sns.jointplot(x="Reviews",y="Rating",data=df1)

# Does more review mean a better rating always?
df1.corr()

# Make boxplot for Rating vs. Content Rating
# Is there any difference in the ratings? Are some types liked better?
df1["Content Rating"].unique()

sns.boxplot(x="Rating",y="Content Rating",data=df1)
#shows the distribution of quantitative data in away that shows the comparision between variables

plt.figure(figsize=(10,10)) #creates a new figure objects,figsize displays the width size and height size
sns.boxplot(x="Rating",y="Category",data=df1)