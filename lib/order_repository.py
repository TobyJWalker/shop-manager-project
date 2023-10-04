from lib.order import Order
from lib.item_repository import *
from datetime import datetime

class OrderRepository:
    def __init__(self, connection):
        self._connection = connection
        self._item_repo = ItemRepository(connection)

    def all(self, sort_by = lambda order: order.id):
        rows = self._connection.execute('SELECT * FROM orders')
        return sorted([Order(row['id'], row['customer_name'], row['date_placed']) for row in rows], key=sort_by)

    def find_by_name(self, name):
        rows = self._connection.execute("SELECT * FROM orders WHERE customer_name = %s", 
                                        [name])
        return [Order(row['id'], row['customer_name'], row['date_placed']) for row in rows]

    def find_by_id(self, id):
        rows = self._connection.execute("SELECT orders.id as order_id, orders.customer_name, orders.date_placed, items.id as item_id " \
                                        "FROM orders JOIN orders_items ON orders.id = orders_items.order_id " \
                                        "JOIN items ON orders_items.item_id = items.id " \
                                        "WHERE orders.id = %s", [id])
        item_ids = [row['item_id'] for row in rows]
        try:
            return Order(rows[0]['order_id'], rows[0]['customer_name'], rows[0]['date_placed'], item_ids)
        except:
            return None
    
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
    
    def delete_by_id(self, id):
        if type(self.find_by_id(id)) == Order:
            self._connection.execute(
                'DELETE FROM orders WHERE id = %s',
                [id]
            )
            return True

        return False