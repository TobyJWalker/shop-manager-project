class Item:
    def __init__(self, id, name, quantity, unit_price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price

    def __repr__(self):
        return f"{self.id}: {self.name} - {self.quantity} @ £{self.unit_price:.2f}"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__