from app.commands import Command
from decimal import Decimal

class MathCommand(Command):
    def execute(self):
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

            print(f"Result: {result}")
        except ValueError:
            print("Invalid input. Please ensure you enter numeric values for the numbers.")