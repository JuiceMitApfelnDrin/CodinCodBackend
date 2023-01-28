__all__ = ["db_client"]


from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final

from ..environment_variables import load_dotenv

database_name: Final  = "CodinCod"
connection_string: Final = load_dotenv()['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]