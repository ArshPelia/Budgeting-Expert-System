import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random, os, calendar, datetime
from datetime import datetime
import re

headerlist = ['Date', 'Withdrawal', 'Deposit', 'Balance']
spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 'Entertainment', 'Bills', 'Loan Repayment']
essentialList = ['Groceries', 'Housing', 'Bills', 'Loan Repayment', 'Transportation']
nonessentialList = ['Dining Out', 'Shopping', 'Entertainment']
incomeList = ['Salary', 'Bonus', 'Interest', 'Return on Investement', 'Personal Sale']

global savings_per_week, savings_per_month, total_deposited, total_spent, return_rate, semi_annual_raise, current_savings

debt_list = [
    {'name': 'Credit card', 'amount': 5000, 'interest_rate': 15},
    {'name': 'Student loan', 'amount': 20000, 'interest_rate': 5},
    {'name': 'Car loan', 'amount': 10000, 'interest_rate': 8},
    {'name': 'Mortgage', 'amount': 100000, 'interest_rate': 3},
]

def cleanData():
    global current_savings, total_deposited, total_spent
    if not os.path.exists('data.csv'): # check if the file exists
        df = pd.read_csv('accountactivity.csv', names=headerlist) #assign column names 
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
        print('total deposited: ', total_deposited, 'total spent: ', total_spent, 'current savings: ', current_savings)

        df.to_csv('data.csv', index=False) # save the dataframe to a csv file, index=False means it will not save the index column (0, 1, 2, 3, ...)

        # print(df.columns)
        # print(df)
    else:
        df = pd.read_csv('data.csv')
        current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
        total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
        total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
        print('total deposited: ', total_deposited, 'total spent: ', total_spent, 'current savings: ', current_savings)

        total_spent 
        # print(df)
    return df 

def spending_habits(df): #function to analyze spending habits by category and create a list of the category and amount spent
    global current_savings, total_deposited, total_spent
    df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
    df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
    df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
    df = df.reset_index() # reset the index
    df = df[['Category', 'Withdrawal']] # select only the Category and Withdrawal columns
    df = df.rename(columns={'Withdrawal': 'Amount'}) # rename the Withdrawal column to Amount
    spending_dict = df.to_dict('records') # convert the dataframe to a list of dictionaries
    # print(spending_dict)

    # print list of categories and amount spent
    # for i in range(len(spending_dict)):
    #     print(spending_dict[i]['Category'], ': ', spending_dict[i]['Amount'])
    
    spending_percentages = {row['Category']: row['Amount'] / total_deposited for row in spending_dict} # calculate the percentage of spending for each category

    if spending_percentages.get('Housing', 0) > 0.4:
        print('You are spending more than 40% of your income on housing')
    if spending_percentages.get('Transportation', 0) > 0.1:
        print('You are spending more than 10% of your income on transportation')
    if spending_percentages.get('Dining Out', 0) > 0.1:
        print('You are spending more than 10% of your income on dining out')
    if spending_percentages.get('Shopping', 0) > 0.2:
        print('You are spending more than 20% of your income on shopping')
    if spending_percentages.get('Entertainment', 0) > 0.05:
        print('You are spending more than 5% of your income on entertainment')
    if spending_percentages.get('Bills', 0) > 0.1:
        print('You are spending more than 10% of your income on bills')
    if spending_percentages.get('Loan Repayment', 0) > 0.1:
        print('You are spending more than 10% of your income on loan repayment')
    if spending_percentages.get('Groceries', 0) > 0.1:
        print('You are spending more than 10% of your income on groceries')
    elif sum(spending_percentages.values()) > 0.7:
        return ('Overall spending is greater than 70% of your income, consider reducing expenses in all categories.')
    else:
        return ('Your spending is within a reasonable range.')

def debt_analysis(debt_list):
  high_interest_debt = []
  total_debt = 0
  
  for debt in debt_list:
    total_debt += debt['amount']
    if debt['interest_rate'] >= 8: # if interest rate is greater than or equal to 8%
      high_interest_debt.append(debt)
  
  if high_interest_debt:
    return ('High-interest debt detected, consider paying off the following debts first:', high_interest_debt)
  elif total_debt > 0.5 * total_deposited: # if total debt is more than 50% of annual salary
    return ('Your debt-to-income ratio is high, consider paying off some debt or increasing your income')
  else:
    return ('Your debt is manageable')

def essentialvsNonEssentialSpending(df):
    #compare essential spending to nonessential spending
    df_Essential = df[df['Category'].isin(essentialList)]
    df_Nonessential = df[df['Category'].isin(nonessentialList)]
    essential_spending = df_Essential['Withdrawal'].sum()
    nonessential_spending = df_Nonessential['Withdrawal'].sum()
    print('Essential Spending: ', essential_spending)
    print('Nonessential Spending: ', nonessential_spending)
    if essential_spending > nonessential_spending:
        ratio = essential_spending / nonessential_spending
        print('You are spending', ratio, 'times more on essentials than nonessentials')
    else:
        print('You are spending more on nonessentials than essentials')
        ratio = nonessential_spending / essential_spending
        print('You are spending', ratio, 'times more on nonessentials than essentials')

def main():
    df = cleanData()
    essentialvsNonEssentialSpending(df)
    debt_analysis_result = debt_analysis(debt_list)
    print(debt_analysis_result)
    spending_habits(df)


if __name__ == "__main__":
        main()