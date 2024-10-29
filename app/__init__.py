import os
import sys
import pkgutil
import importlib
import logging
import logging.config
from app.commands import CommandHandler, Command
from app.plugins.menu import MenuCommand  # Explicitly import MenuCommand

class Application:
    def __init__(self):
        # Ensure logging directory exists
        os.makedirs('logs', exist_ok=True)
        self.setup_logging()
        self.env_settings = self.load_env_settings()
        self.env_settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def setup_logging(self):
        config_file = 'logging.conf'
        if os.path.isfile(config_file):
            logging.config.fileConfig(config_file, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging is set up successfully.")

    def load_env_settings(self):
        env_vars = dict(os.environ)
        logging.info("Environment variables are loaded.")
        return env_vars

    def get_env_setting(self, var_name: str = 'ENVIRONMENT'):
        return self.env_settings.get(var_name)

    def initialize_plugins(self):
        plugins_pkg = 'app.plugins'
        plugins_dir = plugins_pkg.replace('.', '/')
        
        if not os.path.isdir(plugins_dir):
            logging.warning(f"Directory '{plugins_dir}' for plugins does not exist.")
            return
        
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_dir]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_pkg}.{plugin_name}')
                    self.add_plugin_commands(plugin_module, plugin_name)
                except ImportError as error:
                    logging.error(f"Failed to import plugin {plugin_name}: {error}")

    def add_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                command_instance = item(self.command_handler) if item is MenuCommand else item()
                self.command_handler.register_command(plugin_name, command_instance)
                logging.info(f"Command '{item_name}' from plugin '{plugin_name}' registered.")

    def launch(self):
        self.initialize_plugins()
        logging.info("App is running. Enter 'exit' to quit.")
        
        try:
            while True:
                user_input = input(">>> ").strip()
                if user_input.lower() == 'exit':
                    logging.info("Shutting down the app.")
                    sys.exit(0)  # Exit without error
                try:
                    self.command_handler.execute_command(user_input)
                except KeyError:
                    logging.error(f"Unknown command: {user_input}")
                    sys.exit(1)  # Exit with error
        except KeyboardInterrupt:
            logging.info("App interrupted by keyboard input.")
            sys.exit(0)  # Exit without error
        finally:
            logging.info("App has stopped.")

if __name__ == "__main__":
    application = Application()
    application.launch()