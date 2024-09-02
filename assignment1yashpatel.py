import csv

class Car:
    """A class to represent a car."""

    def __init__(self, manufacturer, model, year, mileage, engine, transmission, drivetrain, mpg, exterior_color, interior_color, accident, price):
        """Initialize the car with the given attributes."""
        self.manufacturer = manufacturer
        self.model = model
        self.year = int(year)
        self.mileage = float(mileage) if mileage else 0.0  # Handle empty mileage
        self.engine = engine
        self.transmission = transmission
        self.drivetrain = drivetrain
        self.mpg = self.parse_mpg(mpg)  # Handle mpg ranges
        self.exterior_color = exterior_color
        self.interior_color = interior_color
        self.accident = accident.lower() == "yes"
        self.price = float(price) if price else 0.0  # Handle empty price

    def parse_mpg(self, mpg):
        """Parse the mpg field to handle ranges and single values."""
        if '-' in mpg:
            low, high = map(float, mpg.split('-'))
            return (low + high) / 2
        return float(mpg)

    def paint(self, color):
        """Change the exterior color of the car to the color."""
        self.exterior_color = color

    def repair(self, part, new_part):
        """Replace the entered part with the new part."""
        if part == "engine":
            self.engine = new_part
        elif part == "transmission":
            self.transmission = new_part
        elif part == "drivetrain":
            self.drivetrain = new_part
        else:
            raise ValueError("Error in part name")

    def reupholster(self, color):
        """Change the interior color of the car to the color."""
        self.interior_color = color

    def modify_price(self, amount):
        """Change the price of the car to the specified amount."""
        if amount > 0:
            self.price = amount
        else:
            self.price += amount
            print(f"The price has been discounted by {-amount}.")
            if input("Is this the correct price? (y/n): ") != "y":
                self.modify_price(-amount)

class Seller:
    """A class to represent a car seller."""

    def __init__(self, name, rating):
        """Initialize the seller with the given name and rating."""
        self.name = name
        self.rating = rating
        self.inventory = []

    def buy(self, car):
        """Add the given car to the seller's inventory."""
        self.inventory.append(car)

    def sell(self, car):
        """Remove the given car from the seller's inventory."""
        self.inventory.remove(car)

with open("cars.csv") as csvfile:
    reader = csv.DictReader(csvfile)

    sellers = {}
    cars = []

    for row in reader:
        try:
            car = Car(
                row["manufacturer"],
                row["model"],
                row["year"],
                row["mileage"],
                row["engine"],
                row["transmission"],
                row["drivetrain"],
                row["mpg"],
                row["exterior_color"],
                row["interior_color"],
                row.get("accident", "No"),  # Provide a default value if 'accident' key is missing
                row["price"],
            )
            cars.append(car)

            if row["seller_name"] not in sellers:
                sellers[row["seller_name"]] = Seller(row["seller_name"], row["seller_rating"])

            sellers[row["seller_name"]].buy(car)
        except ValueError as e:
            print(f"Skipping row due to error: {e}")

# Print the inventory count for each seller
for seller_name, seller in sellers.items():
    print(f"{seller_name} has {len(seller.inventory)} cars in inventory.")