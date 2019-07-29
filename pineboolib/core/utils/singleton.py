"""
Singleton module.
"""
from typing import Any, Dict


class Singleton(type):
    """
    Singleton metaclass.

    Use this class as your metaclass to ensure only one instance of your class is created.
    """

    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Record class instance created to prevent duplicate references."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
