import sqlite3
from datetime import datetime

db_file = "./assessment_database"
db = sqlite3.connect(db_file)
cursor = db.cursor()

get_date = datetime.now()
curr_date = get_date.strftime("%d/%m/%Y, %H:%M:%S")
curr_day = get_date.strftime("%Y-%m-%d")
address_choice = 0
card_choice = 0


# Function to call the main menu.
def main_menu():
    options_list = ['1. Display your order history', '2. Add an item to your basket', '3. View your basket',
                    '4. Checkout', '5. Exit']
    print("ORINOCO - SHOPPER MAIN MENU")
    print("""""")
    for name in options_list:
        print(name)


# Function for options list
def _display_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(option_num, desc))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


# Altered function for additional options field
def _seller_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        prices = option[2]
        print("{0}.\t{1}\t£{2:.2f}".format(option_num, desc, prices))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


# Altered function specific to delivery options
def _delivery_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        ad1 = option[1]
        ad2 = option[2]
        ad3 = option[3]
        county = option[4]
        pcode = option[5]
        print("{0}.\t{1}\t{2}\t{3}\t{4}\t{5}".format(option_num, ad1, ad2, ad3, county, pcode))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


# Altered function specific to card options
def _card_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        type = option[1]
        number = option[2]
        print(option_num, type, "ending in", number)
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


# Function for storing quantity and checking restraints.
def quantity_select():
    try:
        quantity_prompt = int(input("Enter the quantity of the selected product you wish to buy: "))
        if quantity_prompt < 1:
            print("Error! Value entered is too low.")
        else:
            return quantity_prompt
    except ValueError:
        print("Invalid Input")


# Initial login check to assert user validity.
try:
    shopper_check = int(input("Please enter your username: "))
    sql_id_query = ("SELECT shopper_first_name \
                    FROM shoppers \
                    WHERE (shopper_id)=(?)")
    cursor.execute(sql_id_query, (shopper_check,))
    shoppers_row = cursor.fetchone()
    if shoppers_row:
        name_format = str(shoppers_row[0])
        print("""""")
        print("Welcome" + " " + name_format + "!")
        print("""""")
    else:
        print("Error! That is not the correct login.")
        exit()

except ValueError:
    print("Error! That is not the correct login.")
    exit()

while True:
    # Call in the main menu.
    main_menu()

    menu_browse = input("Select an option from the above list: ")

    # Open up to part one of the menu, query user's order history with stored ID from A.
    if menu_browse == '1':

        sql_order_query = ("SELECT so.order_id, STRFTIME('%d-%m-%Y', so.order_date) , p.product_description, so.seller_name, op.price, op.quantity, op.ordered_product_status \
                          FROM shoppers s \
                            INNER JOIN shopper_orders so ON s.shopper_id = so.shopper_id \
                           INNER JOIN ordered_products op ON so.order_id = op.order_id \
                           INNER JOIN product_sellers ps ON op.product_id = ps.product_id \
                                                         AND op.seller_id = ps.seller_id \
                           INNER JOIN sellers so ON op.seller_id = so.seller_id \
                           INNER JOIN products p ON ps.product_id = p.product_id \
                          WHERE (s.shopper_id)=(?) \
                           ORDER BY order_date DESC")
        cursor.execute(sql_order_query, (shopper_check,))
        all_shopper_orders = cursor.fetchall()

        # If shopper has previous orders, print them.
        if all_shopper_orders:
            print("""""")
            print('{0}\t{1}\t\t{2:80}\t\t{3:20}\t\t{4:10}\t\t{5:10}\t\t{6:20}'.format("Order ID", "Order Date",
                                                                                      "Product Description",
                                                                                      "Seller Name",
                                                                                      "Price", "Qty", "Status"))
            print("""""")
            for shopper_orders_row in all_shopper_orders:
                order_id = shopper_orders_row[0]
                order_date = shopper_orders_row[1]
                product_description = shopper_orders_row[2]
                seller_name = shopper_orders_row[3]
                price = shopper_orders_row[4]
                quantity = shopper_orders_row[5]
                ordered_product_status = shopper_orders_row[6]
                print('{0}\t\t{1}\t\t{2:80}\t\t{3:20}\t\t£{4:10.2f}\t\t{5:10}\t\t{6:20}'.format(order_id, order_date,
                                                                                                product_description,
                                                                                                seller_name, price,
                                                                                                quantity,
                                                                                                ordered_product_status))
        # Else, display no orders.
        else:
            print("No orders placed by this customer.")



    # Open up to part two of the menu, show product categories menu.

    elif menu_browse == '2':
        sql_discovery_query = ("SELECT category_id, category_description \
                           FROM categories \
                           ORDER BY category_description DESC")
        cursor.execute(sql_discovery_query)
        all_categories = cursor.fetchall()

        # Get shopper choice.

        category_select = _display_options(all_categories, 'Categories', 'category')

        # Show product selection for the inputted category.

        sql_products_list = ("SELECT p.product_id, p.product_description \
                        FROM products p \
                        INNER JOIN categories c ON p.category_id = c.category_id \
                        WHERE (c.category_id)=(?)")
        cursor.execute(sql_products_list, (category_select,))
        product_selection = cursor.fetchall()

        if product_selection:
            product_select = _display_options(product_selection, 'Products', 'product')

            # Select a seller who sells this item, store that result.

            sql_sellers_list = ("SELECT s.seller_id, s.seller_name, ps.price\
                            FROM sellers s \
                            INNER JOIN product_sellers ps ON s.seller_id = ps.seller_id \
                            WHERE (ps.product_id)=(?)")
            cursor.execute(sql_sellers_list, (product_select,))
            all_sellers = cursor.fetchall()

            sellers_select_id = _seller_options(all_sellers, 'Sellers', 'seller')

            # Prompt for quantity, store result.
            quantity = quantity_select()

            # Obtaining price for selected product.

            sql_order_product = ("SELECT ps.price \
                                    FROM product_sellers ps \
                                    INNER JOIN products p ON ps.product_id = p.product_id\
                                    WHERE (p.product_id)=(?) \
                                    AND (ps.seller_id)=(?)")
            cursor.execute(sql_order_product, (product_select, sellers_select_id))
            price_result = cursor.fetchone()
            price = float(price_result[0])

            # Searching for an open basket.

            find_basket = ("SELECT basket_id \
                            FROM shopper_baskets \
                            WHERE (shopper_id)=(?)")
            cursor.execute(find_basket, (shopper_check,))
            current_basket = cursor.fetchone()

            # If a basket exists, add to it.

            if current_basket:
                try:
                    current_basket_id = int(current_basket[0])
                    basket_content_insert = ("INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price) \
                                        VALUES (?, ?, ?, ?, ?)")
                    cursor.execute(basket_content_insert, (current_basket_id, product_select, sellers_select_id,
                                                           quantity, price))
                    db.commit()
                    print('Item added to your basket')

                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")

            # If no basket exists, create a new one.
            # Exceptions given in case of errors.

            else:

                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("SELECT seq + 1 \
                                                     FROM sqlite_sequence \
                                                     WHERE name = 'shopper_baskets'")
                new_basket = cursor.fetchone()
                next_basket_id = new_basket[0]

                try:
                    new_basket_insert = ("INSERT INTO shopper_baskets(shopper_id, basket_created_date_time) \
                                    VALUES (?, ?)")
                    cursor.execute(new_basket_insert, (shopper_check, curr_date))
                    db.commit()
                    print("Basket Created.")

                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")

                # Jump over to basket_contents, use the new basket_id, and fill the basket with user input.
                # Exceptions given in case of error.

                try:
                    basket_content_insert = ("INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price) \
                                    VALUES (?, ?, ?, ?, ?)")
                    cursor.execute(basket_content_insert, (next_basket_id, product_select, sellers_select_id,
                                                           quantity, price))
                    db.commit()
                    print('''''''')
                    print('Item added to your basket')


                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")


    elif menu_browse == '3':

        # Find a basket ID.
        find_basket_id = ("SELECT basket_id \
                                FROM shopper_baskets \
                                WHERE (shopper_id)=(?)")
        cursor.execute(find_basket_id, (shopper_check,))
        current_basket = cursor.fetchone()

        # If current basket exists, query it.

        if current_basket:
            current_basket_id = int(current_basket[0])
            sql_shopper_basket = ("SELECT p.product_description, s.seller_name, b.quantity, b.price, SUM(b.price * b.quantity) \
                              FROM basket_contents b \
                               INNER JOIN product_sellers ps ON b.product_id = ps.product_id \
                                                             AND b.seller_id = ps.seller_id \
                               INNER JOIN products p ON ps.product_id = p.product_id \
                               INNER JOIN sellers s ON ps.seller_id = s.seller_id \
                              WHERE (b.basket_id)=(?) \
                              GROUP BY p.product_description, s.seller_name, b.quantity, b.price")
            cursor.execute(sql_shopper_basket, (current_basket_id,))
            shopper_basket = cursor.fetchall()

            # Show shopper basket.
            if shopper_basket:
                print('Basket Contents')
                print('---------------')
                print('{0:40}\t{1:40}\t{2}\t\t\t{3:5}\t\t{4:5}'.format("Product Description", "Seller Name",
                                                                       "Qty", "Price", "Total"))
                for shopper_basket_row in shopper_basket:
                    product_description = shopper_basket_row[0]
                    seller_name = shopper_basket_row[1]
                    qty = shopper_basket_row[2]
                    price = shopper_basket_row[3]
                    total = shopper_basket_row[4]
                    print('{0:40}\t{1:40}\t{2}\t\t\t£{3:5.2f}\t\t£{4:5.2f}'.format(product_description, seller_name,
                                                                                   qty,
                                                                                   price, total))
                # Query the database for an order total, then display it.
                basket_query_total = ("SELECT SUM(b.price * b.quantity)\
                                        FROM basket_contents b \
                                        WHERE (b.basket_id)=(?) \
                                        GROUP BY b.basket_id")
                cursor.execute(basket_query_total, (current_basket_id,))
                fetch_total = cursor.fetchone()
                basket_total = float(fetch_total[0])
                print('''''''')
                print('\t\t\t\t\t\t\t\t\t\t\t{0}\t\t\t\t\t\t\t\t\t\t\t\t\t\t£{1:5.2f}'.format("Basket Total",
                                                                                              basket_total))

        # Else, let the shopper know no basket exists and prompt a return to the main menu.
        else:
            print("Error! No basket currently open.")

    elif menu_browse == '4':

        # Recalling the code from menu_browse 3 to display a basket.

        find_basket_id = ("SELECT basket_id \
                                    FROM shopper_baskets \
                                    WHERE (shopper_id)=(?)")
        cursor.execute(find_basket_id, (shopper_check,))
        current_basket = cursor.fetchone()

        if current_basket:
            current_basket_id = int(current_basket[0])
            sql_shopper_basket = ("SELECT p.product_description, s.seller_name, b.quantity, b.price, SUM(b.price * b.quantity) \
                                      FROM basket_contents b \
                                       INNER JOIN product_sellers ps ON b.product_id = ps.product_id \
                                                                     AND b.seller_id = ps.seller_id \
                                       INNER JOIN products p ON ps.product_id = p.product_id \
                                       INNER JOIN sellers s ON ps.seller_id = s.seller_id \
                                      WHERE (b.basket_id)=(?) \
                                      GROUP BY p.product_description, s.seller_name, b.quantity, b.price")
            cursor.execute(sql_shopper_basket, (current_basket_id,))
            shopper_basket = cursor.fetchall()

            # Show shopper basket.#
            if shopper_basket:
                print('Basket Contents')
                print('---------------')
                print('{0:40}\t{1:40}\t{2}\t\t\t{3:5}\t\t{4:5}'.format("Product Description", "Seller Name",
                                                                       "Qty", "Price", "Total"))
                print('''''''')
                for shopper_basket_row in shopper_basket:
                    product_description = shopper_basket_row[0]
                    seller_name = shopper_basket_row[1]
                    qty = shopper_basket_row[2]
                    price = shopper_basket_row[3]
                    total = shopper_basket_row[4]
                    print('{0:40}\t{1:40}\t{2}\t\t\t£{3:5.2f}\t\t£{4:5.2f}'.format(product_description,
                                                                                   seller_name, qty, price, total))

            # Querying for a basket total on a separate line, printing the basket total.

            basket_query_total = ("SELECT SUM(b.price * b.quantity)\
                                                FROM basket_contents b \
                                                WHERE (b.basket_id)=(?) \
                                                GROUP BY b.basket_id")
            cursor.execute(basket_query_total, (current_basket_id,))
            fetch_total = cursor.fetchone()
            basket_total = float(fetch_total[0])
            print('''''''')
            print('\t\t\t\t\t\t\t\t\t\t\t{0}\t\t\t\t\t\t\t\t\t\t\t\t\t\t£{1:5.2f}'.format("Basket Total", basket_total))

            # Search for stored delivery addresses, respond according to amount.
            sql_address_search = ("SELECT DISTINCT de.delivery_address_id\
                                        FROM shopper_delivery_addresses de \
                                        INNER JOIN shopper_orders so ON de.delivery_address_id = so.delivery_address_id \
                                        INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                                WHERE (s.shopper_id)=(?)")
            cursor.execute(sql_address_search, (shopper_check,))
            collect_addresses = cursor.fetchall()

            address_length = len(collect_addresses)

            if address_length > 1:
                sql_get_addresses = (
                    "SELECT DISTINCT de.delivery_address_id, de.delivery_address_line_1, IFNULL(de.delivery_address_line_2, ''), "
                    "IFNULL(de.delivery_address_line_3, ''), de.delivery_county, de.delivery_post_code \
                                   FROM shopper_delivery_addresses de \
                                   INNER JOIN shopper_orders so ON de.delivery_address_id = so.delivery_address_id \
                                   INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                   WHERE (s.shopper_id)=(?)")
                cursor.execute(sql_get_addresses, (shopper_check,))
                address_information = cursor.fetchall()

                address_choice = _delivery_options(address_information, "Delivery Addresses", 'address')

            elif address_length == 1:
                sql_get_addresses = ("SELECT DISTINCT de.delivery_address_id, de.delivery_address_line_1, IFNULL(de.delivery_address_line_2, ''), IFNULL(de.delivery_address_line_3, ''), de.delivery_county, de.delivery_post_code \
                                                                FROM shopper_delivery_addresses de \
                                                                INNER JOIN shopper_orders so ON de.delivery_address_id = so.delivery_address_id \
                                                                INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                                                WHERE (s.shopper_id)=(?)")
                cursor.execute(sql_get_addresses, (shopper_check,))
                address_information = cursor.fetchall()

                print('\t{0:40}'.format("Delivery Address"))
                option_num = 1
                option_list = []
                for addresses_row in address_information:
                    code = addresses_row[0]
                    address_line_1 = addresses_row[1]
                    address_line_2 = addresses_row[2]
                    address_line_3 = addresses_row[3]
                    county = addresses_row[4]
                    postcode = addresses_row[5]
                    print('{0}.\t\t{1:40}\t{2:20}\t{3:5}\t\t\t\t\t{4:5}{5:5}'.format(option_num, address_line_1,
                                                                                     address_line_2, address_line_3,
                                                                                     county, postcode))
                    option_num = option_num + 1
                    option_list.append(code)

                print('''''''')
                print("We will use the above address")
                address_choice = option_list[0]

            # Prompt the user to enter a new address.
            else:
                print("As you have not placed any orders, you will need to add a new delivery address.")
                print('''''''')

                fetch_line_1 = input("Enter the delivery address line 1: ")
                fetch_line_2 = input("Enter the delivery address line 2: ")
                fetch_line_3 = input("Enter the delivery address line 3: ")
                fetch_county = input("Enter the delivery County: ")
                fetch_postcode = input("Enter the delivery postcode: ")

                # Try inserting the new address into the database. Rollback in cases of failure.
                try:
                    address_insert = ("INSERT INTO shopper_delivery_addresses (delivery_address_line_1, "
                                      "delivery_address_line_2, delivery_address_line_3, delivery_county, "
                                      "delivery_post_code) \
                                    VALUES (?, ?, ?, ?, ?)")
                    cursor.execute(address_insert, (fetch_line_1, fetch_line_2, fetch_line_3,
                                                    fetch_county, fetch_postcode))
                    db.commit()
                    print('New address created!')

                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")

                cursor.execute("SELECT seq \
                                 FROM sqlite_sequence \
                                 WHERE name = 'shopper_delivery_addresses'")
                address_store = cursor.fetchone()
                address_choice = int(address_store[0])
                print(address_choice)

            # Query for existing cards.
            sql_card_query = ("SELECT DISTINCT p.payment_card_id\
                                            FROM shopper_payment_cards p \
                                            INNER JOIN shopper_orders so ON p.payment_card_id = so.payment_card_id \
                                            INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                                    WHERE (s.shopper_id)=(?)")
            cursor.execute(sql_card_query, (shopper_check,))
            collect_card = cursor.fetchall()

            # Check amount of cards stored
            card_amount = len(collect_card)

            # If multiple cards are found, run the below code.
            if card_amount > 1:
                sql_get_cards = ("SELECT DISTINCT p.payment_card_id, p.card_type, p.card_number \
                                                    FROM shopper_payment_cards p \
                                                        INNER JOIN shopper_orders so ON p.payment_card_id = so.payment_card_id \
                                                        INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                                    WHERE (s.shopper_id)=(?)")
                cursor.execute(sql_get_cards, (shopper_check,))
                card_information = cursor.fetchall()

                card_choice = _card_options(card_information, "Payment Cards", 'card')

            # Else if, present the card information for the singular stored card and store it in Python for further use.
            elif card_amount == 1:
                sql_get_card = ("SELECT DISTINCT p.payment_card_id, p.card_type, p.card_number \
                                                  FROM shopper_payment_cards p  \
                                                    INNER JOIN shopper_orders so ON p.payment_card_id = so.payment_card_id \
                                                    INNER JOIN shoppers s ON so.shopper_id = s.shopper_id \
                                                  WHERE (s.shopper_id)=(?)")
                cursor.execute(sql_get_card, (shopper_check,))
                fetch_card = cursor.fetchall()

                print('{0:40}'.format("Payment Method"))
                print('''''''')
                option_num = 1
                option_list = []
                for cards_row in fetch_card:
                    code = cards_row[0]
                    card_type = cards_row[1]
                    card_number = cards_row[2]
                    print(option_num, card_type, "ending in", card_number)
                    option_num = option_num + 1
                    option_list.append(code)

                print('''''''')
                print("We will use the above Payment Method")
                card_choice = option_list[0]

            # Else, create a new card. Transaction should roll back if constraints are not met.
            else:
                print("As you have not placed any orders, you will need to enter your payment details.")
                print('''''''')

                fetch_type = input("Enter the card type (Visa, Mastercard, or AMEX): ")
                fetch_number = input("Enter the 16-digit card number: ")

                try:
                    card_insert = ("INSERT INTO shopper_payment_cards (card_type, card_number) \
                                        VALUES (?, ?)")
                    cursor.execute(card_insert, (fetch_type, fetch_number))
                    db.commit()
                    print('New payment method added!')

                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")

                cursor.execute("SELECT seq \
                                             FROM sqlite_sequence \
                                             WHERE name = 'shopper_payment_cards'")
                card_store = cursor.fetchone()
                card_choice = int(card_store[0])

            # Insert new row into shopper_order table.
            try:
                order_insert = ("INSERT INTO shopper_orders (shopper_id, delivery_address_id, payment_card_id, order_date, order_status) \
                                    VALUES (?, ?, ?, ?, ?)")
                cursor.execute(order_insert, (shopper_check, address_choice, card_choice, curr_day, "Placed"))
                db.commit()

            except db.Error:
                print("Transaction failed, rolling back")
                cursor.execute("ROLLBACK")

            # Query the database for contents of the current basket using the current basket ID.
            current_basket_id = int(current_basket[0])
            sql_query_basket = ("SELECT p.product_id, s.seller_id, b.quantity, b.price \
                                              FROM basket_contents b \
                                               INNER JOIN product_sellers ps ON b.product_id = ps.product_id \
                                                                             AND b.seller_id = ps.seller_id \
                                               INNER JOIN products p ON ps.product_id = p.product_id \
                                               INNER JOIN sellers s ON ps.seller_id = s.seller_id \
                                              WHERE (b.basket_id)=(?)")
            cursor.execute(sql_query_basket, (current_basket_id,))
            shopper_basket = cursor.fetchall()

            # Grab the previously created order ID for this order.
            cursor.execute("SELECT seq \
                                         FROM sqlite_sequence \
                                         WHERE name = 'shopper_orders'")
            order_id_store = cursor.fetchone()
            order_select = int(order_id_store[0])

            # Cycle through all objects in the fetch, for each one, insert that data as a row in the database.
            for basket_row in shopper_basket:
                product_id = basket_row[0]
                seller_name = basket_row[1]
                quantity = basket_row[2]
                price = basket_row[3]

                try:
                    products_insert = ("INSERT INTO ordered_products (order_id, product_id, seller_id, quantity, price, ordered_product_status) \
                                    VALUES (?, ?, ?, ?, ?, ?) ")
                    cursor.execute(products_insert, (order_select, product_id, seller_name, quantity, price, "Placed"))
                    db.commit()

                except db.Error:
                    print("Transaction failed, rolling back")
                    cursor.execute("ROLLBACK")

            # Delete the rows for this shopper from shopper_basket and basket_contents.
            try:
                sql_contents_delete = ("DELETE FROM basket_contents \
                                                      WHERE (basket_id)=(?)")
                cursor.execute(sql_contents_delete, (current_basket_id,))
                db.commit()

                sql_basket_delete = ("DELETE FROM shopper_baskets \
                                  WHERE (basket_id)=(?)")
                cursor.execute(sql_basket_delete, (current_basket_id,))
                db.commit()
                print("Checkout complete, your order has been placed")

            except db.Error:
                print("Transaction failed, rolling back")
                cursor.execute("ROLLBACK")


        else:
            print("Error! No basket currently open.")

    # Return back to the main menu

    # Exit the program, close the database.

    elif menu_browse == '5':
        print("Goodbye! Have a great day.")
        db.close()
        exit()

    else:
        print("Invalid Menu Option! Please try again.")

    input("Press enter to continue back to main menu... ")