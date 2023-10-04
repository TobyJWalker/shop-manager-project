from lib.item import Item

class ItemRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * FROM items')
        return sorted([Item(row['id'], row['name'], row['quantity'], row['unit_price']) for row in rows], key=lambda item: item.id)
    
    def find_by_name(self, name):
        rows = self._connection.execute('SELECT * FROM items WHERE name = %s', [name])
        if rows != []:
            return Item(rows[0]['id'], rows[0]['name'], rows[0]['quantity'], rows[0]['unit_price'])
        else:
            return None
    
    def create_item(self, name, quantity, price):
        if type(self.find_by_name(name)) != Item:
            self._connection.execute(
                "INSERT INTO items (name, quantity, unit_price) VALUES (%s, %s, %s)",
                [name, quantity, price]
            )
            return True
        else:
            return False
    
    def update_item(self, name, quantity, price):
        if type(self.find_by_name(name)) == Item:
            self._connection.execute(
                "UPDATE items SET quantity = %s, unit_price = %s WHERE name = %s",
                [quantity, price, name]
            )
            return True
        else:
            return False
    