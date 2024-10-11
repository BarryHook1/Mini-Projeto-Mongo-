
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from pymongo import MongoClient
from database.entities import User, ChatMessage

class MongoHandler:
    def __init__(self, connection_string=None):
        if connection_string is None:
            self.connection_string = "mongodb+srv://henrique:123@cluster0.xumie.mongodb.net/"
        else:
            self.connection_string = connection_string
            
        self.client = MongoClient(self.connection_string)
        self.db = self.client['pychat']

    def insert_user(self, user: User):
        users_collection = self.db['users']
        users_collection.insert_one(user.to_dict())

    def insert_message(self, message: ChatMessage):
        chats_collection = self.db['chats']
        chats_collection.insert_one(message.to_dict())

    def find_user(self, user_id):
        users_collection = self.db['users']
        return users_collection.find_one({'userID': user_id})

    def find_messages(self, receiver):
        chats_collection = self.db['chats']
        return chats_collection.find({"receiver": {"$regex": receiver, "$options": "i"}}) # regex para busca insensível a maiúsculas/minúsculas
