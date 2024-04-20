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
            # Update customer details.
            update_customer(customer_name, 0);
            # Return the customer name
            return customer_name;
        else:
            # Display error message
            display_message("\nError: Customer name should contain only alphebetic characters.\n\n");

def read_product_name_and_validate():
    while True:
        # Display message asking for product's name
        display_message("Enter the list of Product's name seperated by commas: ");
        # Read product name
        product_name_list = [product_name.strip() for product_name in sys.stdin.readline().split(',')];
        for product_name in product_name_list:
            if product_name not in products:
                # Display error message
                display_message("\nError: Enterd product is invalid.\n\n");
                break;
        # Return the product name
        return product_name_list;

def check_is_prescription_needed(product_name_list):
    for product_name in product_name_list:
        # Check prescription is needed or not each product
        if(products[product_name]["prescription"] == 'y'):
            # Return true if any product needs a prescription
            return True;
    # Return false if any product do not needs a prescription
    return False;

def is_prescription_available():
    # Display message asking prescription
    display_message("Do you have a doctor's prescription for this product? (y/n): ");
    while True:
        # Read answer
        answer = sys.stdin.readline().strip();
        if answer.lower() == 'y':
            return True;
        elif answer.lower() == 'n':
            display_message("This product requires a doctor's prescription. Purchase cannot be completed.");
            return False;
        else:
            display_message("\nError: Invalid character Enter (y - Yes, n - No)");

def read_product_quantity_and_validate(product_name_list):
    quantity_list = [];
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
            # Set product details and push to product list
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
    return round(total_price);

def display_receipt(customer_name, product_list, total_price, reward_points, discount_details):
    # Creating a multiline string with formatted expressions
    receipt = f"""
-------------------------------------------------
                    Receipt 
-------------------------------------------------
Name:                         {customer_name}""";
    for product in product_list:
        receipt += f"""
Product:                      {product['name']}
Unit Price:                   {products[product['name']]['unit_price']} (AUD)
Quantity:                     {product['quantity']}""";

    receipt += f"""
-------------------------------------------------
Total cost:                   {total_price} (AUD)
Earned reward:                {reward_points}
-------------------------------------------------""";
    
    if (discount_details["is_eligible"]):
        receipt += f"""
Discount amount:              {discount_details["discount_amount"]} (AUD)
Total after discount:         {discount_details["total_after_discount"]}  (AUD)
-------------------------------------------------""";

    # Display the receipt
    display_message(receipt);

def update_customer(customer_name, reward_points):
    if customer_name in customers:
        # For an existing customer reward points added to the existing ones
        customers[customer_name] += reward_points;
    else:
        # For a new customer rewars points set as his reward points
        customers[customer_name] = reward_points;

def calculate_reward_discounts(total_price, total_rewards):
    discount_details = {
        "is_eligible": False,
        "discount_amount": 0,
        "used_rewards": 0,
        "total_after_discount": total_price
    }
    if (total_price >= 10 and total_rewards >= 100):
        discount_details["is_eligible"] = True;
        discount_details["discount_amount"] = min(round(total_price - 5, -1), round(total_rewards - 50, -2) / 10);
        discount_details["used_rewards"] = discount_details["discount_amount"] * 10
        discount_details["total_after_discount"] -= discount_details["discount_amount"];
    return discount_details;


# Handles the make a purchase logic
def make_purchase():
    # Read inputs
    customer_name = read_customer_name_and_validate();
    product_name_list = read_product_name_and_validate();
    if (check_is_prescription_needed(product_name_list) and (not is_prescription_available())):
        return;
    product_list = read_product_quantity_and_validate(product_name_list);
    # Do calculation
    total_price = calculate_total_price(product_list);
    earned_reward_points = calculate_reward_points(total_price);
    discount_details = calculate_reward_discounts(total_price, customers[customer_name]);
    # Print receipt
    display_receipt(customer_name, product_list, total_price, earned_reward_points, discount_details);
    # Update customer details with earned rewards
    update_customer(customer_name, earned_reward_points);
    # Update customer details with used rewards
    update_customer(customer_name, -discount_details["used_rewards"]);

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
        display_message("""\n\n
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