from lib.order import *

def test_init():
    order = Order(1, 'name', '01/01/2023')

    assert order.id == 1
    assert order.customer_name == 'name'
    assert order.date_placed == '01/01/2023'

def test_repr():
    order = Order(1, 'name', '01/01/2023')

    assert str(order) == '1: name (01/01/2023)'

def test_eq():
    order1 = Order(1, 'name', '01/01/2023')
    order2 = Order(1, 'name', '01/01/2023')

    assert order1 == order2

def test_calculate_total(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    item_repo = ItemRepository(db_connection)

    order = Order(1, 'name', '01/01/2023', [1, 1])
    total = order.calculate_total(item_repo)

    assert total == 1