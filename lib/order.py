class Order:
    def __init__(self, id, customer_name, date_placed, items=None):
        self.id = id
        self.customer_name = customer_name
        self.date_placed = date_placed
        self.items = items
    
    def __repr__(self):
        return f"{self.id}: {self.customer_name} ({self.date_placed})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__