import pymongo
from ..database import db_client

submissions_collection = db_client.get_collection("SUBMISSIONS")