
from motor.motor_asyncio import AsyncIOMotorClient

import os
from pathlib import Path
import json
import sys

# setting
PROJECT_ROOT = Path(__file__).resolve().parent
config_path = 'settings.json'
config_file = os.path.join(PROJECT_ROOT, config_path)
config = json.loads(open(config_file).read())
for key, value in config.items():
    setattr(sys.modules[__name__], key, value)


client = AsyncIOMotorClient(MONGO_DB_URL)
db = client.college
