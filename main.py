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

global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income

debt_list = [
    {'name': 'Credit card', 'amount': 5000, 'interest_rate': 15},
    {'name': 'Student loan', 'amount': 20000, 'interest_rate': 5},
    {'name': 'Car loan', 'amount': 10000, 'interest_rate': 7},
    {'name': 'Mortgage', 'amount': 100000, 'interest_rate': 3},
]

class ExpertSystem:
    def __init__(self, data, debt_list):
        self.data = data
        self.debt_list = debt_list
        self.rules = []
        self.facts = []
        self.inferences = []
        self.types = ['Spending', 'Savings', 'Debt', 'Cashflow', 'Spike']

    def add_rule(self, type, premise, conclusion, severity):
        self.rules.append(Rule(type, premise, conclusion, severity))

    def get_rules(self):
        return self.rules

    def add_inference(self, type, premise, conclusion, severity):
        self.inferences.append(Inference(type, premise, conclusion, severity))

    def evaluateDebt(self):
        high_interest_debt = []
        total_debt = 0
        
        for debt in self.debt_list:
            total_debt += debt['amount']
            if debt['interest_rate'] >= 8: # if interest rate is greater than or equal to 8%
                high_interest_debt.append(debt)
        
        if high_interest_debt:
            self.add_fact('Debt','high_interest_debt', True)
        else:
            self.add_fact('Debt','high_interest_debt', False)
        if total_debt > 0.5 * monthly_income:
            self.add_fact('Debt','high_debt_to_MonthlyIncome', True)
        else:
            self.add_fact('Debt','high_debt_to_MonthlyIncome', False)

    def makeInferences(self):
        for rule in self.rules:
            if rule.check(self.facts):
                for type in self.types:
                    if rule.type == type:
                        self.add_inference(type, rule.premise, rule.conclusion, rule.severity)

    def getInferences(self):
        # return self.spendingInferences, self.savingsInferences, self.debtInferences, self.cashflowInferences
        return self.inferences

    def add_fact(self, type, name, value):
        self.facts.append(Fact(type, name, value))

    def getFacts(self):
        return self.facts
    
    def getRules(self):
        return self.rules

class Fact:
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

class Rule:
    def __init__(self, type, premise, conclusion, severity):
        self.type = type
        self.premise = premise
        self.conclusion = conclusion
        self.severity = severity

    def check(self, facts):
        for f in facts:
            if self.premise == f.name and f.value == True and self.type == f.type:
                # print('premise in facts')
                return True
        # print('premise not in facts')
        return False

    def getConclusion(self):
        return self.conclusion
    
    def getPremises(self):
        return self.premise

class Inference:
    def __init__(self, type, premise, conclusion, severity):
        self.type = type
        self.premise = premise
        self.conclusion = conclusion
        self.severity = severity
    
    def getConclusion(self):
        return self.conclusion
    
    def getPremises(self):
        return self.premise

def preprocess():
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income

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

        df.to_csv('data.csv', index=False) # save the dataframe to a csv file, index=False means it will not save the index column (0, 1, 2, 3, ...)

    else:
        df = pd.read_csv('data.csv')
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

    return df 

def addRules(es, df):

    es.add_rule('Cashflow','Weekly Cashflow is negative', 'You currently have a negative Weekly cashflow Adjust your budget.', 1)
    es.add_rule('Cashflow','Monthly Cashflow is negative', 'You currently have a negative Monthly cashflow Adjust your budget.', 1)
    es.add_rule('Cashflow','Total Net Cashflow is negative', 'You currently have a negative net cashflow. Adjust your budget.', 1)

    es.add_rule('Spending','Essential Costs Spending is too high', 'Lower your Essential spending.', 2)
    es.add_rule('Spending','Non-Essential Costs Spending is too high', 'Lower your Nonessential spending.', 1)

    categories = df['Category'].unique()
    for category in categories:
        if category in ['Groceries', 'Shopping']:
            es.add_rule('Spending', category + ' Spending is too high', 'Lower your ' + category + ' spending.', 2)
        elif category in ['Transportation', 'Essential Costs']:
            es.add_rule('Spending', category + ' Spending is too high', 'Lower your ' + category + ' spending.', 3)
        else:
            es.add_rule('Spending', category + ' Spending is too high', 'Lower your ' + category + ' spending.', 1)


    es.add_rule('Debt','high_interest_debt', 'High-interest debt detected, consider paying off the debt first.', 1)
    es.add_rule('Debt','high_debt_to_MonthlyIncome', 'Your debt-to-income ratio is high, consider paying off some debt or increasing your income.', 2)

    es.add_rule('Savings','low_savings', 'Your savings are low, consider increasing your savings.', 2)
    es.add_rule('Savings','Insufficient Emergency Fund', 'Your emergency fund is insufficient, consider increasing your emergency fund.', 1)
    es.add_rule('Savings','Insufficient Retirement Fund', 'Your retirement fund is insufficient, consider increasing your retirement fund.', 3)

def checkBudget(es, df):
    global current_savings, total_deposited, total_spent
    df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
    df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
    df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
    df = df.reset_index() # reset the index
    df = df[['Category', 'Withdrawal']] # select only the Category and Withdrawal columns
    df = df.rename(columns={'Withdrawal': 'Amount'}) # rename the Withdrawal column to Amount
    spending_dict = df.to_dict('records') # convert the dataframe to a list of dictionaries
    # add the percentage of spending for essential and non-essential costs
    spending_dict.append({'Category': 'Essential Costs', 'Amount': df[df['Category'].isin(['Housing', 'Bills', 'Groceries', 'Transportation'])]['Amount'].sum()})
    spending_dict.append({'Category': 'Non-Essential Costs', 'Amount': df[df['Category'].isin(['Entertainment', 'Dining Out', 'Shopping', 'Loan Repayment'])]['Amount'].sum()})


    # print list of categories and amount spent
    # for i in range(len(spending_dict)):
    #     print(spending_dict[i]['Category'], ': ', spending_dict[i]['Amount'])
    
    spending_percentages = {row['Category']: row['Amount'] / total_deposited for row in spending_dict} # calculate the percentage of spending for each category

    # print list of categories and percentage of spending
    # for key, value in spending_percentages.items():
    #     print(key, ': ', value)

    # #evaluate each category against its threshold and add fact if it does not meet the threshold
    spending_thresholds = {'Housing': 0.4, 'Groceries': 0.1, 'Dining Out': 0.1, 'Shopping': 0.2, 'Transportation': 0.1, 'Bills': 0.1, 'Loan Repayment': 0.1, 'Essential Costs': 0.6, 'Non-Essential Costs': 0.4, 'Entertainment': 0.1}
    for category in spending_percentages:
        if spending_percentages[category] > spending_thresholds[category]:
            # print(category + ' Spending is too high')
            es.add_fact('Spending', category + ' Spending is too high', True)
        else:
            # print(category + ' Spending is not too high')
            es.add_fact('Spending', category + ' Spending is too high', False)

def getSpendingPercentages(df):
    spending_percentages = {}
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    for category in spending_percentages:
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

def eval_Savings(es, df):
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
    emergency_fund_goal, retirement_goal = 1000, 100000
    savings_percentage = total_deposited / total_spent * 100
    investment_percentage = total_invested / total_deposited * 100
    emergency_fund_achieved = current_savings >= emergency_fund_goal
    retirement_goal_achieved = total_invested >= retirement_goal

    # recommendations = []
    if savings_percentage < 10:
        # recommendations.append("Consider increasing your savings to ensure a secure future.")
        es.add_fact('Savings','low_savings', True)
    else:
        es.add_fact('Savings','low_savings', False)
    if not emergency_fund_achieved:
        # recommendations.append("Consider starting an emergency fund to cover unexpected expenses.")
        es.add_fact('Savings','Insufficient Emergency Fund', True)
    else:
        es.add_fact('Savings','Insufficient Emergency Fund', False)
    if not retirement_goal_achieved:
        # recommendations.append("Consider increasing contributions to your retirement account.")
        es.add_fact('Savings','Insufficient Retirement Fund', True)
    else:
        es.add_fact('Savings','Insufficient Retirement Fund', False)

def checkCashflow(es):
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
    if avg_weekly_deposits < avg_weekly_withdrawals:
        es.add_fact('Cashflow','Weekly Cashflow is negative', True)
    else:
        es.add_fact('Cashflow','Weekly Cashflow is negative', False)
    if avg_monthly_deposits < avg_monthly_withdrawals:
        es.add_fact('Cashflow','Monthly Cashflow is negative', True)
    else:
        es.add_fact('Cashflow','Monthly Cashflow is negative', False)
    if total_deposited < total_spent:
        es.add_fact('Cashflow','Total Net Cashflow is negative', True)
    else:
        es.add_fact('Cashflow','Total Net Cashflow is negative', False)

def checkforSpikes(es, df): #function to check for spikes in spending by category
    #if there are more than 3 spikes in a category, then create a corresponding rule and fact in the expert system
    global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
    categories = df['Category'].unique()
    for category in categories:
        category_df = df[df['Category'] == category]
        category_df = category_df.groupby(['Month'])['Withdrawal'].sum().reset_index()
        avg_spending = category_df['Withdrawal'].mean()
        category_df['Above_Avg'] = category_df['Withdrawal'] > avg_spending
        spikes = category_df[category_df['Above_Avg'] == True]
        spikes = spikes.reset_index(drop=True)
        if len(spikes) >= 3 and category != 'Loan Repayment':
            es.add_rule('Spike', 'More than 3 monthly spikes in ' + category, 'Consider creating a strict Monthly budget for ' + category, 1)
            es.add_fact('Spike', 'More than 3 monthly spikes in ' + category, True)
        else:
            # es.add_fact('Spike', 'More than 3 monthly spikes in ' + category, False)
            pass #if there are no spikes, then don't add a fact

def main():
    global debt_list
    df = preprocess()
    expert_system = ExpertSystem(None, debt_list)
    addRules(expert_system, df)
    checkBudget(expert_system, df)
    eval_Savings(expert_system, df)
    checkCashflow(expert_system)
    checkforSpikes(expert_system, df)
    expert_system.evaluateDebt()
    expert_system.makeInferences()
    inferences = expert_system.getInferences()
    inferences.sort(key=lambda x: x.severity)
    print('\nAll Inferences: \n')
    for i in inferences:
        # if i.type == 'Spike':
            print(i.type, 'Inference: Premise:', i.premise, '\nRecommendation:', i.conclusion, '\nSeverity:',i.severity , '\n')

if __name__ == "__main__":
    main()
