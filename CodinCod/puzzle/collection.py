import pymongo
from ..database import db_client

puzzles_collection = db_client.get_collection("PUZZLES")
puzzles_collection.create_index("title", unique=True)