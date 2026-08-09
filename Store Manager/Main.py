from sqlite3 import Connection
#from typing import Optional



#-------Importing functions from Databse file-------------
from Database import(
    get_connection,
    add_customer,
    display_customers,
    prompt_delete_customer,
    add_employee,
    prompt_delete_employee,
    display_employees,
    display_products,
    display_sales,
    add_product,
    update_product,
    sell_product,
    prompt_delete_product,
)


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



#------------ Main Menu ------------
def Main_Menu():
        # Simple main menu
        print("Welcome to the Store Management\n")
        print("1. Manage Employees")
        print("2. Manage Customers")
        print("3. Manage Products")
        print("4. Manage Sales\n")
        print("0. Exit\n")

#----- Class to manage employees and customers --------------
class Person_Manager:
    def Manage_Employees(conn: Connection):
        # while loop to continuosly ask the user for their selection if they choose one outside the desired range
        while True:
            # Employees main menu
            print("\t1. Add employee")
            print("\t2. Remove employee")
            print("\t3. Display employees")
            print("\t0. Return to main menu\n")
            
            choice = input("Please select an option above: ")       # allows the user to select an option from the menu
            # if statement to determine the user's selection
            if choice == "1":
                # allows the user to enter a new employee's information
                name = input_non_empty("Name: ")
                surname = input_non_empty("Surname: ")
                cell_number = input_non_empty("Cell Number: ")
                email = input_non_empty("Email address: ")
                new_id = add_employee(conn,name,surname,cell_number,email)
                print(f"Employee added with EmployeeID = {new_id}\n")
            
            elif choice == "2":
                prompt_delete_employee(conn)         # calls the prompt_delete_employee function from the database file to delete an employee


            elif choice == "3":
                display_employees(conn)             # calls the display_employee function from the database file to display all employees

            elif choice == "0":
                Main_Menu()                         # calls the main_menu function
                break
            else:
                print("Invalid option try again: ")     # prints an error message if the user's selection is out of the range

    def Manage_Customers(conn: Connection):
        # while loop to continuosly ask the user for their selection if they choose one outside the desired range
        while True:
            # Customers main menu
            print("\t1. Add customer")
            print("\t2. Remove customer")
            print("\t3. Display customers")
            print("\t0. Return to main menu\n")
            
            choice = input("Please select an option above: ")       # allows the user to select an option from the menu
            #if statement to determine the user's selection
            if choice == "1":
                # allows the user to enter a new customer's information
                name = input_non_empty("Name: ")
                surname = input_non_empty("Surname: ")
                cell_num = input_non_empty("Cell Number: ")
                Email = input_non_empty("Email address: ")
                billing = input_non_empty("Billing Address: ")
                new_id = add_customer(conn, name, surname, cell_num, Email, billing)
                print(f"Customer added with CustomerID = {new_id}\n")

            elif choice == "2":
                prompt_delete_customer(conn)        # calls the prompt_delete_customer function from the database file to delete a customer

            elif choice == "3":
                display_customers(conn)             # calls the display_customers functino from the database file to display all customers

            elif choice == "0":
                Main_Menu()                     # calls the main_menu function 
                break
            else:
                print("Invalid option try again: ")         # prints an error message if the user's selection is not within the desired range

#---------- Class to manage products and sales --------------------
class Store:
    def Manage_Products(conn: Connection):
        # while loop to continuosly ask the user for their selection if they choose one outside the desired range
        while True:
            # Products Menu
            print("\t1. Add a product")
            print("\t2. Remove a product")
            print("\t3. Update a product")
            print("\t4. Display all products")
            print("\t5. Sell a product")
            print("\t0. Return to main menu\n")

            choice = input("Please select an option above: ")       # allows the user to select an option from the menu
            # if statement to determine the user's selection
            if choice == "1":
                # allows the user to enter a new customer's information
                name = input_non_empty("Name: ")
                price = input_float("Price: ")
                quantity = input_int("Quantity: ")
                new_id = add_product(conn,name,price,quantity)
                print(f"Product added with ProductID = {new_id}\n")

            elif choice == "2":
                prompt_delete_product(conn)         #Prompts the user to deuserIDe if they really want to delete a product

            elif choice == "3":
                display_products(conn)      # displays all the products to be updated
                
                userID = input_int("ProductID to update (blank to cancel): ", allow_blank=True) # gets the user's selection for product to be updated
                
                if userID is None:  # checks if the user entered nothing and prints an error message
                    print("Update Cancelled.")
                    continue

                # allows the user to update a products information
                print("Enter new values (leave blank to keep current value):")
                new_name = input("New name: ").strip() or None
                new_price = input_float("New price: ", allow_blank=True)
                new_quantity = input_int("New quantity: ", allow_blank=True)
                rows_updated = update_product(conn, userID, name=new_name, Price=new_price, Quantity=new_quantity)
                
                #checks if the product has been updated and prints a message to follow that check
                if rows_updated:
                    print(f"Product {userID} updated.\n")
                else:
                    print("No changes made or invalid ProductID\n")

            elif choice == "4":
                display_products(conn)      # displays all the products in the products table

            elif choice == "5":
                sell_product(conn)          # calls the sell_product function to sell a product

            elif choice == "0":
                Main_Menu()             # prints the main menu
                break
            else:
                print("Invalid option try again: ") # print an error message if the user's selection is out of the desired range

    def Manage_Sales(conn: Connection):
        # while loop to continuosly ask the user for their selection if they choose one outside the desired range
        while True:
            # Sales Menu
            print("\t1. Sell a product")
            print("\t2. Display all sales")
            print("\t0. Return to main menu\n")

            # If statement to get user selection 
            choice = input("Please select an option above: ")
            # if statement to determine the user's selection
            if choice == "1":
                sell_product(conn)          #calls the sell_product function in the database file

            elif choice == "2":
                display_sales(conn)         #calls the display_sales function in the database file

            elif choice == "0":
                Main_Menu()                 #calls the main menu if user selects for it
                break
            else:
                print("Invalid option try again: ")




#----------- Main calls all the main functions and runs the program --------------------
def main():
    conn = get_connection()
    try:
        # While loop to continue asking for user input until they select '0' to exit the program    
        while(True):
            option = int(input("select an option: "))
            print()
            if option == 1:
                Person_Manager.Manage_Employees(conn)   # Connects to the Employee function inside the Person manages class
            elif option == 2:
                Person_Manager.Manage_Customers(conn)   # Connects to the Customers function inside the Person manages class
            elif option == 3:
                Store.Manage_Products(conn) # Connects to the products function insdie the store class
            elif option == 4:
                Store.Manage_Sales(conn)    # Connects to the Sales function insdie the store class
            elif option == 0:
                print("Good Bye!")
                break
            else:
                print("Invalid option please select 1-4 or 0 to exit")
    finally:
        print()#  conn.close()

# Calls the main menu for the user to select an option
Main_Menu()


#Calls the main function to run the while loop for user interaction
main()
