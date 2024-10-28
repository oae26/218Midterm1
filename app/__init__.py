import os
import pkgutil
import importlib
import sys
from app.commands import CommandHandler, Command
from app.plugins.menu import MenuCommand  # Import MenuCommand explicitly if needed
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Determine if the command requires the CommandHandler upon instantiation
                if item is MenuCommand:
                    command_instance = item(self.command_handler)
                else:
                    command_instance = item()
                self.command_handler.register_command(plugin_name, command_instance)
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        self.load_plugins()
        logging.info("Application started. Type 'exit' to exit.")
        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    logging.info("Application exiting.")
                    sys.exit(0)  # Use sys.exit(0) for an exit with no problems.
                try:
                    self.command_handler.execute_command(cmd_input)
                except KeyError:  # Easier to ask for forgiveness logic, throws an error if something goes awry.
                    logging.error(f"Unknown command: {cmd_input}")
                    sys.exit(1)  # Use a non-zero exit code to indicate failure or incorrect command.
        except KeyboardInterrupt:
            logging.info("Application interrupted by keyboard and exiting with no problems..")
            sys.exit(0)  # LBYL, we are already implementing functionality for a keyboard interrupt.
        finally:
            logging.info("Application shutdown.")


if __name__ == "__main__":
    app = App()
    app.start()