#!/usr/bin/python3
"""
Contains the MongoStorage class for NoSQL storage using MongoDB
"""

from pymongo import MongoClient
from os import getenv
from models.user import User

classes = {"User": User}


class MongoStorage:
    """Interacts with the MongoDB database"""

    def __init__(self):
        """Initialize a new MongoStorage instance"""
        MONGO_HOST = getenv('MONGO_HOST') or "localhost"
        MONGO_PORT = int(getenv('MONGO_PORT', 27017))  # Default port is 27017
        MONGO_DB = getenv('MONGO_DB') or "unidate"

        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]

    def all(self, cls=None):
        """Returns all objects of a certain class or all objects in the database"""
        if cls:
            cls_name = cls.__name__
            return list(self.db[cls_name].find())  # Return all objects of that class
        else:
            # Return all objects for all classes
            all_objects = {}
            for cls_name in classes:
                all_objects[cls_name] = list(self.db[cls_name].find())
            return all_objects

    def new(self, obj):
        """Adds a new object to the database"""
        cls_name = obj.__class__.__name__
        self.db[cls_name].insert_one(obj.to_dict())  # Convert object to dict before storing

    def save(self):
        """No explicit save needed for MongoDB as it automatically writes"""
        pass

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj is not None:
            cls_name = obj.__class__.__name__
            self.db[cls_name].delete_one({"_id": obj.id})

    def get(self, cls, id):
        """Returns an object based on the class and its ID"""
        if cls is not None:
            cls_name = cls.__name__
            obj_data = self.db[cls_name].find_one({"_id": id})
            if obj_data:
                return classes[cls_name](**obj_data)  # Recreate the object from stored data
        return None

    def count(self, cls=None):
        """Counts the number of objects in the database"""
        if cls:
            cls_name = cls.__name__
            return self.db[cls_name].count_documents({})
        else:
            total_count = 0
            for cls_name in classes:
                total_count += self.db[cls_name].count_documents({})
            return total_count

    def close(self):
        """Closes the MongoDB connection"""
        self.client.close()
