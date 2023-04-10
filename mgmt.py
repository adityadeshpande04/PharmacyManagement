import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime
from queries import queries
from credentials import user_name,pass_word


def mgmt(root):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aditya04",
        database="pharmacy"
    )
    cursor =db.cursor()

    def add_medication():
        db = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=pass_word,
        database="pharmacy"
     )
        cursor =db.cursor()
        # Fetch medication data from Entry widgets
        name = entry_name.get()
        dosage = entry_dosage.get()
        manufacturer = entry_manufacturer.get()
        
        # Fetch current user ID (you may replace this with your actual code to get the current user ID)
        user_id = 1
        
        # Insert medication data into database
        cursor.execute("INSERT INTO medications (name, dosage, manufacturer, user_id) VALUES (%s, %s, %s, %s)",
                    (name, dosage, manufacturer, user_id))
        db.commit()
        
        # Show success message
        messagebox.showinfo("Success", "Medication added successfully")

    # Create the GUI
    # root = tk.Tk()
    # root.geometry("800x600")

    def queries_caller():
        for widget in root.winfo_children():
         widget.destroy()
        queries(root)
    
    root.title("Pharmacy Management System")

    # Create the left frame for adding medication
    left_frame = tk.Frame(root, width=200, height=600, bg="#f0f0f0")
    left_frame.pack(side="left", fill="both", expand=True)

    # Add Medication Label
    label_add_medication = tk.Label(left_frame, text="Add Medication", font=("Helvetica", 16))
    label_add_medication.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Name Label
    label_name = tk.Label(left_frame, text="Name:")
    label_name.grid(row=1, column=0, padx=5, pady=5)

    # Name Entry
    entry_name = tk.Entry(left_frame)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    # Dosage Label
    label_dosage = tk.Label(left_frame, text="Dosage:")
    label_dosage.grid(row=2, column=0, padx=5, pady=5)

    # Dosage Entry
    entry_dosage = tk.Entry(left_frame)
    entry_dosage.grid(row=2, column=1, padx=5, pady=5)

    # Manufacturer Label
    label_manufacturer = tk.Label(left_frame, text="Manufacturer:")
    label_manufacturer.grid(row=3, column=0, padx=5, pady=5)

    # Manufacturer Entry
    entry_manufacturer = tk.Entry(left_frame)
    entry_manufacturer.grid(row=3, column=1, padx=5, pady=5)

    user_name = tk.Label(left_frame, text="User ID:")
    user_name.grid(row=4, column=0, padx=5, pady=5)

    cursor.execute("SELECT id FROM users")
    user_ids = cursor.fetchall()
    user_ids = [str(med_id[0]) for med_id in user_ids]

    # Create a Combobox for medication IDs in the search Entry field
    search_var = tk.StringVar()
    search_combobox = ttk.Combobox(left_frame, textvariable=search_var, values=user_ids)
    search_combobox.grid(row=4, column=1, padx=5, pady=5)



    # Add Medication Button
    btn_add_medication = tk.Button(left_frame, text="Add Medication", command=add_medication)
    btn_add_medication.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    btn_add_medication = tk.Button(left_frame, text="Statistics", command=queries_caller)
    btn_add_medication.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    

    def sell_medication():
        db = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=pass_word,
        database="pharmacy"
     )
        cursor =db.cursor()
        # Fetch data from GUI entries
        medication_id = medication_id_combobox.get()
        sold_quantity = int(quantity_entry.get())
        cursor.execute("SELECT selling_price FROM inventory WHERE medication_id= %s",(medication_id,))
        selling_price = cursor.fetchone()[0]
        firstName=fName_entry.get()
        lastName=lName_entry.get()
        # print(selling_price)

        # Fetch current inventory quantity from database
        cursor.execute("SELECT quantity FROM inventory WHERE medication_id = %s", (medication_id,))
        current_quantity = cursor.fetchone()[0]
        # print(current_quantity)

        # Calculate new quantity after selling
        new_quantity = current_quantity - sold_quantity

        # Update inventory table in the database
        cursor.execute("UPDATE inventory SET quantity = %s WHERE medication_id = %s", (new_quantity, medication_id))
        current_date = datetime.now()
        date_string = current_date.strftime('%Y-%m-%d')
        # Insert sales record into sales table in the database
        cursor.execute("INSERT INTO sales_records (medication_id, quantity, price, date_sold,first_name,last_name) VALUES (%s, %s, %s,%s, %s, %s)",
                    (medication_id, sold_quantity, selling_price, date_string,firstName,lastName))
        sales_record_id=cursor.lastrowid
        total_price=sold_quantity*selling_price
        cursor.execute("INSERT INTO sales(sales_record_id,total_price) VALUES (%s, %s)",(sales_record_id,total_price))

        # Commit changes to the database
        db.commit()

        # Show success message
        messagebox.showinfo("Success", "Inventory and Sales record updated successfully!")


    # Create the right frame for selling medication
    right_frame = tk.Frame(root, width=200, height=600, bg="#f0f0f0")
    right_frame.pack(side="right", fill="both", expand=True)

    right_title = tk.Label(right_frame, text="Sell Medication", font=("Helvetica", 18))
    right_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    fName_label = tk.Label(right_frame, text="First Name:")
    fName_label.grid(row=1, column=0, padx=5, pady=5)

    fName_entry = tk.Entry(right_frame)
    fName_entry.grid(row=1, column=1, padx=5, pady=5)

    lName_label = tk.Label(right_frame, text="First Name:")
    lName_label.grid(row=2, column=0, padx=5, pady=5)

    lName_entry = tk.Entry(right_frame)
    lName_entry.grid(row=2, column=1, padx=5, pady=5)



    # Create a label for medication ID
    medication_id_label = tk.Label(right_frame, text="Medication ID:")
    medication_id_label.grid(row=3, column=0, padx=5, pady=5)

    # Fetch medication IDs from database
    cursor.execute("SELECT id FROM medications")
    medication_ids = cursor.fetchall()
    medication_ids = [str(med_id[0]) for med_id in medication_ids]

    # You can fetch the medication IDs from the medication table in the database and populate the combobox here
    medication_id_var = tk.StringVar()
    medication_id_combobox = ttk.Combobox(right_frame, textvariable=medication_id_var, values=medication_ids)
    medication_id_combobox.grid(row=3,column=1,padx=5,pady=5)

    # Create a label for quantity
    quantity_label = tk.Label(right_frame, text="Quantity:")
    quantity_label.grid(row=4, column=0, padx=5, pady=5)

    # Create an entry for quantity
    quantity_entry = tk.Entry(right_frame)
    quantity_entry.grid(row=4, column=1, padx=5, pady=5)

    # Create a button for selling medication
    sell_button = tk.Button(right_frame, text="Sell Medication", command=sell_medication)
    sell_button.grid(row=5, columnspan=2, padx=5, pady=5)


    # Create the lower frame for seeing inventory
    lower_frame = tk.Frame(root, width=800, height=200, bg="#f0f0f0")
    lower_frame.pack(side="bottom", fill="both", expand=True)

    lower_title = tk.Label(lower_frame, text="Inventory", font=("Helvetica", 18))
    lower_title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    cursor.execute("SELECT * FROM inventory")
    inventory_records = cursor.fetchall()

    # Create listbox
    listbox = tk.Listbox(lower_frame)
    listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

    # Insert inventory records into listbox
    for record in inventory_records:
        record_str = f"ID: {record[0]}, Medication ID: {record[1]}, Quantity: {record[2]}, Expiration Date: {record[3]}, Date Created: {record[4]}, Selling Price: {record[5]}"
        listbox.insert(tk.END, record_str)

    # Create scrollbar for listbox
    scrollbar = tk.Scrollbar(lower_frame, command=listbox.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.config(yscrollcommand=scrollbar.set)


    # Fetch medication IDs from database
    cursor.execute("SELECT id FROM medications")
    medication_ids = cursor.fetchall()
    medication_ids = [str(med_id[0]) for med_id in medication_ids]

    # Create a Combobox for medication IDs in the search Entry field
    search_var = tk.StringVar()
    search_combobox = ttk.Combobox(lower_frame, textvariable=search_var, values=medication_ids)
    search_combobox.grid(row=2, column=0,)

    # Create Search button
    def search_inventory():
        db = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=pass_word,
        database="pharmacy"
        )
        cursor =db.cursor()
        
        # Fetch search query from Entry
        search_query = search_var.get()

        # Fetch inventory records from database
        cursor.execute("SELECT * FROM inventory WHERE medication_id LIKE", ('%' + search_query + '%',))
        inventory_records = cursor.fetchall()

        # Clear previous inventory records in Listbox
        listbox.delete(0, tk.END)

        # Update Listbox with fetched inventory records
        for record in inventory_records:
            listbox.insert(tk.END, f"ID: {record[0]}, Medication ID: {record[1]}, Quantity: {record[2]}, Expiration Date: {record[3]}, Date Created: {record[4]}, Selling Price: {record[5]}")


    search_button = ttk.Button(lower_frame, text="Search", command=search_inventory)
    search_button.grid(row=3, column=1, padx=5, pady=5)
    

    cursor.close()
    db.close()

