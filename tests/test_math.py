import unittest
from unittest.mock import patch
from app.plugins.math import MathCommand  # Adjust import as needed
import pandas as pd
import os

class TestMathCommand(unittest.TestCase):

    def setUp(self):
        self.math_command = MathCommand()
        self.math_command.history_df = pd.DataFrame(columns=['num1', 'operator', 'num2', 'result1'])
    
    def test_save_to_history(self):
        self.math_command.save_to_history(5, '+', 3, 8)
        self.assertEqual(len(self.math_command.history_df), 1)
        self.assertEqual(self.math_command.history_df.iloc[0].to_dict(), {'num1': 5, 'operator': '+', 'num2': 3, 'result1': 8})
    
   
    def test_save_history(self):
        self.math_command.save_to_history(5, '+', 3, 8)
        self.math_command.save_history('test_history.csv')
        self.assertTrue(os.path.exists('test_history.csv'))
        
        loaded_df = pd.read_csv('test_history.csv')
        self.assertEqual(len(loaded_df), 1)
        os.remove('test_history.csv')

    def test_load_history(self):
        test_data = pd.DataFrame({'num1': [5], 'operator': ['+'], 'num2': [3], 'result1': [8]})
        test_data.to_csv('test_history.csv', index=False)
        
        self.math_command.load_history('test_history.csv')
        self.assertEqual(len(self.math_command.history_df), 1)
        os.remove('test_history.csv')

    @patch('builtins.print')
    def test_load_history_file_not_found(self, mock_print):
        self.math_command.load_history('non_existent_file.csv')
        mock_print.assert_called_once_with("No saved history found.")

    def test_clear_history(self):
        self.math_command.save_to_history(5, '+', 3, 8)
        self.math_command.clear_history()
        self.assertTrue(self.math_command.history_df.empty)
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=["5", "3", "+"])
    def test_calculate_addition(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Result: 8.0")
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=["5", "3", "-"])
    def test_calculate_subtraction(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Result: 2.0")
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=["5", "3", "*"])
    def test_calculate_multiplication(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Result: 15.0")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=["6", "3", "/"])
    def test_calculate_division(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Result: 2.0")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=["5", "0", "/"])
    def test_calculate_division_by_zero(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Error: Division by zero is not allowed.")
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=["5", "3", "%"])
    def test_calculate_invalid_operator(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Invalid operator. Please use a valid one like '+', '-', '*', '/', 'add', 'subtract', 'multiply', or 'divide'.")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=["abc", "3", "+"])
    def test_calculate_invalid_input(self, mock_input, mock_print):
        self.math_command.calculate()
        mock_print.assert_any_call("Invalid input. Please ensure you enter numeric values for the numbers.")

if __name__ == '__main__':
    unittest.main()