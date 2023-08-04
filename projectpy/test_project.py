import datetime
import pytest
from project import Expense, ExpenseTracker

@pytest.fixture
def expense_tracker():
    tracker = ExpenseTracker()
    yield tracker
    # Teardown: Clean up the expenses after each test
    tracker.expenses = []

def test_add_expense(expense_tracker):
    expense = Expense(10.0, "Food", datetime.datetime.now().strftime("%Y-%m-%d"))
    expense_tracker.add_expense(expense)
    assert len(expense_tracker.expenses) == 1

def test_generate_report(expense_tracker, capsys):
    expense1 = Expense(10.0, "Food", datetime.datetime.now().strftime("%Y-%m-%d"))
    expense2 = Expense(20.0, "Transportation", datetime.datetime.now().strftime("%Y-%m-%d"))
    expense_tracker.add_expense(expense1)
    expense_tracker.add_expense(expense2)

    expense_tracker.generate_report()
    captured = capsys.readouterr()
    assert "\nTotal Expenses: \033[92m$30.00\033[0m\n" in captured.out
    assert "\033[94mFood:\033[0m \033[92m$10.00" in captured.out
    assert "\033[94mTransportation:\033[0m \033[92m$20.00" in captured.out

def test_save_and_load_expenses(expense_tracker, tmp_path):
    filename = tmp_path / "test_expenses.csv"

    # Add expenses
    expense1 = Expense(10.0, "Food", datetime.datetime.now().strftime("%Y-%m-%d"))
    expense2 = Expense(20.0, "Transportation", datetime.datetime.now().strftime("%Y-%m-%d"))
    expense_tracker.add_expense(expense1)
    expense_tracker.add_expense(expense2)

    # Save expenses
    expense_tracker.save_expenses(filename)
    assert filename.exists()

    # Clear existing expenses
    expense_tracker.expenses = []

    # Load expenses
    expense_tracker.load_expenses(filename)
    assert len(expense_tracker.expenses) == 2
    assert expense_tracker.expenses[0].amount == 10.0
    assert expense_tracker.expenses[0].category == "Food"
    assert expense_tracker.expenses[1].amount == 20.0
    assert expense_tracker.expenses[1].category == "Transportation"
