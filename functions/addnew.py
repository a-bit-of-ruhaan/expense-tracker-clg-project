from functions.storage import save_expenses



def add_expense(expenses, title, date, value):

    new_expense = {
        "title": title,
        "date": date,
        "value": value,
        
    }

    expenses.append(new_expense)

    save_expenses(expenses)


def delete_expense(expenses, index):

    expenses.pop(index)

    save_expenses(expenses)


def toggle_expense(expenses, index):

    expenses[index]["completed"] = not expenses[index]["completed"]

    save_expenses(expenses)