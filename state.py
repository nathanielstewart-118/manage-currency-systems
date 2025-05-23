# state.py
from dataclasses import dataclass
@dataclass
class State:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._instance.service_semaphore = False
            cls._instance.service_togo_semaphore = False
        return cls._instance
