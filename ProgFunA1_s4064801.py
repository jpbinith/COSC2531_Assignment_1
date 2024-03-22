import sys

# Initialize existing customers and their reward points
customers = {"Kate": 20, "Tom": 32}

# Initialize products and their unit prices
products = {
    "vitaminC": 12.0,
    "vitaminE": 14.5,
    "coldTablet": 6.4,
    "vaccine": 32.6,
    "fragrance": 25.0,
}

def display_message(message):
    # Displey messages
    sys.stdout.write(message);
    # Flush the buffer
    sys.stdout.flush();

def read_customer_name():
    # Display message asking for customer's name
    display_message("Enter the customer's name: ");
    # Return the customer name
    return sys.stdin.readline().strip();

def read_product_name():
    # Display message asking for product's name
    display_message("Enter the Product's name: ");
    # Return the product name
    return sys.stdin.readline().strip();

def read_product_quantity():
    # Display message asking for product's quantity
    display_message("Enter the Product's quantity: ");
    # Return the product quantity
    return int(sys.stdin.readline().strip());

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
Unit Price:                 {products[product_name]:.2f} (AUD)
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


def main():
    # Main program
    customer_name = read_customer_name();
    product_name = read_product_name();
    product_quantity = read_product_quantity();

    total_price = calculate_total_price(products[product_name], product_quantity);
    earned_reward_points = calculate_reward_points(total_price);

    display_receipt(customer_name, product_name, product_quantity, total_price, earned_reward_points);
    display_message(f"Customer list: {customers}");

# Starting point of the program
main();