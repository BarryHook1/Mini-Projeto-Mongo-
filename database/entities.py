from bson.binary import Binary
import bcrypt

class User:
    def __init__(self, user_id, cripto_key='a2b3'):
        self.user_id = user_id
        self.cripto_key = cripto_key
        self.salt = bcrypt.gensalt()

    def to_dict(self):
        return {
            'userID': self.user_id,
            'criptoKey': self.cripto_key,
            'salt': Binary(self.salt)
        }

class ChatMessage:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'message': Binary(self.message)
        }
