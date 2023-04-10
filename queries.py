import tkinter as tk
import mysql.connector
from credentials import user_name,pass_word

def queries(root):
        
    db = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=pass_word,
        database="pharmacy"
    )

    # create a cursor
    cursor = db.cursor()

    

    root.title("Stats")

    left_frame = tk.Frame(root, width=200, height=600, bg="#f0f0f0")
    left_frame.pack(side="left", fill="both", expand=True)


    # create a dropdown menu of medication names
    cursor.execute("SELECT name FROM medications")
    medication_names = [name[0] for name in cursor.fetchall()]
    label = tk.Label(left_frame, text="Select medication:")
    label.grid(row=0,column=0,pady=5)

    # create dropdown menu with medication names
    medication_var = tk.StringVar()
    medication_var.set(medication_names[0])
    medication_dropdown = tk.OptionMenu(left_frame, medication_var, *medication_names)
    medication_dropdown.grid(row=0, column=1, pady=5)

    # create a function to execute the SQL queries and display the results
    def get_results():
        
        db = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=pass_word,
        database="pharmacy"
       )

    # create a cursor
        cursor = db.cursor()
        # get the selected medication name from the dropdown menu
        medication_name = medication_var.get()
        
        # execute the first SQL query to get the current stock level for the selected medication
        cursor.execute("SELECT SUM(quantity) AS stock_level FROM inventory JOIN medications ON inventory.medication_id = medications.id WHERE medications.name = %s", (medication_name,))
        stock_level = cursor.fetchone()[0]
        
        # execute the second SQL query to get the number of units of the selected medication sold in the last month
        cursor.execute("SELECT SUM(quantity) AS units_sold FROM sales_records JOIN medications ON sales_records.medication_id = medications.id WHERE medications.name = %s AND date_sold >= DATE_SUB(NOW(), INTERVAL 1 MONTH)", (medication_name,))
        units_sold = cursor.fetchone()[0]
        
        # execute the third SQL query to get the sales trend for the selected medication over the past 6 months
        cursor.execute("SELECT YEAR(date_sold) AS year, MONTH(date_sold) AS month, SUM(quantity) AS units_sold FROM sales_records JOIN medications ON sales_records.medication_id = medications.id WHERE medications.name = %s AND date_sold >= DATE_SUB(NOW(), INTERVAL 6 MONTH) GROUP BY YEAR(date_sold), MONTH(date_sold) ORDER BY year ASC, month ASC", (medication_name,))
        sales_trend = cursor.fetchall()
        
        # create a tkinter label to display the results
        results_label = tk.Label(left_frame, text="Stock Level: {}\nUnits Sold in Last Month: {}\nSales Trend Over Past 6 Months: {}".format(stock_level, units_sold, sales_trend))
        results_label.grid(row=2, pady=5)
    get_results_button = tk.Button(left_frame, text="Get Results", command=get_results)
    get_results_button.grid(row=1,pady=5,columnspan=2)




    right_frame = tk.Frame(root, width=200, height=600, bg="#f0f0f0")
    right_frame.pack(side="right", fill="both", expand=True)


    # medicines that will expire in the next 30 days 
    query = "SELECT name, expiration_date FROM inventory JOIN medications ON inventory.medication_id = medications.id WHERE expiration_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY) ORDER BY expiration_date ASC;"
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    label = tk.Label(right_frame, text="Medications expiring soon:\n")
    label.grid(row=0,column=0, padx=5, pady=5)
    listbox = tk.Listbox(right_frame)
    listbox.grid(row=0,column=1, padx=5, pady=5)
    for row in result:
        listbox.insert(tk.END, f"{row[0]} - {row[1].strftime('%Y-%m-%d')}")


    # medication that are currently out of stock
    label2=tk.Label(right_frame,text="Medication that are out of stock:")
    label2.grid(row=1,column=0, padx=5, pady=5)
    query2 = "SELECT name FROM medications LEFT JOIN inventory ON medications.id = inventory.medication_id WHERE quantity IS NULL OR quantity = 0"
    cursor.execute(query)
    results = cursor.fetchall()
    result_label = tk.Label(right_frame, text="")
    if len(results) > 0:
        result_str = "\n".join([row[0] for row in results])
        result_label.config(text=result_str)
    else:
        result_label.config(text="No medications are currently out of stock.")
    result_label.grid(row=1, column=1,padx=5, pady=5)



    # average monthly sales revenue
    query = "SELECT YEAR(date_sold) AS year, MONTH(date_sold) AS month, SUM(price * quantity) AS monthly_sales_revenue \
            FROM sales_records \
            JOIN sales ON sales_records.id = sales.sales_record_id \
            GROUP BY YEAR(date_sold), MONTH(date_sold);"
    cursor.execute(query)
    results = cursor.fetchall()
    label3 = tk.Label(right_frame, text="Monthly Sales Revenue:\n\n")
    label3.grid(row=2, column=0, pady=5, padx=5)
    for result in results:
        label4 = tk.Label(right_frame, text=f"{result[1]}/{result[0]}: ${result[2]:.2f}\n")
        label4.grid(row=2, column=1, pady=5, padx=5)


    # total inventory value
    cursor.execute("SELECT SUM(quantity * selling_price) AS total_inventory_value FROM inventory")
    result = cursor.fetchone()[0]
    label5 = tk.Label(right_frame, text="Total inventory value:")
    label5.grid(row=3,column=0, padx=5, pady=5)
    label6 = tk.Label(right_frame, text=f"{result}")
    label6.grid(row=3,column=1, padx=5, pady=5)



    # medications that are sold most frequently
    label7=tk.Label(right_frame,text="Medications that are sold most frequently:")
    label7.grid(row=4,column=0,padx=5,pady=5)
    listbox = tk.Listbox(right_frame)
    listbox.grid(row=4,column=1,padx=5,pady=5)
    cursor = db.cursor()
    query = "SELECT name, SUM(quantity) AS total_quantity_sold FROM medications JOIN sales_records ON medications.id = sales_records.medication_id GROUP BY medication_id ORDER BY total_quantity_sold DESC"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        listbox.insert(tk.END, f"{row[0]}: {row[1]} units sold")


    # medication that have highest profit margin
    # cursor.execute("SELECT name, AVG(price - selling_price) AS avg_profit_margin FROM medications JOIN sales_records ON medications.id = sales_records.medication_id JOIN sales ON sales_records.id = sales.sales_record_id JOIN inventory ON medications.id = inventory.medication_id WHERE sales.date_sold >= DATE_SUB(NOW(), INTERVAL 6 MONTH) GROUP BY medication_id ORDER BY avg_profit_margin DESC")
    # results = cursor.fetchall()
    # label8 = tk.Label(right_frame, text="Medication Profit Margins:", font=("Arial Bold", 16))
    # label8.grid(row=5,column=0,padx=5,pady=5)
    # table = tk.Frame(right_frame)
    # table.grid(row=5,column=1,padx=5,pady=5)
    # name_header = tk.Label(table, text="Name", font=("Arial Bold", 12))
    # name_header.grid(row=0, column=0)
    # profit_margin_header = tk.Label(table, text="Profit Margin", font=("Arial Bold", 12))
    # profit_margin_header.grid(row=0, column=1)
    # row_num = 1
    # for result in results:
    #     name = tk.Label(table, text=result[0])
    #     name.grid(row=row_num, column=0)
    #     profit_margin = tk.Label(table, text=result[1])
    #     profit_margin.grid(row=row_num, column=1)
    #     row_num += 1


    # medication that have lowest turnover rate
    cursor.execute("SELECT name, (SUM(quantity) / DATEDIFF(NOW(), MIN(date_added))) AS turnover_rate FROM medications JOIN inventory ON medications.id = inventory.medication_id GROUP BY medication_id ORDER BY turnover_rate ASC;")
    label9 = tk.Label(right_frame, text='Medication with lowest Turnover Rate:')
    label9.grid(row=6,column=0,padx=5,pady=5)
    for (name, turnover_rate) in cursor:
        label10=tk.Label(right_frame,text=f"{name} : {turnover_rate}")
        label10.grid(row=6,column=1,padx=5,pady=5)

    