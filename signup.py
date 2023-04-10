from tkinter import *
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from login import login

def signup(root):
        # Initialize the Tkinter window
    # root = Tk()
    root.title("Sign Up")

    # Create a function to add new user to the database
    def add_user():
        # Get the values entered by the user
        username = username_entry.get()
        password = password_entry.get()
        
        # Connect to the database
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='pharmacy',
                                                user='root',
                                                password='aditya04')
            if connection.is_connected():
                # Insert new user into the database
                cursor = connection.cursor()
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                val = (username, password)
                cursor.execute(sql, val)
                connection.commit()
                cursor.close()
                connection.close()
                # Show a success message
                messagebox.showinfo("Success", "User created successfully!")
                cursor.close()
                login(root)
        except Error as e:
            print("Error while connecting to MySQL", e)
            # Show an error message
            messagebox.showerror("Error", "Could not create user.")
            exit()

    # Create labels and entry boxes for the sign-up page
    username_label = Label(root, text="Username:")
    username_entry = Entry(root)
    password_label = Label(root, text="Password:")
    password_entry = Entry(root, show="*")

    # Create a button to submit the sign-up form
    submit_button = Button(root, text="Sign Up", command=add_user)

    # Add the labels, entry boxes, and button to the sign-up page
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    submit_button.pack()

    
