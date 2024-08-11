# Samuel Omirin 2019946

import csv
from datetime import datetime

class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def load_manufacturer_list(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"Processing row: {row}")
                if len(row) < 3:  # Check if the row has at least 3 elements
                    print(f"Skipping incomplete row: {row}")
                    continue
                item_id = row[0].strip()
                manufacturer = row[1].strip()
                item_type = row[2].strip()
                damaged = row[3].strip() if len(row) > 3 else ""  # Handle optional damaged indicator

                self.inventory[item_id] = {
                    "manufacturer": manufacturer,
                    "item_type": item_type,
                    "damaged": damaged,
                    "price": None,
                    "service_date": None
                }

    def load_price_list(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    print(f"Skipping incomplete row: {row}")
                    continue
                item_id = row[0].strip()
                price = row[1].strip()
                if item_id in self.inventory:
                    self.inventory[item_id]["price"] = float(price)

    def load_service_dates_list(self, filename):
        with open(filename, 'r') as file:  # Corrected the extra closing parenthesis
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    print(f"Skipping incomplete row: {row}")
                    continue
                item_id = row[0].strip()
                service_date = row[1].strip()
                if item_id in self.inventory:
                    self.inventory[item_id]["service_date"] = datetime.strptime(service_date, '%m/%d/%Y')

    def generate_full_inventory(self, filename):
        sorted_inventory = sorted(self.inventory.items(), key=lambda x: x[1]["manufacturer"])
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for item_id, item_info in sorted_inventory:
                    row = [
                        item_id,
                        item_info["manufacturer"],
                        item_info["item_type"],
                        item_info["price"],
                        item_info["service_date"].strftime('%m/%d/%Y') if item_info["service_date"] else "",
                        "damaged" if item_info["damaged"] else ""
                    ]
                    writer.writerow(row)
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")

    def generate_item_type_inventory(self):
        item_types = {}
        for item_id, item_info in self.inventory.items():
            item_type = item_info["item_type"]
            if item_type not in item_types:
                item_types[item_type] = []
            item_types[item_type].append((item_id, item_info))

        for item_type, items in item_types.items():
            items.sort(key=lambda x: x[1]["price"])
            filename = f'{item_type.capitalize()}Inventory.csv'  # Generates LaptopInventory.csv, PhoneInventory.csv, etc.
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for item_id, item in items:
                        row = [
                            item_id,
                            item["manufacturer"],
                            item["price"],
                            item["service_date"].strftime('%m/%d/%Y') if item["service_date"] else "",
                            "damaged" if item["damaged"] else ""
                        ]
                        writer.writerow(row)
            except IOError as e:
                print(f"Error writing to file {filename}: {e}")

    def generate_past_service_date_inventory(self, filename):
        past_service_date_items = [
            (item_id, item) for item_id, item in self.inventory.items()
            if item["service_date"] and item["service_date"] < datetime.now()
        ]
        past_service_date_items.sort(key=lambda x: x[1]["service_date"])
        
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for item_id, item in past_service_date_items:
                    row = [
                        item_id,
                        item["manufacturer"],
                        item["item_type"],
                        item["price"],
                        item["service_date"].strftime('%m/%d/%Y') if item["service_date"] else "",
                        "damaged" if item["damaged"] else ""
                    ]
                    writer.writerow(row)
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")

    def generate_damaged_inventory(self, filename):
        damaged_items = [
            (item_id, item) for item_id, item in self.inventory.items() if item["damaged"]
        ]
        damaged_items.sort(key=lambda x: x[1]["price"], reverse=True)
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for item_id, item in damaged_items:
                    row = [
                        item_id,
                        item["manufacturer"],
                        item["item_type"],
                        item["price"],
                        item["service_date"].strftime('%m/%d/%Y') if item["service_date"] else ""
                    ]
                    writer.writerow(row)
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")


# Instantiate and load data
inventory_manager = InventoryManager()
inventory_manager.load_manufacturer_list('ManufacturerList.csv')
inventory_manager.load_price_list('PriceList.csv')
inventory_manager.load_service_dates_list('ServiceDatesList.csv')

# Generate reports
inventory_manager.generate_full_inventory('FullInventory.csv')
inventory_manager.generate_item_type_inventory()  # Generates files for each type of item
inventory_manager.generate_past_service_date_inventory('PastServiceDateInventory.csv')
inventory_manager.generate_damaged_inventory('DamagedInventory.csv')
