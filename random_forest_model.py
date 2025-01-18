#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# In[14]:


# read in file
df_combined = pd.read_csv("completed_df.csv")
df_combined.head()


# In[15]:


# drop columns that are unimportant/have too many missing values to be useful
df_combined = df_combined.drop(columns = ["qb_hit_1_player_id", "qb_hit_1_player_name", "qb_hit_2_player_id",
                                         "qb_hit_2_player_name", "sack_player_id", "sack_player_name", 
                                         "half_sack_1_player_id", "half_sack_1_player_name", "half_sack_2_player_id", 
                                         "half_sack_2_player_name"], axis=1)


# In[16]:


df_combined = df_combined.drop('was_pressure.1', axis=1) # delete the extra was_pressure column
df_combined['was_pressure'] = df_combined['was_pressure'].replace({True: 1, False: 0}) # replace True/False to 1/0


# In[17]:


# make numeric values for the teams
df_combined["teams_numeric"] = pd.factorize(df_combined["posteam"])[0]


# In[18]:


# replace any missing values in the column "was_pressure" with the value "TRUE"
# This is because the missing values are for observations of a sack, so we cannot remove the missing value as
# it will remove all the rows where a sack occurred
# instead we will replace the missing values with TRUE since a sack is considered pressure by the defense
df_combined["was_pressure"] = df_combined["was_pressure"].apply(lambda x : 1.0 if pd.isna(x) or x == '' else x)


# In[20]:


# Preparing the Random Forest Model
X = df_combined.drop(columns = ['sack', 'defense_man_zone_type', 'defense_coverage_type'], axis=1)
y = df_combined['sack']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = X_train.dropna()
y_train = y_train.loc[X_train.index]
X_test = X_test.dropna()
y_test = y_test.loc[X_test.index]


# In[21]:


# encode categorical columns
ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

categorical_columns = X_train.select_dtypes(include=['object']).columns

X_train[categorical_columns] = ordinal_encoder.fit_transform(X_train[categorical_columns])
X_test[categorical_columns] = ordinal_encoder.transform(X_test[categorical_columns])


# In[22]:


# build the model
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)
y_pred = rfc.predict(X_test)


# In[23]:


# check accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# In[24]:


# build confusion matrix for the model
conf_matrix = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(conf_matrix)

