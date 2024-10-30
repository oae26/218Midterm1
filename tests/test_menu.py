import unittest
from unittest.mock import Mock, patch
import logging
from app.plugins.menu import MenuCommand  # Adjust import as needed

class TestMenuCommand(unittest.TestCase):
    def setUp(self):
        # Mock the command_handler with a mock commands dictionary
        self.mock_command_handler = Mock()
        self.menu_command = MenuCommand(self.mock_command_handler)
    
    @patch('builtins.print')
    def test_execute_with_no_commands(self, mock_print):
        # Set up the mock command_handler to have no commands
        self.mock_command_handler.commands = {}
        
        # Run the execute method
        self.menu_command.execute()
        
        # Verify the output and log messages
        mock_print.assert_any_call("Available commands:")
        mock_print.assert_any_call("No commands available.")
    
    @patch('builtins.print')
    def test_execute_with_commands(self, mock_print):
        # Set up the mock command_handler to have some commands
        self.mock_command_handler.commands = {"math": Mock(), "help": Mock()}
        
        # Run the execute method
        self.menu_command.execute()
        
        # Verify that the command names are printed
        mock_print.assert_any_call("Available commands:")
        mock_print.assert_any_call("- math")
        mock_print.assert_any_call("- help")
    
    @patch('logging.Logger.info')
    def test_logging_for_execute(self, mock_logger_info):
        # Set up the mock command_handler to have some commands
        self.mock_command_handler.commands = {"math": Mock(), "help": Mock()}
        
        # Run the execute method
        self.menu_command.execute()
        
        # Verify that logging calls were made
        mock_logger_info.assert_any_call("Displaying available commands.")
        mock_logger_info.assert_any_call("Available commands displayed successfully.")

if __name__ == '__main__':
    unittest.main()