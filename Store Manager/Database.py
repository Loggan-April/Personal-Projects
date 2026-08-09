import sqlite3
from sqlite3 import Connection
from typing import Optional
from datetime import datetime


DB_PATH = "shop.db"

# ---------- Input helpers ----------
def input_non_empty(prompt: str):
    while True:
        string = input(prompt).strip()      # allows user to enter a string and removes any spaces after the string
        if string == "":                    # checks if the user entered nothing 
            print("Input cannot be empty. Try again.")
            continue
        return string                       #returns the user's input

def input_float(prompt: str, allow_blank: bool = False):
    while True:
        num = input(prompt).strip()            # allows the user to enter a float value and removes any spaces after the float
        if num == "" and allow_blank:          # allows the user to leave this variable empty if they choose to
            return None
        try:
            return float(num)                   # returns the value the user has entered
        except ValueError:
            print("Please enter a valid number (e.g. 12.50).")  # prints an error message if the user enters anything other than an integer or float

def input_int(prompt: str, allow_blank: bool = False):
    while True:
        integer = input(prompt).strip()     # allows user to enter a integer and removes any spaces after the integer
        if integer == "" and allow_blank:   # checks if the user entered a value and allows user to leave the variable empty if the choose to
            return None
        try:
            return int(integer)             # returns the value the user entered
        except ValueError:
            print("Please enter a valid integer.")     # prints an error message if the user enters anything other than an integer 


#-------- Database functions ----------
def get_connection(path: str = DB_PATH):
    conn = sqlite3.connect(path)        # creates a connection to the SQLite databse file at the given path
    conn.row_factory = sqlite3.Row      # allows to access columns by name
    conn.execute("PRAGMA foreign_keys = ON;")   # allows for ralational integrity
    return conn     #returns the configured connection object


#------- Manages the Customers table --------------
def add_customer(conn: Connection, name: str, surname: str, Cell_Number: str, Email: str, billing_address: str):
    cursor = conn.cursor()          # assigns the tables cursor to a variable "cursor"
    cursor.execute(
        "INSERT INTO Customers (Name, Surname, Cell_Number, Email, Billing_Address) VALUES (?, ?, ?, ?, ?)",
        (name, surname, Cell_Number, Email, billing_address)
    )       # inserts data into table customers
    conn.commit()   # commits that data to the table
    print("Customer added successfully!")
    return cursor.lastrowid     # returns the ID of the last row

def display_customers(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers ORDER BY CustomerID")
    rows = cursor.fetchall()
    if not rows:        # checks if the rows variable is empty
        print("\nNo customers found.\n")
        return
    print("\nCustomer List:")
    for row in rows:        #prints all the data inside the rows variable
        print("-" * 30)
        print(f"CustomerID           : {row['CustomerID']}")
        print(f"Name                 : {row['Name']}")
        print(f"Surname              : {row['Surname']}")
        print(f"Cell_Number          : {row['Cell_Number']}")
        print(f"Email                : {row['Email']}")
        print(f"Billing_Address      : {row['Billing_Address']}")
    print("-" * 30 + "\n")

def delete_customer(conn: Connection, customer_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE CustomerID = ?", (customer_id,))        #deletes from the customer table where specified
    conn.commit()
    print("Customer Successfully Deleted!")
    return cursor.rowcount      # returns the ID of the last row

def prompt_delete_customer(conn: Connection):
    display_customers(conn) # dispalys the customers
    userID = input_int("Enter CustomerID to remove (blank to cancel): ", allow_blank=True)
    if userID is None:      # checks if the userID is blank
        print("Cancelled.")
        return
    confirm = input(f"Are you sure you want to DELETE custoemr {userID}? Type 'yes' to confirm: ").strip() # prompts the user to confirm deletion
    if confirm != "yes":        # checks if the user entered a string other than "yes"
        print("Deletion cancelled.\n")
        return
    
    try:
        deleted = delete_customer(conn,userID)      # assigns the values to a variable "deleted"
    except Exception as e:
        print("Error deleting employee:",e,"\n")    # prints error if deletion errors occur 
        return
    
    if deleted:     # checks if deletion was successful
        print(f"Employee {userID} deleted successfully. \n")     # prints a message if deletion was successful
    else:
        print(f"No employee found with EmployeeID {userID}. \n")    # prints a message if deletion failed



#-------- Manages the Employees table ----------------------
def add_employee(conn: Connection, name: str, surname: str, cell_number: str, email: str):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Employees (Name, Surname, Cell_Number, Email) VALUES (?,?,?,?)",
        (name, surname, cell_number, email)
    )       # inserts data into table Employees
    conn.commit()   # commits everything to the table
    print("Employee added Successfully!")
    return cursor.lastrowid         # returns the ID of the last row ID

def delete_employee(conn: Connection, employee_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE EmployeeID = ?", (employee_id,)) # Deletes data from the Employees tables where specified
    conn.commit()       # commits the deletion
    print("Employee Successfully Deleted!\n")
    return cursor.rowcount      #returns the ID of the last row ID

def prompt_delete_employee(conn: Connection):
    display_employees(conn)
    userID = input_int("Enter EmployeeID to remove (blank to cancel): ", allow_blank=True)
    if userID is None:      #checks if the variable is empty
        print("Cancelled.")
        return
    confirm = input(f"Are you sure you want to DELETE employee {userID}? Type 'yes' to confirm: ").strip() # gets user input and removes any spaces after their input
    if confirm != "yes":
        print("Deletion cancelled.\n")
        return
    
    try:
        deleted = delete_employee(conn, userID)
    except Exception as e:
        print("Error deleting employee:",e,"\n")
        return
    
    if deleted:         # checks if the information was deleted
        print(f"Employee {userID} deleted successfully.\n")
    else:
        print(f"No employee found with EmployeeID {userID}.\n")

def display_employees(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees ORDER BY EmployeeID")       # selects everything from the table
    rows = cursor.fetchall()        # assigns all the data inside the table to rows
    if not rows:            #checks if rows is empty
        print("\nNo Employees found.\n")
        return
    print("\nEmployee List:")
    for row in rows:                #prints a list of all the employees
        print("-" * 30)
        print(f"EmployeeID : {row['EmployeeID']}")
        print(f"Name       : {row['Name']}")
        print(f"Surname    : {row['Surname']}")
        print(f"Cell_Number: {row['Cell_Number']}")
        print(f"Email      : {row['Email']}")
    print("-" * 30 + "\n")



#--------- Manages the Products table ------------------
def display_products(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products ORDER BY ProductID")     # selects everything from the products table
    rows = cursor.fetchall()
    
    if not rows:        # checks if the rows variable is empty
        print("\nNo Products found.\n")
        return
    
    print("\nProduct List:")
    for row in rows:        # prints all the information inside the rows variable
        print("-" * 30)
        print(f"ProductID  : {row['ProductID']}")
        print(f"Name       : {row['Name']}")
        print(f"Price      : {row['Price']}")
        print(f"Quantity   : {row['Quantity']}")
    print("-" * 30 + "\n")

def add_product(conn: Connection, name: str, price: float, quantity: int):
    cursor = conn.cursor()
    cursor.execute("" \
        "INSERT INTO Products (Name, Price, Quantity) VALUES (?,?,?)",
        (name, price, quantity)
        )   # inserts data into the products tables where specified
    conn.commit()       # commits that data to the table
    print("Product added Successfully!")
    return cursor.lastrowid     # returns the ID of the last row 

def update_product(conn: Connection, product_id: int, name: Optional[str] = None, Price: Optional[float]= None, Quantity: Optional[int]= None):
    update = []
    params = []
    if name is not None:        # Updates the name column if a name is provided
        update.append("Name = ?"); params.append(name)
    if Price is not None:       # Updates the Price column if a Price is provided
        update.append("Price = ?"); params.append(Price)
    if Quantity is not None:    # Updates the quantity column if a Quantity is provided
        update.append("Quantity = ?"); params.append(Quantity)
    if not update:      # checks if the update list has any values
        return 0
    params.append(product_id)
    sql = "Update Products SET " + ", ".join(update) + " WHERE ProductID = ?"
    cursor = conn.cursor()
    cursor.execute(sql, tuple(params))
    conn.commit()       # commits the changes to the table
    print("Product updates successfully")
    return cursor.rowcount      # returns the ID of the last row

def delete_product(conn: Connection, product_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Profucts WHERE ProductID = ?", (product_id,))       # Deletes from the products table where specified
    print("Product Successfully Deleted!\n")
    return cursor.rowcount  # Returns the ID of the last row

def prompt_delete_product(conn: Connection):
    display_products(conn)
    userID = input_int("Enter ProductID to remove (leave blank to cancel): ", allow_blank=True)
    if userID is None:      #  checks if the userID variable has a value
        print("Cancelled.\n")
        return
    confirm = input(f"Are you sure you want to DELETE employee {userID}? Type 'yes' to confirm: ").strip()
    if confirm != "yes":        # stops the deletion if "yes" isn't entered
        print("Deletion cancelled.\n")
        return
    try:
        deleted = delete_product(conn, userID)  # deletes specified information 
    except Exception as e:
        print("Error deleteing product:",e,"\n")
        return
    if deleted:
        print(f"Product {userID} deleted successfully.\n")
    else:
        print(f"No employee found with ProductID {userID}.\n")

#----------- Manages the Sales table ------------------------
def display_sales(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sales ORDER BY SalesID")      # Selects everything from the Sales table
    rows = cursor.fetchall()
    if not rows:            # checks if the rows variable has values assigned to it
        print("\nNo Sales found.\n")
        return
    print("\nSales List:")
    for row in rows:
        print("-" * 30)
        print(f"SaleID  : {row['SalesID']}")
        print(f"Date    : {row['Date']}")
        print(f"Name    : {row['Name']}")
        print(f"Total   : {row['Total']}")
    print("-" * 30 + "\n")


#---------- Creates a sale and posts to sales table ------------------------
def sell_product(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID,name, price, quantity FROM Products")
    rows = cursor.fetchall()

    if not rows:                        #Checks if there are products in the product table
        print("No products available.\n")
        return
    
    print("\nAvailable Products:")
    for row in rows:                    #Returns all products in the product table
        print(f"ID = {row[0]} | Name = {row[1]} | Price = {row[2]} | Quantity = {row[3]}")  
    
    product_id = input_int("\nPlease choose a Product (ID) to sell: ")      #User input on product to sell
    
    if product_id is None:              #If user enters nothing the sale is cancelled
        print("Cancelled.\n")
        return
    
    try:                
        product_id = int(product_id)    # matches the selection with the product ID
    except ValueError:
        print("Invalid Product ID.\n")
        return
    
    cursor.execute("SELECT Name, Price, Quantity FROM Products WHERE ProductID = ?",(product_id,))
    product = cursor.fetchone()

    if not product:         # checks if the product variable is empty
        print("Invalid Product ID. \n")
        return
    name, price, quantity_available = product

    qty_to_sell = input_int("How many units would you like to sell? ")

    if qty_to_sell <= 0:        # checks if the quantity is less than 1
        print("Quantity must be greater than 0.\n")
        return
    
    if qty_to_sell > quantity_available:    # checks if the quantity you want to sell is more than available stock
        print("Not enough stock.\n")
        return
    
    total = price * qty_to_sell     # calculates the total price based on quantity to sell and price
    sale_date = datetime.now().strftime("%Y-%m-%d")     # retrieves the current date

    cursor.execute("INSERT INTO Sales (Date, Name, Total) VALUES (?, ?, ?)", (sale_date,name,total))
    
    new_quantity = quantity_available - qty_to_sell
    cursor.execute("UPDATE Products SET Quantity = ? WHERE ProductID = ?", (new_quantity,product_id))

    conn.commit()       # commits the data to both the sales and products table

    print("\nSale completed successfully!")
    print(f"Product: {name}")
    print(f"Quantity Sold: {qty_to_sell}")
    print(f"Total: {total}\n")