import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib, operator, calendar
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure
# from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import random, os

LARGE_FONT= ("Verdana", 14, 'bold', 'underline')
NORM_FONT = ("Helvetica", 12)
SMALL_FONT = ("Serif", 10)

headerlist = ['Date', 'Withdrawal', 'Deposit', 'Balance']
spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
             'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
essentialList = ['Groceries', 'Housing', 'Bills', 'Loan Payment', 'Transportation', 'Healthcare']
nonessentialList = ['Dining Out', 'Shopping', 'Entertainment', 'Personal Care']
incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Trading']

global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals
global savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
global allInferences, dataFrame, age, retirement_fund, emergency_fund, spending_percentages
global Weekly_essentialSpend, Weekly_nonessentialSpend, monthly_essentialSpend, monthly_nonessentialSpend
global essential_spendingPercentages, nonessential_spendingPercentages, Monthly_debt_payment
global debt_list, statusDict, spending_thresholds, default_debt_list

default_debt_list = [ {'id': 1, 'name': 'Credit Card 1', 'amount': 5000, 'interest_rate': 5, 'min_payment': 5}, 
                     {'id': 2, 'name': 'Student Loan', 'amount': 2000, 'interest_rate': 9, 'min_payment': 7},
                     {'id': 3, 'name': 'Car Loan', 'amount': 1000, 'interest_rate': 4, 'min_payment': 10},
                     {'id': 4, 'name': 'Credit Card 2', 'amount': 500, 'interest_rate': 12, 'min_payment': 9}]

debt_list = []
allInferences = []
statusDict= {'Spending': 'Optimal', 'Savings': 'Optimal', 'Debt': 'Optimal', 'Chronic Overspending': 'Optimal'}
spending_thresholds = {'Housing': 0.4, 'Groceries': 0.1, 'Dining Out': 0.1, 
                       'Shopping': 0.2, 'Transportation': 0.1, 'Bills': 0.1, 
                       'Loan Payment': 0.1, 'Essential Costs': 0.5, 
                       'Non-Essential Costs': 0.3, 'Entertainment': 0.1,
                       'Personal Care': 0.1, 'Healthcare': 0.1}

def getTheme():
    custom_theme = {
        'TLabel': {
            'configure': {
                'background': '#F6D9A6',
                'foreground': '#403B3B',
                'font': ('Roboto', 14),
                'padx': 10,
                'pady': 5,
            },
        },
        'TButton': {
            'configure': {
                'background': '#6AB5D6',
                'foreground': '#F6D9A6',
                'font': ('Open Sans', 14, 'bold'),
                'padx': 10,
                'pady': 5,
                'borderwidth': 0,
                'relief': 'flat',
                'cursor': 'hand2',
            },
            'map': {
                'background': [('active', '#F6D9A6'), ('disabled', '#A9A9A9')],
                'foreground': [('active', '#403B3B'), ('disabled', '#AFAFAF')],
            },
        },
        'TEntry': {
            'configure': {
                'background': '#F6D9A6',
                'foreground': '#403B3B',
                'font': ('Lato', 12),
                'padx': 10,
                'pady': 5,
                'borderwidth': 0,
                'highlightthickness': 1,
                'highlightcolor': '#6AB5D6',
            },
            'map': {
                'background': [('active', '#FFFFFF'), ('disabled', '#EFEFEF')],
                'foreground': [('active', '#403B3B'), ('disabled', '#AFAFAF')],
                'highlightcolor': [('focus', '#6AB5D6'), ('!focus', '#EFEFEF')],
            },
        },
        'Treeview': {
            'configure': {
                'background': '#FFFFFF',
                'foreground': '#403B3B',
                'font': ('Roboto', 12),
                'highlightthickness': 1,
                'highlightcolor': '#6AB5D6',
                'selectbackground': '#6AB5D6',
                'selectforeground': '#FFFFFF',
                'rowheight': 25,
            },
            'map': {
                'background': [('active', '#F6D9A6'), ('disabled', '#EFEFEF')],
                'foreground': [('active', '#403B3B'), ('disabled', '#AFAFAF')],
            },
        },
        'Treeview.Heading': {
            'configure': {
                'background': '#6AB5D6',
                'foreground': '#F6D9A6',
                'font': ('Open Sans', 12, 'bold'),
                'padx': 10,
                'pady': 5,
            },
        },
        'TFrame': {
            'configure': {
                'background': '#FFFFFF',
                'foreground': '#403B3B',
                'font': ('Lato', 12),
                'padx': 10,
                'pady': 5,
            },
        },
        'TNotebook': {
            'configure': {
                'background': '#F6D9A6',
                'foreground': '#403B3B',
                'tabmargins': [0, 0, 0, 0],
                'font': ('Roboto', 12),
            },
            'map': {
                'background': [('selected', '#6AB5D6'), ('background', '#FFFFFF')],
                'foreground': [('selected', '#FFFFFF'), ('background', '#403B3B')],
                    'expand': [('selected', [1, 1, 1, 0]), ('!selected', [1, 1, 1, 0])],
                    'padding': [('selected', [10, 5]), ('!selected', [10, 5])],
                    },
            },
        }

    return custom_theme

def popupmsg(msg):
    popup = tk.Tk() # create popup window
    style = ttk.Style(popup) # create style for popup
    style.theme_create('modern1', parent='default') # create theme 'modern1' with parent theme 'default'
    style.theme_settings('modern1', getTheme()) # add the settings from the getTheme() function to 'modern1'
    style.theme_use('modern1') # apply the theme 'modern1' to the popup window

    popup.wm_title("!") # set the title of the popup
    heading = ttk.Label(popup, text="Error", font=LARGE_FONT) # create a label for the heading
    heading.pack(side="top", anchor="center", pady=10, padx=10) # add the label to the popup window
    label = ttk.Label(popup, text=msg, font=NORM_FONT) # create a label for the message
    label.pack(side="top", anchor="center", pady=10, padx=10 ) # add the label to the popup window
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy) # create a button with the text 'Okay' and the command popup.destroy
    B1.pack(padx=10, pady=10) # add the button to the popup window
    popup.mainloop() # run the popup window

def viewInference(type, premise, conclusion):
    global dataFrame, savings_per_month, debt_list, essential_spendingPercentages, nonessential_spendingPercentages
    global monthly_income, Monthly_debt_payment, monthly_essentialSpend, monthly_nonessentialSpend, savings_per_month
    global avg_monthly_withdrawals
    popup = tk.Tk()
    style = ttk.Style(popup)
    style.theme_create('modern1', parent='default')
    style.theme_settings('modern1', getTheme())
    style.theme_use('modern1')
    popup.wm_title("Inference")
    label = ttk.Label(popup, text=("Inference Type: " + type), font=LARGE_FONT, anchor="center", justify="center")
    label.pack(side="top", pady=13, padx=10)
    label1 = ttk.Label(popup, text=("Premise: " + premise), font=NORM_FONT)
    label1.pack(side="top", fill="x", pady=10, padx=10)
    label2 = ttk.Label(popup, text=("Conclusion: " + conclusion), font=NORM_FONT)
    label2.pack(side="top", fill="x", pady=10, padx=10)

    if type == 'Cashflow': 
        if premise == 'Total Net Cashflow is negative':
            df = dataFrame
            df = df.groupby(['Week']).sum() # group the dataframe by Date and sum the Deposit and Withdrawal columns
            df = df.sort_values(by=['Week'], ascending=True) # sort the dataframe by Date column in ascending order
            df = df.reset_index() # reset the index
            # print(df)

            f = Figure(figsize=(12,5), dpi=100)
            a = f.add_subplot(111)
            a.plot(df['Week'], df['Deposit'], label='Income')
            a.plot(df['Week'], df['Withdrawal'], label='Spending')
            a.set_xlabel('Week')
            a.set_ylabel('Amount')
            a.set_title('Cashflow')
            a.legend()

            canvas = FigureCanvasTkAgg(f, popup)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        elif premise == 'Monthly Cashflow is negative' or premise == 'Monthly Cashflow is low':
            df = dataFrame
            avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
            avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
            # calculate the sum of deposits and withdrawals for each month
            month_sums = df.groupby(['Month', 'Category']).agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
            # calculate the number of months
            num_months = month_sums['Month'].nunique()
                # calculate the average deposits and withdrawals per month
            month_avgs = month_sums.groupby('Category').agg({'Deposit': 'mean', 'Withdrawal': 'mean'})
            month_avgs['Deposit'] = month_avgs['Deposit'] / num_months
            month_avgs['Withdrawal'] = month_avgs['Withdrawal'] / num_months

            f = Figure(figsize=(12,5), dpi=100)
            a = f.add_subplot(111)
            # a.plot(month_avgs['Deposit'], label='Income')
            # a.plot(month_avgs['Withdrawal'], label='Spending')
            a.barh(month_avgs.index, month_avgs['Deposit'], label='Income')
            a.barh(month_avgs.index, month_avgs['Withdrawal'], label='Spending')
            a.set_ylabel('Category')
            a.set_xlabel('Amount')
            a.set_title('Average Monthly Cashflow')
            a.legend()

            canvas = FigureCanvasTkAgg(f, popup)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        elif premise == 'Weekly Cashflow is negative':
            df = dataFrame
            avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
            avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
            # calculate the sum of deposits and withdrawals for each week
            week_sums = df.groupby(['Week', 'Category']).agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
            # calculate the number of weeks
            num_weeks = week_sums['Week'].nunique()
                # calculate the average deposits and withdrawals per week
            week_avgs = week_sums.groupby('Category').agg({'Deposit': 'mean', 'Withdrawal': 'mean'})
            week_avgs['Deposit'] = week_avgs['Deposit'] / num_weeks
            week_avgs['Withdrawal'] = week_avgs['Withdrawal'] / num_weeks

            f = Figure(figsize=(12,5), dpi=100)
            a = f.add_subplot(111)
            # a.plot(week_avgs['Deposit'], label='Income')    
            # a.plot(week_avgs['Withdrawal'], label='Spending')
            a.barh(week_avgs.index, week_avgs['Deposit'], label='Income')
            a.barh(week_avgs.index, week_avgs['Withdrawal'], label='Spending')
            a.set_ylabel('Category')
            a.set_xlabel('Amount')
            a.set_title('Average Weekly Cashflow')
            a.legend()

            canvas = FigureCanvasTkAgg(f, popup)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    elif type == 'Debt':

        lblIncome = ttk.Label(popup, text="Monthly Income: " + str('$%.2f' % monthly_income), font=NORM_FONT)
        lblIncome.pack(side="top", fill="x", pady=10, padx=10)

        lblDebt = ttk.Label(popup, text="Minimium Monthly Payments: " + str('$%.2f' % Monthly_debt_payment), font=NORM_FONT)
        lblDebt.pack(side="top", fill="x", pady=10, padx=10)

        #insert table of debt list
        debt_tree = ttk.Treeview(popup, columns=("name", "amount", "interest_rate", "min_payment"))
        debt_tree.heading("#0", text="ID")
        debt_tree.heading("name", text="Name")
        debt_tree.heading("amount", text="Amount")
        debt_tree.heading("interest_rate", text="Interest Rate")
        debt_tree.heading("min_payment", text="Minimum Payment (%)")

        debt_tree.column("#0", minwidth=50, anchor=tk.CENTER)
        debt_tree.column("name", minwidth=100, anchor=tk.CENTER)
        debt_tree.column("amount", minwidth=100, anchor=tk.CENTER)
        debt_tree.column("interest_rate", minwidth=100, anchor=tk.CENTER)
        debt_tree.column("min_payment", minwidth=100, anchor=tk.CENTER)

        debt_tree.pack(fill="both", expand=True, padx=10, pady=10)

        for debt in debt_list:
            debt_tree.insert("", "end", text=debt['id'], values=(debt['name'], debt['amount'], debt['interest_rate'], debt['min_payment']))

        for item in debt_tree.get_children():
            interest_rate = float(debt_tree.item(item)['values'][2])
            if interest_rate > 8:
                debt_tree.item(item, tags=('high_interest',))
        debt_tree.tag_configure('high_interest', foreground='red')
    
    elif type == 'Spending':
        # print('Spending')
        if premise == 'Essential Costs accounts for more than 0.5% of your income.':
            # create a treeview widget
            tree = ttk.Treeview(popup)

            lblIncome = ttk.Label(popup, text="Monthly Income: " + str('$%.2f' % monthly_income), font=NORM_FONT)
            lblIncome.pack(side="top", fill="x", pady=10, padx=10)

            lblEssential = ttk.Label(popup, text="Monthly Essential Spending: " + str('$%.2f' % monthly_essentialSpend), font=NORM_FONT)
            lblEssential.pack(side="top", fill="x", pady=10, padx=10)

            # define the columns of the treeview
            tree['columns'] = ('Percentage', 'Amount Spent')

            # add column headings
            tree.heading('#0', text='Category')
            tree.heading('Percentage', text='Percentage of Essential Spending')
            tree.heading('Amount Spent', text='Amount Spent')

            for category, data in essential_spendingPercentages.items():
                percentage = "{:.2%}".format(data["percentage"])
                amount = "${:.2f}".format(data["amount"])
                tree.insert("", tk.END, text=category, values=(percentage, amount))

            tree.pack(fill="both", expand=True, padx=10, pady=10)

        elif premise == 'Non-Essential Costs accounts for more than 0.3% of your income.':
            # create a treeview widget
            tree = ttk.Treeview(popup)

            lblIncome = ttk.Label(popup, text="Monthly Income: " + str('$%.2f' % monthly_income), font=NORM_FONT)
            lblIncome.pack(side="top", fill="x", pady=10, padx=10)

            lblEssential = ttk.Label(popup, text="Monthly Non-Essential Spending: " + str('$%.2f' % monthly_nonessentialSpend), font=NORM_FONT)
            lblEssential.pack(side="top", fill="x", pady=10, padx=10)

            # define the columns of the treeview
            tree['columns'] = ('Percentage', 'Amount Spent')

            # add column headings
            tree.heading('#0', text='Category')
            tree.heading('Percentage', text='Percentage of Non-Essential Spending')
            tree.heading('Amount Spent', text='Amount Spent')

            for category, data in nonessential_spendingPercentages.items():
                percentage = "{:.2%}".format(data["percentage"])
                amount = "${:.2f}".format(data["amount"])
                tree.insert("", tk.END, text=category, values=(percentage, amount))
    

            tree.pack(fill="both", expand=True, padx=10, pady=10)

    elif type == 'Chronic Overspending':
        df = dataFrame
        for c in spendList:
            if c in conclusion:
                category = c
               
                category_df = df[df['Category'] == category] # filter out all the rows that have the category we are looking for
                category_df = category_df.groupby(['Month'])['Withdrawal'].sum().reset_index() # group the dataframe by Category and sum the Withdrawal column
                avg_spending = category_df['Withdrawal'].mean() # calculate the average spending for the category
                category_df['Above_Avg'] = category_df['Withdrawal'] > avg_spending # create a new column that is True if the spending is above the average spending
                spikes = category_df[category_df['Above_Avg'] == True] # filter out all the rows that have False in the Above_Avg column

                # convert month number to month name
                category_df['Month'] = category_df['Month'].apply(lambda x: calendar.month_name[x])
                spikes['Month'] = spikes['Month'].apply(lambda x: calendar.month_name[x])

                f = Figure(figsize=(12,5), dpi=100)
                a = f.add_subplot(111)
                a.plot(category_df['Month'], category_df['Withdrawal'], label='Spending')
                a.plot(spikes['Month'], spikes['Withdrawal'], 'ro', label='Spike')
                a.axhline(avg_spending, color='black', linestyle='dashed', label='Average Monthly Spending')
                a.set_xlabel('Month')
                a.set_ylabel('Withdrawal')
                a.legend()
                a.set_title(f"Spikes in average spending in category '{category}'")

                canvas = FigureCanvasTkAgg(f, popup)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    elif type == 'Savings':
        if 'Monthly Savings' in premise:           
            lblIncome = ttk.Label(popup, text="Monthly Income: " + str('$%.2f' % monthly_income), font=NORM_FONT)
            lblIncome.pack(side="top", pady=10, padx=10)       

            lblSavings = ttk.Label(popup, text="Monthly Savings: " + str('$%.2f' % savings_per_month), font=NORM_FONT)
            lblSavings.pack(side="top", pady=10, padx=10)

            df = dataFrame
            avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
            avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
            # calculate the sum of deposits and withdrawals for each month
            month_sums = df.groupby(['Month', 'Category']).agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
            # calculate the number of months
            num_months = month_sums['Month'].nunique()
                # calculate the average deposits and withdrawals per month
            month_avgs = month_sums.groupby('Category').agg({'Deposit': 'mean', 'Withdrawal': 'mean'})
            month_avgs['Deposit'] = month_avgs['Deposit'] / num_months
            month_avgs['Withdrawal'] = month_avgs['Withdrawal'] / num_months

            f = Figure(figsize=(12,5), dpi=100)
            a = f.add_subplot(111)
            # a.plot(month_avgs['Deposit'], label='Income')
            # a.plot(month_avgs['Withdrawal'], label='Spending')
            a.barh(month_avgs.index, month_avgs['Deposit'], label='Income')
            a.barh(month_avgs.index, month_avgs['Withdrawal'], label='Spending')
            a.set_ylabel('Category')
            a.set_xlabel('Amount')
            a.set_title('Average Monthly Cashflow')
            a.legend()

            canvas = FigureCanvasTkAgg(f, popup)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        elif 'Emergency' in premise:
            lblIncome = ttk.Label(popup, text="Monthly Income: " + str('$%.2f' % monthly_income), font=NORM_FONT)
            lblIncome.pack(side="top", pady=10, padx=10)       

            lblSavings = ttk.Label(popup, text="Monthly Spendature: " + str('$%.2f' % avg_monthly_withdrawals), font=NORM_FONT)
            lblSavings.pack(side="top", pady=10, padx=10)

            lblEmergency = ttk.Label(popup, text="Emergency Fund: " + str('$%.2f' % emergency_fund), font=NORM_FONT)
            lblEmergency.pack(side="top", pady=10, padx=10)

            coverage = emergency_fund / avg_monthly_withdrawals
            lblCoverage = ttk.Label(popup, text="Max Coverage by current fund: " + str('%.2f' % coverage) + ' Months.', font=NORM_FONT)
            lblCoverage.pack(side="top", pady=10, padx=10)

        elif 'Retirement' in premise:
            yearly_income = monthly_income * 12
            optimal_retirement_fund = (yearly_income * 0.15) * (age - 25)
            currAvgDeposit = retirement_fund / (age - 25)
            lblIncome = ttk.Label(popup, text="Yearly Income: " + str('$%.2f' % yearly_income), font=NORM_FONT)
            lblIncome.pack(side="top", pady=10, padx=10) 

            lblavg = ttk.Label(popup, text="Current Average yearly Deposit: " + str('$%.2f' % currAvgDeposit), font=NORM_FONT)
            lblavg.pack(side="top", pady=10, padx=10)

            lblRetirement = ttk.Label(popup, text="Current Retirement Fund: " + str('$%.2f' % retirement_fund), font=NORM_FONT)
            lblRetirement.pack(side="top", pady=10, padx=10)

            lblOptimal = ttk.Label(popup, text="Optimal Retirement Fund: " + str('$%.2f' % optimal_retirement_fund), font=NORM_FONT)
            lblOptimal.pack(side="top", pady=10, padx=10)

            frame = tk.Frame(popup)
            frame.pack(side="top", pady=10, padx=10)

            lblnote = ttk.Label(frame, text="Note: Optimal retirement fund is calculated assuming a 15% allocation of yearly income beginning at the age of 25.", font=NORM_FONT)
            lblnote.pack(side="top", fill="x", pady=10, padx=10)

            f = Figure(figsize=(12,5), dpi=100)
            a = f.add_subplot(111)

            optimalProjections= [(yearly_income * 0.15) * (age - 25) for age in range(25, 65)]
            currPojections = [currAvgDeposit * (age - 25) for age in range(25, 65)]
            # Create x-axis values
            years = [year for year in range(25, 65)]

            a.plot(years, currPojections, label='Current Projections')
            a.plot(years, optimalProjections, label='Optimal Retirement Fund')
            a.set_title('Projections over Years for Current Average Deposit and Optimal Retirement Fund')
            a.set_xlabel('Age')
            a.set_ylabel('Dollars')
            a.legend()

            # Add annotations for current age and retirement fund
            a.annotate('Current Age',
                    xy=(age, currAvgDeposit * (age - 25)),
                    xytext=(age + 2, currAvgDeposit * (age - 25) + 5000),
                    arrowprops=dict(facecolor='black', shrink=0.05))

            # Add vertical lines for current age and retirement age
            a.axvline(age, color='gray', linestyle='--')
            # a.axvline(age_retirement, color='gray', linestyle='--')

            canvas = FigureCanvasTkAgg(f, frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack(padx=10, pady=10)
    popup.mainloop()

def viewFileSpecs():
    popup = tk.Tk()
    style = ttk.Style(popup)
    style.theme_create('modern1', parent='default')
    style.theme_settings('modern1', getTheme())
    style.theme_use('modern1')
    popup.wm_title("File Requirements")

    lbl = ttk.Label(popup, text='File Requirements: ', font=LARGE_FONT, anchor='center', justify='center')
    lbl.pack(side="top", fill="x", pady=10, padx=10)

    fileSpecs = """
        Users must upload a csv file containing account activity. (Commonly found on bank websites). 
        
        The Datasets folder contains 4 preprocessed data sets (Data-1, Data-2, Data-3, Data-4) as well
        as an unprocessed file (Randomize.csv). 
            NOTE: if Randomize.csv is selected, the program will randomly assign categories for withdrawals and deposits. 

        Predefined Categories:
            spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
                        'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
            incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Trading']

        The User can also select their own income statement if their file has the following column order: (Data, Transaction Description, Withdrawal, Deposit, Balance) and DOES NOT contain any column HEADERS. 
        
        If successfully processed, 'userData.csv' will be created in the Datasets folder for future user. 
            NOTE: Once again your spending/deposit categories will be randomized. 

        If the file is successfully processed then the Expert system will initialize and the user will be taken to the blackboard. Otherwise UserData.csv will be deleted. 
    """

    label = tk.Label(popup, text=fileSpecs, justify="left")
    label.pack(pady=10, padx=10)

    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack(padx=10, pady=10)

    popup.mainloop()

def preprocess(filename):
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
    file = filename.split('/')[-1]
    # print('filename: ', file)
    df = pd.read_csv(filename)
    expected_headers = ['Date', 'Withdrawal', 'Deposit', 'Balance', 'Week', 'Month', 'Year', 'Category']
    path = os.path.join(os.getcwd(), 'Datasets')
    if 'Budgeting-Expert-System' not in path:
        popupmsg('Please restart the program after opening the Budgeting-Expert-System folder in your IDE')
        return
    print('path: ', path)
    try:
        # if set(df.columns.tolist()) == set(expected_headers):

        if file == 'Randomize.csv' or file == 'userData.csv':
            # print('Randomizing data')
            df = pd.read_csv(filename, names=headerlist) #assign column names 
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

            monthly_income = avg_monthly_deposits
            total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()
        
        elif os.path.exists(path + '/' + file):
            print('File already exists')
            current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
            total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
            total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
            
            avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
            avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
            savings_per_week = avg_weekly_deposits - avg_weekly_withdrawals
            
            avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
            avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
            savings_per_month = avg_monthly_deposits - avg_monthly_withdrawals
            
            monthly_income = avg_monthly_deposits

            total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

        else:
            print('File does not exist')
            initialheaderlist = ['Date', 'desc', 'Withdrawal', 'Deposit', 'Balance']
            data = pd.read_csv(filename, names=initialheaderlist)
            data.drop('desc', inplace=True, axis=1)
            if os.path.exists(path + '/userData.csv'):
                os.remove(path + '/userData.csv')
            data.to_csv(path + '/userData.csv', index=False, header=False) 
            
            print('Randomizing data')
            df = pd.read_csv('Datasets/userData.csv', names=headerlist) #assign column names 
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

            monthly_income = avg_monthly_deposits
            total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()
    except Exception as e:
        popupmsg('File Processing Error. Please try again. Errortype: \n' +str(e))
        if os.path.exists(path +'/userData.csv'):
            os.remove(path +'/userData.csv')
    return df

def getSpendingPercentages(df):
    global essential_spendingPercentages, nonessential_spendingPercentages, essentialList, nonessentialList
    spending_percentages = {}
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    df = df[df['Withdrawal'] != 0]
    categories = df['Category'].unique()
    for category in categories:
        category_spending = df[df['Category'] == category]['Withdrawal'].sum()
        spending_percentages[category] = {
            'percentage': category_spending / total_deposited,
            'amount': category_spending
        }

    df_Essential = df[df['Category'].isin(essentialList)]
    df_Nonessential = df[df['Category'].isin(nonessentialList)]
    essential_spending = df_Essential['Withdrawal'].sum()
    nonessential_spending = df_Nonessential['Withdrawal'].sum()

    spending_percentages['Essential Costs'] = {
        'percentage': essential_spending / total_spent,
        'amount': essential_spending
    }
    spending_percentages['Non-Essential Costs'] = {
        'percentage': nonessential_spending / total_spent,
        'amount': nonessential_spending
    }

    # create a dictionary for essential and nonessential spending percentages
    essential_spendingPercentages = {}
    nonessential_spendingPercentages = {}
    for category in essentialList:
        category_spending = df[df['Category'] == category]['Withdrawal'].sum()
        essential_spendingPercentages[category] = {
            'percentage': category_spending / essential_spending,
            'amount': category_spending
        }
    for category in nonessentialList:
        category_spending = df[df['Category'] == category]['Withdrawal'].sum()
        nonessential_spendingPercentages[category] = {
            'percentage': category_spending / nonessential_spending,
            'amount': category_spending
        }

def getSavingPercentages(df):
    global saving_percentages
    saving_percentages = {}
    total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
    total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
    df = df[df['Deposit'] != 0]
    categories = df['Category'].unique()
    for category in categories:
        category_saving = df[df['Category'] == category]['Deposit'].sum()
        saving_percentages[category] = {
            'percentage': category_saving / total_deposited,
            'amount': category_saving
        }

class ESapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs) 

        # set the root style to the theme from getTheme()
        self.style = ttk.Style()
        self.style.theme_create('modern', parent='default')
        self.style.theme_settings('modern', getTheme())
        self.style.theme_use('modern')
        
        # tk.Tk.iconbitmap(self,default='clienticon.ico')
        tk.Tk.wm_title(self, "Financial Budget Expert System")
        self.geometry("500x300")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(background='dark grey')

        self.frames = {}

        for F in (StartPage, statsPage, GraphPage, DebtPage, filePage, inferencesPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        global filename, allInferences
        if cont == DebtPage:
            self.geometry("800x500")
        elif cont == GraphPage:
            self.geometry("1100x850")
        elif cont == filePage:
            self.geometry("1050x300")
        elif cont == statsPage:
            if allInferences == []:
                self.select_file()
            self.geometry("1100x650")        
        frame = self.frames[cont]
        frame.tkraise()
    
    def select_file(self):
        global filename, allInferences, dataFrame, debt_list, statusDict
        filetypes = (
                    ('CSV files', '*.csv'),
                    # ('All files', '*.*')
        )
        #open at path to datasets folder
        path = os.path.join(os.getcwd(), 'Datasets')
        print('path: ', path)

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=path,
            filetypes=filetypes)
        
        df = preprocess(filename)
        getSpendingPercentages(df)
        getSavingPercentages(df)
        # print(spending_percentages)
        dataFrame = df
        self.expert_system = ExpertSystem(df, debt_list)
        self.expert_system.checkBudget()
        self.expert_system.eval_Savings()
        self.expert_system.checkCashflow()
        self.expert_system.checkforSpikes()
        self.expert_system.evaluateDebt()
        self.expert_system.makeInferences()
        allInferences = self.expert_system.getInferences()
        allInferences.sort(key=lambda x: x.severity, reverse=True)
        # print('\nAll Inferences: \n')
        # for i in allInferences:
        #     # if i.type == 'Spike':
        #         print(i.type, 'Inference: Premise:', i.premise, '\nRecommendation:', i.conclusion, '\nSeverity:',i.severity , '\n')
        # print('Facts: \n')
        # for i in self.expert_system.facts:
        #     print(i.name, i.value)
        # print('Rules: \n')
        # for i in self.expert_system.rules:
        #     print(i.type, i.premise, i.conclusion)

        inferenceTypes = ["Spending", "Chronic Overspending", "Debt", "Savings", "Cashflow"]

        for inferenceType in inferenceTypes:
            #check if allinferencetypes has any inferences of that type
            if not any(i.type == inferenceType for i in allInferences):
                continue

            most_severe = 0  # keep track of the most severe inference
            for i in allInferences:
                if i.type == inferenceType:
                    if i.severity > most_severe:
                        most_severe = i.severity
        
            # update the label based on the most severe inference
            if most_severe == 1:
                statusDict[inferenceType] = "Managable"
            elif most_severe == 2:
                statusDict[inferenceType] = "Moderate"
            elif most_severe == 3:
                statusDict[inferenceType] = "Alarming"
            elif most_severe == 4:
                statusDict[inferenceType] = "Critical"

        # print(statusDict)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global age, retirement_fund, emergency_fund 
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("Welcome to the budgeting Expert System"), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text=("Please begin by entering the following information"), font=NORM_FONT)
        label1.pack(pady=10,padx=10)

        input_frame = tk.Frame(self)
        input_frame.pack(fill="both", expand=True, padx=5, pady=5, side=tk.TOP)

        label2 = tk.Label(input_frame, text=("Age:"), font=NORM_FONT)
        label2.grid(row=0, column=0, padx=10, pady=10)

        age = tk.Entry(input_frame)
        age.grid(row=0, column=1, padx=10, pady=10)

        label3 = tk.Label(input_frame, text=("Retirement Fund:"), font=NORM_FONT)
        label3.grid(row=1, column=0, padx=10, pady=10)

        retirement_fund = tk.Entry(input_frame)
        retirement_fund.grid(row=1, column=1, padx=10, pady=10)

        label4 = tk.Label(input_frame, text=("Emergency Fund:"), font=NORM_FONT)
        label4.grid(row=2, column=0, padx=10, pady=10)

        emergency_fund = tk.Entry(input_frame)
        emergency_fund.grid(row=2, column=1, padx=10, pady=10)

        button = ttk.Button(input_frame, text=" Continue ",
                            command=lambda: self.set_variables_and_show_frame(controller, DebtPage))
        button.grid(row=3, column=1, padx=10, pady=10)

        button2 = ttk.Button(input_frame, text=" Exit Program ",
                            command=quit)
        button2.grid(row=3, column=0, padx=10, pady=10)

    def set_variables_and_show_frame(self, controller, next_frame):
        global age, retirement_fund, emergency_fund 
        if age.get() == '' or age.get().isnumeric() == False:
            popupmsg("Please enter a valid age.")
            return
        elif retirement_fund.get() == '' or retirement_fund.get().isnumeric() == False:
            popupmsg("Please enter a valid retirement fund.")
            return
        elif emergency_fund.get() == '' or emergency_fund.get().isnumeric() == False:
            popupmsg("Please enter a valid emergency fund.")
            return
        age = float(age.get())
        retirement_fund = float(retirement_fund.get() or 0)
        emergency_fund = float(emergency_fund.get() or 0)
        controller.show_frame(next_frame)

class DebtPage(tk.Frame):

    def __init__(self, parent, controller):
        global debt_list
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Debt List", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text=" Continue ",
                            command=lambda: controller.show_frame(filePage))
        button.pack()

        input_frame = tk.Frame(self)
        input_frame.pack(fill="both", expand=True)
        # input_frame.pack(side="top", fill="x", pady=10)

        # Create labels and entry widgets for the debt parameters
        name_label = tk.Label(input_frame, text="Account:")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        amount_label = tk.Label(input_frame, text="Debt Amount:")
        amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        interest_rate_label = tk.Label(input_frame, text="Interest Rate (%):")
        interest_rate_label.grid(row=2, column=0, padx=10, pady=10)
        self.interest_rate_entry = tk.Entry(input_frame)
        self.interest_rate_entry.grid(row=2, column=1, padx=10, pady=10)

        min_payment_label = tk.Label(input_frame, text="Minimum Payment (%):")
        min_payment_label.grid(row=3, column=0, padx=10, pady=10)
        self.min_payment_entry = tk.Entry(input_frame)
        self.min_payment_entry.grid(row=3, column=1, padx=10, pady=10)

        #create a button to add use default_debt_list and populate the treeview
        default_button = ttk.Button(input_frame, text="Load Preset Values", command=self.use_default_debt_list)
        default_button.grid(row=2, column=2, columnspan=4, padx=10, pady=10)

        # Create a button to add a new debt to the list
        add_button = ttk.Button(input_frame, text="Add Debt", command=self.add_debt)
        add_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        # Create a frame for the debt list
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10)) #fill both means it will fill the entire frame, expand true means it will expand to fill the entire frame

        # Create a Treeview widget to display the debt list
        self.debt_treeview = ttk.Treeview(list_frame, columns=("name", "amount", "interest_rate", "min_payment"))
        self.debt_treeview.heading("#0", text="ID")
        self.debt_treeview.heading("name", text="Account")
        self.debt_treeview.heading("amount", text="Debt Amount")
        self.debt_treeview.heading("interest_rate", text="Interest Rate (%)")
        self.debt_treeview.heading("min_payment", text="Minimum Payment (%)")
        #center all columns
        self.debt_treeview.column("#0", anchor="center", width=50)
        self.debt_treeview.column("name", anchor="center", width=100)
        self.debt_treeview.column("amount", anchor="center", width=100)
        self.debt_treeview.column("interest_rate", anchor="center", width=100)
        self.debt_treeview.column("min_payment", anchor="center", width=100)
        self.debt_treeview.pack(fill="both", expand=True)

        # Initialize the debt list
        self.debt_list = debt_list
        self.next_debt_id = 1
    
    def use_default_debt_list(self):
        global default_debt_list, debt_list
        debt_list = default_debt_list
        self.debt_list = default_debt_list
        self.update_debt_list()

    def add_debt(self):

        if self.name_entry.get() == '':
            popupmsg("Please enter all fields.")
            return
        elif self.amount_entry.get() == '' or self.amount_entry.get().isnumeric() == False:
            popupmsg("Please enter a valid amount for debt.")
            return
        elif self.interest_rate_entry.get() == '' or self.interest_rate_entry.get().isnumeric() == False:
            popupmsg("Please enter a valid rate for interest.")
            return
        elif self.min_payment_entry.get() == '' or self.min_payment_entry.get().isnumeric() == False:
            popupmsg("Please enter a valid amount for minimum payment.")
            return
        # Get the input values
        name = self.name_entry.get()
        amount = float(self.amount_entry.get())
        interest_rate = float(self.interest_rate_entry.get())
        min_payment = float(self.min_payment_entry.get())

        # Add the new debt to the list
        self.debt_list.append({'id': self.next_debt_id, 'name': name, 'amount': amount, 'interest_rate': interest_rate, 'min_payment': min_payment})
        self.next_debt_id += 1

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.interest_rate_entry.delete(0, tk.END)
        self.min_payment_entry.delete(0, tk.END)

        # Update the debt list display
        self.update_debt_list()

    def update_debt_list(self):
        # Clear the existing items in the Treeview
        self.debt_treeview.delete(*self.debt_treeview.get_children())

        # Insert the updated debt list into the Treeview
        for debt in self.debt_list:
            self.debt_treeview.insert("", "end", text=debt['id'], values=(debt['name'], debt['amount'], debt['interest_rate'], debt['min_payment']))

        # print(self.debt_list)

class filePage(tk.Frame):

    def __init__(self, parent, controller):
        global filename
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="File Select", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        lbl_selectFile = ttk.Label(self, text="Select a file to initialize the Expert system:")
        lbl_selectFile.pack(pady=10,padx=10)

        lbl_warn = ttk.Label(self, text="NOTE: Ensure the Budgeting-Expert-System folder is not opened within another folder after importing/uncompressing in your IDE.")
        lbl_warn.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text="Open a File",
                            # command=lambda: controller.startup(InferencesPage))
                            command=lambda: controller.show_frame(statsPage))
        button1.pack(padx=10, pady=15)

        btn = ttk.Button(self, text="View File Specifications", command=viewFileSpecs)
        btn.pack(pady=10,padx=10)

        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button2.pack(padx=10, pady=5)

class statsPage(tk.Frame):

    def __init__(self, parent, controller):
        global filename, essential_spendingPercentages, nonessential_spendingPercentages
        global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals
        global savings_per_week, savings_per_month, total_deposited, total_spent
        global Weekly_essentialSpend, Weekly_nonessentialSpend, monthly_essentialSpend, monthly_nonessentialSpend
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Account Activity", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="Show System Facts",
                            command= lambda: self.showFinancialStats())
        button3.pack(padx=10, pady=5)

        button4 = ttk.Button(self, text="View Graphs",
                            command=lambda: controller.show_frame(GraphPage))
        button4.pack(padx=10, pady=5)

        button5 = ttk.Button(self, text="View Analysis",
                            command=lambda: controller.show_frame(inferencesPage))
        button5.pack(padx=10, pady=5)

        button2 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button2.pack(padx=10, pady=10)

    def showFinancialStats(self):
        global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals
        global savings_per_week, savings_per_month, total_deposited, total_spent, Monthly_debt_payment
        global Weekly_essentialSpend, Weekly_nonessentialSpend, monthly_essentialSpend, monthly_nonessentialSpend
        global saving_percentages
        if hasattr(self, 'statsFrame'): 
            print("statsFrame already exists")
            return
        
        if hasattr(self, 'spendFrame'):
            print("spendFrame already exists")
            return
        
        #create spending percentages frame
        self.spendFrame = ttk.Frame(self)
        self.spendFrame.pack(padx=5, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

        lbl = ttk.Label(self.spendFrame, text="SPENDING OVERVIEW")
        lbl.pack(padx=10, pady=10)

        columns = ("Category", "Percentage", "Amount")
        table = ttk.Treeview(self.spendFrame, columns=columns, show="headings")
        table.heading("#1", text="Category")
        table.heading("#2", text="Percentage")
        table.heading("#3", text="Amount")
        table.column("#1", width=100, anchor='center')
        table.column("#2", width=80, anchor='center')
        table.column("#3", width=80, anchor='center')
        table.pack(expand=True, side=tk.LEFT, fill=tk.BOTH, padx=5, pady=10)

        essential_spending_percentages = essential_spendingPercentages.items()
        nonessential_spending_percentages = nonessential_spendingPercentages.items()

        for category, values in essential_spending_percentages:
            percentage = values['percentage'] * 100
            amount = values['amount']
            table.insert('', tk.END, text=category, values=(category, '%.2f %%' % percentage, '$%.2f' % amount))

        for category, values in nonessential_spending_percentages:
            percentage = values['percentage'] * 100
            amount = values['amount']
            table.insert('', tk.END, text=category, values=(category, '%.2f %%' % percentage, '$%.2f' % amount))

        #create stats frame
        self.statsFrame = ttk.Frame(self)
        self.statsFrame.pack(padx=5, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

        lbl = ttk.Label(self.statsFrame, text="ACCOUNT OVERVIEW")
        lbl.pack(padx=10, pady=10)

        # Create a treeview
        tree = ttk.Treeview(self.statsFrame)
        
        # Define columns for the treeview
        tree["columns"] = ("value")
        tree.column("value", width=80, anchor="center")
        
        # Add headers to the columns
        tree.heading("#0", text="Variable")
        tree.heading("value", text="Value")

        # Pack the treeview
        tree.pack(expand=True, side=tk.LEFT, fill=tk.BOTH)
        
        # Add values to the treeview
        tree.insert("", tk.END, text="Average Weekly Deposits", values=('$%.2f' % avg_weekly_deposits,))
        tree.insert("", tk.END, text="Average Weekly Withdrawals", values=('$%.2f' % avg_weekly_withdrawals,))
        tree.insert("", tk.END, text="Average Monthly Deposits", values=('$%.2f' % avg_monthly_deposits,))
        tree.insert("", tk.END, text="Average Monthly Withdrawals", values=('$%.2f' % avg_monthly_withdrawals,))
        tree.insert("", tk.END, text="Savings Per Week", values=('$%.2f' % savings_per_week,))
        tree.insert("", tk.END, text="Savings Per Month", values=('$%.2f' % savings_per_month,))
        tree.insert("", tk.END, text="Total Deposited", values=('$%.2f' % total_deposited,))
        tree.insert("", tk.END, text="Total Spent", values=('$%.2f' % total_spent,))
        tree.insert("", tk.END, text="Weekly Essential Spending", values=('$%.2f' % Weekly_essentialSpend,))
        tree.insert("", tk.END, text="Weekly Non-Essential Spending", values=('$%.2f' % Weekly_nonessentialSpend,))
        tree.insert("", tk.END, text="Monthly Essential Spending", values=('$%.2f' % monthly_essentialSpend,))
        tree.insert("", tk.END, text="Monthly Non-Essential Spending", values=('$%.2f' % monthly_nonessentialSpend,))
        tree.insert("", tk.END, text="Minimum Monthly Debt Cost", values=('$%.2f' % Monthly_debt_payment,))
        
        #create savings frame
        self.savingsFrame = ttk.Frame(self)
        self.savingsFrame.pack(padx=5, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)

        lbl = ttk.Label(self.savingsFrame, text="SAVING OVERVIEW")
        lbl.pack(padx=10, pady=10)

        # Create a treeview
        columns = ("Category", "Percentage", "Amount")
        tree = ttk.Treeview(self.savingsFrame, columns=columns, show="headings")
        tree.heading("#1", text="Category")
        tree.heading("#2", text="Percentage")
        tree.heading("#3", text="Amount")
        tree.column("#1", width=100, anchor="center")
        tree.column("#2", width=80, anchor="center")
        tree.column("#3", width=80, anchor="center")
        tree.pack(expand=True, side=tk.LEFT, fill=tk.BOTH, padx=5, pady=10)

        saving_percentages = saving_percentages.items()
        # Add values to the treeview
        for category, values in saving_percentages:
            percentage = values['percentage'] * 100
            amount = values['amount']
            tree.insert('', tk.END, text=category, values=(category, '%.2f %%' % percentage, '$%.2f' % amount))

        

    def showInferences(self):
        global allInferences
        if len(allInferences) == 0:
            return
        
        # check if the table already exists
        if hasattr(self, "inferenceTable"):
            self.inferenceTable.destroy()

        columns = ("Type", "Premise", "Recommendation")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Premise", text="Premise")
        tree.heading("Recommendation", text="Recommendation")
        tree.pack(expand=True, side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # save the table to the instance variable
        self.inferenceTable = tree
        
        for i in allInferences:
            if i.severity == 1:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Managable",))
            elif i.severity == 2:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Moderate",))
            elif i.severity == 3:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Alarming",))
            elif i.severity == 4:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Critical",))

        tree.tag_configure("Critical", background="red")
        tree.tag_configure("Alarming", background="orange")
        tree.tag_configure("Moderate", background="yellow")
        tree.tag_configure("Managable", background="white")

        def selectRecord(event):
            item = tree.focus()
            values = tree.item(item, "values")
            type, premise, recommendation = values

            viewInference(type, premise, recommendation)
    
        tree.bind("<Double-1>", selectRecord)
        tree["displaycolumns"] = ("Type", "Premise")
    
class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="GRAPHS", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Account Activity Page",
                            command=lambda: controller.show_frame(statsPage))
        button.pack(padx=10, pady=5)

        btn = ttk.Button(self, text="Analysis Page",
                            command=lambda: controller.show_frame(inferencesPage))
        btn.pack(padx=10, pady=5)

        btnFrame = ttk.Frame(self)
        btnFrame.pack(padx=10, pady=10, side=tk.TOP)

        button2 = ttk.Button(btnFrame, text="View Spending",
                            command=lambda: self.viewSpending())
        button2.grid(row=0, column=0, padx=15, pady=8)

        button3 = ttk.Button(btnFrame, text="View Income",
                            command=lambda: self.viewIncome())
        button3.grid(row=0, column=1, padx=15, pady=8)

        button4 = ttk.Button(btnFrame, text="View Cashflow",
                            command=lambda: self.viewCashflow())
        button4.grid(row=0, column=2, padx=15, pady=8)

        button5 = ttk.Button(btnFrame, text="View Weekly Averages",
                            command=lambda: self.weeklyAvg())
        button5.grid(row=1, column=0, padx=15, pady=8)

        button6 = ttk.Button(btnFrame, text="View Monthly Averages",
                            command=lambda: self.monthlyAvg())
        button6.grid(row=1, column=1, padx=15, pady=8)

        button7 = ttk.Button(btnFrame, text="View Balance",
                            command=lambda: self.viewBalance())
        button7.grid(row=1, column=2, padx=15, pady=8)

        button8 = ttk.Button(btnFrame, text="View Retirement Projection",
                            command=lambda: self.viewRetirement())
        button8.grid(row=3, column=1, padx=15, pady=8)

        self.canvas = None


    def viewRetirement(self):
        if age < 25:
            popupmsg("You must be at least 25 years old to project your retirement fund.")
            return
        
        yearly_income = monthly_income * 12
        optimal_retirement_fund = (yearly_income * 0.15) * (age - 25)
        currAvgDeposit = retirement_fund / (age - 25)

        # lblnote = ttk.Label(frame, text="Note: Optimal retirement fund is calculated assuming a 15% allocation of yearly income beginning at the age of 25.", font=NORM_FONT)
        # lblnote.pack(side="top", fill="x", pady=10, padx=10)

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111)

        optimalProjections= [(yearly_income * 0.15) * (age - 25) for age in range(25, 65)]
        currPojections = [currAvgDeposit * (age - 25) for age in range(25, 65)]
        # Create x-axis values
        years = [year for year in range(25, 65)]

        a.plot(years, currPojections, label='Current Projections')
        a.plot(years, optimalProjections, label='Optimal Retirement Fund')
        a.set_title('Projections over Years for Current Average Deposit and Optimal Retirement Fund')
        a.set_xlabel('Age')
        a.set_ylabel('Dollars')
        a.legend()

        # Add annotations for current age and retirement fund
        a.annotate('Current Age',
                xy=(age, currAvgDeposit * (age - 25)),
                xytext=(age + 2, currAvgDeposit * (age - 25) + 5000),
                arrowprops=dict(facecolor='black', shrink=0.05))

        # Add vertical lines for current age and retirement age
        a.axvline(age, color='gray', linestyle='--')

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



    def viewSpending(self):
        global dataFrame

        df = dataFrame
        df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
        df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
        df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
        df = df.reset_index() # reset the index

        f = Figure(figsize=(10,7), dpi=100) #dpi = dots per inch
        a = f.add_subplot(111)
        a.barh(df['Category'], df['Withdrawal'])
        a.set_xlabel('Category')
        a.set_ylabel('Spending')

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
    def viewIncome(self):
        global dataFrame

        df = dataFrame
        df = df[df['Deposit'] != 0]
        df = df.groupby(['Category']).sum()
        df = df.sort_values(by=['Deposit'], ascending=False)
        df = df.reset_index()

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111) 
        a.bar(df['Category'], df['Deposit'])
        a.set_xlabel('Category')
        a.set_ylabel('Income')

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def viewCashflow(self):
        global dataFrame

        df = dataFrame
        df = df.groupby(['Week']).sum() # group the dataframe by Date and sum the Deposit and Withdrawal columns
        df = df.sort_values(by=['Week'], ascending=True) # sort the dataframe by Date column in ascending order
        df = df.reset_index() # reset the index
        # print(df)

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(df['Week'], df['Deposit'], label='Income')
        a.plot(df['Week'], df['Withdrawal'], label='Spending')
        a.set_xlabel('Week')
        a.set_ylabel('Amount')
        a.set_title('Cashflow')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def weeklyAvg(self):
        global dataFrame, savings_per_week

        df = dataFrame
        avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
        avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
        # calculate the sum of deposits and withdrawals for each week
        week_sums = df.groupby(['Week', 'Category']).agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
        # calculate the number of weeks
        num_weeks = week_sums['Week'].nunique()
            # calculate the average deposits and withdrawals per week
        week_avgs = week_sums.groupby('Category').agg({'Deposit': 'mean', 'Withdrawal': 'mean'})
        week_avgs['Deposit'] = week_avgs['Deposit'] / num_weeks
        week_avgs['Withdrawal'] = week_avgs['Withdrawal'] / num_weeks

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111)
        # a.plot(week_avgs['Deposit'], label='Income')    
        # a.plot(week_avgs['Withdrawal'], label='Spending')
        a.barh(week_avgs.index, week_avgs['Deposit'], label='Income')
        a.barh(week_avgs.index, week_avgs['Withdrawal'], label='Spending')
        a.set_ylabel('Category')
        a.set_xlabel('Amount')
        a.set_title('Average Weekly Cashflow')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def monthlyAvg(self):
        global dataFrame, savings_per_month
        df = dataFrame
        avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
        avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
        # calculate the sum of deposits and withdrawals for each month
        month_sums = df.groupby(['Month', 'Category']).agg({'Deposit': 'sum', 'Withdrawal': 'sum'}).reset_index()
        # calculate the number of months
        num_months = month_sums['Month'].nunique()
            # calculate the average deposits and withdrawals per month
        month_avgs = month_sums.groupby('Category').agg({'Deposit': 'mean', 'Withdrawal': 'mean'})
        month_avgs['Deposit'] = month_avgs['Deposit'] / num_months
        month_avgs['Withdrawal'] = month_avgs['Withdrawal'] / num_months

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111)
        # a.plot(month_avgs['Deposit'], label='Income')
        # a.plot(month_avgs['Withdrawal'], label='Spending')
        a.barh(month_avgs.index, month_avgs['Deposit'], label='Income')
        a.barh(month_avgs.index, month_avgs['Withdrawal'], label='Spending')
        a.set_ylabel('Category')
        a.set_xlabel('Amount')
        a.set_title('Average Monthly Cashflow')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def viewBalance(self):
        global dataFrame

        df = dataFrame
        df = df[['Date', 'Balance']]
        df = df.set_index('Date')
        df = df.sort_index()

        df = df.iloc[::25, :]

        f = Figure(figsize=(12,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(df['Balance'], label='Balance')
        a.set_xlabel('Date')
        a.set_ylabel('Amount')
        a.set_title('Balance')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class inferencesPage(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Analysis Overview", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Back to Stats",
                            command=lambda: controller.show_frame(statsPage))
        button.pack()

        button3 = ttk.Button(self, text="Show Analysis",
                            command= lambda: self.showInferences())
        button3.pack(padx=10, pady=5)

    def showInferences(self):
        global allInferences, statusDict
        if len(allInferences) == 0:
            return
        
        # check if the notebook already exists
        if hasattr(self, "inferenceNotebook"):
            # self.inferenceNotebook.destroy()
            return

        #check if summary frame already exists
        if hasattr(self, "summaryFrame"):
            # self.summaryFrame.destroy()
            return
                #create summary frame
        
        self.sumFrame = tk.Frame(self)
        self.sumFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        lbl = ttk.Label(self.sumFrame, text=("Summary"), font=LARGE_FONT)
        lbl.pack(pady=5,padx=10)
        
        # create the treeview
        columns = ("Category", "Status", "Total Suggestions", "Most Severe Inference")
        self.sumTree = ttk.Treeview(self.sumFrame, columns=columns, show="headings")
        self.sumTree.heading("Category", text="Category")
        self.sumTree.heading("Status", text="Status")
        self.sumTree.heading("Total Suggestions", text="Total Suggestions")
        self.sumTree.heading("Most Severe Inference", text="Most Severe Inference")
        self.sumTree.column("Category", width=100, anchor=tk.CENTER)
        self.sumTree.column("Status", width=100, anchor=tk.CENTER)
        self.sumTree.column("Total Suggestions", width=100, anchor=tk.CENTER)
        self.sumTree.column("Most Severe Inference", width=100, anchor=tk.CENTER)
        self.sumTree.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        
        # sort the categories by status
        categories = sorted(statusDict.keys(), key=lambda x: {"Optimal": 0, "Managable": 1, "Moderate": 2, "Alarming": 3, "Critical": 4}[statusDict[x]], reverse=True)
        
        # populate the treeview with data for each category
        for category in categories:
            count = sum(i.type == category for i in allInferences)
            most_severe = max([i.severity for i in allInferences if i.type == category] + [0])
            
            self.sumTree.insert("", "end", values=(category, statusDict[category], count, most_severe), tags=(statusDict[category],))
            self.sumTree.tag_configure("Optimal", background="light Green")
            self.sumTree.tag_configure("Managable", background="light yellow")
            self.sumTree.tag_configure("Moderate", background="yellow")
            self.sumTree.tag_configure("Alarming", background="orange")
            self.sumTree.tag_configure("Critical", background="red")
        
        # make the table sortable by clicking on the column headers
        for col in columns:
            self.sumTree.heading(col, text=col, command=lambda c=col: operator.sortby(self.sumTree, c, 0))
            
        # set the default sort order to be by status
        self.sumTree.set("", "Status")
        self.sumTree['displaycolumns'] = ["Category", "Status", "Total Suggestions",]
        self.sumTree.configure(height=len(self.sumTree.get_children()))

        # create the notebook

        lblInferences = ttk.Label(self, text=("Recommendations"), font=LARGE_FONT)
        lblInferences.pack(pady=5,padx=10)
        
        lbl1 = ttk.Label(self, text=("Double-Click on an recommendation to view explanation."), font=NORM_FONT)
        lbl1.pack(pady=5,padx=5)

        self.inferenceNotebook = ttk.Notebook(self)
        self.inferenceNotebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        inferenceTypes = ["Spending", "Chronic Overspending", "Debt", "Savings", "Cashflow"]

        for inferenceType in inferenceTypes:
            #check if allinferencetypes has any inferences of that type
            if not any(i.type == inferenceType for i in allInferences):
                continue

            # create a frame for the tab
            frame = tk.Frame(self.inferenceNotebook)
            frame.pack(expand=True, fill=tk.BOTH)

            label = ttk.Label(frame, text=(inferenceType + " Status: "), font=LARGE_FONT)
            label.pack(pady=10,padx=10)


            most_severe = 0  # keep track of the most severe inference
            for i in allInferences:
                if i.type == inferenceType:
                    if i.severity > most_severe:
                        most_severe = i.severity
                        
            # update the label based on the most severe inference
            if most_severe == 0:
                label["text"] += "Optimal"
                label['background'] = "light Green"
            elif most_severe == 1:
                label["text"] += "Managable"
                # statusDict[inferenceType] = "Managable"
                label["background"] = "light yellow"
            elif most_severe == 2:
                label["text"] += "Moderate"
                # statusDict[inferenceType] = "Moderate"
                label["background"] = "yellow"
            elif most_severe == 3:
                label["text"] += "Alarming"
                # statusDict[inferenceType] = "Alarming"
                label["background"] = "orange"
            elif most_severe == 4:
                label["text"] += "Critical"
                # statusDict[inferenceType] = "Critical"
                label["background"] = "red"

            columns = ("Type", "Premise", "Recommendation")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.heading("Type", text="Type")
            tree.heading("Premise", text="Premise")
            tree.heading("Recommendation", text="Recommendation")
            tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=5, side=tk.LEFT)

            for i in allInferences:
                if i.type == inferenceType:
                    if i.severity == 1:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Managable",))
                    elif i.severity == 2:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Moderate",))
                    elif i.severity == 3:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Alarming",))
                    elif i.severity == 4:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Critical",))

            tree.tag_configure("Critical", background="red")
            tree.tag_configure("Alarming", background="orange")
            tree.tag_configure("Moderate", background="yellow")
            tree.tag_configure("Managable", background="white")
            tree.configure(height=len(tree.get_children()))

            def selectRecord(event):
                # get the the active frame in the notebook
                frame = self.inferenceNotebook.nametowidget(self.inferenceNotebook.select())
                # get the treeview in the active frame
                tree = frame.winfo_children()[1]
                item = tree.focus()
                values = tree.item(item, "values")
                type, premise, recommendation = values

                viewInference(type, premise, recommendation)


            tree.bind("<Double-1>", selectRecord)
            tree["displaycolumns"] = ("Recommendation")
            
            # add the tab to the notebook
            self.inferenceNotebook.add(frame, text=' ' + inferenceType + ' ')

            # create a scrollbar for each table in each tab
            scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scroll.set)

class ExpertSystem:
    def __init__(self, df, debt_list):
        self.df = df
        self.debt_list = debt_list
        self.rules = []
        self.facts = []
        self.inferences = []
        self.types = ['Spending', 'Savings', 'Debt', 'Cashflow', 'Chronic Overspending']

    def add_rule(self, type, premise, conclusion, severity):
        self.rules.append(Rule(type, premise, conclusion, severity))

    def get_rules(self):
        return self.rules

    def add_inference(self, type, premise, conclusion, severity):
        self.inferences.append(Inference(type, premise, conclusion, severity))

    def evaluateDebt(self):
        global monthly_income, Monthly_debt_payment, debt_list
        high_interest_debt = []
        Monthly_debt_payment = 0

        self.debt_list = debt_list
        # print('Debt List: ')
        # print(self.debt_list)

        for debt in self.debt_list:
            Monthly_debt_payment += (debt['amount'] * debt['min_payment'] / 100) 
            if debt['interest_rate'] >= 8: # if interest rate is greater than or equal to 8%
                high_interest_debt.append(debt)

        # print('Monthly Debt Payment: ' + str(Monthly_debt_payment))
        
        dti = Monthly_debt_payment / monthly_income
        
        if high_interest_debt:
            self.add_rule('Debt','high_interest_debt', 'High-interest debt detected, prioritize paying off debts with an interest rate greater than 8%.', 2)
            self.add_fact('Debt','high_interest_debt', True)
        
        if Monthly_debt_payment > 0.5 * monthly_income:
            self.add_rule('Debt','High_DTI', 'Your debt-to-income ratio is greater than 50% of monthly income, you must reduce this ratio for optmal financial health. DTI: ' + str('%.2f' % dti), 3)
            self.add_fact('Debt','High_DTI', True)
       
        elif Monthly_debt_payment > 0.3 * monthly_income and Monthly_debt_payment <= 0.5 * monthly_income:
            self.add_rule('Debt','Moderate_DTI', 'Your debt-to-income ratio is sustainable but leaves little to invest. DTI:' + str('%.2f' % dti), 2)
            self.add_fact('Debt','Moderate_DTI', True)
        
        elif Monthly_debt_payment <= 0.3 * monthly_income and Monthly_debt_payment > 0.1 * monthly_income:
            self.add_rule('Debt','Low_DTI', 'Your debt-to-income ratio is moderate but it can be improved. DTI: ' + str('%.2f' % dti), 1)
            self.add_fact('Debt','Low_DTI', True)

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

    def checkBudget(self):
        global current_savings, total_deposited, total_spent, spending_thresholds, essentialList, nonessentialList, monthly_income, weekly_income, monthly_essentialSpend, monthly_nonessentialSpend, weekly_essentialSpend, weekly_nonessentialSpend
        global Weekly_essentialSpend, Weekly_nonessentialSpend, monthly_essentialSpend, monthly_nonessentialSpend
        df = self.df
        dfCopy = df.copy()
        df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
        df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
        df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
        df = df.reset_index() # reset the index
        df = df[['Category', 'Withdrawal']] # select only the Category and Withdrawal columns
        df = df.rename(columns={'Withdrawal': 'Amount'}) # rename the Withdrawal column to Amount
        spending_dict = df.to_dict('records') # convert the dataframe to a list of dictionaries
        # add the percentage of spending for essential and non-essential costs
        # spending_dict.append({'Category': 'Essential Costs', 'Amount': df[df['Category'].isin(['Housing', 'Bills', 'Groceries', 'Transportation'])]['Amount'].sum()})
        spending_dict.append({'Category': 'Essential Costs', 'Amount': df[df['Category'].isin(essentialList)]['Amount'].sum()})
        # spending_dict.append({'Category': 'Non-Essential Costs', 'Amount': df[df['Category'].isin(['Entertainment', 'Dining Out', 'Shopping', 'Loan Repayment'])]['Amount'].sum()})
        spending_dict.append({'Category': 'Non-Essential Costs', 'Amount': df[df['Category'].isin(nonessentialList)]['Amount'].sum()})
        
        essentialSpend = spending_dict[-2]['Amount']
        nonessentialSpend = spending_dict[-1]['Amount']
        Weekly_essentialSpend = essentialSpend / dfCopy['Week'].nunique()
        Weekly_nonessentialSpend = nonessentialSpend / dfCopy['Week'].nunique()
        monthly_essentialSpend = essentialSpend / dfCopy['Month'].nunique()
        monthly_nonessentialSpend = nonessentialSpend / dfCopy['Month'].nunique()
        
        spending_percentages = {row['Category']: row['Amount'] / total_deposited for row in spending_dict} # calculate the percentage of spending for each category

        # #evaluate each category against its threshold and add fact if it does not meet the threshold
        for category in spending_percentages:
            threshold = spending_thresholds[category]
            #     print(category + ' accounts for ' + str(spending_percentages[category]) + '% of your income threshold: ' + str(threshold) + '%')
            if spending_percentages[category] > spending_thresholds[category]:
                # print(category + ' Spending is too high')
                if category == 'Essential Costs':
                    self.add_rule('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', 'Lower your ' + category + ' spending.', 1)
                    self.add_fact('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', True)
                elif category == 'Non-Essential Costs':
                    self.add_rule('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', 'Lower your ' + category + ' spending.', 3)
                    self.add_fact('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income.', True)

    def eval_Savings(self):
        global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
        global emergency_fund, retirement_fund, age
        avs_monthly_savings = avg_monthly_deposits - avg_monthly_withdrawals
        if avs_monthly_savings <= monthly_income * 0.1:
            self.add_rule('Savings','Low Monthly Savings', 'Saving less than 10% of monthly income, you MUST decreasing your spendature.', 3)
            self.add_fact('Savings','Low Monthly Savings', True)
        elif avs_monthly_savings <= monthly_income * 0.15 and avs_monthly_savings > monthly_income * 0.1:
            self.add_rule('Savings','Moderate Monthly Savings', 'Saving less than 15% of monthly income, consider decreasing your spendature.', 1)
            self.add_fact('Savings','Moderate Monthly Savings', True)

        if emergency_fund < avg_monthly_withdrawals * 5:
            if emergency_fund >= avg_monthly_withdrawals * 3:
                self.add_rule('Savings','Moderate Emergency Fund', 'Your emergency fund can support you for 3-5 months based on current spending', 1)
                self.add_fact('Savings','Moderate Emergency Fund', True)
            elif emergency_fund >= avg_monthly_withdrawals and emergency_fund < avg_monthly_withdrawals * 3:
                self.add_rule('Savings','Low Emergency Fund', 'Your emergency fund can support you for 1-3 months based on current spending', 2)
                self.add_fact('Savings','Low Emergency Fund', True)
            elif emergency_fund < avg_monthly_withdrawals:
                self.add_rule('Savings','Insufficient Emergency Fund', 'Your emergency fund can support you for less than 1 month based on current spending', 4)
                self.add_fact('Savings','Insufficient Emergency Fund', True)
        if age >= 25:
            yearly_income = monthly_income * 12
            optimal_retirement_fund = (yearly_income * .15) * (age - 25)
            if retirement_fund < optimal_retirement_fund:
                if retirement_fund > optimal_retirement_fund * 0.8:
                    self.add_rule('Savings','Moderate Retirement Fund', 'Your retirement fund is moderate but not optimal assuming 15% of yearly income from age 25.', 1)
                    self.add_fact('Savings','Moderate Retirement Fund', True)
                elif retirement_fund < optimal_retirement_fund * 0.8 and retirement_fund > optimal_retirement_fund * 0.5:
                    self.add_rule('Savings','Low Retirement Fund', 'Your retirement fund needs attention 50-80% of expected value assuming 15% of yearly income from age 25.', 2)
                    self.add_fact('Savings','Low Retirement Fund', True)
                elif retirement_fund < optimal_retirement_fund * 0.5:
                    self.add_rule('Savings','Insufficient Retirement Fund', 'Your retirement fund is insufficient at < 50% of expected value, you MUST allocate more funds towards it assuming 15% of yearly income from age 25.', 3)
                    self.add_fact('Savings','Insufficient Retirement Fund', True)

    def checkCashflow(self):
        global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals
        global savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
        if avg_weekly_deposits < avg_weekly_withdrawals:
            self.add_rule('Cashflow','Weekly Cashflow is negative', 'You currently have a negative Weekly cashflow Adjust your budget.', 3)
            self.add_fact('Cashflow','Weekly Cashflow is negative', True)
        # else:
        #     self.add_fact('Cashflow','Weekly Cashflow is negative', False)
        if avg_monthly_deposits < avg_monthly_withdrawals:
            self.add_rule('Cashflow','Monthly Cashflow is negative', 'You currently have a negative Monthly cashflow Adjust your budget.', 4)
            self.add_fact('Cashflow','Monthly Cashflow is negative', True)
        # else:
        #     self.add_fact('Cashflow','Monthly Cashflow is negative', False)
        if total_deposited < total_spent:
            self.add_rule('Cashflow','Total Net Cashflow is negative', 'You currently have a negative net cashflow. Adjust your budget.', 2)
            self.add_fact('Cashflow','Total Net Cashflow is negative', True)
        # else:
        #     self.add_fact('Cashflow','Total Net Cashflow is negative', False)
        if avg_monthly_deposits > avg_monthly_withdrawals:
            if savings_per_month < avg_monthly_deposits * 0.2 and savings_per_month > avg_monthly_deposits * 0.15:
                self.add_rule('Cashflow','Monthly Cashflow is low', 'Saving less than 20% of monthly income, consider improving cashflow', 1)
                self.add_fact('Cashflow','Monthly Cashflow is low', True)

    def checkforSpikes(self): #function to check for spikes in spending by category
        #if there are more than 3 spikes in a category, then create a corresponding rule and fact in the expert system
        global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
        categories = self.df['Category'].unique()
        for category in categories:
            category_df = self.df[self.df['Category'] == category]
            category_df = category_df.groupby(['Month'])['Withdrawal'].sum().reset_index()
            avg_spending = category_df['Withdrawal'].mean()
            category_df['Above_Avg'] = category_df['Withdrawal'] > avg_spending
            spikes = category_df[category_df['Above_Avg'] == True]
            spikes = spikes.reset_index(drop=True)
            if len(spikes) >= 5 and category != 'Loan Payment':
                self.add_rule('Chronic Overspending', '5+ monthly spikes over average spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 3)
                self.add_fact('Chronic Overspending', '5+ monthly spikes over average spent on ' + category, True)
                # print('More than 3 monthly spikes in ' + category)
            elif len(spikes) >= 3 and category != 'Loan Payment' and len(spikes) < 5:
                self.add_rule('Chronic Overspending', '3+ monthly spikes over average spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 1)
                self.add_fact('Chronic Overspending', '3+ monthly spikes over average spent on ' + category, True)
                # print('More than 3 monthly spikes in ' + category)
            else:
                # es.add_fact('Spike', 'More than 3 monthly spikes in ' + category, False)
                pass #if there are no spikes, then don't add a fact

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

def main():
    global debt_list
    app = ESapp()
    app.mainloop()

if __name__ == '__main__':
    main()