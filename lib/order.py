from lib.item_repository import *

class Order:
    def __init__(self, id, customer_name, date_placed, items=None):
        self.id = id
        self.customer_name = customer_name
        self.date_placed = date_placed
        self.items = items

    def calculate_total(self, item_repo):
        total = 0
        for item in self.items:
            total += item_repo.find_by_id(item).unit_price
        return total
    
    def __repr__(self):
        return f"{self.id}: {self.customer_name} ({self.date_placed})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__