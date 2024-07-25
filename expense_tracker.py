import calendar
import datetime
import matplotlib.pyplot as plt
import csv
import os

class Expense:
    def __init__(self, name, category, amount, date=None) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, Rs{self.amount:.2f}, {self.date} >"


def main():
    print(green("🎯 Running Expense Tracker!"))
    expense_file_path = "expenses.csv"
    budget = set_initial_budget()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == '1':
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == '2':
            summarize_expenses(expense_file_path, budget)
        elif choice == '3':
            budget = set_savings_goal(budget)
        elif choice == '4':
            export_expenses(expense_file_path)
        elif choice == '5':
            break
        else:
            print(red("Invalid choice. Please try again."))


def print_menu():
    print("\nExpense Tracker Menu:")
    print("1. Add an Expense")
    print("2. View Summary")
    print("3. Set Monthly Savings Goal")
    print("4. Export Expenses")
    print("5. Exit")


def get_user_expense():
    print(green("🎯 Getting User Expense"))
    expense_name = input("Enter expense name: ")
    
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                raise ValueError
            break
        except ValueError:
            print(red("Invalid amount. Please enter a positive number."))

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        try:
            selected_index = int(input(f"Enter a category number [1 - {len(expense_categories)}]: ")) - 1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(
                    name=expense_name, category=selected_category, amount=expense_amount
                )
                return new_expense
            else:
                raise ValueError
        except ValueError:
            print(red("Invalid category. Please try again!"))


def save_expense_to_file(expense: Expense, expense_file_path):
    print(green(f"🎯 Saving User Expense : {expense} to {expense_file_path}"))
    with open(expense_file_path, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.amount, expense.category, expense.date])


def summarize_expenses(expense_file_path, budget):
    print(green("🎯 Summarizing User Expense"))
    expenses = read_expenses_from_file(expense_file_path)

    if not expenses:
        print(red("No expenses recorded yet."))
        return

    amount_by_category = {}
    for expense in expenses:
        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount
        else:
            amount_by_category[expense.category] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: Rs{amount:.2f}")

    total_spent = sum(expense.amount for expense in expenses)
    print(f"💵 Total Spent: Rs{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: Rs{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: Rs{daily_budget:.2f}"))

    plot_expenses_by_category(amount_by_category)
    plot_expenses_over_time(expenses)


def read_expenses_from_file(expense_file_path):
    expenses = []
    if os.path.exists(expense_file_path):
        with open(expense_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    expense_name, expense_amount, expense_category, expense_date = row
                    expenses.append(Expense(
                        name=expense_name,
                        amount=float(expense_amount),
                        category=expense_category,
                        date=expense_date,
                    ))
                else:
                    print(f"Skipping invalid line: {row}")
    return expenses


def set_initial_budget():
    while True:
        try:
            budget = float(input("Enter your initial budget: "))
            if budget <= 0:
                raise ValueError
            print(green(f"Initial budget set to Rs{budget:.2f}"))
            return budget
        except ValueError:
            print(red("Invalid budget. Please enter a positive number."))


def set_savings_goal(current_budget):
    while True:
        try:
            savings_goal = float(input("Enter your monthly savings goal: "))
            if savings_goal < 0:
                raise ValueError
            new_budget = current_budget - savings_goal
            if new_budget < 0:
                print(red("Savings goal exceeds current budget. Please enter a lower amount."))
            else:
                print(green(f"New budget after savings goal set to Rs{new_budget:.2f}"))
                return new_budget
        except ValueError:
            print(red("Invalid savings goal. Please enter a non-negative number."))


def export_expenses(expense_file_path):
    expenses = read_expenses_from_file(expense_file_path)
    if not expenses:
        print(red("No expenses to export."))
        return

    export_path = "exported_expenses.csv"
    with open(export_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Amount", "Category", "Date"])
        for expense in expenses:
            writer.writerow([expense.name, expense.amount, expense.category, expense.date])
    print(green(f"Expenses exported to {export_path}"))


def plot_expenses_by_category(amount_by_category):
    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())

    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def plot_expenses_over_time(expenses):
    expenses.sort(key=lambda x: x.date)
    dates = [expense.date for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, amounts, marker='o')
    plt.title("Expenses Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount (Rs)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"


if __name__ == "__main__":
    main()
