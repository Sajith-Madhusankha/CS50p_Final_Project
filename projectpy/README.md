# Simple Expense Tracker
#### Video Demo:  <https://youtu.be/3O804TcrlOU>
#### Description: This is a simple Expense Tracker programmed using Python. It helps users to manage their expenses and get summarized reports about their expenses.
I used ANSCI Escape sequences to make the interface look more appealing to the users.

Users have 5 choices. First choice is Add expense. when user choose this option it will prompt the user to give amount and category of the expense. User can run this option to muliple times to add more expenses. But these expenses does'nt added to csv file directly. User need to save expenses if need to add to csv file.
2nd Choice is Generate report. This will print a summerized report about total expenditure. If user added expenses to same category, they will be all added and shown as one expenditure. Also total amount of all expenditure will be shown too. Here's example.

    Total Expenses: $175.00

    Expense by Category:
    toys: $15.00
    games: $20.00
    medicine: $50.00
    foods: $40.00
    beverages: $50.00

Load expenses helps user to detect any changed done to csv file. If some item removed from the expenses.csv, it won't be shown in report unless user load it to program.

Heres a brief explanation about whats going on inside this program.

- First I imported necessary libraries
    - CSV library to handle csv file operations
    ```
    import csv
    ```
    - datetime library to get date
    ```
    import datetime
    ```
---------------------
- This is the main function
    ```
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
    ```
    - It calls ExpenseTracker() function. then assign "expense.csv" as file name. Then it calls load_expenses method to load any data available in CSV file.
    - Then it starts a infinite loop. It calls show_menu function so menu will be printed to screen. then by the user choices it calls different functions to
        1. add expenses
        2. Generate report
        3. Save expenses
        4. Load expenses
        5. exit program
--------------------
- add_expense function
    ```
    def add_expense(expense_tracker):
        amount = float(input("Enter the expense amount: "))
        category = input("Enter the expense category: ")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        expense = Expense(amount, category, date)
        expense_tracker.add_expense(expense)
        print("\033[92mExpense added successfully.\033[0m")
    ```
    - Calling this function will prompt user to get amount, category for a particular expense. It'll get the current date using

    ```
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ```
--------------------------
- get_user_choice function
    ```
    def get_user_choice():
        while True:
          choice = input("Enter your choice (1-5): ")
          if choice.isdigit() and 1 <= int(choice) <= 5:
              return int(choice)
          print("Invalid choice. Please try again.")
    ```
    - This function will check which option user chosen. It should be between 1 and 5. If it's less or larger than 1 - 5 range, Error message will be printed to screen saying "Invalid choice, Please try again"
------------------------
- show_menu function
    ```
    def show_menu():
        print("\nExpense Tracker")
        print("1. \033[93mAdd Expense\033[0m")
        print("2. \033[93mGenerate Report\033[0m")
        print("3. \033[93mSave Expenses\033[0m")
        print("4. \033[93mLoad Expenses\033[0m")
        print("5. \033[93mExit\033[0m")
    ```

    - Calling this function will print available options in the program.

------------------
- Expense Class
    ```
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

    class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def save_expenses(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense.to_dict())

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
    ```
    - Above Class handle all the main functionality of the program. It Opens, reads csv file, generates reports, load files, handle certain errors like file not found.



    I Used ANSCI escape sequences because it's easy to apply. If I added other libraries like colorama and prettytable, it'll be hard for me to make pytest.

