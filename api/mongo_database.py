from dotenv import load_dotenv
import os
from mongoengine import connect

load_dotenv()

def conn():
    return connect(os.getenv('APP_DATABASE'), username=os.getenv('APP_MONGO_USER'),
        password=os.getenv('APP_MONGO_PASS'), authentication_source='admin')