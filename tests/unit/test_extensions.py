import pytest

from src.errors import CustomException
from src.extensions import SecurityManager


def test_env_validation(monkeypatch):
    # test env validation
    monkeypatch.setattr("src.extensions.required_variables", ["KEY"])
    with pytest.raises(SystemExit):
        SecurityManager.validate_env()
