class InventoryItem:
    def __init__(self, item_id, count):
        self.item_id = item_id
        self.count = count
    def __repr__(self):
        return f"{self.count}n{self.item_id}"