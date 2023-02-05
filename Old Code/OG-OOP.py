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

#declare global variables to be used in the program and amount spent or deposited in each category
# current_savings = 0
# total_deposited = 0
# total_spent = 0
# SpentDiningOut = 0
# SpentGroceries = 0
# SpentShopping = 0
# SpentTransportation = 0
# SpentHousing = 0
# SpentEntertainment = 0
# SpentBills = 0
# SpentLoanRepayment = 0
# DepositedSalary = 0
# DepositedBonus = 0
# DepositedInterest = 0
# DepositedReturnOnInvestment = 0
# DepositedPersonalSale = 0


class ExpertSystem:
    def __init__(self, data):
        self.data = data # data used by the system
        self.knowledge_base = [] # a list of rules used by the system
        self.working_memory = [] # a list of facts used by the system
        self.inferences = [] # a list of inferences made by the system
        
    def add_knowledge(self, rule):
        self.knowledge_base.append(rule) # add a rule to the knowledge base
        
    def add_fact(self, fact):
        self.working_memory.append(fact) # add a fact to the working memory
    
    def match_fact(self, fact_name):
        for fact in self.working_memory:
            if fact.name == fact_name:
                return fact
        return None
    
    def run(self):
        for rule in self.knowledge_base:
            self.current_premises = []
            for premise in rule.premises:
                fact = self.match_fact(premise)
                if not fact:
                    break
                self.current_premises.append(fact)
            else:
                if not rule._check_func(self.current_premises):
                    print(rule.conclusion)            
    # def make_inferences(self):
    #     # loop through the knowledge base and make inferences based on the facts in the working memory
    #     for rule in self.knowledge_base:
    #         if rule.check(self.working_memory):
    #             if rule.conclusion not in self.inferences:
    #                 self.inferences.append(rule.conclusion)
    #             if rule.conclusion not in self.working_memory:
    #                 self.working_memory.append(rule.conclusion)
                
    # def get_inferences(self):
    #     return self.inferences # return the list of inferences made by the system
        
class Rule:
    def __init__(self, premises, conclusion, check_func):
        self.premises = premises
        self.conclusion = conclusion
        self._check_func = check_func
        
    def check(self, facts):
        return self._check_func(facts)

class Fact:
    def __init__(self, name, value):
        self.name = name
        self.value = value

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

def create_Facts(df):

    current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()

    currSaveFact = Fact('current_savings', current_savings)
    totalDepositedFact = Fact('total_deposited', total_deposited)
    totalSpentFact = Fact('total_spent', total_spent)


    df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
    df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
    df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
    df = df.reset_index() # reset the index
    df = df[['Category', 'Withdrawal']] # select only the Category and Withdrawal columns
    df = df.rename(columns={'Withdrawal': 'Amount'}) # rename the Withdrawal column to Amount
    spending_dict = df.to_dict('records') # convert the dataframe to a list of dictionaries

    #create a fact for each category
    for i in range(len(spending_dict)):
        globals()[spending_dict[i]['Category']] = Fact(spending_dict[i]['Category'], spending_dict[i]['Amount'])
    
    #create a list of all the facts
    facts = [currSaveFact, totalDepositedFact, totalSpentFact]
    for i in range(len(spending_dict)):
        facts.append(globals()[spending_dict[i]['Category']])

    #print the facts 
    # for i in range(len(facts)):
    #     print(facts[i].name, facts[i].value)

    return facts

def add_facts_to_es(es, facts):
    for i in range(len(facts)):
        es.add_fact(facts[i])

def create_Rules():
    entertainment_rule = Rule(["total_deposited", "Entertainment"], "High Spending Alert: Amount spent on entertainment is greater than 10% of income", check_entertainment_expense)
    housing_rule = Rule(["total_deposited", "Housing"], "High Spending Alert: Amount spent on housing is greater than 30% of income", check_housing_expense)
    diningout_rule = Rule(["total_deposited", "Dining Out"], "High Spending Alert: Amount spent on dining out is greater than 10% of income", check_diningout_expense)
    transportation_rule = Rule(["total_deposited", "Transportation"], "High Spending Alert: Amount spent on transportation is greater than 10% of income", check_transportation_expense)
    shopping_rule = Rule(["total_deposited", "Shopping"], "High Spending Alert: Amount spent on shopping is greater than 10% of income", check_shopping_expense)
    loanrepay_rule = Rule(["total_deposited", "Loan Repayment"], "High Spending Alert: Amount spent on loan repayments is greater than 10% of income", check_loanrepay_expense)
    groceries_rule = Rule(["total_deposited", "Groceries"], "High Spending Alert: Amount spent on groceries is greater than 10% of income", check_groceries_expense)
    Bills_rule = Rule(["total_deposited", "Bills"], "High Spending Alert: Amount spent on bills is greater than 10% of income", check_bills_expense)

    rules = [entertainment_rule, housing_rule, diningout_rule, transportation_rule, loanrepay_rule, groceries_rule, shopping_rule, Bills_rule]
    # for rule in rules:
    #     print(rule.premises, rule.conclusion, rule._check_func)

    return rules
    
def add_rules_to_es(es, rules):
    for i in range(len(rules)):
        es.add_knowledge(rules[i])

def check_entertainment_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Entertainment":
            entertainment_expense = fact.value
    return entertainment_expense / income < 0.1

def check_housing_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Housing":
            houseing_expense = fact.value
    print('Housing percentage: ',houseing_expense / income)
    return houseing_expense / income < 0.3

def check_diningout_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Dining Out":
            diningout_expense = fact.value
    return diningout_expense / income < 0.1

def check_transportation_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Transportation":
            transportation_expense = fact.value
    return transportation_expense / income < 0.1

def check_shopping_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Shopping":
            shopping_expense = fact.value
    return shopping_expense / income < 0.1

def check_loanrepay_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Loan Repayment":
            loanrepay_expense = fact.value
    return loanrepay_expense / income < 0.1

def check_groceries_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Groceries":
            groceries_expense = fact.value
    return groceries_expense / income < 0.1

def check_bills_expense(facts):
    for fact in facts:
        if fact.name == "total_deposited":
            income = fact.value
        if fact.name == "Bills":
            bills_expense = fact.value
    return bills_expense / income < 0.1


# entertainment_rule = Rule(["income", "entertainment_expense"], "High Spending Alert: Amount spent on entertainment is greater than 10% of income", check_entertainment_expense)
# income_fact = Fact("income", 50000)
# entertainment_expense_fact = Fact("entertainment_expense", 500)

# es = ExpertSystem(None)
# es.add_knowledge(entertainment_rule)
# es.add_fact(income_fact)
# es.add_fact(entertainment_expense_fact)
# es.make_inferences()
# print(es.get_inferences())
def main():
    df = cleanData()
    facts = create_Facts(df)
    es = ExpertSystem(None)
    add_facts_to_es(es, facts)
    # print("Facts in the expert system:")
    # for i in range(len(es.working_memory)):
        # print(es.working_memory[i].name, es.working_memory[i].value)

    print('')
    rules = create_Rules()
    add_rules_to_es(es, rules)
    # print("Rules in the expert system:")
    # for i in range(len(es.knowledge_base)):
        # print(es.knowledge_base[i].premises, es.knowledge_base[i].conclusion, es.knowledge_base[i]._check_func)

    # es.knowledge_base[2].check(es.working_memory)
    # es.make_inferences()
    # print(es.get_inferences())
    es.run()
    print('finished')






if __name__ == "__main__":
    main()


