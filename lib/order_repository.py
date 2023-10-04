from lib.order import Order
from lib.item import Item
from datetime import datetime

class OrderRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM orders')
        return [Order(row['id'], row['customer_name'], row['date_placed']) for row in rows]

    def find_by_name(self, name):
        rows = self._connection.execute("SELECT * FROM orders WHERE customer_name = %s", 
                                        [name])
        return [Order(row['id'], row['customer_name'], row['date_placed']) for row in rows]
    
    def create_order(self, name, item_ids):
        date = datetime.today().strftime('%Y-%m-%d')

        self._connection.execute(
            'INSERT INTO orders (customer_name, date_placed) VALUES (%s, %s)',
            [name, date]
        )
        order_id = self.find_by_name(name)[-1].id

        for item_id in item_ids:
            self._connection.execute(
                'INSERT INTO orders_items (order_id, item_id) VALUES (%s, %s)',
                [order_id, item_id]
            )