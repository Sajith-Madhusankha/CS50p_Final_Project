# Simple Expense Tracker
# Sajith Madhusankha
# Final Project for CS50p

# Import Necessary Libraries
import csv
import datetime

# Define Expense Class
class Expense:
    def __init__(self, amount, category, date):
        self.amount = float(amount)
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Expense(data["amount"], data["category"], data["date"])

# Define ExpenseTracker Class
class ExpenseTracker:
    # Initialize ExpenseTracker Class
    def __init__(self):
        self.expenses = []

    # Add Expense
    def add_expense(self, expense):
        self.expenses.append(expense)

    # Save Expenses
    def save_expenses(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense.to_dict())

    # Load Expenses
    def load_expenses(self, filename):
        self.expenses = []
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense.from_dict(row)
                    self.add_expense(expense)
        except FileNotFoundError:
            pass

    # Generate Report
    def generate_report(self):
        total_expenses = sum(expense.amount for expense in self.expenses)
        print(f"\nTotal Expenses: \033[92m${total_expenses:.2f}\033[0m\n")
        categories = {}
        for expense in self.expenses:
            category = expense.category
            if category not in categories:
                categories[category] = 0
            categories[category] += expense.amount
        print("Expense by Category:")
        for category, amount in categories.items():
            print(f"\033[94m{category}:\033[0m \033[92m${amount:.2f}\033[0m")

# Show Menu
def show_menu():
    print("\nExpense Tracker")
    print("1. \033[93mAdd Expense\033[0m")
    print("2. \033[93mGenerate Report\033[0m")
    print("3. \033[93mSave Expenses\033[0m")
    print("4. \033[93mLoad Expenses\033[0m")
    print("5. \033[93mExit\033[0m")

# Get User Choice
def get_user_choice():
    while True:
        choice = input("Enter your choice (1-5): ")
        if choice.isdigit() and 1 <= int(choice) <= 5:
            return int(choice)
        print("Invalid choice. Please try again.")

# Add Expense
def add_expense(expense_tracker):
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the expense category: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    expense = Expense(amount, category, date)
    expense_tracker.add_expense(expense)
    print("\033[92mExpense added successfully.\033[0m")


# Main Function
def main():
    expense_tracker = ExpenseTracker()
    filename = "expenses.csv"
    expense_tracker.load_expenses(filename)

    while True:
        # Show Menu
        show_menu()
        choice = get_user_choice()

        if choice == 1:
            add_expense(expense_tracker)
        elif choice == 2:
            expense_tracker.generate_report()
        elif choice == 3:
            expense_tracker.save_expenses(filename)
            print("\033[92mExpenses saved successfully.\033[0m")
        elif choice == 4:
            expense_tracker.load_expenses(filename)
            print("\033[92mExpenses loaded successfully.\033[0m")
        elif choice == 5:
            expense_tracker.save_expenses(filename)
            print("\033[92mExpenses saved. Exiting...\033[0m")
            break


# Run Main Function
if __name__ == "__main__":
    main()
