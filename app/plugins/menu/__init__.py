from app.commands import Command
import logging

class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler
        self.logger = logging.getLogger(__name__)

    def execute(self, sub_command=None):
        """Display the available commands."""
        self.logger.info("Displaying available commands.")
        print("Available commands:")
        
        # Check if there are any commands to display
        if not self.command_handler.commands:
            print("No commands available.")
            return
        
        for command_name in self.command_handler.commands:
            print(f"- {command_name}")

        self.logger.info("Available commands displayed successfully.")