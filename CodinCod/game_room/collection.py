import pymongo
from ..database import db_client

games_collection = db_client.get_collection("GAMES")