# Budgeting Expert System 

This expert system is designed to evaluate chequeing account statements and analyze your financial
health across the following categories: Debt, Savings, Spending, Chronic Overspending and Cashflow. 
The expert system begins by evaluating account activity and provides recommendations based on current financial health.

```bash
  Status Dictionary = [Optimal, Managable, Moderate, Alarming, Critical]
```

## Run Locally

Clone the project

Go to the project directory

```bash
  cd Budgeting-Expert-System
```

Install dependencies

```bash
    cd setup
    conda create --name BudgetExpert --file requirements.txt
```

Start the app

```bash
  cd .. # Not needed if dependencies were previously installed
  python main.py
```


## Documentation

### Start Page

At startup, the user is prompted for their age and current amounts in their emergency and retirement
funds. These fields are REQUIRED.

### Debt Page

Then users can create a list of their current debt or load in preset values. This is OPTIONAL but 
debt will not be accounted for by the expert system. (Assumes that you have no debt.)

#### Preset debt dictionary: 
```bash
default_debt_list = [ {'id': 1, 'name': 'Credit Card 1', 'amount': 5000, 'interest_rate': 5,
                     'min_payment': 5}, 
                     {'id': 2, 'name': 'Student Loan', 'amount': 2000, 'interest_rate': 9, 'min_payment': 7},
                     {'id': 3, 'name': 'Car Loan', 'amount': 1000, 'interest_rate': 4, 'min_payment': 10},
                     {'id': 4, 'name': 'Credit Card 2', 'amount': 500, 'interest_rate': 12, 'min_payment': 9}]
```

### File Select Page

Upon hitting the Continue button on the debt page, users will be asked to upload a csv file containing their account activity. (Commonly found on bank websites). 

The Datasets folder contains 4 preprocessed data sets (Data-1, Data-2, Data-3, Data-4) as well
as an unprocessed file (Randomize.csv). 
    NOTE: if Randomize.csv is selected, the program will randomly assign categories for withdrawals and deposits. 

#### Predefined Categories:
```bash
    spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
                'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
    incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Trading']
```
The User can also select their own chequeing account statement if their file has the following column order: (Data, Transaction Description, Withdrawal, Deposit, Balance) and DOES NOT contain any column HEADERS. If successfully processed, 'userData.csv' will be created in the Datasets folder for future user. 
NOTE: Once again your spending/deposit categories will be randomized. 

If the file is successfully processed then the Expert system will initialize and the user will be taken to the blackboard. Otherwise UserData.csv will be deleted. 

### Blackboard

#### Statistics Page

By executing the 'Show Stats', the user can view the facts that the expert system has extracted by analysing the account activity. 

#### Graphs Page

Likewise, the Graphs page provides multiple option to visualize your account activity. 

### Inference Engine (Analysis Page)

Based on the facts deduced from your account activity and the predefined rules, the expert system will show a summary status of each category: Debt, Savings, Spending, Chronic Overspending and Cashflow. 

Users will also be given the inferences it has made in each category below the summary table in individual tabs. NOTE: a tab will only be created if inferences for the corresponding tab exists otherwise, the category is assumed as optimal. 

By double-clicking each individual inference, the user can view the premise and conclusion of the inference as well as related information. 

#### Predefined Rules: format = (Type, Premise, Conclusion, Severity)

```bash
1. ('Debt','high_interest_debt', 'High-interest debt detected, prioritize paying off debts with an interest rate greater than 8%.', 2)         
2. ('Debt','High_DTI', 'Your debt-to-income ratio is greater than 50% of monthly income, you must reduce this ratio for optmal financial health. DTI: ' + str(dti), 3)         
3. ('Debt','Moderate_DTI', 'Your debt-to-income ratio is sustainable but leaves little to invest. DTI:' + str(dti), 2)             
4. ('Debt','Low_DTI', 'Your debt-to-income ratio is moderate but it can be improved. DTI: ' + str(dti), 1)       

5. ('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', 'Lower your ' + category + ' spending.', 1)                  
6. ('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', 'Lower your ' + category + ' spending.', 3)

7. ('Savings','Low Monthly Savings', 'Saving less than 10% of monthly income, you MUST decreasing your spendature.', 3)
8. ('Savings','Moderate Monthly Savings', 'Saving less than 15% of monthly income, consider decreasing your spendature.', 1)
9. ('Savings','Moderate Emergency Fund', 'Your emergency fund can support you for 3-5 months based on current spending', 1)
10. ('Savings','Low Emergency Fund', 'Your emergency fund can support you for 1-3 months based on current spending', 2)
11. ('Savings','Insufficient Emergency Fund', 'Your emergency fund can support you for less than 1 month based on current spending', 4)               
12. ('Savings','Moderate Retirement Fund', 'Your retirement fund is moderate but not optimal assuming 15% of yearly income from age 25.', 1)          
13. ('Savings','Low Retirement Fund', 'Your retirement fund needs attention 50-80% of expected value assuming 15% of yearly income from age 25.', 2)                 
14. ('Savings','Insufficient Retirement Fund', 'Your retirement fund is insufficient at < 50% of expected value, you MUST allocate more funds towards it assuming 15% of yearly income from age 25.', 3)               

15. ('Cashflow','Weekly Cashflow is negative', 'You currently have a negative Weekly cashflow Adjust your budget.', 3)            
16. ('Cashflow','Monthly Cashflow is negative', 'You currently have a negative Monthly cashflow Adjust your budget.', 4)            
17. ('Cashflow','Total Net Cashflow is negative', 'You currently have a negative net cashflow. Adjust your budget.', 2)                
18. ('Cashflow','Monthly Cashflow is low', 'Saving less than 20% of monthly income, consider improving cashflow', 1)   

19. ('Chronic Overspending', '5+ monthly spikes over average spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 3)               
20. ('Chronic Overspending', '3+ monthly spikes over average spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 1)
```


