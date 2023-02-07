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
    # {'name': 'Car loan', 'amount': 10000, 'interest_rate': 7},
    {'name': 'Mortgage', 'amount': 100000, 'interest_rate': 3},
]

class ExpertSystem:
    def __init__(self, data, debt_list):
        self.data = data
        self.debt_list = debt_list
        self.budget_rules = []
        self.facts = []
        self.budget_violations = []
        self.budget_infereces = []
        # self.debt_rules = {
        #                 "high_income": "Your income is high, consider investing in stocks or real estate.",
        #                 "low_income": "Your income is low, consider finding a higher paying job or reducing expenses.",
        #                 "high_expenses": "Your expenses are high, consider reducing expenses or finding a higher paying job.",
        #                 "manageable_expenses": "Your expenses are manageable.",
        #                 "high_interest_debt": "High-interest debt detected, consider paying off the debt first.",
        #                 "high_debt_to_income": "Your debt-to-income ratio is high, consider paying off some debt or increasing your income.",
        #                 "manageable_debt": "Your debt is manageable."
        #             }
        self.debt_rules = []
        self.debt_violations = []

    def add_debt_rule(self, premise, conclusion):
        self.debt_rules.append(DebtRule(premise, conclusion))

    def get_debt_rules(self):
        return self.debt_rules

    def evaluateDebt(self):
        result = debt_analysis(self.debt_list)
        # print('result: ', result[0])
        if result[0].startswith("High-interest"):
            # return self.debt_rules["high_interest_debt"]
            # self.debt_violations.append(self.debt_rules["high_interest_debt"])
            self.add_fact('high_interest_debt', True)
        if result[0].startswith("Y"): # high debt to income ratio detected
            # return self.debt_rules["high_debt_to_income"]
            # self.debt_violations.append(self.debt_rules["high_debt_to_income"])
            self.add_fact('high_debt_to_income', True)
        # else:
        #     # return self.debt_rules["manageable_debt"]
        #     self.debt_violations.append(self.debt_rules["manageable_debt"])

    def makeDebtInfereces(self):
        for rule in self.debt_rules:
            if rule.check(self.facts):
                self.debt_violations.append(rule.conclusion)        

    def getDebtViolations(self):
        return self.debt_violations

    def add_fact(self, name, value):
        self.facts.append(Fact(name, value))

    def add_budget_rule(self, category, comparison_operator, threshold):
        self.budget_rules.append(BudgetRule(category, comparison_operator, threshold))

    def getFacts(self):
        return self.facts
    
    def getRules(self):
        return self.budget_rules

    def evaluateSpending(self):
        for rule in self.budget_rules:
            if not rule.check_SpendingPercent(self.facts[0].value): # facts[0] is the spending percentages    #         if not rule.check_SpendingPercent(spending_percentages):
                self.budget_violations.append('Budgeting rule violated: {} {} {}'.format(rule.category, rule.comparison_operator, rule.threshold))
    
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

class DebtRule:
    def __init__(self, premise, conclusion):
        self.premise = premise
        self.conclusion = conclusion

    def check(self, facts):
        # print('facts: ', facts)
        # for f in facts:
        #     print('fact: ', f.name, f.value)
        # # for premise in self.premises:
        #     print('premise: ', self.premise)
        # if self.premise not in facts: # if the premise is not in the facts, return false
        #     print('premise not in facts')
        #     return False
        # print('premise in facts')
        # return True
        for f in facts:
            if self.premise == f.name:
                # print('premise in facts')
                return True
        # print('premise not in facts')
        return False
    

    def getConclusion(self):
        return self.conclusion
    
    def getPremises(self):
        return self.premise

def preprocess():
    global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income

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

    return df 

def debt_analysis(debt_list):
    high_interest_debt = []
    total_debt = 0
    
    for debt in debt_list:
        total_debt += debt['amount']
        if debt['interest_rate'] >= 8: # if interest rate is greater than or equal to 8%
            high_interest_debt.append(debt)
    
    if high_interest_debt:
        return ('High-interest debt detected, consider paying off the following debts first:', high_interest_debt)
    # elif total_debt > 0.5 * total_deposited: # if total debt is more than 50% of annual salary
    elif total_debt > 0.5 * monthly_income: # if total debt is more than 50% of monthly salary
        return ('Your debt-to-Monthlyincome ratio is greater than 2:1, consider paying off some debt or increasing your income')
    else:
        return ('Your debt is manageable')

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

    # self.debt_rules = {
    #                 "high_interest_debt": "High-interest debt detected, consider paying off the debt first.",
    #                 "high_debt_to_income": "Your debt-to-income ratio is high, consider paying off some debt or increasing your income.",
    #             }
    es.add_debt_rule('high_interest_debt', 'High-interest debt detected, consider paying off the debt first.')
    es.add_debt_rule('high_debt_to_income', 'Your debt-to-income ratio is high, consider paying off some debt or increasing your income.')

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
    global debt_list
    df = preprocess()
    expert_system = ExpertSystem(None, debt_list)
    addRules(expert_system)
    # print all debt rules with their premises and conclusions
    drules = expert_system.get_debt_rules()
    # for rule in drules:
    #     print([rule.getPremises(), rule.getConclusion()])
    
    # addFacts(expert_system, df)
    # expert_system.evaluateSpending()
    # budget_violations = expert_system.getBudgetViolations()
    # expert_system.MakeBudgetInferences()
    # budget_inferences = expert_system.getBudgetInferences()
    # print('Budget Inferences: ')
    # for i in budget_inferences:
    #     print(i)

    expert_system.evaluateDebt()
    expert_system.makeDebtInfereces()
    debt_analysis = expert_system.getDebtViolations()
    print('Debt Analysis: ')
    for i in debt_analysis:
        print(i)

if __name__ == "__main__":
    main()
