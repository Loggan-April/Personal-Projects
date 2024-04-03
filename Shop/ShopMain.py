# ctuClass.py
from ShopClass import Stock

# Will be used to stop the program if the user enters the said sentinal value
import sys

# create four objects from the ctuStock class with default values
shop_Name1 = Stock()
shop_Name2 = Stock()
shop_Name3 = Stock()
shop_Name4 = Stock()

#list of all the shops
shop_List = [shop_Name1,shop_Name2,shop_Name3,shop_Name4]

#Makes the following variables global so that the values can be changed later
global shop1_customers,shop2_customers,shop3_customers,shop4_customers,shop1_Sales,shop2_Sales,shop3_Sales,shop4_Sales,shop1_Returns,shop2_Returns,shop3_Returns,shop4_Returns

#Each shops cutomer number is set to zero
shop1_customers = 0
shop2_customers = 0
shop3_customers = 0
shop4_customers = 0

#each Shops sales number is set to zero
shop1_Sales = 0
shop2_Sales = 0
shop3_Sales = 0
shop4_Sales = 0

#Each shops returns number is set to zero
shop1_Returns = 0
shop2_Returns = 0
shop3_Returns = 0
shop4_Returns = 0

# Stores the names,Prices, and values of the stock that will be sold
stock = { 
    "Jive": {"Price": 9.99, "quantity": 22},
    "1L Coke": {"Price": 15.99, "quantity": 12},
    "2L Coke": {"Price": 30.99, "quantity": 8},
    "Doritos": {"Price": 21.99, "quantity": 10}
}


# Function contains the main menu options
def main_menu():
    # main menu 
    print("Welcome to The One Stop Shop")
    print("1. Shop Management")
    print("2. Sales")
    print("3. Returns")
    print("4. Stock")
    print("99. Exit")
    print()
    global Main_option
    Main_option =  input("Select an option or 99 to exit: ")    #Stores the user's option to navigate the menu
    print()     #Creates a space underneath the user's input

# Function contains the shop management menu options
def shop_ManagementMenu():
    # shop management menu
    print("Shop Management Menu")
    print("1. Change Shop Name")
    print("2. Change Shop Location")
    print("3. Display Current Shops")
    print("4. Display all shops information")
    print("0. Back")
    print()
    global Shop_option
    Shop_option = input("Select an option: ") # Stores the user's option to navigate the menu
    print()     #Creates a space underneath the user's input

#Function allows the user to change the shop's
def Change_ShopName():
    print("Change Shop Name")
    print()
    print("Select Shop")
    print("1. ",shop_Name1.shop_Name)
    print("2. ",shop_Name2.shop_Name)
    print("3. ",shop_Name3.shop_Name)
    print("4. ",shop_Name4.shop_Name)
    print("0. Back")
    global ChangeName_option
    ChangeName_option = int(input("Select an option: ")) # stores the user's option to navigate the menu
    print()     #Creates a space underneath the user's input

#Function allows the user to change the shop's location 
def Change_ShopLocation():
    print("Change Shop Location")
    print()
    print("Select Shop")
    print("1. ",shop_Name1.shop_Name,",",shop_Name1.shop_Location)  #prints the shop name and location
    print("2. ",shop_Name2.shop_Name,",",shop_Name2.shop_Location)  #prints the shop name and location
    print("3. ",shop_Name3.shop_Name,",",shop_Name3.shop_Location)  #prints the shop name and location
    print("4. ",shop_Name4.shop_Name,",",shop_Name4.shop_Location)  #prints the shop name and location
    print("0. Back")
    global Location_option
    Location_option = int(input("Select an option: ")) # stores the user's option for which shop's location to change
    print()     #Creates a space underneath the user's input

#Function displays all the current shops
def Display_CurrentShops():
    #Displays all the current shops
    print("Current Shops")
    print("1.",shop_Name1.shop_Name,",",shop_Name1.shop_Location)   # Prints the current shops as well as their locations
    print("2.",shop_Name2.shop_Name,",",shop_Name2.shop_Location)   # Prints the current shops as well as their locations
    print("3.",shop_Name3.shop_Name,",",shop_Name3.shop_Location)   # Prints the current shops as well as their locations
    print("4.",shop_Name4.shop_Name,",",shop_Name4.shop_Location)   # Prints the current shops as well as their locations
    print()

#Function Displays all the shops and their information
def Display_AllShopsInfo():
    # prints all the shops and their Location,customers,Sales, and Returns
    print("----------------------")
    print()
    print("Shop Name:",shop_Name1.shop_Name)
    print("Shop Location:",shop_Name1.shop_Location)
    print("Number of Customers:",shop1_customers)
    print("Current Sales:",shop1_Sales)
    print("Returns: ",shop1_Returns)
    print()
    print("----------------------")
    print()

    print("----------------------")
    print()
    print("Shop Name:",shop_Name2.shop_Name)
    print("Shop Location:",shop_Name2.shop_Location)
    print("Number of Customers:",shop2_customers)
    print("Current Sales:",shop2_Sales)
    print("Returns: ",shop2_Returns)
    print()
    print("----------------------")
    print()

    print("----------------------")
    print()
    print("Shop Name:",shop_Name3.shop_Name)
    print("Shop Location:",shop_Name3.shop_Location)
    print("Number of Customers:",shop3_customers)
    print("Current Sales:",shop3_Sales)
    print("Returns: ",shop3_Returns)
    print()
    print("----------------------")
    print()

    print("----------------------")
    print()
    print("Shop Name:",shop_Name4.shop_Name)
    print("Shop Location:",shop_Name4.shop_Location)
    print("Number of Customers:",shop4_customers)
    print("Current Sales:",shop4_Sales)
    print("Returns: ",shop4_Returns)
    print()
    print("----------------------")
    print()

# Function prints the Sales menu
def Sales_Menu():
    print("Sales Menu")
    print("1.","Jive ","R",stock["Jive"]["Price"])
    print("2.","1L Coke ","R",stock["1L Coke"]["Price"])
    print("3.","2L Coke ","R",stock["2L Coke"]["Price"])
    print("4.","Doritos","R",stock["Doritos"]["Price"])
    print("0. Back")
    global Sales_option,Sales_Quantity,Sales_shop_option
    Sales_option = input("Select an option: ")
    Sales_Quantity = int(input("How many would you like to buy?")) #Captures how many items the user would like to buy
    print("Which shop would you like to purchase from? ","\n",shop_Name1.shop_Name,"\n",shop_Name2.shop_Name,"\n",shop_Name3.shop_Name,"\n",shop_Name4.shop_Name) #prints the shops that the customer would like to make the prucahse from
    Sales_shop_option = int(input("Select a shop: ")) #Captures the shop that the user would like to purchase from
    print("Thank you for your purchase.")
    print()     #Creates a space underneath the user's input

# Function prints the Returns Menu
def Returns_Menu():
    print()
    print("Returns Menu")
    print("1. Return")
    print("0. Back")
    global Return_option
    Return_option = input("Select an option")
    print()     #Creates a space underneath the user's input

# Function Prints the Stock Menu
def Stock_Menu():
    print()
    print("Stock Menu")
    print("1. Display Stock") #Displays the current stock
    print("2. Add Stock") #Allows the user to add stock
    print("0. Back")    #Allows the user to back 
    print()     #Creates a space underneath the user's input

# while loop for the program to repeat
while True:
    #Displays the main menu
    main_menu() 

    #Displays the shop management menu if "1" is selected
    if Main_option == "1":
        shop_ManagementMenu() #Displays the Shop management if "1" is selected

        if Shop_option == "1":
            Change_ShopName()   #Displays the Change name menu if "1" is selected

            selected_shop = shop_List[ChangeName_option-1] #finds the shop user is looking for and changes it to the user's desired name
            NewName = input("Type the new shop name: ")    
            selected_shop.shop_Name = NewName # changes the name of the shop to the user's input
            print()
            print("Shop name was successfully changed to ",'"',NewName,'"')

            if ChangeName_option == 0:
                print("Going back...")
                shop_ManagementMenu()   #Displays the shop management if "0" is selected
                
            else:
                print()
                Change_ShopName() 

        elif Shop_option == "2":
            Change_ShopLocation()
            selected_shop = shop_List[Location_option-1]# finds the shop that the user is looking for and changes the loction for that specific shop
            NewName = input("Enter a location Free State,Gauteng, KZN, Limpopo:")    
            selected_shop.shop_Location = NewName
            print()
            print("Shop name was successfully changed to ",NewName)

            if ChangeName_option == 0:
                print("Going back...")
                shop_ManagementMenu()
                
            else:
                print()
                Change_ShopLocation()

        elif Shop_option == "3":
            Display_CurrentShops()
        
        elif Shop_option == "4":
            Display_AllShopsInfo()

        # It will display the main menu if "0" is entered by the user
        elif Shop_option == "0":
            print("Going back...")
            shop_ManagementMenu()

        # Displays the Shop Management menu again if the user's input is not one of the above
        else:
            print("Invalid Input. Please pick an option above")  
            print()
            shop_ManagementMenu() 

    # Displays the Sales menu
    elif Main_option == "2":
        Sales_Menu()
        if Sales_shop_option == 1:
            shop1_customers += 1 # increase the shops customer number by one
            shop1_Sales = Sales_Quantity    # increase the sales amount by the amount that the user purchases

        elif Sales_shop_option == 2:
            shop2_customers += 1 # increase the shops customer number by one
            shop2_Sales = Sales_Quantity    # increase the sales amount by the amount that the user purchases

        elif Sales_shop_option == 3:
            shop3_customers += 1 # increase the shops customer number by one
            shop3_Sales = Sales_Quantity    # increase the sales amount by the amount that the user purchases

        elif Sales_shop_option == 4:
            shop4_customers += 1 # increase the shops customer number by one
            shop4_Sales = Sales_Quantity    # increase the sales amount by the amount that the user purchases

    # Displays the Returns menu
    elif Main_option == "3":
        Returns_Menu()
        if Return_option == "1":
            print("1. ","Jive","R",stock["Jive"]["Price"])   # prints the stock inventory
            print("2. ","1L Coke","R",stock["1L Coke"]["Price"])  # prints the stock inventory
            print("3. ","2L Coke","R",stock["2L Coke"]["Price"])  # prints the stock inventory
            print("4. ","Doritos","R",stock["Doritos"]["Price"])  # prints the stock inventory
            print()
            Returns_option = input("Select an option: ") # stores the user's selection
            Returns_quantity = input("Please enter the amount to return:") # captures the amount of stock to be returned
            print("Which shop would you like to Return to? ","\n",shop_Name1.shop_Name,"\n",shop_Name2.shop_Name,"\n",shop_Name3.shop_Name,"\n",shop_Name4.shop_Name) #prints the shops that the customer would like to make the return to
            Return_shop = int(input("Please select a shop to return to: ")) # Captures the shop that the returns are going to
            
            if Return_shop == 1:
                shop1_customers += 1 # increase the shops customer number by one
                shop1_Returns = Returns_quantity    # increase the returns amount to the amount the user specifies

            elif Return_shop == 2:
                shop2_customers += 1 # increase the shops customer number by one
                shop2_Returns = Returns_quantity    # increase the returns amount to the amount the user specifies

            elif Return_shop == 3:
                shop3_customers += 1 # increase the shops customer number by one
                shop3_Returns = Returns_quantity    # increase the returns amount to the amount the user specifies

            elif Return_shop == 4:
                shop4_customers += 1 # increase the shops customer number by one
                shop4_Returns = Returns_quantity    # increase the returns amount to the amount the user specifies

        elif Return_option == "0": # if the user enters "0" then the program willprint the main menu again
            print()
            main_menu()

        else:
            print()
            print("Invalid input. Please enter a valid input")

    # Displays the Stock menu 
    elif Main_option == "4":
        Stock_Menu()
        stock_option = input("Select an option: ") # stores the user's selection
        if stock_option == "1":
            print("Jive",stock["Jive"]["quantity"],"Left","@","R",stock["Jive"]["Price"])   # prints the stock inventory
            print("1L Coke",stock["1L Coke"]["quantity"],"Left","@","R",stock["1L Coke"]["Price"])  # prints the stock inventory
            print("2L Coke",stock["2L Coke"]["quantity"],"Left","@","R",stock["2L Coke"]["Price"])  # prints the stock inventory
            print("Doritos",stock["Doritos"]["quantity"],"Left","@","R",stock["Doritos"]["Price"])  # prints the stock inventory
            print()

        elif stock_option == "2":
            item_name = input("Enter the name of the item: ") # Captures the new stock name
            item_price = float(input("Enter the price of the item: ")) # Captures the new price for the stock
            item_quantity = int(input("Enter the quantity of the stock on hand: ")) # Captures the quantity of the new stock

            stock[item_name]= {'Price': item_price,'quantity': item_quantity} #inserts the new stock into the stock list
            print("item has been added to stock") # confirms the stock has been added to the stock list
            print(stock) # prints the new stock list with the added item


        elif stock_option == "0":
            main_menu()

        else:
            print()
            print("Invalid input. Please enter a valid option")
            
    # Exits the program if the user selects "99"
    elif Main_option == "99":
        print("Exiting program..")
        # Exits the program
        sys.exit()

    # Displays the main menu again if the user's input is not one of the above
    else:
        print("Invalid Input. Please pick an option above")
        print()
        main_menu()     
