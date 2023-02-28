import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random, os, calendar, datetime
from datetime import datetime
import re, csv
from tkinter import filedialog as fd

headerlist = ['Date', 'Withdrawal', 'Deposit', 'Balance']
spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
             'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
essentialList = ['Groceries', 'Housing', 'Bills', 'Loan Payment', 'Transportation', 'Healthcare']
nonessentialList = ['Dining Out', 'Shopping', 'Entertainment', 'Personal Care']
incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Trading']

global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income


filetypes = (
            ('CSV files', '*.csv'),
            # ('All files', '*.*')
)

filename = fd.askopenfilename(
    title='Open a file',
    initialdir='/',
    filetypes=filetypes)

#exract filename from the path
file = filename
filename = filename.split('/')[-1]

print('Filename: ' + filename)

#check if filename exists in the dataset folder
if os.path.exists('Datasets/' + filename):
    print('File exists')
else:
    print('File does not exist')
    # read_csv function which is used to read the required CSV file
    initialheaderlist = ['Date', 'desc', 'Withdrawal', 'Deposit', 'Balance']
    data = pd.read_csv(file, names=initialheaderlist)
    
    # display 
    print("Original 'input.csv' CSV Data: \n")
    print(data)
    
    # drop function which is used in removing or deleting rows or columns from the CSV files
    data.drop('desc', inplace=True, axis=1)
    
    # display 
    print("\nCSV Data after deleting the column 'year':\n")
    print(data)


data.to_csv('Datasets/accountactivity.csv', index=False, header=False) 