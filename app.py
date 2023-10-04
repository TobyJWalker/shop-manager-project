from lib.database_connection import DatabaseConnection
from lib.order_repository import *
from lib.item_repository import *
from os import system

clear = lambda: system('clear')

class Application:
    def __init__(self):
        self._connection = DatabaseConnection()
        self._connection.connect()
        self._connection.seed("seeds/shop_manager.sql")
        self._order_repo = OrderRepository(self._connection)
        self._item_repo = ItemRepository(self._connection)
    
    # ask user what object they want to manage
    def _prompt_for_object_to_manage(self, choice=None):
        while choice != '3':
            print("\nWhat would you like to manage?\n")
            print("1. Orders")
            print("2. Items")
            print("3. Exit app")
            
            choice = input("\nEnter your choice: ")
            clear()

            if choice == '1':
                return 'orders'
            elif choice == '2':
                return 'items'
            elif choice != '3':
                print("Invalid choice. Please try again.")
            else:
                exit()

    # ask user what action they want to perform on an item
    def _prompt_for_item_action(self, choice=None):

        # loop until a valid choice is entered
        while choice != "5":
            print("\nWhat would you like to do?\n")
            print("1. Create new item")
            print("2. Update existing item")
            print("3. Delete existing item")
            print("4. List all items")
            print("5. Return to main menu")

            choice = input("\nEnter your choice: ")
            clear()

            if choice == "1":
                return 'create'
            elif choice == "2":
                return 'update'
            elif choice == "3":
                return 'delete'
            elif choice == "4":
                return 'list'
            elif choice != "5":
                print("Invalid choice. Please try again.")
            else:
                return 'back'
    
    # ask user for the properties of an item
    def _prompt_for_item_contents(self, name=None, quantity=None, price=None):

        # loop until a valid name is entered
        while name == None:
            name = input("\nEnter the item name: ")
            clear()
            if name == "" or name.isspace():
                print("Invalid name. Please try again.")
                name = None

        # loop until a valid quantity is entered
        while quantity == None:
            try:
                quantity = int(input("\nEnter the item quantity: "))
                clear()
                if quantity < 0:
                    print("Invalid quantity. Please try again.")
                    quantity = None
            except:
                print("Quantity must be a number. Please try again.")
                quantity = None

        # loop until a valid price is entered
        while price == None:
            try:
                price = float(input("\nEnter the item price: "))
                clear()
                if price < 0:
                    print("Invalid price. Please try again.")
                    price = None
            except:
                print("Price must be a number. Please try again.")
                price = None

        return name, quantity, price

    # ask user for the name of an item to delete
    def _prompt_for_item_delete(self, name=None):
        while name == None:
            name = input("\nEnter the name of the item to delete: ")
            clear()
            if name == "" or name.isspace():
                print("Invalid name. Please try again.")
                name = None
        return name
    
    # ask user what action they want to perform on an order
    def _prompt_for_order_action(self, choice=None):

        # loop until a valid choice is entered
        while choice != "5":
            print("\nWhat would you like to do?\n")
            print("1. Create new order")
            print("2. Cancel order")
            print("3. List all orders")
            print("4. View order details")
            print("5. Return to main menu")

            choice = input("\nEnter your choice: ")
            clear()

            if choice == "1":
                return 'create'
            elif choice == "2":
                return 'delete'
            elif choice == "3":
                return 'list'
            elif choice == "4":
                return 'find'
            elif choice != "5":
                print("Invalid choice. Please try again.")
            else:
                return 'back'
    
    # ask user for the properties of an order
    def _prompt_for_order_details(self, name=None, item_ids=[]):
            
            # loop until a valid name is entered
            while name == None:
                name = input("\nEnter the customer name: ")
                clear()
                if name == "" or name.isspace():
                    print("Invalid name. Please try again.")
                    name = None
    
            # loop until a valid list of item names are entered
            item_name = None
            while item_name != 'q':
                self._list_all_items()
                item_name = input("\nEnter the name of an item to add (q to stop): ")
                if item_name == 'q' and len(item_ids) == 0:
                    clear()
                    item_name = None
                    print("An order must have at least one item. Please try again.")
                elif item_name == 'q':
                    clear()
                    break
                else:
                    clear()
                    item = self._item_repo.find_by_name(item_name)
                    if type(item) != Item:
                        print("Invalid item. Please try again.")
                        item = None
                    else:             
                        print(f"Item '{item_name}' added to order.")       
                        item_ids.append(item.id)

            return name, sorted(item_ids)

    def _prompt_for_order_id(self, id=None):

        # loop until valid id entered
        while id == None:
            try:
                id = int(input("\nEnter the order id (-1 to cancel): "))
                clear()
                if id == -1:
                    return None
                
                order = self._order_repo.find_by_id(id)

                if type(order) != Order:
                    print("Order does not exist, Please try again.")
                    id = None
                else:
                    return order
            
            except:
                print("Invalid id. Please try again.")
                id = None
    
    # format an orders details with items
    def _format_order_details(self, order):
        print(f"\nOrder ID: {order.id}")
        print(f"Customer Name: {order.customer_name}")
        print(f"Date Placed: {order.date_placed}")
        print(f"Items: ")
        for item in order.items:
            print(f"\t{self._item_repo.find_by_id(item).name} - £{self._item_repo.find_by_id(item).unit_price:.2f}")
        print(f"\n\tTotal: £{order.calculate_total(self._item_repo):.2f}")
    
    # list all items in a readable format
    def _list_all_items(self):
        print("\nAll items:")

        items = self._item_repo.all()
        for item in items:
            print(item)
    
    # list all orders in a readable format
    def _list_all_orders(self):
        print("\nAll orders:")

        orders = self._order_repo.all()
        for order in orders:
            print(order)

    def run(self):
        # loop until user exits
        while True:

            # welcome user and prompt for object to manage
            print("\nWelcome to the Shop Manager\n")
            obj_choice = self._prompt_for_object_to_manage()

            # manage orders
            while obj_choice == 'orders':
                order_action = self._prompt_for_order_action()

                # break out of loop to go back to menu
                if order_action == 'back':
                    break

                # create a new order
                elif order_action == 'create':
                    name, item_ids = self._prompt_for_order_details()
                    self._order_repo.create_order(name, item_ids)
                    print(f"\nOrder for '{name}' created successfully.")
                    input("\nPress enter to continue...")
                    clear()
                
                # cancel an existing order
                elif order_action == 'delete':
                    self._list_all_orders()
                    target = input("\nEnter the id of the order to cancel: ")
                    success = self._order_repo.delete_by_id(target)

                    if success:
                        print(f"\nOrder '{target}' deleted successfully.")
                    else:
                        print(f"\nOrder '{target}' does not exist.")
                    input("\nPress enter to continue...")
                    clear()

                # list all orders
                elif order_action == 'list':
                    self._list_all_orders()
                    input("\nPress enter to continue...")
                    clear()
                
                elif order_action == 'find':
                    self._list_all_orders()
                    order = self._prompt_for_order_id()
                    if type(order) != Order:
                        break
                    else:
                        self._format_order_details(order)
                    input("\nPress enter to continue...")
                    clear()
                    
            # manage items
            while obj_choice == 'items':
                item_action = self._prompt_for_item_action()

                # break out of loop to go back to menu
                if item_action == 'back':
                    break

                # create a new item
                elif item_action == 'create':
                    name, quantity, price = self._prompt_for_item_contents()
                    success = self._item_repo.create_item(name, quantity, price)
                    
                    if success:
                        print(f"\nItem '{name}' created successfully.")
                    else:
                        print(f"\nItem '{name}' already exists.")
                    input("\nPress enter to continue...")
                    clear()

                # update an existing item
                elif item_action == 'update':
                    self._list_all_items()
                    name, quantity, price = self._prompt_for_item_contents()
                    success = self._item_repo.update_item(name, quantity, price)

                    if success:
                        print(f"\nItem '{name}' updated successfully.")
                    else:
                        print(f"\nItem '{name}' does not exist.")
                    input("\nPress enter to continue...")
                    clear()

                # delete an existing item
                elif item_action == 'delete':
                    self._list_all_items()
                    target = self._prompt_for_item_delete()
                    success = self._item_repo.delete_item(target)

                    if success:
                        print(f"\nItem '{target}' deleted successfully.")
                    else:
                        print(f"\nItem '{target}' does not exist.")
                    input("\nPress enter to continue...")
                    clear()

                # list all items
                elif item_action == 'list':
                    self._list_all_items()
                    input("\nPress enter to continue...")
                    clear()


if __name__ == '__main__':
    clear()
    app = Application()
    app.run()