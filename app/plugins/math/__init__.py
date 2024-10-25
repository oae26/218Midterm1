from app.commands import Command
from decimal import Decimal
import pandas as pd

class MathCommand(Command):

    def __init__(self):
        self.history_df = pd.DataFrame(columns=['num1','operator','num2','result1'])
    def execute(self, sub_command=None):
        if sub_command == 'show':
            self.show_history()
        elif sub_command == 'save':
            self.save_history()
        elif sub_command == 'load':
            self.load_history()
        elif sub_command == 'delete':
            self.clear_history()
        else:
            self.calculate()


    def save_to_history(self, num1, operator, num2, result):
   # """Append a new calculation to the history DataFrame."""
        new_entry = {'num1': num1, 'operator': operator, 'num2': num2, 'result1': result}
        self.history_df = pd.concat([self.history_df, pd.DataFrame([new_entry])], ignore_index=True)


   # """show_history is in charge of displaying calculation history from pandas."""
    def show_history(self):
        print(self.history_df if not self.history_df.empty else "no existing calculation history available")
   #  """save_history is a function in charge of saving the pandas history to a local csv file."""
    def save_history(self, file_path='history.csv'):
        self.history_df.to_csv(file_path, index=False)
        print("Calculation history saved successfully")
    # """load_history is a function in charge of loading pandas data from a csv file"""
    def load_history(self, file_path='history.csv'):
        try:
            self.history_df = pd.read_csv(file_path)
            print("History loaded successfully.")
        except FileNotFoundError:
            print("No saved history found.")
    
   # """clear_history is a function in charge of clearing the pandas history back to what it was."""
    def clear_history(self):
        self.history_df = pd.DataFrame(columns=['num1','operator','num2','result'])
        print("Calculation history cleared.")
    def calculate(self):
        try:
            num1 = float(input("Please provide the first number: "))
            num2 = float(input("Please provide the second number: "))
            operator = input("Please provide the operator you would like to use, for example: +, -, *, /, or the arithmetic function(add, subtract): ")

            if operator == '+' or operator == 'add':
                result = num1 + num2
            elif operator == '-' or operator == 'subtract':
                result = num1 - num2
            elif operator == '*' or operator == 'multiply':
                result = num1 * num2
            elif operator == '/' or operator == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("Error: Division by zero is not allowed.")
                    return
            else:
                print("Invalid operator. Please use a valid one like '+', '-', '*', '/', 'add', 'subtract', 'multiply', or 'divide'.")
                return

         #   """Saves data to history"""
            self.save_to_history(num1, operator, num2, result) 

            print(f"Result: {result}")
        except ValueError:
            print("Invalid input. Please ensure you enter numeric values for the numbers.")


