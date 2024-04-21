# python version Python 3.8.18
# Git hub repository https://github.com/jpbinith/COSC2531_Assignment_1

import sys

# Initialize existing customers details
customers = {
    "Kate": {
        "total_rewards": 20
    }, 
    "Tom": {
        "total_rewards": 32
    }
};

# Initialize existing products details
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
            # Update customer details.
            update_customer(customer_name, 0);
            # Return the customer name
            return customer_name;
        else:
            # Display error message
            display_message("\nError: Customer name should contain only alphebetic characters.\n\n");

def read_product_name_and_validate():
    # Keep repeating until a valid input is entered
    while True:
        is_valid_products = True;
        # Display message asking for product's name
        display_message("Enter the list of Product's name seperated by commas: ");
        # Read product name
        product_name_list = [product_name.strip() for product_name in sys.stdin.readline().split(',')];
        # Check for invalid products
        for product_name in product_name_list:
            if product_name not in products:
                # Display error message
                display_message(f"\nError: Enterd product {product_name} is invalid.\n\n");
                is_valid_products = False;
                break;
        # Skip the below execution and point to the start of the function
        if (not is_valid_products):
            continue;
        
        # Return the product names
        return product_name_list;

def prescription_needed_products(product_name_list):
    pres_need_products = [];
    for product_name in product_name_list:
        # Check prescription is needed or not each product
        if(products[product_name]["prescription"] == 'y'):
            # Return true if any product needs a prescription
            pres_need_products.append(product_name)
    # Return false if any product do not needs a prescription
    return pres_need_products;

def is_prescription_available(product):
    # Display message asking prescription
    display_message(f"Do you have a doctor's prescription for the product {product}? (y/n): ");
    # Keep repeating until a valid input is entered
    while True:
        # Read answer
        answer = sys.stdin.readline().strip();
        if answer.lower() == 'y':
            return True;
        elif answer.lower() == 'n':
            display_message(f"This product {product} requires a doctor's prescription. This product cannot be purchased. skipping...\n\n");
            return False;
        else:
            display_message("\nError: Invalid character. Enter (y - Yes, n - No)");

def read_product_quantity_and_validate(product_name_list, prescription_needed_products_list):
    quantity_list = [];
    # Keep repeating until a valid input is entered
    while True:
        # Display message asking for product's quantity
        display_message("Enter the list of Product's quantity seperated by commas: ");
        quantity_list = [quantity.strip() for quantity in sys.stdin.readline().split(',')];

        # Validate number of products and number of quantities
        if (len(product_name_list) != len(quantity_list)):
            display_message("\nError: Number of products and quantities should be the same.\n\n");
        else:
            break;
    product_list = [];
    for index, quantity in enumerate(quantity_list):
        if (quantity.isnumeric() and int(quantity) > 0):
            # Check for prescription and if not available skip adding the product
            if (product_name_list[index] in prescription_needed_products_list and not is_prescription_available(product_name_list[index])):
                continue;
            product = {
                'name': product_name_list[index],
                'quantity': int(quantity)
            }
            product_list.append(product);
        else:
            # Display error message
            display_message("\nError: Quantity should contain only positive Integer values.\n\n");
            break;
    # Return product list
    return product_list;

def calculate_total_price(product_list):
    # Calculate the total price and return it
    total_price = 0;
    for product in product_list:
        total_price += products[product['name']]['unit_price'] * product['quantity'];
    return total_price;

def calculate_reward_points(total_price):
    # Round points to the nearest integer and return it
    return int(total_price + 0.5);

def display_receipt(customer_name, product_list, total_price, reward_points, discount_details):
    # Creating a multiline string with formatted expressions
    receipt = f"""
{"-" * 50}
{"Receipt":^50} 
{"-" * 50}
Name:                         {customer_name}""";
    for product in product_list:
        receipt += f"""
Product:                      {product['name']}
Unit Price:                   {products[product['name']]['unit_price']:.2f} (AUD)
Quantity:                     {product['quantity']}""";

    receipt += f"""
{"-" * 50}
Total cost:                   {total_price:.2f} (AUD)
Earned reward:                {reward_points}
{"-" * 50}""";
    
    if (discount_details["is_eligible"]):
        receipt += f"""
Discount amount:              {discount_details["discount_amount"]:.2f} (AUD)
Total after discount:         {discount_details["total_after_discount"]:.2f}  (AUD)
{"-" * 50}""";

    # Display the receipt
    display_message(receipt);

def update_customer(customer_name, reward_points):
    if customer_name in customers:
        # For an existing customer reward points added to the existing ones
        customers[customer_name]["total_rewards"] += int(reward_points);
    else:
        # For a new customer rewars points set as his reward points
        customers[customer_name] = {};
        customers[customer_name]["total_rewards"] = int(reward_points);

def calculate_reward_discounts(total_price, total_rewards):
    discount_details = {
        "is_eligible": False,
        "discount_amount": 0,
        "used_rewards": 0,
        "total_after_discount": total_price
    }
    # Check whether the discount is available or not
    if (total_price >= 10 and total_rewards >= 100):
        discount_details["is_eligible"] = True;
        # Calculate discount amount
        discount_details["discount_amount"] = min(round(total_price - 5, -1), round(total_rewards - 50, -2) / 10);
        discount_details["used_rewards"] = discount_details["discount_amount"] * 10
        discount_details["total_after_discount"] -= discount_details["discount_amount"];
    return discount_details;


# Handles the make a purchase logic
def make_purchase():
    # Read inputs
    customer_name = read_customer_name_and_validate();
    product_name_list = read_product_name_and_validate();
    # Get prescription needed products
    prescription_needed_products_list = prescription_needed_products(product_name_list);
    product_list = read_product_quantity_and_validate(product_name_list, prescription_needed_products_list);
    # Check any products are left to purchase after the validations
    if(len(product_list) > 0):
        # Do calculation
        total_price = calculate_total_price(product_list);
        earned_reward_points = calculate_reward_points(total_price);
        discount_details = calculate_reward_discounts(total_price, customers[customer_name]["total_rewards"]);
        # Save order
        save_order(customer_name, product_list, total_price, earned_reward_points);
        # Print receipt
        display_receipt(customer_name, product_list, total_price, earned_reward_points, discount_details);
        # Update customer details with earned rewards
        update_customer(customer_name, earned_reward_points);
        # Update customer details with used rewards
        update_customer(customer_name, -discount_details["used_rewards"]);
    else:
        display_message("No products are left to purchase. Please purchase again.\n")

# This function used to save order purchased by a customer
def save_order(customer_name, product_list, total_price, earned_reward_points):
    order = {
        "products": product_list,
        "total_price": total_price,
        "earned_reward_points": earned_reward_points
    }
    # If customer already have previous orders add current order to the existing order list
    if ("orders" in customers[customer_name]):
        customers[customer_name]["orders"].append(order);
    # If customer do not have any previous orders create new orders list and add current order to it
    else:
        customers[customer_name]["orders"] = [order];


def add_or_update_product():
    temp_products = {};
    # Keep repeating until a valid input is entered
    while True:
        temp_products = {};
        # Add or update product information
        display_message("\n\nEnter the product information (name price dr_prescription(y/n)) seperated by commas:");
        # Read product information and split by whitespace (default seperator)
        product_info_list = [product_info.strip() for product_info in sys.stdin.readline().split(',')];
        for product_info_input in product_info_list:
            product_info = product_info_input.split();
            if (len(product_info) != 3):
                display_message("Invalid input format. Please enter product information in the correct format.");
                break;
            product_name = product_info[0];
            if (not product_info[1].isnumeric() and not float(product_info[1]) > 0):
                # Display error message
                display_message("\nError: Quantity should contain only positive Integer values.\n\n");
                break;
            price = float(product_info[1]);
            if not(product_info[2].lower() == 'y' or product_info[2].lower() == 'n'):
                display_message("\nError: Invalid character for doctor's prescription. Enter (y - Yes, n - No)");
                break;
            prescription = product_info[2];
            temp_products[product_name] = {
                "unit_price": price, 
                "prescription": prescription
            }
        
        if (len(temp_products) == len(product_info_list)):
            break;
    # Update or add product info to the exiting products
    for product_name, product_detail in temp_products.items():
        products[product_name] = product_detail;

def display_customers():
    # Display existing customers and their reward points
    display_customer_details = f"""\n\nExisting customers and their reward points:
    {"-" * 50}\n""";
    # Display customer info by iterating customers
    for customer_name, customer_details in customers.items():
        display_customer_details += f"Name: {customer_name} \n"
        display_customer_details += f'Reward points: {customer_details["total_rewards"]}\n';
        display_customer_details += f'{"-" * 50}\n';
    display_message(display_customer_details);

def display_products():
    # Display existing products and their informations
    product_details = f"""\n\nExisting products and their informations:
    {"-" * 50}\n""";
    # Display customer info by iterating customers
    for product, product_info in products.items():
        product_details += f"Name: {product}\n";
        product_details += f"Price: {product_info['unit_price']:.2f}\n";
        # Ternary operator used to display 'Yes' & 'No' instead of 'y' & 'n'
        product_details += f"Prescription Required: {'Yes ' if product_info['prescription'] == 'y' else 'No'}\n";
        product_details += f'{"-" * 50}\n';
    display_message(product_details);

def display_customer_order_history():
    customer_name = "";
    while True:
        # Display message asking for customer's name
        display_message("\n\nEnter the customer's name: ");
        # Read customer name
        customer_name = sys.stdin.readline().strip();
        if (customer_name in customers):
            break;
        else:
            display_message("Invalid customer name. Enter a valid customer name.")
    if ("orders" in customers[customer_name]):
        order_details_header = f"This is the order history of {customer_name}\n";
        order_details_header += f'{"":13}{"Products":<53}{"Total Cost":<13}{"Earned Rewards":<14}\n';
        order_details_header += f'{"-" * 93}\n';
        order_details = "";
        for order_index, order in enumerate(customers[customer_name]["orders"]):
            order_number = f"order {order_index}";
            product_list = "";
            for product_index, product in enumerate(order["products"]):
                if not product_index == 0:
                    product_list += ", ";
                product_list += f'{product["quantity"]} X {product["name"]}';
            order_details += f'{order_number:<10}{"":3}{product_list:<50}{"":3}{order["total_price"]:<10.2f}{"":3}{order["earned_reward_points"]:<14}\n';
        display_message(order_details_header + order_details);
    else:
        display_message(f"No orders from the customer named {customer_name}");

def main_menu():
    # Display main menu. After completing each selected option user will automatically directed to main menu until the user exit from the system
    while True:
        display_message("""\n
Menu:
1. Make a purchase
2. Add/update information of a product
3. Display existing customers
4. Display existing products
5. Display a customer order history
6. Exit
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
            display_customer_order_history();
        elif choice == '6':
            sys.exit();
        else:
            display_message("\nError: Invalid choice. Please enter a number between 1 and 5.\n\n");

# Starting point of the program
main_menu();