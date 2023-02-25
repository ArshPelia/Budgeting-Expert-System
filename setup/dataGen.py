import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random, os, calendar, datetime
from datetime import datetime
import re, csv

headerlist = ['Date', 'Withdrawal', 'Deposit', 'Balance']
spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
             'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
essentialList = ['Groceries', 'Housing', 'Bills', 'Loan Payment', 'Transportation', 'Healthcare']
nonessentialList = ['Dining Out', 'Shopping', 'Entertainment', 'Personal Care']
incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Trading']

global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income


# def preprocess():
#     global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income

#     if not os.path.exists('Datasets/data.csv'): # check if the file exists
#         df = pd.read_csv('Datasets/accountactivity.csv', names=headerlist) #assign column names 
#         df.replace(np.nan, 0, inplace=True) # replace NaN with 0, inplace=True means it will change the original dataframe

#         # convert the date column to a datetime format
#         df['Date'] = pd.to_datetime(df['Date'])
#         df['Week'] = df['Date'].dt.week
#         df['Month'] = df['Date'].dt.month
#         df['Year'] = df['Date'].dt.year

#         for i in range(len(df)): # iterate through the dataframe
#             if df.at[i, 'Deposit'] == 0: # if the Deposit column is 0
#                 df.at[i, 'Category'] = random.choice(spendList) # assign a random spend category to each row
#             else:
#                 df.at[i, 'Category'] = random.choice(incomeList) # assign a random income category to each row

#         current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
#         total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
#         total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
        
#         avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
#         avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
#         savings_per_week = avg_weekly_deposits - avg_weekly_withdrawals
        
#         avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
#         avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
#         savings_per_month = avg_monthly_deposits - avg_monthly_withdrawals
        
#         monthly_income = df[df['Category'] == 'Salary']['Deposit'].sum()
#         avg_monthly_income = monthly_income / df['Month'].nunique()
#         monthly_income = avg_monthly_income
#         total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

#         df.to_csv('Datasets/data.csv', index=False) # save the dataframe to a csv file, index=False means it will not save the index column (0, 1, 2, 3, ...)

#     else:
#         df = pd.read_csv('Datasets/data.csv')
#         current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
#         total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
#         total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
        
#         avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
#         avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
#         savings_per_week = avg_weekly_deposits - avg_weekly_withdrawals
        
#         avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
#         avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
#         savings_per_month = avg_monthly_deposits - avg_monthly_withdrawals
        
#         monthly_income = df[df['Category'] == 'Salary']['Deposit'].sum()
#         avg_monthly_income = monthly_income / df['Month'].nunique()
#         monthly_income = avg_monthly_income

#         total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

#     return df 

def preprocess():
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income

    df = pd.read_csv('Datasets/accountactivity.csv', names=headerlist) #assign column names 
    df.replace(np.nan, 0, inplace=True) # replace NaN with 0, inplace=True means it will change the original dataframe

    # convert the date column to a datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.week
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    for i in range(len(df)): # iterate through the dataframe
        if df.at[i, 'Deposit'] == 0: # if the Deposit column is 0
            df.at[i, 'Category'] = random.choice(spendList) # assign a random spend category to each row
        else:
            df.at[i, 'Category'] = random.choice(incomeList) # assign a random income category to each row

    current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    
    avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
    avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
    savings_per_week = avg_weekly_deposits - avg_weekly_withdrawals
    
    avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
    avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
    savings_per_month = avg_monthly_deposits - avg_monthly_withdrawals
    
    monthly_income = df[df['Category'] == 'Salary']['Deposit'].sum()
    avg_monthly_income = monthly_income / df['Month'].nunique()
    monthly_income = avg_monthly_income
    total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

    df.to_csv('New Data/data-4.csv', index=False) # save the dataframe to a csv file, index=False means it will not save the index column (0, 1, 2, 3, ...)


preprocess()

# # read_csv function which is used to read the required CSV file
# data = pd.read_csv('Datasets/accountactivity.csv')
  
# # display 
# print("Original 'input.csv' CSV Data: \n")
# print(data)
  
# # drop function which is used in removing or deleting rows or columns from the CSV files
# data.drop('desc', inplace=True, axis=1)
  
# # display 
# print("\nCSV Data after deleting the column 'year':\n")
# print(data)

# data.to_csv('Datasets/accountactivity.csv', index=False)