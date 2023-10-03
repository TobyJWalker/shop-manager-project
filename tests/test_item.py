from lib.item import Item

def test_init():
    item = Item(1, 'test', 1, 1)
    assert item.id == 1
    assert item.name == 'test'
    assert item.quantity == 1
    assert item.unit_price == 1

def test_repr():
    item = Item(1, 'test', 1, 1)
    assert repr(item) == 'Item(1, test, 1, 1)'

def test_eq():
    item1 = Item(1, 'test', 1, 1)
    item2 = Item(1, 'test', 1, 1)
    assert item1 == item2