from lib.item_repository import ItemRepository

def test_all_items(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = ItemRepository(db_connection)

    items = repo.all()

    assert len(items) == 5
    assert items[0].id == 1
    assert items[0].name == 'apple'
    assert items[-1].id == 5
    assert items[-1].name == 'milk'

def test_create_item(db_connection):
    db_connection.seed('seeds/shop_manager.sql')
    repo = ItemRepository(db_connection)

    item1_success = repo.create_item('orange', 10, 1.5)
    item2_success = repo.create_item('apple', 10, 1.5)
    items = repo.all()

    '''
    assert len(items) == 6
    assert items[-1].id == 6
    assert items[-1].name == 'orange'
    assert items[-1].quantity == 10
    assert items[-1].unit_price == 1.5
    assert item1_success
    assert not item2_success
    '''