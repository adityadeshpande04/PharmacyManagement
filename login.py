from tkinter import *
import mysql.connector
from tkinter import messagebox
from mgmt import mgmt
from mysql.connector import Error



def login(root):
  root.title("Login")

  

  # Create a cursor to interact with the database
  

  # Create a function to check login credentials
  def check_login():
      # Get the username and password entered by the user
      username = username_entry.get()
      password = password_entry.get()

      try:
        connection = mysql.connector.connect(host='localhost',
                                                database='pharmacy',
                                                user='root',
                                                password='aditya04')
        mycursor = connection.cursor()
        if connection.is_connected():
           # Check if the credentials exist in the database
           mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
           result = mycursor.fetchone()
      
           if result:
             # If the credentials are correct, show a success message and redirect to main menu
             messagebox.showinfo("Success", "Login Successful!")
             for widget in root.winfo_children():
                 widget.destroy()
             mgmt(root)
           else:
          # Else, show an error message
             messagebox.showerror("Error", "Invalid username or password")
             mycursor.close()
             connection.close()

      except Error as e:
             print("Error while connecting to MySQL", e)
             # Show an error message
             messagebox.showerror("Error", "Could not create user.")
             exit()
  
          
      
      
      
  # Create a frame for the login page
  login_frame = Frame(root)

  # Create labels and entry boxes for the login page
  username_label = Label(login_frame, text="Username:")
  username_entry = Entry(login_frame)
  password_label = Label(login_frame, text="Password:")
  password_entry = Entry(login_frame, show="*")

  # Create a button to submit the login form
  login_button = Button(login_frame, text="Login", command=check_login)

  # Add the labels, entry boxes, and button to the login frame
  username_label.pack()
  username_entry.pack()
  password_label.pack()
  password_entry.pack()
  login_button.pack()

  # Pack the login frame
  login_frame.pack()

  # Run the Tkinter window
#   root.mainloop()

