# database/__init__.py
from .database_setup import create_database, insert_laermdaten, insert_massnahmen

__all__ = ["create_database", "insert_laermdaten", "insert_massnahmen"]
