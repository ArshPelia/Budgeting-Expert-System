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
        self.budget_violations = []
        self.budget_infereces = []

    def add_fact(self, name, value):
        self.facts.append(Fact(name, value))

    def add_budget_rule(self, category, comparison_operator, threshold):
        self.rules.append(BudgetRule(category, comparison_operator, threshold))

    def getFacts(self):
        return self.facts
    
    def getRules(self):
        return self.rules

    def evaluateSpending(self):
        for rule in self.rules:
            if not rule.check_SpendingPercent(self.facts[0].value): # facts[0] is the spending percentages    #         if not rule.check_SpendingPercent(spending_percentages):
                self.budget_violations.append('Budgeting rule violated: {} {} {}'.format(rule.category, rule.comparison_operator, rule.threshold))

        # if len(self.budget_violations) == 0:
        #     return 'No violations, Budgeting rules satisfied.'
    
    def getBudgetViolations(self):
        return self.budget_violations
    
    def MakeBudgetInferences(self):
        if len(self.budget_violations) <= 0:
            return 'No violations, All Budgeting rules satisfied.'
        else:
            for violation in self.budget_violations:
                # print(violation)
                if 'Housing' in violation:
                    self.budget_infereces.append('You are spending too much on Housing. Consider moving to a cheaper location.')
                elif 'Groceries' in violation:
                    self.budget_infereces.append('You are spending too much on Groceries. Consider buying in bulk and cooking at home more.')
                elif 'Entertainment' in violation:
                    self.budget_infereces.append('You are spending too much on Entertainment. Consider going out less or doing more free activities.')
                elif 'Transportation' in violation:
                    self.budget_infereces.append('You are spending too much on Transportation. Consider taking public transportation more often or carpooling.')
                elif 'Bills' in violation:
                    self.budget_infereces.append('You are spending too much on Bills. Consider switching to a cheaper internet provider or cutting cable.')
                elif 'Loan Repayment' in violation:
                    self.budget_infereces.append('You are spending too much on Loan Repayment. Consider paying off your loans faster or refinancing.')
                elif 'Dining Out' in violation:
                    self.budget_infereces.append('You are spending too much on Dining Out. Consider cooking at home more or eating out less.')
                elif 'Shopping' in violation:
                    self.budget_infereces.append('You are spending too much on Shopping. Consider buying less or buying used items.')
                elif 'Essential Costs' in violation:
                    self.budget_infereces.append('You are spending too much on Essential Costs. Consider cutting back on non-essential costs.')
                elif 'Non-Essential Costs' in violation:
                    self.budget_infereces.append('You are spending too much on Non-Essential Costs. Consider cutting back on non-essential costs.')
                else:
                    self.budget_infereces.append('You are spending too much on {}'.format(violation.split()[2]))
            return self.budget_infereces
    
    def getBudgetInferences(self):
        return self.budget_infereces

       
class Fact:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
class BudgetRule:
    def __init__(self, category, comparison_operator, threshold):
        self.category = category
        self.comparison_operator = comparison_operator
        self.threshold = threshold

    def check_SpendingPercent(self, spending_percentages):
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
    es.add_budget_rule('Entertainment', '<', 0.1)
    es.add_budget_rule('Housing', '<', 0.3)
    es.add_budget_rule('Groceries', '<', 0.1)
    es.add_budget_rule('Dining Out', '<', 0.1)
    es.add_budget_rule('Shopping', '<', 0.2)
    es.add_budget_rule('Transportation', '<', 0.1)
    es.add_budget_rule('Bills', '<', 0.1)
    es.add_budget_rule('Loan Repayment', '<', 0.1)
    es.add_budget_rule('Essential Costs', '<', 0.6)
    es.add_budget_rule('Non-Essential Costs', '<', 0.4)

def addFacts(es, df):
    global current_savings, total_deposited, total_spent
    es.add_fact('Spending Percentages', getSpendingPercentages(df))
    es.add_fact('Total Deposited', total_deposited)
    es.add_fact('Total Spent', total_spent)
    es.add_fact('Current Savings', current_savings)

def getSpendingPercentages(df):
    spending_percentages = {}
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    for category in spendList:
        spending_percentages[category] = df[df['Category'] == category]['Withdrawal'].sum() / total_spent
        # spending_percentages[category] = df[df['Category'] == category]['Withdrawal'].sum() / total_deposited
    # print(spending_percentages)
    df_Essential = df[df['Category'].isin(essentialList)]
    df_Nonessential = df[df['Category'].isin(nonessentialList)]
    essential_spending = df_Essential['Withdrawal'].sum()
    nonessential_spending = df_Nonessential['Withdrawal'].sum()

    spending_percentages['Essential Costs'] = essential_spending / total_spent
    spending_percentages['Non-Essential Costs'] = nonessential_spending / total_spent
        
    return spending_percentages

def main():
    df = preprocess()
    expert_system = ExpertSystem(None)
    addRules(expert_system)
    addFacts(expert_system, df)
    expert_system.evaluateSpending()
    budget_violations = expert_system.getBudgetViolations()
    expert_system.MakeBudgetInferences()
    budget_inferences = expert_system.getBudgetInferences()
    for i in budget_inferences:
        print(i)

if __name__ == "__main__":
    main()
