from lib.item import Item

class ItemRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def all(self, sort_by=lambda item: item.id):
        rows = self._connection.execute('SELECT * FROM items')
        return sorted([Item(row['id'], row['name'], row['quantity'], row['unit_price']) for row in rows], key=sort_by)
    
    def find_by_name(self, name):
        rows = self._connection.execute('SELECT * FROM items WHERE SIMILARITY(name, %(name)s) > 0.3 ' \
                                        'ORDER BY SIMILARITY(name, %(name)s)', {'name': name})
        if rows != []:
            return Item(rows[0]['id'], rows[0]['name'], rows[0]['quantity'], rows[0]['unit_price'])
        else:
            return None
    
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * FROM items WHERE id = %s', [id])
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
        found_item = self.find_by_name(name)
        if type(found_item) != Item:
            return name, False
        elif type(found_item) == Item and found_item.name == name:
            self._connection.execute(
                "UPDATE items SET quantity = %s, unit_price = %s WHERE name = %s",
                [quantity, price, name]
            )
            return found_item.name, True
        elif type(found_item) == Item and found_item.name != name:
            return found_item.name, False
    
    def delete_item(self, name):
        found_item = self.find_by_name(name)
        if type(found_item) != Item:
            return name, False
        elif type(found_item) == Item and found_item.name == name:
            self._connection.execute(
                "DELETE FROM items WHERE name = %s",
                [found_item.name]
            )
            return found_item.name, True
        elif type(found_item) == Item and found_item.name != name:
            return found_item.name, False
    