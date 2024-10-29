"""tests all the commands the app is in charge of"""
import pytest
from app import Application

def test_app_get_environment_variable():
    """Tests that the REPL acquires the environment variable correctly"""
    app = Application()
#   Retrieve the current env setting
    current_env = app.get_env_setting('ENVIRONMENT')
    # Assert environment
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRO: {current_env}"
def test_app_start_exit_command(monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = Application()
    with pytest.raises(SystemExit) as e:
        app.launch()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = Application()
    with pytest.raises(SystemExit):
        app.launch()
    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out
