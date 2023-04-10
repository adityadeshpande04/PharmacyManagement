from login import login
from signup import signup
from mgmt import mgmt
from queries import queries
import tkinter as tk
import mysql.connector
class Application(tk.Frame):
    

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        # Create a button to call function1
        self.button1 = tk.Button(self, text="Login", command=self.function1)
        self.button1.pack()
        
        # Create a button to call function2
        self.button2 = tk.Button(self, text="SignUp", command=self.function2)
        self.button2.pack()
    
    def function1(self):
        # Call function1 from login file
        for widget in self.winfo_children():
         widget.destroy()
        login(self.master)
    
    def function2(self):
        # Call function2 from signup file
        for widget in self.winfo_children():
         widget.destroy()
        signup(self.master)

root = tk.Tk()
root.title("Pharmacy Management App")
root.geometry("1500x1500")
app = Application(master=root)
app.mainloop()

