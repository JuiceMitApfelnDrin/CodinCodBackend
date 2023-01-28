import pymongo
from pymongo.collation import Collation, CollationStrength
from ..database import db_client

users_collection = db_client.get_collection("USERS") 
users_collection.create_index("nickname", unique=True, collation=Collation(locale="en_US", strength=CollationStrength.SECONDARY))
users_collection.create_index("email",    unique=True, collation=Collation(locale="en_US", strength=CollationStrength.SECONDARY))