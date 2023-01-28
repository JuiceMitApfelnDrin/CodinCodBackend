__all__ = ["load_dotenv"]

import os
from dotenv import load_dotenv as _load_dotenv


def load_dotenv():
    envpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
    _load_dotenv(envpath)
    return os.environ
