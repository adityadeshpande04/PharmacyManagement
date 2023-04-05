from tkinter import *
import mysql.connector
from tkinter import messagebox

def login():
      # Initialize the Tkinter window
  root = Tk()
  root.title("Login")

  # Connect to the database
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aditya04",
    database="pharmacy"
  )

  # Create a cursor to interact with the database
  mycursor = mydb.cursor()

  # Create a function to check login credentials
  def check_login():
      # Get the username and password entered by the user
      username = username_entry.get()
      password = password_entry.get()
      
      # Check if the credentials exist in the database
      mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
      result = mycursor.fetchone()
      
      if result:
          # If the credentials are correct, show a success message and redirect to main menu
          messagebox.showinfo("Success", "Login Successful!")
      else:
          # Else, show an error message
          messagebox.showerror("Error", "Invalid username or password")
      
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
  root.mainloop()
