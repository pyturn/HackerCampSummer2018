
# coding: utf-8

# In[1]:

import pandas as pd
#importing dataframe
df = pd.read_csv('Intermediate_Output.csv')
#First 5 rows of datfarame
df.head()


# In[2]:

#Sorting the dataframe with cluster_id columns.
df = df.sort_values('Cluster ID')
df = df.reset_index(drop=True)
df['Cluster ID'].max()


# In[3]:

#Again looking at the 5 rows of dataset.
df.head()


# In[4]:

df


# In[5]:

#Creating new dataframe that finally will converted into output file.
df1 = pd.DataFrame(columns=['ln','dob','gn','fn'])


# In[9]:

# Logic to enter data in new dataframe of all the cluster_ids. If the cluster_id is same then only data corresponding to 
# one row is taken. 
for i in range(df['Cluster ID'].max()+1):
    if(str(df[df['Cluster ID'] == int(i)].iloc[0][1]) == 'nan'):
        df1 = df1.append(df[df['Cluster ID'] == int(i)].iloc[0][3:7])
    else:
        ln = df[df['Cluster ID'] == int(i)].iloc[0][-4][2:-1]
        dob = df[df['Cluster ID'] == int(i)].iloc[0][-3][2:-1]
        gn = df[df['Cluster ID'] == int(i)].iloc[0][-2][2:-1]
        fn = df[df['Cluster ID'] == int(i)].iloc[0][-1][2:-1]
        diction = {'ln':ln, 'dob':dob, 'gn':gn, 'fn':fn}
        df1 = df1.append([diction])

        


# In[11]:

df1 = df1.reset_index(drop=True)
df1.to_csv('Final_Output.csv',index=False)

