"""This function is in charge of testing commands"""
import pytest
from app import Application

def test_app_exit_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'exit' command."""
    inputs = iter(['exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = Application()
    with pytest.raises(SystemExit) as e:
        app.launch()
    # Check that the exit was graceful with the correct exit code
    assert e.value.code == 0, "The app did not exit as expected"
  