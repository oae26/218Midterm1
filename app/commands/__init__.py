from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command
    
    def execute_command(self, command_name: str):
        """Look before you leap (LBYL) - Use when its less likely to work
        if command_name in self.commands:
            self.commands[command_name].exeucte()
        else:
            print(f"No such command: {command_name}")
        
        Easier to ask forgiveness than permission"""
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name }")