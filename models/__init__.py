#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

# Get the storage type from environment variable
storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.database import DBStorage
    storage = DBStorage()
elif storage_t == "file":
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
elif storage_t == "mongo":
    from models.engine.mongostorage import MongoStorage
    storage = MongoStorage()
else:
    # Default to file storage if nothing else is specified
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()