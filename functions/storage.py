import json

FILE = "data/expenses.json"


def load_expenses():
    try:
        with open(FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open(FILE, "w") as file:
        json.dump(expenses, file, indent=4)