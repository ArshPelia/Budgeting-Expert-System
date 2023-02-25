import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import random, os

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Serif", 8)

headerlist = ['Date', 'Withdrawal', 'Deposit', 'Balance']
spendList = ['Dining Out', 'Groceries', 'Shopping', 'Transportation', 'Housing', 
             'Entertainment', 'Personal Care', 'Loan Payment', 'Healthcare', 'Bills']
essentialList = ['Groceries', 'Housing', 'Bills', 'Loan Payment', 'Transportation', 'Healthcare']
nonessentialList = ['Dining Out', 'Shopping', 'Entertainment', 'Personal Care']
incomeList = ['Salary', 'Bonus', 'Investment Income', 'Capital Gains', 'Other']

global avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals
global savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
global allInferences, dataFrame, age, retirement_fund, emergency_fund, spending_thresholds, spending_percentages
global Weekly_essentialSpend, Weekly_nonessentialSpend, monthly_essentialSpend, monthly_nonessentialSpend
global essential_spendingPercentages, nonessential_spendingPercentages

spending_thresholds = {'Housing': 0.4, 'Groceries': 0.1, 'Dining Out': 0.1, 
                       'Shopping': 0.2, 'Transportation': 0.1, 'Bills': 0.1, 
                       'Loan Payment': 0.1, 'Essential Costs': 0.5, 
                       'Non-Essential Costs': 0.3, 'Entertainment': 0.1,
                       'Personal Care': 0.1, 'Healthcare': 0.1}

# debt_list = [
#     {'name': 'Credit card', 'amount': 5000, 'interest_rate': 15},
#     {'name': 'Student loan', 'amount': 20000, 'interest_rate': 5},
#     {'name': 'Car loan', 'amount': 10000, 'interest_rate': 7},
#     {'name': 'Mortgage', 'amount': 100000, 'interest_rate': 3},
# ]

global debt_list, investment_list
debt_list = []
investment_list = []
allInferences = []

def getTheme():
    modern_theme = {
        'tHeading': {
            'configure': {
                'background': '#009B4D',
                'foreground': '#FAF5E9',
                'font': ('Serif', 15, 'bold'),
                'padx': 8,
                'pady': 8,
                'borderwidth': 3,
            }
        },      
        'TLabel': {
            'configure': {
                'background': '#009B4D',
                'foreground': '#FAF5E9',
                'font': ('Helvetica', 10, 'bold'),
                'borderwidth': 0,
                'highlightthickness': 0,
                'padx': 5,
                'pady': 5
            }
        },
        'TButton': {
            'configure': {
                'background': '#FFCC00',
                'foreground': 'Black',
                'font': ('Serif', 13, 'bold'),
                'fontcolor': 'black',
                'borderwidth': 0,
                'highlightthickness': 0,
                'activebackground': '#FFB300',
                'activeforeground': '#FAF5E9',
                'relief': 'flat',
                'padx': 5,
                'pady': 5,
                'width': 18,
                'anchor': 'center'
            }
        },
        'TEntry': {
            'configure': {
                'background': '#FAF5E9',
                'foreground': '#272727',
                'font': ('Helvetica', 10),
                'borderwidth': 0,
                'highlightthickness': 0,
                'padx': 5,
                'pady': 5,
                'width': 30
            }
        },
        'Treeview': {
            'configure': {
                'background': '#FAF5E9',
                'foreground': '#272727',
                'font': ('Helvetica', 10),
                'rowheight': 25,
                'borderwidth': 0,
                'highlightthickness': 0,
                'selectbackground': '#FFCC00',
                'selectforeground': '#272727'
            }
        },
        'Treeview.Heading': {
            'configure': {
                'background': '#009B4D',
                'foreground': '#FAF5E9',
                'font': ('Helvetica', 10, 'bold'),
                'borderwidth': 0,
                'highlightthickness': 0,
                'padx': 5,
                'pady': 5,
                'relief': 'raised'
            }
        },
        'Tframe': {
            'configure': {
                'background': '#FAF5E9',
                'foreground': '#272727',
                'borderwidth': 5,
                'relief': 'flat',
                'highlightthickness': 0,
                'padx': 10,
                'pady': 10
            }
        },
        'TNotebook': {
            'configure': {
                'background': '#FAF5E9',
                'foreground': '#272727',
                'tabposition': 'n',
                'borderwidth': 1,
                'relief': 'flat',
                'highlightthickness': 0,
                'padx': 10,
                'pady': 10
            }
        },
        'TNotebook.Tab': {
            'configure': {
                'background': '#009B4D',
                'foreground': '#FAF5E9',
                'font': ('Helvetica', 10, 'bold'),
                'borderwidth': 0,
                'highlightthickness': 0,
                'padx': 10,
                'pady': 10,
                'relief': 'raised'
            }
        },

    }

    return modern_theme

def validateFile(file):
    if file.endswith('.csv'):
        return True
    else:
        return False

def popupmsg(msg):
    popup = tk.Tk()
    popup.style = ttk.Style()
    popup.style.theme_create('modern1', parent='default')
    popup.style.theme_settings('modern1', getTheme())
    popup.style.theme_use('modern1')

    popup.wm_title("!")
    heading = ttk.Label(popup, text="Error")
    heading.pack(side="top", fill="x")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x")
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def viewInference(type, premise, conclusion):
    global dataFrame, savings_per_month, debt_list, essential_spendingPercentages, nonessential_spendingPercentages
    popup = tk.Tk()
    popup.wm_title("Inference")
    label = ttk.Label(popup, text=("Inference Type: " + type), font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10, padx=10)
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

        elif premise == 'Monthly Cashflow is negative':
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
            a.bar(month_avgs.index, month_avgs['Deposit'], label='Income')
            a.bar(month_avgs.index, month_avgs['Withdrawal'], label='Spending')
            a.set_xlabel('Category')
            a.set_ylabel('Amount')
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
            a.bar(week_avgs.index, week_avgs['Deposit'], label='Income')
            a.bar(week_avgs.index, week_avgs['Withdrawal'], label='Spending')
            a.set_xlabel('Category')
            a.set_ylabel('Amount')
            a.set_title('Average Weekly Cashflow')
            a.legend()

            canvas = FigureCanvasTkAgg(f, popup)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    elif type == 'Debt':
        #insert table of debt list
        debt_tree = ttk.Treeview(popup, columns=("name", "amount", "interest_rate"))
        debt_tree.heading("#0", text="ID", anchor=tk.W)
        debt_tree.heading("name", text="Name", anchor=tk.W)
        debt_tree.heading("amount", text="Amount", anchor=tk.W)
        debt_tree.heading("interest_rate", text="Interest Rate", anchor=tk.W)

        debt_tree.column("#0", minwidth=0, width=50, stretch=tk.NO)
        debt_tree.column("name", minwidth=0, width=100, stretch=tk.NO)
        debt_tree.column("amount", minwidth=0, width=100, stretch=tk.NO)
        debt_tree.column("interest_rate", minwidth=0, width=100, stretch=tk.NO)

        debt_tree.pack(fill="both", expand=True, padx=10, pady=10)

        for debt in debt_list:
            debt_tree.insert("", "end", text=debt['id'], values=(debt['name'], debt['amount'], debt['interest_rate']))

        for item in debt_tree.get_children():
            interest_rate = float(debt_tree.item(item)['values'][2])
            if interest_rate > 8:
                debt_tree.item(item, tags=('high_interest',))
        debt_tree.tag_configure('high_interest', foreground='red')
    
    elif type == 'Spending':
        if premise == 'Essential Costs accounts for more than 0.5% of your income':
            # create a treeview widget
            tree = ttk.Treeview(popup)

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

        elif premise == 'Non-Essential Costs accounts for more than 0.3% of your income':
            # create a treeview widget
            tree = ttk.Treeview(popup)

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

                # Plot the spikes
                # f = Figure(figsize=(12,5), dpi=100)
                # ax = plt.subplots()
                # ax.plot(category_df['Month'], category_df['Withdrawal'], label='Spending')
                # ax.plot(spikes['Month'], spikes['Withdrawal'], 'ro', label='Spike')
                # ax.axhline(avg_spending, color='black', linestyle='dashed', label='Average Monthly Spending')
                # ax.set_xlabel('Month')
                # ax.set_ylabel('Withdrawal')
                # ax.legend()
                # ax.set_title(f"Spikes in average spending in category '{category}'")
                # plt.show()

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
                


    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack(padx=10, pady=10)
    popup.mainloop()

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

        for F in (StartPage, InferencesPage, GraphPage, DebtPage, filePage, recommendationsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            #q: how can adjust the frame location from the class to be centered?
            # frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        global filename, allInferences
        if cont == DebtPage:
            self.geometry("950x650")
        elif cont == GraphPage:
            self.geometry("1100x850")
        elif cont == filePage:
            self.geometry("400x200")
        elif cont == InferencesPage:
            if allInferences == []:
                self.select_file()
            self.geometry("950x650")
        frame = self.frames[cont]
        frame.tkraise()

    # def startup(self, cont):
    #     self.select_file()
    #     frame = self.frames[cont]
    #     frame.tkraise()
    
    def select_file(self):
        global filename, allInferences, dataFrame, debt_list
        filetypes = (
                    ('CSV files', '*.csv'),
                    # ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        df = preprocess(filename)
        getSpendingPercentages(df)
        # print(spending_percentages)
        dataFrame = df
        self.expert_system = ExpertSystem(df, debt_list)
        # self.expert_system.addRules()
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

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global age, retirement_fund, emergency_fund 
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("Welcome to the budgeting Expert System"), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text=("Please begin by entering the following information"), font=NORM_FONT)
        label1.pack(pady=10,padx=10)

        input_frame = tk.Frame(self)
        input_frame.pack(fill="both", expand=True, padx=5, pady=5)

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

        button = ttk.Button(input_frame, text="Continue",
                            command=lambda: self.set_variables_and_show_frame(controller, DebtPage))
        # button.pack()
        button.grid(row=3, column=0, padx=10, pady=10)

        button2 = ttk.Button(input_frame, text="Exit Program",
                            command=quit)
        # button2.pack(padx=10, pady=10)
        button2.grid(row=3, column=1, padx=10, pady=10)

    def set_variables_and_show_frame(self, controller, next_frame):
        global age, retirement_fund, emergency_fund 
        if age.get() == '':
            popupmsg("Please enter your age")
            return
        elif retirement_fund.get() == '':
            popupmsg("Please enter your retirement fund")
            return
        elif emergency_fund.get() == '':
            popupmsg("Please enter your emergency fund")
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

        button = ttk.Button(self, text="Continue",
                            command=lambda: controller.show_frame(filePage))
        button.pack()

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)

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
        self.debt_treeview.column("name", anchor="center", width=200)
        self.debt_treeview.column("amount", anchor="center", width=200)
        self.debt_treeview.column("interest_rate", anchor="center", width=200)
        self.debt_treeview.pack(fill="both", expand=True)

        # Initialize the debt list
        self.debt_list = debt_list
        self.next_debt_id = 1

    def add_debt(self):
        # Get the input values
        name = self.name_entry.get()
        amount = int(self.amount_entry.get())
        interest_rate = float(self.interest_rate_entry.get())
        min_payment = float(self.min_payment_entry.get())

        # Add the new debt to the list
        self.debt_list.append({'id': self.next_debt_id, 'name': name, 'amount': amount, 'interest_rate': interest_rate, 'min_payment': min_payment})
        self.next_debt_id += 1

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.interest_rate_entry.delete(0, tk.END)

        # Update the debt list display
        self.update_debt_list()

    def update_debt_list(self):
        # Clear the existing items in the Treeview
        self.debt_treeview.delete(*self.debt_treeview.get_children())

        # Insert the updated debt list into the Treeview
        for debt in self.debt_list:
            self.debt_treeview.insert("", "end", text=debt['id'], values=(debt['name'], debt['amount'], debt['interest_rate'], debt['min_payment']))

        # print(self.debt_list)

class investmentPage(tk.Frame):

    def __init__(self, parent, controller):
        global investment_list
        tk.Frame.__init__(self, parent)
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        label = ttk.Label(self, text="Investment List", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Continue",
                            command=lambda: controller.show_frame(InferencesPage))
        button.pack()

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)

        input_frame = tk.Frame(self)
        #pack frame so it sits in the middle of the page
        input_frame.pack(fill="both", expand=True)


        # Create labels and entry widgets for the investment parameters
        name_label = tk.Label(input_frame, text="Account:")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        amount_label = tk.Label(input_frame, text="investment Amount:")
        amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        interest_rate_label = tk.Label(input_frame, text="Interest Rate (%):")
        interest_rate_label.grid(row=2, column=0, padx=10, pady=10)
        self.interest_rate_entry = tk.Entry(input_frame)
        self.interest_rate_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create a button to add a new investment to the list
        add_button = ttk.Button(input_frame, text="Add investment", command=self.add_investment)
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Create a frame for the investment list
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10)) #fill both means it will fill the entire frame, expand true means it will expand to fill the entire frame

        # Create a Treeview widget to display the investment list
        self.investment_treeview = ttk.Treeview(list_frame, columns=("name", "amount", "interest_rate"))
        self.investment_treeview.heading("#0", text="ID")
        self.investment_treeview.heading("name", text="Account")
        self.investment_treeview.heading("amount", text="investment Amount")
        self.investment_treeview.heading("interest_rate", text="Interest Rate (%)")
        #center all columns
        self.investment_treeview.column("#0", anchor="center", width=50)
        self.investment_treeview.column("name", anchor="center", width=200)
        self.investment_treeview.column("amount", anchor="center", width=200)
        self.investment_treeview.column("interest_rate", anchor="center", width=200)
        self.investment_treeview.pack(fill="both", expand=True)

        # Initialize the investment list
        self.investment_list = investment_list
        self.next_investment_id = 1

    def add_investment(self):
        # Get the input values
        name = self.name_entry.get()
        amount = int(self.amount_entry.get())
        interest_rate = float(self.interest_rate_entry.get())

        # Add the new investment to the list
        self.investment_list.append({'id': self.next_investment_id, 'name': name, 'amount': amount, 'interest_rate': interest_rate})
        self.next_investment_id += 1

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.interest_rate_entry.delete(0, tk.END)

        # Update the investment list display
        self.update_investment_list()

    def update_investment_list(self):
        # Clear the existing items in the Treeview
        self.investment_treeview.delete(*self.investment_treeview.get_children())

        # Insert the updated investment list into the Treeview
        for investment in self.investment_list:
            self.investment_treeview.insert("", "end", text=investment['id'], values=(investment['name'], investment['amount'], investment['interest_rate']))

        print(self.investment_list)

class filePage(tk.Frame):

    def __init__(self, parent, controller):
        global filename
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="File Select", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        lbl_selectFile = ttk.Label(self, text="Select a file to initialize the Expert system:")
        lbl_selectFile.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Open a File",
                            # command=lambda: controller.startup(InferencesPage))
                            command=lambda: controller.show_frame(InferencesPage))
        button1.pack(padx=10, pady=5)


        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button2.pack(padx=10, pady=5)

class InferencesPage(tk.Frame):

    def __init__(self, parent, controller):
        global filename
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Blackboard", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # lbl_selectFile = ttk.Label(self, text="Select a file to initialize the Expert system:")
        # lbl_selectFile.pack(pady=10,padx=10)

        # button1 = ttk.Button(self, text="Open a File",
        #                     command=lambda: controller.startup(InferencesPage))
        # button1.pack(padx=10, pady=5)

        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button2.pack(padx=10, pady=5)

        button3 = ttk.Button(self, text="Show Inferences",
                            command= lambda: self.showInferences())
        button3.pack(padx=10, pady=5)

        button4 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(GraphPage))
        button4.pack(padx=10, pady=5)

        button5 = ttk.Button(self, text="View by Category",
                            command=lambda: controller.show_frame(recommendationsPage))
        button5.pack(padx=10, pady=5)

        label1 = ttk.Label(self, text=("Double-Click on an inference to view explanation."), font=NORM_FONT)
        label1.pack(pady=10,padx=5)
        
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
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Minor",))
            elif i.severity == 2:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Moderate",))
            elif i.severity == 3:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Alarming",))
            elif i.severity == 4:
                tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Critical",))

        tree.tag_configure("Critical", background="red")
        tree.tag_configure("Alarming", background="orange")
        tree.tag_configure("Moderate", background="yellow")
        tree.tag_configure("Minor", background="white")

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
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="View Inferences",
                            command=lambda: controller.show_frame(InferencesPage))
        button.pack(padx=10, pady=10)

        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack(padx=10, pady=10)
        button1 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button1.pack(padx=10, pady=5)

        button2 = ttk.Button(self, text="View Spending",
                            command=lambda: self.viewSpending())
        button2.pack(padx=10, pady=5)

        button3 = ttk.Button(self, text="View Income",
                            command=lambda: self.viewIncome())
        button3.pack(padx=10, pady=5)

        button4 = ttk.Button(self, text="View Cashflow",
                            command=lambda: self.viewCashflow())
        button4.pack(padx=10, pady=5)

        button5 = ttk.Button(self, text="View Weekly Averages",
                            command=lambda: self.weeklyAvg())
        button5.pack(padx=10, pady=5)

        button6 = ttk.Button(self, text="View Monthly Averages",
                            command=lambda: self.monthlyAvg())
        button6.pack(padx=10, pady=5)

        self.canvas = None

        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def viewSpending(self):
        global dataFrame

        df = dataFrame
        df = df[df['Withdrawal'] != 0] # filter out all the rows that have 0 in the Withdrawal column
        df = df.groupby(['Category']).sum() # group the dataframe by Category and sum the Withdrawal column
        df = df.sort_values(by=['Withdrawal'], ascending=False) # sort the dataframe by Withdrawal column in descending order
        df = df.reset_index() # reset the index

        f = Figure(figsize=(10,7), dpi=100) #dpi = dots per inch
        a = f.add_subplot(111)
        a.bar(df['Category'], df['Withdrawal'])
        a.set_xlabel('Category')
        a.set_ylabel('Spending')
        # a.xticks(rotation=90) 
        # a.set_xticklabels(df['Category'], rotation=90)

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.canvas.get_tk_widget().pack(side=tk.BOTTOM)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
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
        # self.canvas.get_tk_widget().pack(side=tk.BOTTOM)


        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

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
        a.bar(week_avgs.index, week_avgs['Deposit'], label='Income')
        a.bar(week_avgs.index, week_avgs['Withdrawal'], label='Spending')
        a.set_xlabel('Category')
        a.set_ylabel('Amount')
        a.set_title('Average Weekly Cashflow')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

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
        a.bar(month_avgs.index, month_avgs['Deposit'], label='Income')
        a.bar(month_avgs.index, month_avgs['Withdrawal'], label='Spending')
        a.set_xlabel('Category')
        a.set_ylabel('Amount')
        a.set_title('Average Monthly Cashflow')
        a.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().forget()
            # canvas._tkcanvas.forget()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class recommendationsPage(tk.Frame):
    
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Recommendations", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Back to Inferences",
                            command=lambda: controller.show_frame(InferencesPage))
        button.pack()

        button3 = ttk.Button(self, text="Show Inferences",
                            command= lambda: self.showInferences())
        button3.pack(padx=10, pady=5)

    def showInferences(self):
        global allInferences
        if len(allInferences) == 0:
            return
        
        # check if the notebook already exists
        if hasattr(self, "inferenceNotebook"):
            self.inferenceNotebook.destroy()

        self.inferenceNotebook = ttk.Notebook(self)
        self.inferenceNotebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        inferenceTypes = ["Spending", "Chronic Overpending", "Debt", "Savings", "Cashflow"]

        for inferenceType in inferenceTypes:
            # create a frame for the tab
            frame = tk.Frame(self.inferenceNotebook)
            frame.pack(expand=True, fill=tk.BOTH)

            columns = ("Type", "Premise", "Recommendation")
            tree = ttk.Treeview(frame, columns=columns, show="headings")
            tree.heading("Type", text="Type")
            tree.heading("Premise", text="Premise")
            tree.heading("Recommendation", text="Recommendation")
            tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

            for i in allInferences:
                if i.type == inferenceType:
                    if i.severity == 1:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Minor",))
                    elif i.severity == 2:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Moderate",))
                    elif i.severity == 3:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Alarming",))
                    elif i.severity == 4:
                        tree.insert("", "end", values=(i.type, i.premise, i.conclusion), tags=("Critical",))

            tree.tag_configure("Critical", background="red")
            tree.tag_configure("Alarming", background="orange")
            tree.tag_configure("Moderate", background="yellow")
            tree.tag_configure("Minor", background="white")

            # def selectRecord(event):
            #     item = tree.focus()
            #     values = tree.item(item, "values")
            #     type, premise, recommendation = values

            #     viewInference(type, premise, recommendation)

            # tree.bind("<Double-1>", selectRecord)
            tree["displaycolumns"] = ("Recommendation",)
            
            # add the tab to the notebook
            self.inferenceNotebook.add(frame, text=inferenceType)

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
        global monthly_income
        high_interest_debt = []
        Monthly_debt_payment = 0

        for debt in self.debt_list:
            Monthly_debt_payment += debt['amount'] * debt['min_payment']
            if debt['interest_rate'] >= 8: # if interest rate is greater than or equal to 8%
                high_interest_debt.append(debt)
        
        if high_interest_debt:
            self.add_rule('Debt','high_interest_debt', 'High-interest debt detected, consider paying off the debt first.', 2)
            self.add_fact('Debt','high_interest_debt', True)
        
        if Monthly_debt_payment > 0.5 * monthly_income:
            self.add_rule('Debt','High_DTI', 'Your debt-to-income ratio greater than 50% of monthly income, consider paying off some debt or increasing your income.', 3)
            self.add_fact('Debt','High_DTI', True)
        elif Monthly_debt_payment > 0.3 * monthly_income and Monthly_debt_payment <= 0.5 * monthly_income:
            self.add_rule('Debt','Moderate_DTI', 'Your debt-to-income ratio is managable but leaves little to invest. (30% > DIT < 50% of monthly income)', 2)
            self.add_fact('Debt','Moderate_DTI', True)
        elif Monthly_debt_payment <= 0.3 * monthly_income and Monthly_debt_payment > 0.1 * monthly_income:
            self.add_rule('Debt','Low_DTI', 'Your debt-to-income ratio is low (<30% of monthly income) but it can be improved.', 1)
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
        # print('Essential Costs: ', essentialSpend)
        # print('Non-Essential Costs: ', nonessentialSpend)
        # print('Weekly Essential Costs: ', Weekly_essentialSpend)
        # print('Weekly Non-Essential Costs: ', Weekly_nonessentialSpend)
        # print('Monthly Essential Costs: ', monthly_essentialSpend)
        # print('Monthly Non-Essential Costs: ', monthly_nonessentialSpend)


        # print list of categories and amount spent
        # for i in range(len(spending_dict)):
        #     print(spending_dict[i]['Category'], ': ', spending_dict[i]['Amount'])
        
        spending_percentages = {row['Category']: row['Amount'] / total_deposited for row in spending_dict} # calculate the percentage of spending for each category

        # print list of categories and percentage of spending
        # for key, value in spending_percentages.items():
        #     print(key, ': ', value)

        # #evaluate each category against its threshold and add fact if it does not meet the threshold
        for category in spending_percentages:
            threshold = spending_thresholds[category]
            #     print(category + ' accounts for ' + str(spending_percentages[category]) + '% of your income threshold: ' + str(threshold) + '%')
            if spending_percentages[category] > spending_thresholds[category]:
                # print(category + ' Spending is too high')
                if category == 'Essential Costs':
                    self.add_rule('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income', 'Lower your ' + category + ' spending.', 1)
                    self.add_fact('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income', True)
                elif category == 'Non-Essential Costs':
                    self.add_rule('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income', 'Lower your ' + category + ' spending.', 3)
                    self.add_fact('Spending', category + ' accounts for more than '+ str(threshold) + '% of your income', True)

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
            optimal_retirement_fund = (yearly_income * 1.15) * (65 - age)
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
        global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
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
                self.add_rule('Chronic Overspending', 'More than 5 monthly spikes over average amount spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 3)
                self.add_fact('Chronic Overspending', 'More than 5 monthly spikes over average amount spent on ' + category, True)
                # print('More than 3 monthly spikes in ' + category)
            elif len(spikes) >= 3 and category != 'Loan Payment' and len(spikes) < 5:
                self.add_rule('Chronic Overspending', 'More than 3 monthly spikes over average amount spent on ' + category, 'Consider creating a strict Monthly budget for ' + category, 1)
                self.add_fact('Chronic Overspending', 'More than 3 monthly spikes over average amount spent on ' + category, True)
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

def preprocess(filename):
    global total_invested, avg_weekly_deposits, avg_weekly_withdrawals, avg_monthly_deposits, avg_monthly_withdrawals, savings_per_week, savings_per_month, total_deposited, total_spent, current_savings, monthly_income
    
    df = pd.read_csv(filename)
    expected_headers = ['Date', 'Withdrawal', 'Deposit', 'Balance', 'Week', 'Month', 'Year', 'Category']
  
    if set(df.columns.tolist()) == set(expected_headers):
        current_savings = df[df['Withdrawal'] != 0]['Withdrawal'].sum() - df[df['Deposit'] != 0]['Deposit'].sum()
        total_spent = df[df['Withdrawal'] != 0]['Withdrawal'].sum()
        total_deposited = df[df['Deposit'] != 0]['Deposit'].sum()
        
        avg_weekly_deposits = df['Deposit'].sum() / df['Week'].nunique()
        avg_weekly_withdrawals = df['Withdrawal'].sum() / df['Week'].nunique()
        savings_per_week = avg_weekly_deposits - avg_weekly_withdrawals
        
        avg_monthly_deposits = df['Deposit'].sum() / df['Month'].nunique()
        avg_monthly_withdrawals = df['Withdrawal'].sum() / df['Month'].nunique()
        savings_per_month = avg_monthly_deposits - avg_monthly_withdrawals
        
        # monthly_income = df[df['Category'] == 'Salary']['Deposit'].sum()
        # avg_monthly_income = monthly_income / df['Month'].nunique()
        # monthly_income = avg_monthly_income
        monthly_income = avg_monthly_deposits

        total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

    else:
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

        # monthly_income = df[df['Category'] == 'Salary']['Deposit'].sum()
        # avg_monthly_income = monthly_income / df['Month'].nunique()
        # monthly_income = avg_monthly_income
        monthly_income = avg_monthly_deposits
        total_invested = df[df['Category'] == 'Investment']['Deposit'].sum()

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

    # print('\nEssential Spending:')
    # print(essential_spendingPercentages)
    # print('Non-Essential Spending:')
    # print(nonessential_spendingPercentages)

def main():
    global debt_list
    app = ESapp()
    app.mainloop()

if __name__ == '__main__':
    main()