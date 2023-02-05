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


class ExpertSystem:
    def __init__(self, data):
        self.data = data
        self.rules = []
        self.facts = []
        self.inferences = []

    def add_fact(self, name, value):
        self.facts.append(Fact(name, value))

    def add_rule(self, category, comparison_operator, threshold):
        self.rules.append(Rule(category, comparison_operator, threshold))
        
    def evaluateSpending(self, spending_percentages):
        for rule in self.rules:
            if not rule.check(spending_percentages):
                # return 'Budgeting rule violated: {} {} {}'.format(rule.category, rule.comparison_operator, rule.threshold)
                self.inferences.append('Budgeting rule violated: {} {} {}'.format(rule.category, rule.comparison_operator, rule.threshold))
        
        if len(self.inferences) == 0:
            return 'No violations, Budgeting rules satisfied.'
    
    def getInference(self):
        return self.inferences
    
    
class Fact:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
class Rule:
    def __init__(self, category, comparison_operator, threshold):
        self.category = category
        self.comparison_operator = comparison_operator
        self.threshold = threshold

    def check(self, spending_percentages):
        # print('Category: ',spending_percentages[self.category], 'threshold: ', self.threshold)
        # print('Category: ',self.category, 'threshold: ', self.threshold, 'value: ', spending_percentages[self.category])
        if self.comparison_operator == '<':
            return spending_percentages[self.category] < self.threshold
        elif self.comparison_operator == '>':
            return spending_percentages[self.category] > self.threshold
        else:
            return False

def preprocess():
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
        # print('total deposited: ', total_deposited, 'total spent: ', total_spent, 'current savings: ', current_savings)

        df.to_csv('data.csv', index=False) # save the dataframe to a csv file, index=False means it will not save the index column (0, 1, 2, 3, ...)

        # print(df.columns)
        # print(df)
    else:
        df = pd.read_csv('data.csv')
        current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
        total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
        total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
        # print('total deposited: ', total_deposited, 'total spent: ', total_spent, 'current savings: ', current_savings)

        total_spent 
        # print(df)
    return df 

def addRules(es):
    es.add_rule('Entertainment', '<', 0.1)
    es.add_rule('Housing', '<', 0.3)
    es.add_rule('Groceries', '<', 0.1)
    es.add_rule('Dining Out', '<', 0.1)
    es.add_rule('Shopping', '<', 0.2)
    es.add_rule('Transportation', '<', 0.1)
    es.add_rule('Bills', '<', 0.1)
    es.add_rule('Loan Repayment', '<', 0.1)

def getSpendingPercentages(df):
    # should look like this: spending_percentages = {'Entertainment': 0.12, 'Housing': 0.3}
    spending_percentages = {}
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    for category in spendList:
        spending_percentages[category] = df[df['Category'] == category]['Withdrawal'].sum() / total_spent
        # spending_percentages[category] = df[df['Category'] == category]['Withdrawal'].sum() / total_deposited
    # print(spending_percentages)
        
    return spending_percentages

# # Create an instance of the ExpertSystem class
# expert_system = ExpertSystem(None)

# # Add some rules
# expert_system.add_rule('Entertainment', '<', 0.1)
# expert_system.add_rule('Housing', '<', 0.4)

# # Evaluate the spending habits
# spending_percentages = {'Entertainment': 0.12, 'Housing': 0.3}
# print(expert_system.evaluateSpending(spending_percentages)) # Budgeting rule violated: Entertainment < 0.1

def main():
    df = preprocess()
    expert_system = ExpertSystem(None)
    addRules(expert_system)
    #print expert_system.rules
    # for rule in expert_system.rules:
    #     print(rule.category, rule.comparison_operator, rule.threshold)

    spending_percentages = getSpendingPercentages(df)
    expert_system.evaluateSpending(spending_percentages)
    inferences = expert_system.getInference()
    for inference in inferences:
        print(inference)

if __name__ == "__main__":
    main()
