class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        total = 0

        for item in self.ledger:
            description = item["description"][:23]
            amount = "{:,.2f}".format(item["amount"])   # New style of string formatting
            # amount = "%.2f" % item["amount"]        # Old style of string formatting
            total += item["amount"]
            items += f"{description}{amount.rjust(30 - len(description))}\n"

        return title + items + f"Total:{total:>24.2f}"



def create_spend_chart(categories):
    # Calculate the total spent across all categories.
    total_spent = sum(category.get_withdrawals() for category in categories)

    # Calculate the percentage spent for each category.
    percentages = [(category.get_withdrawals() / total_spent) * 100 for category in categories]

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

food_category.deposit(1000, "Initial deposit")
food_category.withdraw(10.15, "Groceries")
clothing_category.deposit(500, "Initial deposit")
clothing_category.transfer(50, food_category)
categories = [food_category, clothing_category]

print(food_category)
print(clothing_category)
print(create_spend_chart(categories))

