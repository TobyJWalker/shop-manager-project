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
    
    # list all items in a readable format
    def _list_all_items(self):
        print("\nAll items:")

        items = self._item_repo.all()
        for item in items:
            print(item)

    def run(self):
        # loop until user exits
        while True:

            # welcome user and prompt for object to manage
            print("\nWelcome to the Shop Manager\n")
            obj_choice = self._prompt_for_object_to_manage()

            # manage orders
            while obj_choice == 'orders':
                pass
            
            # manage items
            while obj_choice == 'items':
                item_action = self._prompt_for_item_action()

                # break out of loop to go back to menu
                if item_action == 'back':
                    break

                # create a new item
                if item_action == 'create':
                    name, quantity, price = self._prompt_for_item_contents()
                    self._item_repo.create_item(name, quantity, price)
                    print(f"\nItem '{name}' created successfully.")
                    input("\nPress enter to continue...")
                    clear()

                # update an existing item
                elif item_action == 'update':
                    pass

                # delete an existing item
                elif item_action == 'delete':
                    pass

                # list all items
                elif item_action == 'list':
                    self._list_all_items()
                    input("\nPress enter to continue...")
                    clear()


if __name__ == '__main__':
    clear()
    app = Application()
    app.run()