"""Create Category class in budget.py. It should be able to instantiate objects based on
different budget categories like food, clothing, and entertainment. When objects are created,
they are passed in the name of the category. The class should have an instance variable called
ledger that is a list. The class should also contain the following methods:"""


class Category:
    def __init__(self, name):
        self.category = name
        self.ledger = list()

    """A deposit method that accepts an amount and description. If no description is given, 
    it should default to an empty string. The method should append an object to the ledger 
    list in the form of {"amount": amount, "description": description}."""
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    """A withdraw method that is similar to the deposit method, but the amount passed in 
    should be stored in the ledger as a negative number. If there are not enough funds, 
    nothing should be added to the ledger. This method should return True if the withdrawal 
    took place, and False otherwise."""
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            return self.ledger.append({"amount": -amount, "description": description})

    """A get_balance method that returns the current balance of the budget category based on
     the deposits and withdrawals that have occurred. i.e sum up left over amount"""
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    """A check_funds method that accepts an amount as an argument. It returns False if the 
    amount is greater than the balance of the budget category and returns True otherwise. 
    This method should be used by both the withdraw method and transfer method."""
    def check_funds(self, amount):
        if amount <= self.get_balance():
            return True
        return False

    """A transfer method that accepts an amount and another budget category as arguments. 
    The method should add a withdrawal with the amount and the description "Transfer to 
    [Destination Budget Category]". The method should then add a deposit to the other budget 
    category with the amount and the description "Transfer from [Source Budget Category]". 
    If there are not enough funds, nothing should be added to either ledgers. This method 
    should return True if the transfer took place, and False otherwise."""
    def transfer(self, amount, category_to):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category_to.category}")
            category_to.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False

    """When the budget object is printed it should display:
    •	A title line of 30 characters where the name of the category is centered in a line of
     * characters.
    •	A list of the items in the ledger. Each line should show the description and amount. 
    The first 23 characters of the description should be displayed, then the amount. The amount
    should be right aligned, contain two decimal places, and display a maximum of 7 characters.
    •	A line displaying the category total.
    """
    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        total = 0

        # Get the respective items in the  ledger list
        for item in self.ledger:
            description = item["description"][:23]
            amount = "{:,.2f}".format(item["amount"])
            total += item["amount"]
            items += f"{description}{amount.rjust(30 - len(description))}\n"
        return title + items + "{a:<}{b:>24,.2f}\n".format(a="Total:", b=total)

    # Create a function that calculate total withdrawal
    def get_withdrawal(self):
        return sum(item["amount"] for item in self.ledger if item["amount"] < 0)


def create_spend_chart(categories):

    # Calculate the total spent across all categories.
    total_spent = sum(category.get_withdrawal() for category in categories)
    print(total_spent)

    # Calculate the percentage spent for each category.
    percentages = [(category.get_withdrawal() / total_spent) * 100 for category in categories]
    print(percentages)

    # Build the chart.
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    # Add the horizontal line below the bars.
    chart += "    -" + "---" * len(categories) + "\n"

    # Determine the maximum category name length.
    max_name_length = max(len(category.category) for category in categories)

    # Add category names vertically below the bars.
    for i in range(max_name_length):
        chart += "     "
        for category in categories:
            if i < len(category.category):
                chart += category.category[i] + "  "
            else:
                chart += "   "
        if i < max_name_length - 1:
            chart += "\n"

    return chart.strip()


# Example usage:
food_category = Category("Food")
clothing_category = Category("Clothing")
transport_category = Category("Transport")
health_category = Category("Health")

food_category.deposit(1000, "Initial deposit")
food_category.withdraw(10.15, "Groceries")
food_category.withdraw(15.89, "Restaurant and more food")

clothing_category.deposit(5000, "Initial deposit")
clothing_category.withdraw(1000, "chocolate")
food_category.transfer(50, clothing_category)
clothing_category.withdraw(2000, "Fair of shoes")

transport_category.deposit(50000, "Initial deposit")
transport_category.withdraw(4000, "Weekly fare")
transport_category.withdraw(1000, "servicing")

health_category.deposit(2000, "Initial deposit")
health_category.withdraw(1500, "Pharmacy")

categories = [food_category, clothing_category, transport_category, health_category]

print(food_category)
print(clothing_category)
print(transport_category)
print(health_category)
print(create_spend_chart(categories))
