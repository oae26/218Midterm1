from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, sub_command=None):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, user_input: str):
        # Split the input to get command and optional sub-command
        parts = user_input.strip().split()
        command_name = parts[0]
        sub_command = parts[1] if len(parts) > 1 else None
        
        try:
            # Execute with the sub_command if it exists
            self.commands[command_name].execute(sub_command=sub_command)
        except KeyError:
            print(f"No such command: {command_name}")
        except Exception as e:
            print(f"Error executing command: {e}")