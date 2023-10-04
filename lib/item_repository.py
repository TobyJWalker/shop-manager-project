from lib.item import Item

class ItemRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * FROM items')
        return [Item(row['id'], row['name'], row['quantity'], row['unit_price']) for row in rows]
    
    def create_item(self, name, quantity, price):
        self._connection.execute(
            "INSERT INTO items (name, quantity, unit_price) VALUES (%s, %s, %s)",
            [name, quantity, price]
        )
    