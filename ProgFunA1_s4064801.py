import sys

# Initialize existing customers and their reward points
customers = {"Kate": 20, "Tom": 32};

# Initialize products and their unit prices
products = {
    "vitaminC": {
        "unit_price": 12.0, 
        "prescription": 'n'
        },
    "vitaminE": {
        "unit_price": 14.5,
        "prescription": 'n'
        },
    "coldTablet": {
        "unit_price": 6.4,
        "prescription": 'n'
        },
    "vaccine": {
        "unit_price": 32.6,
         "prescription": 'y'
         },
    "fragrance": {
        "unit_price": 25.0,
         "prescription": 'n'
        },
};

def display_message(message):
    # Displey messages
    sys.stdout.write(message);
    # Flush the buffer
    sys.stdout.flush();

def read_customer_name_and_validate():
    # Keep repeating until a valid name is entered
    while True:
        # Display message asking for customer's name
        display_message("\n\nEnter the customer's name: ");
        # Read customer name
        customer_name = sys.stdin.readline().strip();
        # Check is customer name contains only alphebetic characters
        # Python string isalpha() method. Available at: https://www.w3schools.com/python/ref_string_isalpha.asp (Accessed: 22 March 2024). 
        if (customer_name.isalpha()):
            # Return the customer name
            return customer_name;
        else:
            # Display error message
            display_message("\nError: Customer name should contain only alphebetic characters.\n\n");

def read_product_name_and_validate():
    while True:
        # Display message asking for product's name
        display_message("Enter the Product's name: ");
        # Read product name
        product_name = sys.stdin.readline().strip();
        if product_name in products:
            # Return the product name
            return product_name;
        else:
            # Display error message
            display_message("\nError: Enterd product is invalid.\n\n");

def check_is_prescription_needed(product_name):
    # Return prescription is needed or not
    return products[product_name]["prescription"] == 'y';

def is_prescription_available():
    # Display message asking prescription
    display_message("Do you have a doctor's prescription for this product? (y/n): ");
    while True:
        # Read answer
        answer = sys.stdin.readline().strip();
        if answer.lower() == 'y':
            return True
        elif answer.lower() == 'n':
            display_message("This product requires a doctor's prescription. Purchase cannot be completed.");
            return False
        else:
            display_message("\nError: Invalid character Enter (y - Yes, n - No)");

def read_product_quantity_and_validate():
    while True:
        # Display message asking for product's quantity
        display_message("Enter the Product's quantity: ");
        quantity = sys.stdin.readline().strip();
        display_message(f"-{quantity}-{quantity.isnumeric()}-{int(quantity) > 0}-{quantity.isnumeric() and int(quantity) > 0}");
        if (quantity.isnumeric() and int(quantity) > 0):
            # Return the product quantity
            return int(quantity);
        else:
            # Display error message
            display_message("\nError: Quantity should contain only positive Integer values.\n\n");

def calculate_total_price(unitPrice, quantity):
    # Calculate the total price and return it
    return unitPrice * quantity;

def calculate_reward_points(totalPrice):
    # Round points to the nearest integer and return it
    return round(totalPrice);

def display_receipt(customer_name, product_name, product_quantity, total_price, reward_points):
    # Creating a multiline string with formatted expressions
    receipt = f"""
-------------------------------------------------
                    Receipt 
-------------------------------------------------
Name:                       {customer_name}
Product:                    {product_name}
Unit Price:                 {products[product_name]["unit_price"]:.2f} (AUD)
Quantity:                   {product_quantity}
-------------------------------------------------
Total cost:                 {total_price:.2f} (AUD)
Earned reward:              {reward_points}
-------------------------------------------------
    """;
    # Display the receipt
    display_message(receipt);

def update_customer(customer_name, earned_reward_points):
    if customer_name in customers:
        customers[customer_name] += earned_reward_points;
    else:
        customers[customer_name] = earned_reward_points;


# Handles the make a purchase logic
def make_purchase():
    # Read inputs
    customer_name = read_customer_name_and_validate();
    product_name = read_product_name_and_validate();
    if (check_is_prescription_needed(product_name) and (not is_prescription_available())):
        return;
    product_quantity = read_product_quantity_and_validate();
    # Do calculation
    total_price = calculate_total_price(products[product_name]["unit_price"], product_quantity);
    earned_reward_points = calculate_reward_points(total_price);
    # Print receipt
    display_receipt(customer_name, product_name, product_quantity, total_price, earned_reward_points);
    # Update customer details and print
    update_customer(customer_name, earned_reward_points);

def add_or_update_product():
    # Add or update product information
    display_message("\n\nEnter the product information (name price dr_prescription):");
    # Read product information and split by whitespace (default seperator)
    product_info = sys.stdin.readline().strip().split();
    product_name = product_info[0];
    price = float(product_info[1]);
    prescription = product_info[2];
    # Update or add product info to the exiting products
    products[product_name] = [price, prescription];

def display_customers():
    # Display existing customers and their reward points
    display_message("\n\nExisting customers and their reward points:\n");
    display_message("-------------------------------------------------------\n");
    # Display customer info by iterating customers
    for customer, reward_points in customers.items():
        display_message(f"Name: {customer} \n");
        display_message(f"Reward points: {reward_points}\n");
        display_message("-------------------------------------------------------\n");

def display_products():
    # Display existing products and their informations
    display_message("\n\nExisting products and their informations:\n");
    display_message("-------------------------------------------------------\n");
    # Display customer info by iterating customers
    for product, product_info in products.items():
        display_message(f"Name: {product}\n");
        display_message(f"Price: {product_info['unit_price']}\n");
        # Ternary operator used to display 'Yes' & 'No' instead of 'y' & 'n'
        display_message(f"Prescription Required: {'Yes ' if product_info['prescription'] == 'y' else 'No'}\n");
        display_message("-------------------------------------------------------\n");

def main_menu():
    # Display main menu. After completing each selected option user will automatically directed to main menu until the user exit from the system
    while True:
        display_message("""
Menu:
1. Make a purchase
2. Add/update information of a product
3. Display existing customers
4. Display existing products
5. Exit
        """)
        # Display message asking user's choice
        display_message("\nSelect your choice: ");
        # Read user choice and do necessary action
        choice = sys.stdin.readline().strip();
        if choice == '1':
            make_purchase();
        elif choice == '2':
            add_or_update_product();
        elif choice == '3':
            display_customers();
        elif choice == '4':
            display_products();
        elif choice == '5':
            sys.exit();
        else:
            display_message("\nError: Invalid choice. Please enter a number between 1 and 5.\n\n");

# Starting point of the program
main_menu();