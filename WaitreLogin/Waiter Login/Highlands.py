import sys

class Restaurant:
    def __init__(self):    
        self.login_credentials = self.load_login_credentials()
        self.menu_items = self.load_menu_items()
        self.tables = self.initialize_tables()
        self.sales_total = 0.0
        self.orders = {} # Tracks orders for tables

    def main_menu(self):    # main menu for the program 
        print()
        print("1. Login")
        print("2. Exit")
        print()
        
    def load_login_credentials(self):   # function to capture and test the user's information 
        # Read login credentials from Login.txt file
        credentials = {}
        with open('Login.txt', 'r') as file:    # opens the file for reading
            for line in file:
                username, password = line.strip().split(',')        # stores all the usernames and passwords from the file to be tested later
                credentials[username] = password        # makes sure that the user name and the password matches
        return credentials

    def load_menu_items(self):      # function to load the menu items
        # Read menu items from Stock.txt file
        menu_items = {}
        with open('Stock.txt', 'r') as file:
            for line in file:
                item, price = line.strip().split(',')
                menu_items[item] = float(price)
        return menu_items

    def initialize_tables(self):
        # Create tables and initialize their assignments
        tables = {}
        for table_number in range(1, 7):    # creates 6 tables that the user waiter can pick from
            tables[table_number] = None  # Assign None initially
        return tables

    def login(self):
        # Prompt for username and password
        global username
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in self.login_credentials and self.login_credentials[username] == password:     # tests whether the username and password entered match the one in the login.txt file
            print("")
            print("Welcome",username)
            print("What would you like to do today?")
            return True
        else:
            print("Invalid credentials. Please try again.")
            return False

    def display_menu(self):     # Display menu  for the program once the waiter is logged in
        # Display the main menu options
        print("\nMain Menu:")
        print("1. Assign Table")
        print("2. Change customers")
        print("3. Add to Order")
        print("4. Prepare bill")
        print("5. Complete Sale")
        print("6. Cash up")
        print("0. Log Out")

    def display_tables(self):
        # Display all tables and their assignments
        print("\nTable Assignments:")
        for table_number, waiter in self.tables.items():    #Displays all the tables and whether they are assigned to a customer
            if waiter is None:
                print(f"Table {table_number}: Not assigned")
            else:
                print(f"Table {table_number}: {username}") # displays the waiter's name if the tabled is assigned to someone

    def assign_table(self):     # function assigns a table to the waiter logged in
        # Assign a table to the current waiter
        print("\nTable Assignment:")
        table_number = int(input("Enter table number: "))
        if table_number in self.tables:
            if self.tables[table_number] is None:
                self.tables[table_number] = username
                print(f"Table {table_number} assigned to the {username}.")
                self.add_customers(table_number)
            else:
                print(f"Table {table_number} is already assigned to another waiter.")
        else:
            print(f"Table {table_number} does not exist.")

    def add_customers(self, table_number):  # adds customers to the table
        # Add customers to the assigned table
        num_customers = int(input("Enter the number of customers: "))
        self.tables[table_number] = (table_number, num_customers)
        print(f"Table {table_number} has {num_customers} customers.")

    def change_customers(self): # changes the amount of customers that was assigned to a table
        # Change the number of customers for the assigned table
        print("\nChange Customers:")
        table_number = int(input("Enter table number: "))
        if table_number in self.tables and self.tables[table_number] is not None:
            num_customers = int(input("Enter the new number of customers: "))
            self.tables[table_number] = (table_number, num_customers)
            print(f"Table {table_number} now has {num_customers} customers.")
        else:
            print(f"Table {table_number} is not assigned to the current waiter.")

    def display_menu_items(self):
        # Display all the menu items with numbers for selection
        # Display all the menu items with numbers and prices for selection
        print("\nMenu Items:")
        for number, (item, price) in enumerate(self.menu_items.items(), start=1):
            print(f"{number}. {item} - R{price:.2f}")

    def add_to_order(self):     #add to order adds items from the Stock.txt to the order
        print("\nAdd to Order:")
        self.display_assigned_tables()
        table_number = int(input("Enter table number: "))
        if table_number in self.tables and self.tables[table_number] is not None:
            self.display_menu_items()
            item_number = int(input("Enter the item number to add: "))
            if item_number in range(1, len(self.menu_items) + 1):
                item = list(self.menu_items.keys())[item_number - 1]
                quantity = int(input("Enter the quantity: "))

                # Store the order in self.orders
                if table_number not in self.orders:
                    self.orders[table_number] = {}
                if item in self.orders[table_number]:
                    self.orders[table_number][item] += quantity
                else:
                    self.orders[table_number][item] = quantity

                print(f"{quantity} {item}(s) added to the order for Table {table_number}.")
            else:
                print("Invalid item number.")
        else:
            print(f"Table {table_number} is not assigned to the current waiter.")

    def display_assigned_tables(self):
        # Display the assigned tables to the current waiter
        print("Assigned Tables:")
        for table_number, assignment in self.tables.items():
            if assignment is not None:
                waiter_table = assignment[0]
                if waiter_table == table_number:
                    print(f"Table {table_number}")

    def prepare_bill(self):     # prepare bill, prepares the bill for the table selected 
        print("\nPrepare Bill:")
        self.display_assigned_tables()
        table_number = int(input("Enter table number: "))
        if table_number in self.tables and self.tables[table_number] is not None:
            if table_number in self.orders:
                total = 0.0
                print(f"\nBill for Table {table_number}:")
                for item, quantity in self.orders[table_number].items():
                    price = self.menu_items[item]
                    item_total = price * quantity
                    total += item_total
                    print(f"{item}: {quantity} x R{price:.2f} = R{item_total:.2f}")
                print(f"\nTotal: R{total:.2f}")
            else:
                print(f"No orders found for Table {table_number}.")
        else:
            print(f"Table {table_number} is not assigned to the current waiter.")

    def complete_sale(self):        # prepares the table for the bill to be paid
        # Complete the sale for the assigned table
        print("\nComplete Sale:")
        self.display_assigned_tables()
        table_number = int(input("Enter table number: "))
        if table_number in self.tables and self.tables[table_number] is not None:
            # TODO: Check if a bill is prepared and proceed with the sale
            print(f"Sale completed for table {table_number}.")
            self.sales_total += 1.0  # Example: Increment the sales total by 1.0
            self.clear_table(table_number)
        else:
            print(f"Table {table_number} is not assigned to the current waiter.")

    def clear_table(self, table_number):        # clears the table for another waiter to use
        # Clear the orders and waiter assignment for the table
        # TODO: Clear the orders for the table
        self.tables[table_number] = None
        print(f"Table {table_number} is cleared and available for reassignment.")

    def cash_up(self):
        print("\nCash Up:")
        total_income = 0.0

        for table_number, table_data in self.tables.items():
            if table_data is not None and table_number in self.orders:
                print(f"\nTable {table_number} Orders:")
                subtotal = 0.0

                # Calculate the subtotal for this table
                for item, quantity in self.orders[table_number].items():
                    price = self.menu_items[item]
                    item_total = price * quantity
                    subtotal += item_total
                    print(f"{item}: {quantity} x R{price:.2f} = R{item_total:.2f}")

                total_income += subtotal
                print(f"Subtotal for Table {table_number}: R{subtotal:.2f}")

        print(f"\nTotal Income: R{total_income:.2f}")
        self.sales_total = total_income  # Update the total sales for the day

        # Ask the user if they want to save the details
        save_file = input("Do you want to save the cash up details to a file? (yes/no): ")
        if save_file.lower() == 'yes':
            file_name = input("Enter the file name: ")
            with open(file_name, 'w') as file:
                file.write("Cash Up Details\n")
                file.write(f"Total Income: R{total_income:.2f}\n\n")
                for table_number in self.orders:
                    file.write(f"Table {table_number} Orders:\n")
                    for item, quantity in self.orders[table_number].items():
                        price = self.menu_items[item]
                        item_total = price * quantity
                        file.write(f"{item}: {quantity} x R{price:.2f} = R{item_total:.2f}\n")
                    file.write("\n")
            print(f"Cash up details saved to {file_name}.")

    def retrieve_orders(self, table_number):
        # Retrieve the orders for a table
        table_orders = {}

        if table_number in self.orders:
            orders = self.orders[table_number]
            for item, quantity in orders.items():
                if item in table_orders:
                    table_orders[item] += quantity
                else:
                    table_orders[item] = quantity

        return table_orders

    def save_cash_up_details(self, file_name, total_income, tables):
        # Save the cash up details to a file
        with open(file_name, 'w') as file:
            file.write("Cash Up Details\n")
            file.write(f"Total Income: ${total_income:.2f}\n\n")

            for table_number, table_data in tables.items():
                if table_data is not None:
                    table_orders = self.retrieve_orders(table_number)

                    if table_orders:
                        file.write(f"Table {table_number} Orders:\n")
                        for item, quantity in table_orders.items():
                            price = self.menu_items[item]
                            item_total = price * quantity
                            file.write(f"{item}: {quantity} x ${price:.2f} = ${item_total:.2f}\n")

                        file.write("\n")

        print(f"Cash up details saved to {file_name}.")

    def clear_daily_total(self):        # clears the total for another table to be cash_up
        # Clear the daily total sales
        self.sales_total = 0.0
        print("Daily total cleared.")

    def run(self):      # runs the entire program
        # Main program loop
        logged_in = False
        self.main_menu() 
        while True:
            main_menu_option = int(input("Select an option above: "))
            if main_menu_option == 1:
                while True:
                    if not logged_in:
                        logged_in = self.login()
                    else:
                        self.display_menu()
                        option = input("Enter your choice: ")
                        print("")
                        if option == '0':
                            logged_in = False
                            self.main_menu()
                        elif option == '1':
                            self.display_tables()
                            self.assign_table()
                        elif option == '2':
                            self.display_tables()
                            self.change_customers()
                        elif option == '3':
                            self.add_to_order()
                            self.display_menu_items()
                        elif option == '4':
                            self.prepare_bill()
                        elif option == '5':
                            self.complete_sale()
                        elif option == '6':
                            self.cash_up()
                            self.clear_daily_total()
                        else:
                            print("Invalid choice. Please try again.")
            elif main_menu_option == 2:
                print("Exiting...")
                sys.exit()

            else:
                print("Invalid option. please selec an option above")
                print("")


# Create an object of the Restaurant class
restaurant = Restaurant()
# Run the restaurant management system
restaurant.run()
