import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def select_file():
    global filename
    filetypes = (
                ('CSV files', '*.csv'),
                ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
class ESapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self,default='clienticon.ico')
        tk.Tk.wm_title(self, "Financial Budget Expert System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(background='dark grey')
        
        style = ttk.Style(container)
        style.theme_use('alt')
        #list all available themes
        # themes: clam, alt, default, classic, vista, xpnative, winnative, aqua, 

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, GraphPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("Welcome to the budgeting Expert System"), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label1 = tk.Label(self, text=("Please select a CSV file to begin."), font=NORM_FONT)

        button1 = ttk.Button(self, text="Open a File",
                            command=select_file)
        button1.pack()

        button2 = ttk.Button(self, text="Exit Program",
                            command=quit)
        button2.pack()

        button3 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button3.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(GraphPage))
        button3.pack()

class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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


def main():
    app = ESapp()
    app.mainloop()

if __name__ == '__main__':
    main()