#!/usr/bin/python3
"""
initialize the models package
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the storage type from environment variable
storage_t = os.getenv("HBNB_TYPE_STORAGE")

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
