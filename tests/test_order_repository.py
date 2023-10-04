from lib.order_repository import *
from lib.item import Item

def test_all_orders(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = OrderRepository(db_connection)

    orders = repo.all()

    assert len(orders) == 3
    assert orders[0].id == 1
    assert orders[0].customer_name == 'John'
    assert orders[-1].id == 3
    assert orders[-1].customer_name == 'Jack'

def test_find_orders_by_name(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = OrderRepository(db_connection)

    orders = repo.find_by_name('John')

    assert len(orders) == 1
    assert orders[0].customer_name == 'John'

def test_create_order(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = OrderRepository(db_connection)

    item_ids = [1, 2]
    repo.create_order('Toby', item_ids)
    orders = repo.all()

    assert len(orders) == 4
    assert orders[-1].customer_name == 'Toby'

def test_find_by_id(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = OrderRepository(db_connection)

    order = repo.find_by_id(1)

    assert order.items == [1, 2, 5]